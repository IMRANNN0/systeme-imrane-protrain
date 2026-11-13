import argparse
import contextlib
import io
import json
import sys
import tempfile
import tomllib
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from common import ROOT, read_json, write_json
from imrane import initialize, project_add
from agents import generate
from hooks import route_prompt, run_hook
from models import migrate


class RoutingTests(unittest.TestCase):
    def test_shared_classification_cases(self):
        policy = read_json(ROOT / "config/models.json")
        cases = read_json(ROOT / "tests/fixtures/model-routing-cases.json")
        for case in cases:
            with self.subTest(name=case["name"]):
                previous = case.get("previous", {})
                if previous.get("session_id") != "test":
                    previous = {}
                state = route_prompt(case["prompt"], {**previous, "failures": previous.get("failure_count", 0)}, policy)
                self.assertEqual(state["route"], case["route"])
                self.assertEqual(state["reasoning"], policy["routes"][case["route"]]["reasoning_effort"])
                self.assertEqual(state["failures"], case["failures"])
                self.assertNotIn("prompt", state)

    def workspace(self):
        temp_root = ROOT / ".imrane/test-temp"
        temp_root.mkdir(parents=True, exist_ok=True)
        temp = tempfile.TemporaryDirectory(dir=temp_root)
        self.addCleanup(temp.cleanup)
        root = Path(temp.name) / "workspace with spaces"
        initialize(root, apply=True)
        project_add(argparse.Namespace(workspace=str(root), id="alpha", path="projects/alpha", name="Alpha", apply=True, git_init=False))
        return root

    def test_current_policy_handles_darija_and_explicit_failures(self):
        policy = read_json(ROOT / "config/models.json")
        previous = {"route": "fast_safe", "failures": 1}
        for prompt in ("kmmel", "صافي كمل", "safi, continue", "try again"):
            with self.subTest(prompt=prompt):
                result = route_prompt(prompt, previous, policy)
                self.assertEqual((result["route"], result["failures"]), ("fast_safe", 1))
        for prompt in ("مازال ما خدامش", "mazal ma khdamch", "it still doesn't work"):
            with self.subTest(prompt=prompt):
                result = route_prompt(prompt, previous, policy)
                self.assertEqual((result["route"], result["failures"]), ("deep_safe", 2))
        for prompt in ("There was no timeout", "Build a separate fixture for a failed webhook"):
            with self.subTest(prompt=prompt):
                self.assertEqual(route_prompt(prompt, previous, policy)["failures"], 0)

    def test_current_policy_ignores_route_tags_inside_task_text(self):
        policy = read_json(ROOT / "config/models.json")
        quoted = route_prompt("Audit production authentication. Show [route:mechanical] as an example.", {}, policy)
        self.assertEqual(quoted["route"], "deep_safe")
        unknown = route_prompt("[route:bogus-tag] Corrige la marge.", {}, policy)
        self.assertEqual(unknown["route"], "standard_safe")
        explicit = route_prompt("[route:mechanical] Corrige la marge.", {}, policy)
        self.assertEqual(explicit["route"], "mechanical_safe")

    def test_preset_migration_preserves_claude_and_generates_all_efforts(self):
        with contextlib.redirect_stdout(io.StringIO()):
            root = self.workspace()
            old = {"version": 1, "default_route": "standard_safe", "reasoning_effort": "high", "routes": {
                "fast_safe": {"label": "FAST", "codex_model": "old-luna", "claude_model": "personal-fast", "claude_effort": "medium"},
                "standard_safe": {"label": "STANDARD", "codex_model": "old-terra", "claude_model": "personal-standard"},
                "deep_safe": {"label": "DEEP", "codex_model": "old-sol", "claude_model": "personal-deep"}}}
            target = root / ".codex/model-routing-policy.json"
            write_json(target, old)
            migrate(root, "codex-sol-luna-6", apply=False)
            self.assertEqual(read_json(target), old)
            result = migrate(root, "codex-sol-luna-6", apply=True)
            self.assertEqual(result["routes"]["fast_safe"]["claude_model"], "personal-fast")
            self.assertEqual(result["routes"]["fast_safe"]["claude_effort"], "medium")
            self.assertEqual(read_json(next((root / ".imrane/backups").glob("models-*.json"))), old)
            self.assertFalse((root / ".codex/config.toml").read_text().startswith("model"))
            generate(root, apply=True)
            preset = read_json(ROOT / "config/codex-sol-luna-6.json")
            for route, binding in preset["routes"].items():
                filename = "route-" + route.replace("_", "-") + ".toml"
                for base in (root, root / "projects/alpha"):
                    role = tomllib.loads((base / ".codex/agents" / filename).read_text())
                    self.assertEqual(role["model"], binding["codex_model"])
                    self.assertEqual(role["model_reasoning_effort"], binding["reasoning_effort"])
                    self.assertNotIn("sandbox_mode", role)
            claude = (root / ".claude/agents/route-fast-safe.md").read_text()
            self.assertIn('model: "personal-fast"', claude)
            self.assertIn("effort: medium", claude)
            self.assertIsNone(result["routes"]["mechanical_safe"]["claude_model"])

    def test_neutral_install_and_no_preset_keep_personal_bindings(self):
        with contextlib.redirect_stdout(io.StringIO()):
            root = self.workspace()
            policy = read_json(root / ".codex/model-routing-policy.json")
            self.assertTrue(all(r["codex_model"] is None for r in policy["routes"].values()))
            policy["routes"]["fast_safe"]["codex_model"] = "personal-model"
            write_json(root / ".codex/model-routing-policy.json", policy)
            result = migrate(root, apply=True)
            self.assertEqual(result["routes"]["fast_safe"]["codex_model"], "personal-model")
            self.assertEqual(result["routes"]["fast_safe"]["reasoning_effort"], "medium")

    def test_legacy_policy_remains_usable_before_explicit_migration(self):
        policy = {"version": 1, "default_route": "standard_safe", "reasoning_effort": "high",
                  "routes": {name: {"label": name} for name in ("fast_safe", "standard_safe", "deep_safe")},
                  "deep_patterns": ["architecture"], "fast_patterns": ["typo"],
                  "continuity_patterns": ["^ok$"], "failure_patterns": ["toujours pas", "même problème"]}
        state = route_prompt("typo", {}, policy)
        self.assertEqual(state["route"], "fast_safe")
        state = route_prompt("toujours pas", state, policy)
        state = route_prompt("même problème", state, policy)
        self.assertEqual(state["route"], "deep_safe")
        self.assertEqual(state["reasoning"], "high")
        policy["fast_patterns"] = [r"^\S+$"]
        self.assertEqual(route_prompt("token", {}, policy)["route"], "fast_safe")
        self.assertEqual(route_prompt("two words", {}, policy)["route"], "standard_safe")
        policy["fast_patterns"] = [r"^\D+$"]
        self.assertEqual(route_prompt("word", {}, policy)["route"], "fast_safe")
        self.assertEqual(route_prompt("123", {}, policy)["route"], "standard_safe")

    def test_hook_effort_and_session_isolation(self):
        with contextlib.redirect_stdout(io.StringIO()):
            root = self.workspace()
            payload = {"cwd": str(root / "projects/alpha"), "session_id": "one", "prompt": "[route:mechanical] typo"}
            reply = run_hook(root, "UserPromptSubmit", payload)
            self.assertIn("Codex reasoning low", reply["hookSpecificOutput"]["additionalContext"])
            run_hook(root, "UserPromptSubmit", {**payload, "prompt": "failed"})
            other = run_hook(root, "UserPromptSubmit", {**payload, "session_id": "two", "prompt": "continue"})
            self.assertIn("standard_safe", other["hookSpecificOutput"]["additionalContext"])
            escalated = run_hook(root, "UserPromptSubmit", {**payload, "prompt": "failed"})
            self.assertIn("Codex reasoning high", escalated["hookSpecificOutput"]["additionalContext"])
            for file in (root / "tmp/codex-session").rglob("*.json"):
                self.assertNotIn(payload["prompt"], file.read_text())

    def test_invalid_effort_rejected(self):
        policy = read_json(ROOT / "config/models.json")
        policy["routes"]["deep_safe"]["reasoning_effort"] = "ultra"
        with self.assertRaises(ValueError):
            route_prompt("migration", {}, policy)


if __name__ == "__main__":
    unittest.main()

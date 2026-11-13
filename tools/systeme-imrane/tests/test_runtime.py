import argparse
import contextlib
import io
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from imrane import initialize, managed, project_add, snapshot, check_workspace, configure_secrets
from common import ROOT, read_json, relative_path, resolve_project, runtime_dir, write_json
from hooks import route_prompt, run_hook
from graphify_runtime import collect, mark_stale, query, refresh, run_fallback, provider_environment
from graphify_worker import classify_exception
from dependencies import system_plan, version_tuple, inspect_managed
from skills import unpack_skill, tree_hash, adapt_paths, expose
from plugins import sanitize, plan


def setUpModule():
    # Keep all synthetic fixtures inside the test checkout (also works in sandboxed hosts).
    temp_root = ROOT / ".imrane/test-temp"
    temp_root.mkdir(parents=True, exist_ok=True)
    tempfile.tempdir = str(temp_root)


class WorkspaceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="imrane test ")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "workspace with spaces"
        self.quiet = contextlib.redirect_stdout(io.StringIO())
        self.quiet.__enter__()
        self.addCleanup(self.quiet.__exit__, None, None, None)
        initialize(self.root, apply=True)
        self.add_project("alpha", "projects/alpha")

    def add_project(self, name, path):
        project_add(argparse.Namespace(workspace=str(self.root), id=name, name=name.title(), path=path, apply=True, git_init=False))

    def test_init_dry_run_writes_nothing(self):
        target = Path(self.temp.name) / "plan"
        initialize(target)
        self.assertFalse(target.exists())

    def test_idempotence_preserves_registry(self):
        before = (self.root / ".codex/projects.json").read_bytes()
        initialize(self.root, apply=True)
        self.assertEqual(before, (self.root / ".codex/projects.json").read_bytes())

    def test_reinstall_preserves_personal_models_and_graphify_settings(self):
        policy = read_json(self.root / ".codex/model-routing-policy.json")
        policy["routes"]["deep_safe"]["codex_model"] = "personal-deep-model"
        policy["routes"]["deep_safe"]["claude_model"] = "opus"
        write_json(self.root / ".codex/model-routing-policy.json", policy)
        initialize(self.root, apply=True)
        self.assertEqual(read_json(self.root / ".codex/model-routing-policy.json"), policy)
        from agents import generate
        generate(self.root, apply=True)
        import tomllib
        codex = tomllib.loads((self.root / ".codex/agents/route-deep-safe.toml").read_text())
        self.assertEqual(codex["model"], "personal-deep-model")
        self.assertNotIn("sandbox_mode", codex)
        self.assertTrue((self.root / "projects/alpha/.claude/agents/route-deep-safe.md").exists())

    def test_atomic_conflict_preflight(self):
        (self.root / "owned.txt").write_text("private edit")
        with self.assertRaises(ValueError):
            managed(self.root, {"new.txt": "new", "owned.txt": "replacement"}, apply=True)
        self.assertFalse((self.root / "new.txt").exists())
        self.assertEqual((self.root / "owned.txt").read_text(), "private edit")

    def test_upgrade_preserves_user_edits_and_backs_up_unmodified(self):
        managed(self.root, {"owned.txt": "v1"}, apply=True)
        managed(self.root, {"owned.txt": "v2"}, apply=True, upgrade=True)
        self.assertTrue(list((self.root / ".imrane/backups").rglob("owned.txt")))
        (self.root / "owned.txt").write_text("user edited")
        with self.assertRaises(ValueError):
            managed(self.root, {"owned.txt": "v3"}, apply=True, upgrade=True)

    def test_project_path_traversal_rejected(self):
        with self.assertRaises(ValueError):
            relative_path(self.root, "../outside")

    def test_reserved_project_paths_rejected(self):
        for path in ("secrets", "Secrets", "TMP", "tools", "Tools/nested", "docs"):
            with self.assertRaises(ValueError, msg=path):
                self.add_project("reserved", path)

    def test_git_init_failure_can_be_retried(self):
        args = argparse.Namespace(workspace=str(self.root), id="retry", name="Retry", path="projects/retry", apply=True, git_init=True)
        with patch("imrane.subprocess.run", side_effect=subprocess.CalledProcessError(1, "git")):
            with self.assertRaises(subprocess.CalledProcessError):
                project_add(args)
        with patch("imrane.subprocess.run") as retry:
            project_add(args)
            retry.assert_called_once()
            self.assertIn("init", retry.call_args.args[0])

    def test_generated_local_surfaces_are_git_ignored(self):
        project = self.root / "projects/alpha"
        for base in (self.root, project):
            subprocess.run(["git", "init", "-b", "codex/test", str(base)], check=True, capture_output=True)
            for rel in (".codex/hooks.json", ".claude/settings.json", ".claude/skills/systeme-imrane/SKILL.md", ".agents/skills/systeme-imrane/SKILL.md", ".codex/model-routing-policy.json", ".codex/graphify.json", ".codex/agents/example.toml", ".claude/agents/example.md"):
                result = subprocess.run(["git", "-C", str(base), "check-ignore", rel], capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, rel)

    @unittest.skipUnless(os.name == "nt", "Windows ACL failure paths")
    def test_credential_acl_fails_closed_on_exceptions_and_missing_sid(self):
        target = self.root / "secrets/graphify.env"
        for failure in (FileNotFoundError("whoami missing"), OSError("ACL unavailable")):
            with patch("imrane.sys.stdin.isatty", return_value=True), patch("imrane.getpass.getpass", return_value="FICTIONAL_KEY_TEST_ONLY"), patch("imrane.subprocess.run", side_effect=failure):
                with self.assertRaises(ValueError):
                    configure_secrets(self.root)
            self.assertFalse(target.exists())
        missing = subprocess.CompletedProcess([], 0, stdout="no SID")
        with patch("imrane.sys.stdin.isatty", return_value=True), patch("imrane.getpass.getpass", return_value="FICTIONAL_KEY_TEST_ONLY"), patch("imrane.subprocess.run", return_value=missing):
            with self.assertRaises(ValueError):
                configure_secrets(self.root)
        self.assertFalse(target.exists())

    def test_cwd_beats_selector_and_nested_project_isolated(self):
        self.add_project("beta", "projects/alpha/nested")
        write_json(self.root / "tmp/codex-session/ACTIVE_PROJECT.json", {"project_id": "alpha"})
        resolved = resolve_project(self.root, self.root / "projects/alpha/nested/src")
        self.assertEqual(resolved["id"], "beta")
        self.assertIsNone(resolve_project(self.root, Path(self.temp.name) / "outside"))
        # The parent lane must not index its nested child's sources.
        scope = self.root / "projects/alpha/.codex/graphify-scope.json"
        write_json(scope, {"include": ["."], "exclude": []})
        files, _ = collect(self.root, "alpha")
        self.assertFalse(any("nested/" in f for f in files))
        child, _ = collect(self.root, "beta")
        self.assertIn("AGENTS.md", child)

    def test_hooks_no_secret_prompts_or_tool_payloads(self):
        canary = "PRIVATE_CANARY_NEVER_PERSIST_1739"
        cwd = str(self.root / "projects/alpha")
        run_hook(self.root, "UserPromptSubmit", {"cwd": cwd, "prompt": canary, "session_id": "one"})
        run_hook(self.root, "PostToolUse", {"cwd": cwd, "tool_input": {"secret": canary}, "session_id": "one"})
        for file in (self.root / "tmp").rglob("*.json"):
            self.assertNotIn(canary, file.read_text())

    def test_session_context_bounded_and_no_other_lane(self):
        self.add_project("beta", "projects/beta")
        current = self.root / "projects/alpha/.codex/memory/CURRENT.md"
        current.write_text("ALPHA " * 3000)
        result = run_hook(self.root, "SessionStart", {"cwd": str(current.parent), "session_id": "s"})
        text = result["hookSpecificOutput"]["additionalContext"]
        self.assertLessEqual(len(text), 3600)
        self.assertNotIn("Beta", text)

    def test_two_sessions_do_not_share_routes(self):
        cwd = str(self.root / "projects/alpha")
        first = run_hook(self.root, "UserPromptSubmit", {"cwd": cwd, "prompt": "audit complet", "session_id": "one"})
        other = run_hook(self.root, "UserPromptSubmit", {"cwd": cwd, "prompt": "ok", "session_id": "two"})
        self.assertIn("deep_safe", str(first))
        self.assertIn("standard_safe", str(other))

    def test_checkpoint_guidance_for_new_and_resumed_project_chats(self):
        self.add_project("beta", "projects/beta")
        alpha = self.root / "projects/alpha"
        beta = self.root / "projects/beta"
        alpha_note = "## Current\nALPHA_NEXT_ACTION\n\n## Earlier\nOLD_ALPHA_ACTION\n"
        (alpha / ".codex/memory/CURRENT.md").write_text(alpha_note, encoding="utf-8")
        (beta / ".codex/memory/CURRENT.md").write_text("BETA_NEXT_ACTION", encoding="utf-8")

        def event(kind, path, session):
            return run_hook(self.root, kind, {"cwd": str(path), "session_id": session, "prompt": "PRIVATE_TEXT"})

        first = str(event("UserPromptSubmit", alpha, "one"))
        self.assertIn("Restart Checkpoint", first)
        self.assertIn("ALPHA_NEXT_ACTION", first)
        self.assertNotIn("OLD_ALPHA_ACTION", first)
        self.assertNotIn("BETA_NEXT_ACTION", first)
        self.assertNotIn("PRIVATE_TEXT", first)
        event("PostToolUse", alpha, "one")
        continued = str(event("UserPromptSubmit", alpha, "one"))
        self.assertIn("Restart Checkpoint", continued)
        self.assertNotIn("ALPHA_NEXT_ACTION", continued)
        self.assertIn("ALPHA_NEXT_ACTION", str(event("SessionStart", alpha, "two")))
        self.assertIn("BETA_NEXT_ACTION", str(event("UserPromptSubmit", beta, "one")))
        self.assertEqual(event("UserPromptSubmit", Path(self.temp.name) / "outside", "one"), {})
        event("Stop", alpha, "one")
        snapshot = read_json(runtime_dir(self.root, "alpha") / "latest-snapshot.json")
        self.assertEqual(len(snapshot["memory"]), 4)
        self.assertEqual(snapshot["memory"]["CURRENT.md"], alpha_note)
        states = [read_json(file) for file in (runtime_dir(self.root, "alpha") / "sessions").glob("*.json")]
        stopped = next(state for state in states if state["event"] == "Stop")
        self.assertEqual(set(stopped["lifecycle"]), {"UserPromptSubmit", "Stop"})
        self.assertNotIn("PRIVATE_TEXT", json.dumps(stopped))

    def test_precompact_blocks_global_auto_refresh_without_lane_consent(self):
        cfg = read_json(self.root / ".codex/graphify.json")
        cfg["auto_refresh"] = True
        write_json(self.root / ".codex/graphify.json", cfg)
        with patch("graphify_runtime.refresh") as refresh:
            reply = run_hook(self.root, "PreCompact", {"cwd": str(self.root / "projects/alpha")})
            refresh.assert_not_called()
        snap = read_json(runtime_dir(self.root, "alpha") / "latest-snapshot.json")
        self.assertEqual(snap["graphify"]["status"], "stale")
        self.assertIn("automatic refresh skipped", reply["hookSpecificOutput"]["additionalContext"])
        self.assertEqual(len(snap["memory"]), 4)

    def test_precompact_snapshot_even_if_local_staleness_check_fails(self):
        with patch("graphify_runtime.mark_stale", side_effect=RuntimeError("secret-bearing provider message")):
            run_hook(self.root, "PreCompact", {"cwd": str(self.root / "projects/alpha")})
        snap = read_json(runtime_dir(self.root, "alpha") / "latest-snapshot.json")
        self.assertEqual(snap["graphify"]["status"], "error")
        self.assertNotIn("secret-bearing", json.dumps(snap))

    def test_disabled_graphify_is_not_a_compaction_error(self):
        data = read_json(self.root / ".codex/projects.json")
        data["projects"][0]["graphify_enabled"] = False
        write_json(self.root / ".codex/projects.json", data)
        with patch("graphify_runtime.refresh") as refresh_call:
            run_hook(self.root, "PreCompact", {"cwd": str(self.root / "projects/alpha")})
            refresh_call.assert_not_called()
        snapshot_data = read_json(runtime_dir(self.root, "alpha") / "latest-snapshot.json")
        self.assertEqual(snapshot_data["graphify"]["status"], "disabled")

    def test_graphify_scope_excludes_private_generated_media(self):
        root = self.root / "projects/alpha"
        for path in ("Secrets/key.txt", "dist/output.md", "node_modules/foo.md", ".ENV.txt", "photo.png", "TMP/trace.md", "AUTH.JSON"):
            target = root / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text("not for indexing")
        write_json(root / ".codex/graphify-scope.json", {"include": ["."], "exclude": []})
        files, fingerprint = collect(self.root, "alpha")
        self.assertFalse(any("not for indexing" in b.decode() for b in files.values()))
        self.assertEqual(len(fingerprint), 64)

    def test_secret_assignment_blocks_network_before_provider(self):
        root = self.root / "projects/alpha"
        (root / "docs").mkdir()
        (root / "docs/unsafe.md").write_text("GEMINI_API_KEY=FICTIONAL_TEST_VALUE_123456789")
        with patch("graphify_runtime.invoke_provider") as provider:
            with self.assertRaises(ValueError):
                refresh(self.root, "alpha", True)
            provider.assert_not_called()

    def test_query_budget_freshness_and_project_provenance(self):
        files, fingerprint = collect(self.root, "alpha")
        output = self.root / "projects/alpha/graphify-out"
        write_json(output / "graph.json", {"nodes": [{"id": str(i), "label": "architecture", "source_file": "AGENTS.md", "description": "a" * 400} for i in range(100)]})
        write_json(output / "imrane-provenance.json", {"project_id": "alpha", "files": list(files)})
        write_json(runtime_dir(self.root, "alpha") / "graphify-state.json", {"status": "current", "fingerprint": fingerprint})
        result = query(self.root, "alpha", "architecture", 200)
        self.assertLessEqual(len(json.dumps(result, ensure_ascii=False)), 800)
        (self.root / "projects/alpha/AGENTS.md").write_text("changed")
        self.assertEqual(query(self.root, "alpha", "architecture")["status"], "stale")
        write_json(output / "imrane-provenance.json", {"project_id": "beta"})
        with self.assertRaises(ValueError):
            query(self.root, "alpha", "architecture")

    def test_failed_refresh_keeps_last_graph(self):
        output = self.root / "projects/alpha/graphify-out/graph.json"
        write_json(output, {"nodes": [{"id": "old"}]})
        with patch("graphify_runtime.invoke_provider", return_value="incomplete"):
            self.assertEqual(refresh(self.root, "alpha", True), 1)
        self.assertEqual(read_json(output)["nodes"][0]["id"], "old")

    def test_generated_configuration_parses(self):
        import tomllib
        self.assertTrue(tomllib.loads((self.root / ".codex/config.toml").read_text())["features"]["hooks"])
        hooks = read_json(self.root / ".claude/settings.json")["hooks"]
        self.assertEqual(set(hooks), {"SessionStart", "UserPromptSubmit", "PostToolUse", "Stop", "PreCompact"})
        command = hooks["SessionStart"][0]["hooks"][0]["command"]
        self.assertIn("workspace with spaces", command)
        self.assertNotIn("Bypass", command)
        self.assertEqual(check_workspace(self.root), 0)

    def test_cli_hook_process_actual_stdin(self):
        runner = ROOT / "scripts/hooks.py"
        payload = {"cwd": str(self.root / "projects/alpha"), "prompt": "audit complet", "session_id": "cli"}
        result = subprocess.run([sys.executable, str(runner), "--workspace", str(self.root), "--event", "UserPromptSubmit"], input=json.dumps(payload), text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("deep_safe", json.loads(result.stdout)["hookSpecificOutput"]["additionalContext"])


class PureLogicTests(unittest.TestCase):
    def test_plugin_inventory_never_exports_host_config_or_auth(self):
        canary = "PRIVATE_PLUGIN_CANARY"
        raw = {"installed":[{"pluginId":"browser@openai-bundled", "name":"browser", "version":"1.0", "marketplaceName":"openai-bundled", "installed":True, "enabled":True, "source":{"path":canary}, "auth":{"token":canary}}]}
        result = sanitize(raw)
        self.assertNotIn(canary, json.dumps(result))
        self.assertFalse(result["authentication_verified"])
        self.assertEqual(plan(result, "core")["missing_recommended"], [])
        self.assertFalse(sanitize(raw, "failed to list remote marketplace")["remote_catalogue_complete"])

    def test_routes_continuations_escalation_override(self):
        policy = read_json(ROOT / "config/models.json")
        state = route_prompt("architecture", {}, policy)
        self.assertEqual(state["route"], "standard_safe")
        self.assertEqual(route_prompt("ok", state, policy)["route"], "standard_safe")
        state = route_prompt("travail normal", {}, policy)
        state = route_prompt("toujours pas", state, policy)
        self.assertEqual(state["route"], "standard_safe")
        state = route_prompt("même problème", state, policy)
        self.assertEqual(state["route"], "deep_safe")
        self.assertEqual(route_prompt("[route:luna]", state, policy)["route"], "fast_safe")

    def test_quota_fallback_and_cooldown_recovery(self):
        config = read_json(ROOT / "config/graphify.json")
        calls = []
        state = {}
        def attempt(provider):
            calls.append(provider)
            return "quota" if provider == "gemini" else "ok"
        self.assertEqual(run_fallback(attempt, config, state, clock=lambda: 100), ("ok", "ollama"))
        self.assertEqual(calls, ["gemini", "ollama"])
        calls.clear()
        run_fallback(attempt, config, state, clock=lambda: 200)
        self.assertEqual(calls, ["ollama"])
        calls.clear()
        run_fallback(attempt, config, state, clock=lambda: 10000)
        self.assertEqual(calls[0], "gemini")

    def test_no_fallback_for_auth_timeout_or_parse(self):
        config = read_json(ROOT / "config/graphify.json")
        for status in ("auth", "timeout", "error", "incomplete"):
            calls = []
            def attempt(provider):
                calls.append(provider)
                return status
            self.assertEqual(run_fallback(attempt, config, {}), (status, "gemini"))
            self.assertEqual(calls, ["gemini"])

    def test_both_provider_quotas_visible(self):
        config = read_json(ROOT / "config/graphify.json")
        state = {}
        self.assertEqual(run_fallback(lambda p: "quota", config, state)[0], "quota")
        self.assertEqual(set(state["cooldowns"]), {"gemini", "ollama"})

    def test_exception_classification(self):
        class FakeError(Exception):
            status_code = 401
        self.assertEqual(classify_exception(FakeError("quota exceeded")), "auth")
        self.assertEqual(classify_exception(RuntimeError("RESOURCE_EXHAUSTED")), "quota")
        self.assertEqual(classify_exception(RuntimeError("connection lost")), "error")

    def test_provider_env_only_contains_attempted_key(self):
        with patch.dict(os.environ, {"UNRELATED_SECRET": "private", "OPENAI_API_KEY": "private", "AWS_SECRET_ACCESS_KEY": "private", "OLLAMA_API_KEY": "private"}):
            env = provider_environment("gemini", {"GEMINI_API_KEY": "selected", "OLLAMA_API_KEY": "other"})
        self.assertEqual(env["GEMINI_API_KEY"], "selected")
        self.assertFalse(set(env) & {"UNRELATED_SECRET", "OPENAI_API_KEY", "AWS_SECRET_ACCESS_KEY", "OLLAMA_API_KEY"})

    def test_dependency_plans_use_platform_managers_without_shell(self):
        self.assertEqual(version_tuple("node v24.1.2"), (24, 1, 2))
        rows = [{"name": "git", "status": "missing"}]
        manager, commands = system_plan("core", rows, "Windows")
        self.assertEqual(manager, "winget")
        self.assertIn("Git.Git", commands[0])
        manager, commands = system_plan("core", rows, "Darwin")
        self.assertEqual(commands, [["brew", "install", "git"]])

    def test_metadata_only_package_is_not_reported_usable(self):
        with tempfile.TemporaryDirectory() as tmp:
            spec = read_json(ROOT / "config/npm-tools-lock.json")["packages"][0]
            manifest = Path(tmp) / ".imrane/npm/node_modules" / spec["name"] / "package.json"
            write_json(manifest, {"name": spec["name"], "version": spec["version"]})
            rows = inspect_managed(tmp)
            item = next(row for row in rows if row["name"] == "managed:" + spec["name"])
            self.assertNotEqual(item["status"], "ok")

    def test_archive_path_and_symlink_guards(self):
        import zipfile
        with tempfile.TemporaryDirectory() as tmp:
            archive = Path(tmp) / "bad.zip"
            with zipfile.ZipFile(archive, "w") as z:
                z.writestr("repo/../../escaped.txt", "bad")
            with self.assertRaises(ValueError):
                unpack_skill(archive, {"path": "."}, Path(tmp) / "skill")
            with zipfile.ZipFile(archive, "w") as z:
                info = zipfile.ZipInfo("repo/link")
                info.external_attr = 0o120777 << 16
                z.writestr(info, "../outside")
            with self.assertRaises(ValueError):
                unpack_skill(archive, {"path": "."}, Path(tmp) / "skill")

    def test_archive_import_preserves_license_and_limits_subtree(self):
        import zipfile
        with tempfile.TemporaryDirectory() as tmp:
            archive = Path(tmp) / "good.zip"
            with zipfile.ZipFile(archive, "w") as z:
                z.writestr("repo/skills/example/SKILL.md", "---\nname: example\n---\nInstructions")
                z.writestr("repo/LICENSE", "MIT")
                z.writestr("repo/private.txt", "excluded")
            dest = Path(tmp) / "skill"
            unpack_skill(archive, {"path": "skills/example"}, dest)
            self.assertTrue((dest / "SKILL.md").exists())
            self.assertTrue((dest / "upstream-license/LICENSE").exists())
            self.assertFalse((dest / "private.txt").exists())

    def test_plugin_paths_are_rebound_to_canonical_source(self):
        with tempfile.TemporaryDirectory() as tmp:
            staged = Path(tmp) / "staged"
            staged.mkdir()
            (staged / "SKILL.md").write_text('python "${CLAUDE_PLUGIN_ROOT}/skills/demo/scripts/run.py"')
            target = Path(tmp) / "canonical"
            adapt_paths(staged, {"path": "skills/demo", "url": "https://github.com/example/fixture", "commit": "test"}, target)
            text = (staged / "SKILL.md").read_text()
            self.assertIn(target.as_posix(), text)
            self.assertNotIn("CLAUDE_PLUGIN_ROOT", text)
            self.assertTrue((staged / "IMRANE_OVERLAY.md").exists())

    def test_generated_skill_mirror_is_not_independently_overwritten(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "canonical"
            source.mkdir()
            (source / "SKILL.md").write_text("canonical fixture")
            destination = Path(tmp) / "lane/.agents/skills/fixture"
            manifest = {}
            with patch.object(Path, "symlink_to", side_effect=OSError("link unavailable")):
                expose(source, destination, manifest)
            self.assertEqual(tree_hash(source), tree_hash(destination))
            expose(source, destination, manifest)
            (destination / "SKILL.md").write_text("independent edit")
            with self.assertRaises(ValueError):
                expose(source, destination, manifest)


if __name__ == "__main__":
    unittest.main()

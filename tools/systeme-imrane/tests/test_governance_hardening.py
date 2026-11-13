"""Regressions for scope validation and concurrent managed-file changes."""
import argparse
import contextlib
import io
import json
import os
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import imrane
from common import ROOT, digest, read_json, write_json


class GovernanceHardeningTests(unittest.TestCase):
    def setUp(self):
        base = ROOT / ".imrane/test-temp"
        base.mkdir(parents=True, exist_ok=True)
        tmp = tempfile.TemporaryDirectory(prefix="governance hardening ", dir=base)
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name).resolve() / "workspace with spaces"
        self.output = io.StringIO()
        quiet = contextlib.redirect_stdout(self.output)
        quiet.__enter__()
        self.addCleanup(quiet.__exit__, None, None, None)

    def new_lane(self):
        imrane.initialize(self.root, apply=True)
        imrane.project_add(argparse.Namespace(workspace=self.root, id="alpha", name="Alpha",
                                                  path="alpha", apply=True, git_init=False))
        return self.root / "alpha"

    def check_errors(self):
        code = imrane.check_workspace(self.root)
        report = json.loads(self.output.getvalue().splitlines()[-1])
        self.assertEqual(code, int(bool(report["errors"])))
        return report["errors"]

    def test_malformed_lane_json_and_toml_reported_without_raw_content(self):
        lane = self.new_lane()
        (lane / ".codex/hooks.json").write_text("PRIVATE_CANARY malformed")
        (lane / ".claude/settings.json").write_text("{}")
        (lane / ".codex/config.toml").write_text("PRIVATE_CANARY broken")
        errors = self.check_errors()
        self.assertEqual(errors, [
            "alpha: .codex/config.toml: unreadable or invalid TOML",
            "alpha: .codex/hooks.json: unreadable or invalid JSON",
            "alpha: .claude/settings.json: missing or invalid hooks object",
        ])
        self.assertNotIn("PRIVATE_CANARY", self.output.getvalue())

    def test_rejects_disabled_hooks_missing_event_and_wrong_command_event(self):
        lane = self.new_lane()
        (lane / ".codex/config.toml").write_text("[features]\nhooks = false\n")
        codex_path = lane / ".codex/hooks.json"
        codex = read_json(codex_path)
        codex["hooks"]["Stop"] = []
        codex["hooks"]["PostToolUse"] = codex["hooks"]["SessionStart"]
        write_json(codex_path, codex)
        claude_path = lane / ".claude/settings.json"
        claude = read_json(claude_path)
        claude["disableAllHooks"] = True
        claude["hooks"]["PreCompact"][0]["hooks"] = "invalid"
        write_json(claude_path, claude)
        self.assertEqual(self.check_errors(), [
            "alpha: .codex/config.toml: expected features.hooks = true",
            "alpha: .codex/hooks.json: PostToolUse: missing unfiltered Système Imrane command for this workspace and event",
            "alpha: .codex/hooks.json: Stop: missing or empty hook groups",
            "alpha: .claude/settings.json: hooks are disabled",
            "alpha: .claude/settings.json: PreCompact: invalid or empty hook handlers",
        ])

    def test_valid_extra_settings_and_custom_hook_are_preserved(self):
        lane = self.new_lane()
        path = lane / ".claude/settings.json"
        claude = read_json(path)
        claude["env"] = {"FIXTURE_ONLY": "owner value"}
        claude["hooks"]["PostToolUse"].append({
            "matcher": "^Read$",
            "hooks": [{"type": "command", "command": "owner-helper"}],
        })
        write_json(path, claude)
        before = path.read_bytes()
        self.assertEqual(self.check_errors(), [])
        self.assertEqual(path.read_bytes(), before)

    def test_managed_hook_only_in_filtered_group_fails_workspace_check(self):
        lane = self.new_lane()
        for rel in (".codex/hooks.json", ".claude/settings.json"):
            path = lane / rel
            settings = read_json(path)
            settings["hooks"]["PostToolUse"][0]["matcher"] = "^NeverARealTool$"
            write_json(path, settings)
        self.assertEqual(self.check_errors(), [
            "alpha: .codex/hooks.json: PostToolUse: missing unfiltered Système Imrane command for this workspace and event",
            "alpha: .claude/settings.json: PostToolUse: missing unfiltered Système Imrane command for this workspace and event",
        ])

    def test_nonregular_managed_target_is_refused(self):
        target = self.root / "directory.txt"
        target.mkdir(parents=True)
        with self.assertRaisesRegex(ValueError, "Expected a regular managed file: directory.txt"):
            imrane.managed(self.root, {"directory.txt": "generated"}, apply=True)
        self.assertTrue(target.is_dir())
        self.assertFalse((self.root / imrane.MANAGED_MANIFEST).exists())

    @unittest.skipUnless(hasattr(os, "mkfifo"), "host does not support FIFOs")
    def test_managed_upgrade_refuses_fifo_without_blocking(self):
        self.root.mkdir()
        target = self.root / "pipe.txt"
        os.mkfifo(target)
        # Use a subprocess so regressing to a blocking read fails with a bounded
        # timeout instead of hanging the suite while waiting for a pipe writer.
        program = (
            "import sys; sys.path.insert(0, sys.argv[1]); from imrane import managed\n"
            "try: managed(sys.argv[2], {'pipe.txt': 'generated'}, apply=True, upgrade=True)\n"
            "except ValueError as exc: print(exc)\n"
            "else: raise SystemExit(1)\n"
        )
        result = subprocess.run([sys.executable, "-B", "-c", program, str(ROOT / "scripts"),
                                 str(self.root)], capture_output=True, text=True, timeout=5, check=True)
        self.assertIn("Expected a regular managed file: pipe.txt", result.stdout)
        self.assertTrue(stat.S_ISFIFO(target.stat().st_mode))
        self.assertFalse((self.root / imrane.MANAGED_MANIFEST).exists())

    def test_edit_during_staging_aborts_entire_batch_before_first_commit(self):
        imrane.managed(self.root, {"first.txt": "old first", "second.txt": "old second"}, apply=True)
        manifest = self.root / imrane.MANAGED_MANIFEST
        before = manifest.read_bytes()
        stage_file = imrane.stage_managed_file

        def edit_first_after_staging_second(target, body, cleanup):
            staged = stage_file(target, body, cleanup)
            if target.name == "second.txt":
                (self.root / "first.txt").write_text("owner edit")
            return staged

        with patch.object(imrane, "stage_managed_file", side_effect=edit_first_after_staging_second):
            with self.assertRaisesRegex(ValueError, "Concurrent change detected: first.txt"):
                imrane.managed(self.root, {"first.txt": "new first", "second.txt": "new second"},
                               apply=True, upgrade=True)
        self.assertEqual((self.root / "first.txt").read_text(), "owner edit")
        self.assertEqual((self.root / "second.txt").read_text(), "old second")
        self.assertEqual(manifest.read_bytes(), before)
        self.assertFalse((self.root / imrane.MANAGED_LOCK).exists())
        self.assertEqual(list(self.root.glob(".imrane-*")), [])

    def test_new_file_appearing_after_final_check_is_preserved(self):
        publish = "rename" if os.name == "nt" else "link"
        original = getattr(os, publish)
        target = self.root / "new.txt"

        def create_at_publish(source, destination):
            if destination == target:
                target.write_text("owner new file")
            return original(source, destination)

        with patch.object(imrane.os, publish, side_effect=create_at_publish):
            with self.assertRaisesRegex(ValueError, "Concurrent change detected: new.txt"):
                imrane.managed(self.root, {"new.txt": "generated file"}, apply=True)
        self.assertEqual(target.read_text(), "owner new file")
        self.assertFalse((self.root / imrane.MANAGED_MANIFEST).exists())

    def test_late_edit_stops_writes_and_keeps_manifest_consistent(self):
        imrane.managed(self.root, {"first.txt": "old first", "second.txt": "old second"}, apply=True)
        commit = imrane.commit_managed_file

        def edit_second_after_commit(workspace, rel, staged, expected):
            commit(workspace, rel, staged, expected)
            if rel == "first.txt":
                (self.root / "second.txt").write_text("late owner edit")

        with patch.object(imrane, "commit_managed_file", side_effect=edit_second_after_commit):
            with self.assertRaisesRegex(ValueError, "Concurrent change detected: second.txt"):
                imrane.managed(self.root, {"first.txt": "new first", "second.txt": "new second"},
                               apply=True, upgrade=True)
        self.assertEqual((self.root / "first.txt").read_text(), "new first")
        self.assertEqual((self.root / "second.txt").read_text(), "late owner edit")
        manifest = read_json(self.root / imrane.MANAGED_MANIFEST)["files"]
        self.assertEqual(manifest["first.txt"], digest(b"new first"))
        self.assertEqual(manifest["second.txt"], digest(b"old second"))
        first_backups = list((self.root / ".imrane/backups").rglob("first.txt"))
        self.assertEqual([path.read_bytes() for path in first_backups], [b"old first"])
        with self.assertRaisesRegex(ValueError, "Existing files differ"):
            imrane.managed(self.root, {"first.txt": "new first", "second.txt": "new second"},
                           apply=True, upgrade=True)
        self.assertEqual((self.root / "second.txt").read_text(), "late owner edit")

    def test_another_managed_writer_is_refused_while_lock_is_held(self):
        with imrane.managed_lock(self.root):
            with self.assertRaisesRegex(ValueError, "Managed files are locked"):
                imrane.managed(self.root, {"new.txt": "blocked"}, apply=True)
        self.assertFalse((self.root / "new.txt").exists())
        imrane.managed(self.root, {"new.txt": "after lock release"}, apply=True)
        self.assertEqual((self.root / "new.txt").read_text(), "after lock release")

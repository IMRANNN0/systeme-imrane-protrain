"""Regression coverage for scoped Graphify query and viewer without a provider."""
import json
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from common import runtime_dir, write_json
from graphify_runtime import collect, query, viewer


class OfflineGraphifyTests(unittest.TestCase):
    def setUp(self):
        temporary = TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.workspace = Path(temporary.name).resolve()
        self.root = self.workspace / "alpha"
        self.lane = runtime_dir(self.workspace, "alpha")
        self.state = self.lane / "graphify-state.json"
        self.output = self.root / "graphify-out"
        self.current = self.root / ".codex/memory/CURRENT.md"
        write_json(self.workspace / ".codex/projects.json", {"projects": [
            {"id": "alpha", "path": "alpha", "graphify_enabled": True},
            {"id": "beta", "path": "alpha/beta", "graphify_enabled": True},
        ]})
        write_json(self.workspace / ".codex/graphify.json", {"max_files": 30, "max_words": 1000})
        write_json(self.root / ".codex/graphify-scope.json",
                   {"include": ["AGENTS.md", ".codex/memory", "beta", "secrets"], "exclude": []})
        (self.root / "AGENTS.md").write_text("# Scoped handoff procedure\n", encoding="utf-8")
        self.current.parent.mkdir()
        self.current.write_text("## Restart checkpoint\n- Next action: reconcile the pilot.\n", encoding="utf-8")
        # Even a provenance record containing these names must not expose them.
        for folder in ("beta", "secrets"):
            path = self.root / folder
            path.mkdir()
            (path / "notes.md").write_text("forbidden", encoding="utf-8")
        self.build()
        for name in ("invoke_provider", "mark_stale", "credentials"):
            guard = patch("graphify_runtime." + name, side_effect=AssertionError(name))
            guard.start()
            self.addCleanup(guard.stop)

    def build(self):
        paths, fingerprint = collect(self.workspace, "alpha")
        write_json(self.state, {"status": "current", "fingerprint": fingerprint})
        write_json(self.output / "imrane-provenance.json", {
            "project_id": "alpha", "fingerprint": fingerprint, "at": "2026-10-23T07:11:26+00:00",
            "files": [*paths, "beta/notes.md", "secrets/notes.md"],
        })
        self.graph = {"nodes": [
            {"id": "handoff", "label": "Handoff <script>alert(1)</script>", "source_file": "AGENTS.md"},
            {"id": "pilot", "label": "Pilot", "source_file": str(self.lane / "graphify-work/corpus/.codex/memory/CURRENT.md")},
            {"id": "private", "label": "forbidden", "source_file": "secrets/notes.md"},
            {"id": "beta", "label": "forbidden", "source_file": "beta/notes.md"},
            {"id": "traversal", "label": "forbidden", "source_file": "../alpha/beta/notes.md"},
            {"id": "empty", "label": "forbidden"},
        ], "links": [
            {"source": "handoff", "target": "pilot", "source_file": "AGENTS.md", "relation": "references"},
            {"source": "handoff", "target": "pilot", "source_file": "beta/notes.md", "relation": "forbidden"},
            {"source": "handoff", "target": "beta", "source_file": "AGENTS.md", "relation": "forbidden"},
        ]}
        write_json(self.output / "graph.json", self.graph)

    def test_current_graph_link_and_canonical_fallback_on_miss(self):
        hit = query(self.workspace, "alpha", "handoff")
        self.assertEqual(hit["status"], "current")
        self.assertIsNone(hit["warning"])
        self.assertEqual(hit["results"][0]["source_url"], (self.root / "AGENTS.md").as_uri())
        self.assertEqual(hit["results"][0]["kind"], "graph")
        hit = query(self.workspace, "alpha", "restart checkpoint")
        self.assertEqual(hit["status"], "current")
        self.assertEqual(hit["results"][0]["kind"], "canonical")
        self.assertEqual(hit["results"][0]["line"], 1)
        self.assertEqual(query(self.workspace, "alpha", "no_such_term")["results"], [])

    def test_stale_checkpoint_aliases_without_mutating_state(self):
        stamp = self.state.stat().st_mtime_ns
        data = self.state.read_bytes()
        self.current.write_text("## Restart checkpoint\n- Next action: review the latest evidence.\n", encoding="utf-8")
        for question in ("Restart Checkpoint", "point de reprise", "fin wslna daba ?", "فين وصلنا؟",
                         "prochaine étape", "شنو نديرو دابا"):
            with self.subTest(question=question):
                hit = query(self.workspace, "alpha", question)
                self.assertEqual(hit["status"], "stale")
                self.assertEqual(hit["last_build"], "2026-10-23T07:11:26+00:00")
                self.assertEqual(hit["results"][0]["source_url"], self.current.as_uri())
                self.assertIn("latest evidence", hit["results"][0]["summary"])
        self.assertEqual(self.state.stat().st_mtime_ns, stamp)
        self.assertEqual(self.state.read_bytes(), data)
        self.assertLessEqual(len(json.dumps(query(self.workspace, "alpha", "checkpoint", 100),
                                           ensure_ascii=False)), 400)

    def test_missing_and_malformed_graph_fall_back_and_mismatch_is_refused(self):
        graph = self.output / "graph.json"
        graph.unlink()
        self.state.unlink()
        self.assertEqual(query(self.workspace, "alpha", "checkpoint")["status"], "not-built")
        self.assertFalse(self.state.exists())
        graph.write_text("{", encoding="utf-8")
        hit = query(self.workspace, "alpha", "checkpoint")
        self.assertEqual(hit["status"], "unavailable")
        self.assertEqual(hit["results"][0]["kind"], "canonical")
        write_json(self.output / "imrane-provenance.json", {"project_id": "beta"})
        with self.assertRaisesRegex(ValueError, "provenance"):
            query(self.workspace, "alpha", "checkpoint")

    def test_scope_restrictions_apply_to_saved_nodes_and_canonical_fallback(self):
        self.assertEqual(query(self.workspace, "alpha", "forbidden")["results"], [])
        write_json(self.root / ".codex/graphify-scope.json", {"include": ["AGENTS.md"], "exclude": []})
        self.assertEqual(query(self.workspace, "alpha", "checkpoint")["results"], [])
        self.assertEqual(query(self.workspace, "alpha", "pilot")["results"], [])

    def test_viewer_exposes_scoped_sources_and_escaped_relationships(self):
        path = viewer(self.workspace, "alpha")
        self.assertEqual(path, self.lane / "graphify-viewer.html")
        html = path.read_text(encoding="utf-8")
        for text in ("<dd>alpha</dd>", "<dd>current</dd>", "2026-10-23T07:11:26+00:00",
                     "2 nodes · 1 relationships", "Handoff &lt;script&gt;alert(1)&lt;/script&gt;",
                     self.current.as_uri(), "references", 'type="search"'):
            self.assertIn(text, html)
        for text in ("forbidden", "beta/notes.md", "secrets/notes.md", "<script>alert(1)</script>"):
            self.assertNotIn(text, html)


if __name__ == "__main__":
    unittest.main()

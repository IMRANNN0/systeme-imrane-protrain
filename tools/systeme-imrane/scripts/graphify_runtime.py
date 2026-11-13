#!/usr/bin/env python3
"""Project-scoped Graphify, visible freshness and quota-only provider fallback."""
from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import time
import unicodedata
from contextlib import contextmanager
from pathlib import Path

from common import (ROOT, atomic_write, digest, inside, now, project_by_id, read_json,
                    registry, relative_path, runtime_dir, write_json)
from dependencies import venv_python

BLOCKED = {".git", ".agents", ".claude", "node_modules", ".venv", "__pycache__", "dist", "build", "tmp", "secrets", "graphify-out", ".imrane", ".graphify-cache"}
EXTENSIONS = {".md", ".txt", ".py", ".ps1", ".sh", ".js", ".mjs", ".cjs", ".jsx", ".ts", ".tsx", ".astro", ".json", ".toml", ".yaml", ".yml", ".css", ".html", ".sql"}
PRIVATE_NAMES = {"auth.json", "hooks.json", "settings.local.json", "package-lock.json", "pnpm-lock.yaml", "yarn.lock"}


MEMORY_FILES = tuple(f".codex/memory/{name}.md" for name in
                     ("CURRENT", "CONTEXT_INDEX", "PROJECT_CONTEXT", "DECISIONS"))
CHECKPOINT_ALIASES = {
    "checkpoint": ("restart checkpoint", "checkpoint", "point de reprise", "fiche de reprise",
                   "فين وصلنا", "فين حبسنا", "فين وقفنا", "فين وصل المشروع", "fin wslna",
                   "fin weslna", "fin wsalna", "fin wslnna", "fayn wslna", "fayn wslnna", "fin 7bsna", "fin hbsna",
                   "fin w9fna", "fin w9efna", "fin wsel l projet"),
    "next action": ("next action", "next step", "prochaine action", "prochaine étape",
                    "étape suivante", "شنو نديرو دابا", "شنو الخطوة الجاية", "ach ndir daba",
                    "chno ndiro daba", "chno ndir daba", "chno lkhoutwa jaya", "ach kayn mn b3d"),
    "stage": ("current stage", "étape actuelle", "stade actuel", "avancement",
              "فين وصل المشروع", "fin wsel l projet"),
    "last verified": ("last verified", "dernier résultat vérifié", "آخر حاجة تأكدنا منها"),
    "blocker": ("blocker", "blocage", "شنو اللي حابسنا", "chno li 7absna"),
    "acceptance": ("acceptance check", "critère d'acceptation", "done when", "fini quand"),
}
QUERY_STOP_WORDS = set("""
    about are can comment could dans des est for from how les par pour que quel quelle
    quels quelles qui show sur the this was were what when where which why with would
    nous notre projet project workspace tell please peux pourrait daba
""".split())
CANONICAL_CHARS = 32_000
CANONICAL_HITS = 3


def unlinked(root, path):
    """Reject symlinks and Windows junctions on every component below root."""
    relative = path.relative_to(root)
    current = root
    for part in relative.parts:
        current /= part
        try:
            info = current.lstat()
        except FileNotFoundError:
            break
        if stat.S_ISLNK(info.st_mode) or getattr(info, "st_file_attributes", 0) & stat.FILE_ATTRIBUTE_REPARSE_POINT:
            return False
    return True


def collect(workspace, project_id):
    project = project_by_id(workspace, project_id)
    if not project.get("graphify_enabled", False):
        raise ValueError("Graphify disabled for this project")
    root = relative_path(workspace, project["path"])
    config = read_json(Path(workspace) / ".codex/graphify.json")
    scope_path = root / ".codex/graphify-scope.json"
    ignore_path = root / ".graphifyignore"
    if not unlinked(root, scope_path) or not unlinked(root, ignore_path):
        raise ValueError("Graphify scope or exclusions cannot be linked")
    scope = read_json(scope_path)
    if not scope or not isinstance(scope.get("include"), list):
        raise ValueError("A reviewed include scope is required")
    excludes = list(scope.get("exclude", []))
    if ignore_path.exists():
        excludes += [line.strip() for line in ignore_path.read_text(encoding="utf-8-sig").splitlines() if line.strip() and not line.startswith("#")]
    other_lanes = [relative_path(workspace, p["path"]) for p in registry(workspace)["projects"] if p["id"] != project_id]
    paths = {}
    words = 0
    for include in scope["include"]:
        relative_path(root, include)  # Validate before traversing the lexical path.
        target = root / include
        if not unlinked(root, target):
            continue
        candidates = sorted(target.rglob("*")) if target.is_dir() else [target]
        for source in candidates:
            if not source.exists() or not source.is_file():
                continue
            rel = source.relative_to(root).as_posix()
            if not unlinked(root, source):
                continue
            inside(root, source)
            if any(source.resolve().is_relative_to(p) for p in other_lanes if p != root and p.is_relative_to(root)):
                continue
            if any(p.casefold() in BLOCKED for p in source.relative_to(root).parts):
                continue
            if source.name.casefold().startswith(".env") or source.name.casefold() in PRIVATE_NAMES or source.suffix.lower() not in EXTENSIONS:
                continue
            if any(fnmatch.fnmatch(rel.casefold(), p.casefold()) or fnmatch.fnmatch(source.name.casefold(), p.casefold()) or rel.casefold().startswith(p.casefold().rstrip("/") + "/") for p in excludes):
                continue
            if rel in paths:
                continue
            if source.stat().st_size > 2_000_000:
                raise ValueError("A scoped file exceeds 2 MB; refine scope")
            content = source.read_bytes()
            try:
                text = content.decode("utf-8-sig")
            except UnicodeDecodeError:
                raise ValueError("Non-UTF8 source in scope; exclude it explicitly") from None
            if re.search(r"(?im)^\s*(?:[A-Z_]*(?:API_KEY|TOKEN|PASSWORD|SECRET))\s*=\s*[\"']?[a-zA-Z0-9_\-/]{16,}", text):
                raise ValueError("Possible credential in scoped source; exclude or sanitize before indexing")
            words += len(text.split())
            paths[rel] = content
            if len(paths) > config["max_files"] or words > config["max_words"]:
                raise ValueError("Scope budget exceeded; refine includes or deliberately adjust configuration")
    if not paths:
        raise ValueError("Empty approved corpus")
    h = hashlib.sha256()
    for rel, content in sorted(paths.items()):
        h.update(rel.encode() + b"\0" + content + b"\0")
    return paths, h.hexdigest()


def mark_stale(workspace, project_id):
    project = project_by_id(workspace, project_id)
    if not project.get("graphify_enabled", False):
        state = {"status": "disabled", "at": now()}
        write_json(runtime_dir(workspace, project_id) / "graphify-state.json", state, private=True)
        return state
    paths, fingerprint = collect(workspace, project_id)
    state_path = runtime_dir(workspace, project_id) / "graphify-state.json"
    state = read_json(state_path, {"status": "not-built"})
    if state.get("fingerprint") != fingerprint or state.get("status") == "disabled":
        state.update({"status": "stale", "pending_fingerprint": fingerprint, "files": len(paths), "at": now()})
        write_json(state_path, state, private=True)
    return state


def credentials(workspace):
    values = {}
    path = Path(workspace) / "secrets/graphify.env"
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            key, sep, value = line.partition("=")
            if sep and key in ("GEMINI_API_KEY", "OLLAMA_API_KEY"):
                values[key] = value.strip()
    for key in ("GEMINI_API_KEY", "OLLAMA_API_KEY"):
        if os.environ.get(key):
            values[key] = os.environ[key]
    return values


@contextmanager
def graph_lock(path):
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    except FileExistsError:
        raise ValueError("Graph refresh already locked; inspect the owning process before manual recovery") from None
    try:
        os.write(fd, str(os.getpid()).encode())
        os.close(fd)
        yield
    finally:
        path.unlink(missing_ok=True)


def invoke_provider(workspace, corpus, provider, spec, config, keys):
    python = venv_python(workspace)
    if not python.exists():
        raise ValueError("Graphify venv missing; run deps --profile complete --apply")
    key_name = "GEMINI_API_KEY" if provider == "gemini" else "OLLAMA_API_KEY"
    if not keys.get(key_name) or not spec.get("model"):
        raise ValueError("Selected provider needs its personal key and configured model")
    if provider == "ollama" and spec.get("base_url") != "https://ollama.com/v1":
        raise ValueError("This Cloud fallback adapter only accepts the official Ollama endpoint")
    env = provider_environment(provider, keys)
    error_file = corpus.parent / "provider-error.json"
    error_file.unlink(missing_ok=True)
    env["IMRANE_PROVIDER_ERROR"] = str(error_file)
    if provider == "ollama":
        env["OLLAMA_BASE_URL"] = spec["base_url"]
        env["OLLAMA_MODEL"] = spec["model"]
    # Remove stale manifests so upstream cannot mistake incomplete extraction for coverage.
    (corpus / "graphify-out/manifest.json").unlink(missing_ok=True)
    command = [str(python), str(ROOT / "scripts/graphify_worker.py"), "extract", str(corpus), "--out", str(corpus),
               "--backend", provider, "--model", spec["model"], "--max-concurrency", str(config["max_concurrency"]),
               "--token-budget", str(config["token_budget"]), "--api-timeout", str(config["api_timeout_seconds"])]
    try:
        # Capture and discard untrusted SDK output; only structured status escapes this boundary.
        result = subprocess.run(command, cwd=corpus, env=env, capture_output=True, timeout=config.get("run_timeout_seconds", 240))
        status = read_json(error_file, {}).get("status")
        if status in ("auth", "error"):
            return status
        checked = subprocess.run([str(python), str(ROOT / "scripts/graphify_worker.py"), "validate", str(corpus)],
                                 cwd=corpus, env=env, capture_output=True, timeout=30)
        if result.returncode == 0 and checked.returncode == 0:
            return "ok"
        return status or "incomplete"
    except subprocess.TimeoutExpired:
        return read_json(error_file, {}).get("status", "timeout")


def provider_environment(provider, keys):
    # No unrelated API tokens, PYTHONPATH injection or credentials for the other
    # provider are inherited by the third-party process.
    system_keys = {"PATH", "SYSTEMROOT", "WINDIR", "SYSTEMDRIVE", "COMSPEC", "PATHEXT",
                   "TEMP", "TMP", "HOME", "USERPROFILE", "LOCALAPPDATA", "APPDATA",
                   "LANG", "LC_ALL", "TZ", "SSL_CERT_FILE", "SSL_CERT_DIR"}
    env = {key: value for key, value in os.environ.items() if key.upper() in system_keys}
    env["PYTHONUTF8"] = "1"
    key = "GEMINI_API_KEY" if provider == "gemini" else "OLLAMA_API_KEY"
    if keys.get(key):
        env[key] = keys[key]
    return env


def run_fallback(attempt, config, state, clock=time.time):
    """A quota-only state machine, independently testable without a live API."""
    primary = config["primary"]["provider"]
    fallback = config["fallback"]["provider"]
    cooldown = state.setdefault("cooldowns", {})
    providers = [primary, fallback] if cooldown.get(primary, 0) <= clock() else [fallback]
    for provider in providers:
        if cooldown.get(provider, 0) > clock():
            continue
        status = attempt(provider)
        if status == "ok":
            cooldown.pop(provider, None)
            return "ok", provider
        if status == "quota":
            cooldown[provider] = clock() + config["cooldown_seconds"]
            continue
        return status, provider  # auth, DNS, malformed JSON, timeout never trigger fallback
    return "quota", None


def refresh(workspace, project_id, allow_network=False, max_run_seconds=None):
    workspace = Path(workspace).resolve()
    paths, fingerprint = collect(workspace, project_id)
    config = read_json(workspace / ".codex/graphify.json")
    if max_run_seconds is not None:
        config["run_timeout_seconds"] = min(config.get("run_timeout_seconds", 240), max_run_seconds)
    if not allow_network:
        print(json.dumps({"plan": "selected-project semantic indexing", "files": list(paths), "network": False}, indent=2))
        return 0
    lane = runtime_dir(workspace, project_id)
    state_path = lane / "graphify-state.json"
    state = read_json(state_path, {})
    project = project_by_id(workspace, project_id)
    destination = relative_path(workspace, project["path"]) / "graphify-out"
    if state.get("status") == "current" and state.get("fingerprint") == fingerprint and (destination / "graph.json").exists():
        print("GRAPHIFY_CURRENT: corpus unchanged")
        return 0
    with graph_lock(lane / "graphify.lock"):
        corpus = lane / "graphify-work/corpus"
        corpus.mkdir(parents=True, exist_ok=True)
        # Synchronize only this toolkit-owned private corpus. Preserve caches, not removed source files.
        for source in corpus.rglob("*"):
            if source.is_file() and "graphify-out" not in source.relative_to(corpus).parts and source.relative_to(corpus).as_posix() not in paths:
                inside(corpus, source).unlink()
        for rel, content in paths.items():
            target = relative_path(corpus, rel)
            if not target.exists() or target.read_bytes() != content:
                atomic_write(target, content.decode("utf-8-sig"), private=True)
        state.update({"status": "building", "at": now()})
        write_json(state_path, state, private=True)
        try:
            keys = credentials(workspace)
            spec = {config["primary"]["provider"]: config["primary"], config["fallback"]["provider"]: config["fallback"]}
            status, provider = run_fallback(lambda p: invoke_provider(workspace, corpus, p, spec[p], config, keys), config, state)
            if status == "ok":
                source = corpus / "graphify-out"
                staged = lane / "graphify-promote"
                if staged.exists():
                    raise ValueError("Unfinished promotion exists; inspect before recovery")
                shutil.copytree(source, staged)
                write_json(staged / "imrane-provenance.json", {"project_id": project_id, "fingerprint": fingerprint, "files": list(paths), "provider": provider, "at": now()})
                previous = lane / ("graphify-previous-" + str(time.time_ns()))
                if destination.exists():
                    destination.rename(previous)
                try:
                    staged.rename(destination)
                except OSError:
                    if previous.exists():
                        previous.rename(destination)
                    raise
                state.update({"status": "current", "fingerprint": fingerprint, "provider": provider, "files": len(paths)})
                state.pop("error", None)
                state.pop("pending_fingerprint", None)
            else:
                state.update({"status": status, "pending_fingerprint": fingerprint, "provider": provider})
        except Exception as exc:
            state.update({"status": "error", "error": type(exc).__name__, "pending_fingerprint": fingerprint})
            raise
        finally:
            state["at"] = now()
            write_json(state_path, state, private=True)
    print("GRAPHIFY_" + state["status"].upper())
    return 0 if state["status"] == "current" else 1


def offline_json(workspace, path):
    if not unlinked(workspace, path):
        raise ValueError("Graphify metadata cannot be linked")
    try:
        data = read_json(path)
    except (ValueError, UnicodeError):
        return None
    return data if isinstance(data, dict) else None


def refresh_local(workspace, project_id):
    """Update the scoped Markdown graph locally when its inputs change."""
    workspace = Path(workspace).resolve()
    project = project_by_id(workspace, project_id)
    root = relative_path(workspace, project["path"])
    scope = offline_json(workspace, root / ".codex/graphify-scope.json") or {}
    if not project.get("graphify_enabled") or scope.get("auto_refresh_local") is not True:
        return "disabled"
    from graphify_local import build_graph

    destination = runtime_dir(workspace, project_id) / "graphify-local.json"
    lock = destination.with_suffix(".lock")
    if not unlinked(workspace, destination) or not unlinked(workspace, lock):
        raise ValueError("Local Graphify runtime cannot be linked")
    with graph_lock(lock):
        paths, fingerprint = collect(workspace, project_id)
        existing = offline_json(workspace, destination) or {}
        graph = existing.get("graph")
        if (existing.get("project_id") == project_id and existing.get("fingerprint") == fingerprint
                and isinstance(graph, dict) and isinstance(graph.get("nodes"), list)):
            return "unchanged"
        write_json(destination, {
            "project_id": project_id, "fingerprint": fingerprint, "files": list(paths),
            "at": now(), "graph": build_graph(paths),
        }, private=True)
    return "updated"


def graph_source(value, corpus, scoped, built):
    if not isinstance(value, str) or not value:
        return None
    source = Path(value)
    if source.is_absolute():
        try:
            source = source.relative_to(corpus)
        except ValueError:
            return None
    if source.drive or source.root or ".." in source.parts:
        return None
    rel = source.as_posix()
    return rel if rel in scoped and rel in built else None


def offline_index(workspace, project_id):
    """Read the selected corpus and intersect graph provenance with its current scope."""
    workspace = Path(workspace).resolve()
    project = project_by_id(workspace, project_id)
    root = relative_path(workspace, project["path"])
    meta = {"project": project_id, "status": "disabled", "last_build": None}
    if not project.get("graphify_enabled", False):
        return root, meta, {}, [], []

    paths, fingerprint = collect(workspace, project_id)
    lane = runtime_dir(workspace, project_id)
    output = root / "graphify-out"
    state = offline_json(workspace, lane / "graphify-state.json") or {}
    graph = offline_json(workspace, output / "graph.json") or {}
    provenance = offline_json(workspace, output / "imrane-provenance.json") or {}
    if provenance.get("project_id") not in (None, project_id):
        raise ValueError("Index provenance does not match selected project")
    local = offline_json(workspace, lane / "graphify-local.json") or {}
    local_graph = local.get("graph")
    semantic_current = (provenance.get("project_id") == project_id and provenance.get("fingerprint") == fingerprint
                        and isinstance(graph.get("nodes"), list))
    if not semantic_current and (
        local.get("project_id") == project_id and local.get("fingerprint") == fingerprint
        and isinstance(local_graph, dict) and isinstance(local_graph.get("nodes"), list)
    ):
        provenance = local
        graph = local_graph
        state = {"status": "current"}
        meta["mode"] = "local-markdown"

    # Old provenance may omit its fingerprint. Its project and file list are
    # still required before any saved node can be exposed.
    files = provenance.get("files")
    raw_nodes = graph.get("nodes")
    built = set()
    status = str(state.get("status", "not-built"))[:24]
    if provenance.get("project_id") == project_id and isinstance(files, list) and isinstance(raw_nodes, list):
        built = {source for source in files if isinstance(source, str)}
        saved_fingerprint = provenance.get("fingerprint", state.get("fingerprint"))
        if saved_fingerprint != fingerprint:
            status = "stale"
        elif status == "not-built":
            status = "current"
        stamp = provenance.get("at")
        if isinstance(stamp, str):
            meta["last_build"] = stamp[:48]
    elif graph or (output / "graph.json").exists():
        status = "unavailable"
    elif status in ("current", "stale"):
        status = "not-built"
    meta["status"] = status

    corpus = lane / "graphify-work/corpus"
    nodes = []
    links = []
    if built:
        for node in raw_nodes:
            if not isinstance(node, dict):
                continue
            rel = graph_source(node.get("source_file"), corpus, paths, built)
            if rel is None:
                continue
            identifier = node.get("id")
            label = node.get("label") or identifier
            if not isinstance(identifier, (str, int)) or not isinstance(label, (str, int)):
                continue
            nodes.append({
                "id": identifier, "kind": "graph", "label": str(label)[:240], "source": rel,
                "source_url": (root / rel).as_uri(),
                "summary": str(node.get("description") or node.get("summary") or "")[:500],
            })
        node_ids = {node["id"] for node in nodes}
        raw_links = graph.get("links", graph.get("edges", []))
        for edge in raw_links if isinstance(raw_links, list) else ():
            if not isinstance(edge, dict):
                continue
            start, end = edge.get("source"), edge.get("target")
            if not isinstance(start, (str, int)) or not isinstance(end, (str, int)):
                continue
            rel = graph_source(edge.get("source_file"), corpus, paths, built)
            if rel and start in node_ids and end in node_ids:
                links.append({"source": start, "target": end, "relation": str(edge.get("relation") or "")[:120],
                              "source_url": (root / rel).as_uri()})
    return root, meta, paths, nodes, links


def normalized(text):
    text = unicodedata.normalize("NFKD", text.casefold())
    return " ".join(re.findall(r"[^\W_]+", "".join(c for c in text if not unicodedata.combining(c))))


ALIASES = {key: tuple(normalized(alias) for alias in aliases) for key, aliases in CHECKPOINT_ALIASES.items()}


def search_terms(text):
    text = f" {normalized(text)} "
    concepts = {key for key, aliases in ALIASES.items() if any(f" {alias} " in text for alias in aliases)}
    for key in concepts:
        for alias in sorted(ALIASES[key], key=len, reverse=True):
            text = text.replace(f" {alias} ", " ")
    words = {word for word in text.split() if len(word) >= 3} - QUERY_STOP_WORDS
    return concepts, words


def relevance(text, concepts, words):
    text = f" {normalized(text)} "
    return (
        2 * sum(any(f" {alias} " in text for alias in ALIASES[key]) for key in concepts)
        + len(words.intersection(text.split()))
    )


def canonical_hits(root, paths, concepts, words):
    ranked = []
    for rel in MEMORY_FILES:
        if rel not in paths:
            continue
        text = paths[rel][:CANONICAL_CHARS].decode("utf-8-sig", errors="ignore")
        headings = list(re.finditer(r"(?m)^#{1,6}[ \t]+(.+)$", text))
        sections = [(0, 0, Path(rel).stem), *((m.start(), m.end(), m[1].strip()) for m in headings)]
        for index, (start, body_start, title) in enumerate(sections):
            end = sections[index + 1][0] if index + 1 < len(sections) else len(text)
            body = text[body_start:end].strip()
            if not body and not index:
                continue
            title_score = relevance(title, concepts, words)
            score = 2 * title_score + relevance(body, concepts, words)
            if score == 0:
                continue
            lines = [line.strip() for line in body.splitlines() if line.strip()]
            if not title_score and lines:
                best = max(range(len(lines)), key=lambda i: relevance(lines[i], concepts, words))
                lines = lines[best:]
            summary = " ".join(lines)
            ranked.append((score, {
                "kind": "canonical", "label": title[:240], "source": rel,
                "source_url": (root / rel).as_uri(), "line": text.count("\n", 0, start) + 1,
                "summary": summary[:357].rstrip() + "…" if len(summary) > 357 else summary,
            }))
    ranked.sort(key=lambda item: item[0], reverse=True)
    return ranked[:CANONICAL_HITS]


def query(workspace, project_id, question, budget=1000):
    if not 100 <= budget <= 8000:
        raise ValueError("Budget must be between 100 and 8000 approximate tokens")
    root, meta, paths, nodes, _ = offline_index(workspace, project_id)
    concepts, words = search_terms(question[:500])
    ranked = [
        (2 * relevance(node["label"], concepts, words) + relevance(
            node["source"] + " " + node["summary"], concepts, words
        ), {key: value for key, value in node.items() if key != "id"})
        for node in nodes
    ]
    graph_hits = [(score, node) for score, node in ranked if score]
    fallback = canonical_hits(root, paths, concepts, words) if meta["status"] != "current" or not graph_hits else []
    warning = None if meta["status"] == "current" else "Graph unavailable or stale. Verify canonical sources."
    result = {**meta, "warning": warning, "results": []}
    for _, hit in sorted([*fallback, *graph_hits], key=lambda item: item[0], reverse=True):
        result["results"].append(hit)
        if len(json.dumps(result, ensure_ascii=False)) <= budget * 4:
            continue
        result["results"].pop()
        if result["results"]:
            break
        # Keep a source for a high-ranked result even at the minimum budget.
        short = {**hit, "summary": ""}
        result["results"].append(short)
        available = budget * 4 - len(json.dumps(result, ensure_ascii=False))
        if available < 0:
            result["results"].pop()
            continue
        short["summary"] = hit["summary"][:available]
        while len(json.dumps(result, ensure_ascii=False)) > budget * 4:
            short["summary"] = short["summary"][:-1]
        break
    return result


def viewer(workspace, project_id):
    from graphify_viewer import render_viewer

    workspace = Path(workspace).resolve()
    root, meta, paths, nodes, links = offline_index(workspace, project_id)
    if meta["status"] == "disabled":
        raise ValueError("Graphify disabled for this project")
    output = runtime_dir(workspace, project_id) / "graphify-viewer.html"
    if not unlinked(workspace, output):
        raise ValueError("Graphify viewer output cannot be linked")
    sources = [{"path": rel, "url": (root / rel).as_uri()} for rel in sorted(paths)]
    atomic_write(output, render_viewer(meta, sources, nodes, links), private=True)
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("refresh", "refresh-local", "query", "status", "viewer"))
    parser.add_argument("--workspace", required=True)
    parser.add_argument("--project", required=True)
    parser.add_argument("--allow-network", action="store_true")
    parser.add_argument("--question", default="")
    parser.add_argument("--budget", type=int, default=1000)
    args = parser.parse_args()
    try:
        if args.command == "refresh":
            return refresh(args.workspace, args.project, args.allow_network)
        if args.command == "refresh-local":
            print("GRAPHIFY_LOCAL_" + refresh_local(args.workspace, args.project).upper())
            return 0
        if args.command == "viewer":
            print(viewer(args.workspace, args.project))
        elif args.command == "query":
            if hasattr(sys.stdout, "reconfigure"):
                sys.stdout.reconfigure(encoding="utf-8")
            print(json.dumps(query(args.workspace, args.project, args.question, args.budget), ensure_ascii=False, indent=2))
        else:
            state = mark_stale(args.workspace, args.project)
            _, meta, _, _, _ = offline_index(args.workspace, args.project)
            if meta.get("mode") == "local-markdown":
                state = {**state, "local_index": meta}
            print(json.dumps(state, indent=2))
        return 0
    except Exception as exc:
        # No raw provider output or untrusted source content in errors.
        print("GRAPHIFY_ERROR: " + (str(exc) if isinstance(exc, ValueError) else type(exc).__name__), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())

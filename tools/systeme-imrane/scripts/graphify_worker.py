"""Pinned Graphify adapter in its isolated venv; never prints SDK exception bodies."""
from __future__ import annotations

import functools
import inspect
import json
import os
import runpy
import sys
from pathlib import Path

from common import write_json


def classify_exception(exc):
    status = getattr(exc, "status_code", None)
    if status == 429:
        return "quota"
    if status in (401, 403):
        return "auth"
    # SDKs without a status attribute sometimes expose the gRPC status.
    text = str(exc).casefold()  # memory only; never persisted or printed
    if "resource_exhausted" in text or "quota exceeded" in text:
        return "quota"
    return "error"


def install_adapter(error_path):
    import graphify.llm as llm
    from graphify.cache import save_semantic_cache

    original_call = llm._call_openai_compat

    @functools.wraps(original_call)
    def observed(*args, **kwargs):
        if os.environ.get("IMRANE_OFFLINE") == "1":
            raise RuntimeError("Offline verification forbids all provider calls")
        try:
            return original_call(*args, **kwargs)
        except Exception as exc:
            status = classify_exception(exc)
            # Stronger auth/error signals take precedence over an earlier quota.
            previous = json.loads(error_path.read_text()) if error_path.exists() else {}
            if previous.get("status") not in ("auth", "error"):
                write_json(error_path, {"status": status}, private=True)
            raise

    llm._call_openai_compat = observed
    original = llm.extract_corpus_parallel
    signature = inspect.signature(original)

    @functools.wraps(original)
    def checkpointed(*args, **kwargs):
        bound = signature.bind(*args, **kwargs)
        bound.apply_defaults()
        root = Path(bound.arguments["root"]).resolve()
        previous = bound.arguments["on_chunk_done"]

        def completed(index, total, result):
            if result.get("finish_reason") == "stop" and result.get("nodes"):
                save_semantic_cache(result["nodes"], result.get("edges", []), result.get("hyperedges", []), root=root)
            if previous:
                previous(index, total, result)

        bound.arguments["on_chunk_done"] = completed
        return original(*bound.args, **bound.kwargs)

    llm.extract_corpus_parallel = checkpointed


def validate(corpus):
    from graphify.cache import check_semantic_cache, load_cached
    from graphify.detect import detect
    graph = json.loads((corpus / "graphify-out/graph.json").read_text(encoding="utf-8"))
    nodes = graph.get("nodes", [])
    if not nodes:
        raise ValueError("Empty graph")
    ids = {str(n["id"]) for n in nodes}
    labels = {str(n.get("label", "")).casefold() for n in nodes if n.get("label")}
    for edge in graph.get("links", graph.get("edges", [])):
        if str(edge.get("source")) not in ids or str(edge.get("target")) not in ids:
            raise ValueError("Dangling graph edge")
    semantic = []
    for kind, paths in detect(corpus).get("files", {}).items():
        if kind in ("document", "paper", "image", "video"):
            semantic.extend(paths)
    _, _, _, missing = check_semantic_cache(semantic, root=corpus)
    if missing:
        raise ValueError("Incomplete semantic cache")
    for path in semantic:
        cached = load_cached(Path(path), root=corpus, kind="semantic") or {}
        anchors = cached.get("nodes", [])
        if not any(str(n.get("id")) in ids or str(n.get("label", "")).casefold() in labels for n in anchors):
            raise ValueError("Unrepresented cached source")
    # Every in-scope code file must have at least a represented file anchor.
    sources = {str(n.get("source_file", "")).replace("\\", "/") for n in nodes}
    detection = detect(corpus).get("files", {})
    for kind, paths in detection.items():
        if kind not in ("code",):
            continue
        for path in paths:
            p = Path(path)
            relative = p.resolve().relative_to(corpus).as_posix()
            if relative not in sources and p.as_posix() not in sources:
                raise ValueError("Unrepresented code source")
    print("GRAPHIFY_COVERAGE_OK")


if __name__ == "__main__":
    if sys.argv[1] == "validate":
        validate(Path(sys.argv[2]).resolve())
    else:
        error_path = Path(os.environ["IMRANE_PROVIDER_ERROR"])
        install_adapter(error_path)
        sys.argv = ["graphify", *sys.argv[1:]]
        runpy.run_module("graphify", run_name="__main__")

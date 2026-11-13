"""Real pinned-package smoke test without an API call or private corpus."""
import importlib.metadata
import importlib.util
import inspect
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from common import atomic_write


def main():
    assert importlib.metadata.version("graphifyy") == "0.8.13"
    import graphify.llm as llm
    assert callable(llm._call_openai_compat)
    assert "on_chunk_done" in inspect.signature(llm.extract_corpus_parallel).parameters
    data = Path(importlib.util.find_spec("graphify").origin).parent / "skill-codex.md"
    assert data.is_file(), "Pinned package lacks expected skill data"
    temp = ROOT / ".imrane/offline-smoke"
    temp.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=temp) as name:
        corpus = Path(name)
        atomic_write(corpus / "example.py", "def double(value):\n    return value * 2\n\ndef quadruple(value):\n    return double(double(value))\n")
        env = os.environ.copy()
        for key in list(env):
            if "API_KEY" in key or key.startswith("GRAPHIFY_"):
                env.pop(key, None)
        env["IMRANE_PROVIDER_ERROR"] = str(corpus / "provider-error.json")
        env["IMRANE_OFFLINE"] = "1"
        # Upstream requires an explicit backend even for code-only extraction.
        # The worker blocks every provider call: this does not contact an Ollama server.
        result = subprocess.run([sys.executable, str(ROOT / "scripts/graphify_worker.py"), "extract", str(corpus), "--out", str(corpus), "--backend", "ollama", "--model", "offline-test"], env=env, capture_output=True, text=True, timeout=90)
        if result.returncode:
            print(result.stdout[-2000:] + result.stderr[-2000:])
            return result.returncode
        checked = subprocess.run([sys.executable, str(ROOT / "scripts/graphify_worker.py"), "validate", str(corpus)], env=env, capture_output=True, text=True, timeout=30)
        if checked.returncode:
            print(checked.stdout[-2000:] + checked.stderr[-2000:])
            return checked.returncode
    print("GRAPHIFY_OFFLINE_SMOKE_OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())

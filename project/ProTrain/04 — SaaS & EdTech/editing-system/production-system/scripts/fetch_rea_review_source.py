"""Download a pinned text-only source snapshot for review, without executing it."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path, PurePosixPath
import hashlib
import json
import urllib.request

COMMIT = "ab8580e38a1255425b0d3b481866590766932079"
BASE = "https://raw.githubusercontent.com/JuneYaooo/rea-video/" + COMMIT + "/"
ROOT = Path(__file__).resolve().parents[2] / "tools" / "rea-video"
SOURCE = ROOT / "source"

def get(url):
    request = urllib.request.Request(url, headers={"User-Agent": "ProTrain-source-review"})
    with urllib.request.urlopen(request, timeout=60) as response:
        data = response.read(5_000_001)
    if len(data) > 5_000_000:
        raise RuntimeError("Unexpectedly large source response")
    return data

def selected(path):
    return (path.startswith(("rea_video/", "skills/rea-video/", "scripts/", "tests/"))
            or path in ("pyproject.toml", "LICENSE", "NOTICE", "README.md")
            or (path.startswith("docs/") and path.count("/") == 1 and path.endswith(".md")))

def fetch(entry):
    relative = PurePosixPath(entry["path"])
    if relative.is_absolute() or ".." in relative.parts:
        raise RuntimeError("Unsafe repository path")
    target = SOURCE.joinpath(*relative.parts)
    if target.is_file():
        existing = target.read_bytes()
        digest = hashlib.sha1(b"blob " + str(len(existing)).encode() + b"\0" + existing).hexdigest()
        if digest == entry["sha"]:
            return {"path": str(relative), "git_blob": digest,
                    "sha256": hashlib.sha256(existing).hexdigest(), "bytes": len(existing)}
        raise RuntimeError("Refusing to overwrite changed source: " + str(relative))
    data = get(BASE + relative.as_posix())
    blob = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
    if blob != entry["sha"]:
        raise RuntimeError("Git blob mismatch: " + str(relative))
    data.decode("utf-8")
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists() and target.read_bytes() != data:
        raise RuntimeError("Refusing to overwrite changed source: " + str(relative))
    target.write_bytes(data)
    return {"path": str(relative), "git_blob": blob,
            "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)}

def main():
    tree = json.loads(get("https://api.github.com/repos/JuneYaooo/rea-video/git/trees/" + COMMIT + "?recursive=1"))
    if tree.get("truncated"):
        raise RuntimeError("Incomplete source tree")
    entries = [item for item in tree["tree"] if item["type"] == "blob" and selected(item["path"])]
    with ThreadPoolExecutor(max_workers=8) as pool:
        files = list(pool.map(fetch, entries))
    manifest = {"repository": "https://github.com/JuneYaooo/rea-video", "commit": COMMIT,
                "scope": "text-only review snapshot; no upstream code executed", "files": files}
    ROOT.mkdir(parents=True, exist_ok=True)
    (ROOT / "source-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"commit": COMMIT, "files": len(files), "bytes": sum(x["bytes"] for x in files),
                      "source": str(SOURCE)}))

if __name__ == "__main__":
    main()

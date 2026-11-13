"""Bounded local analysis adapter for the reviewed, pinned rea-video installation.

Creates a new run each time. Does not permit VLM, generation, paid APIs, or remakes.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import uuid

SYSTEM = Path(__file__).resolve().parents[1]
TOOL = SYSTEM.parent / "tools" / "rea-video"
PYTHON = TOOL / ".venv" / "Scripts" / "python.exe"
# OpenCV's native ONNX loader cannot open this Windows workspace's em-dash path.
# Keep this model in the selected client's existing private ASCII runtime lane.
MODELS = Path("{{IMRANE_WORKSPACE_ROOT}}/tmp/codex-session/projects/protrain/rea-video-models")

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("video", type=Path)
    args = ap.parse_args()
    video = args.video.resolve(strict=True)
    if not video.is_file() or video.stat().st_size > 200_000_000:
        raise SystemExit("Expected a local video of at most 200 MB")
    probe = subprocess.run(["ffprobe", "-v", "error", "-show_format", "-show_streams", "-of", "json", str(video)],
                           check=True, capture_output=True, text=True, encoding="utf-8", timeout=30)
    meta = json.loads(probe.stdout)
    duration = float(meta["format"]["duration"])
    stream = next(x for x in meta["streams"] if x["codec_type"] == "video")
    if not 0 < duration <= 120 or stream["width"] * stream["height"] > 3840 * 2160:
        raise SystemExit("Pilot limit: 120 seconds, at most UHD pixel count")
    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-rea-" + uuid.uuid4().hex[:8]
    out = SYSTEM / "runs" / run_id
    out.mkdir(parents=True, exist_ok=False)
    env = os.environ.copy()
    for key in list(env):
        if key.startswith(("REA_VLM_", "VIDEO_ANALYSIS_", "GEMINI3_", "CAPSULE_")) or key.endswith("_API_KEY"):
            del env[key]
    env.update(REA_VIDEO_HOME=str(TOOL / "state"), REA_VIDEO_MODELS=str(MODELS),
               PYTHONIOENCODING="utf-8", PYTHONUTF8="1", OMP_NUM_THREADS="1")
    command = [str(PYTHON), "-m", "rea_video", "decompose", str(video), "-o", str(out),
               "--no-vlm", "--no-whole", "--no-ocr", "--no-stems", "--no-asr", "--no-speakers",
               "--workers", "1", "--lang", "en"]
    record = {"input": str(video), "input_sha256": hashlib.sha256(video.read_bytes()).hexdigest(),
              "duration_seconds": duration, "source_commit": "ab8580e38a1255425b0d3b481866590766932079",
              "disabled": ["VLM", "whole-video VLM", "OCR", "stems", "ASR", "speaker separation", "generation"],
              "review_state": "machine output, visual/listening review required", "command": command}
    (out / "invocation.json").write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"run": str(out), "input_seconds": duration}), flush=True)
    try:
        with (out / "analysis.log").open("w", encoding="utf-8") as log:
            result = subprocess.run(command, env=env, cwd=SYSTEM, stdout=log, stderr=subprocess.STDOUT, timeout=600)
        record["exit_code"] = result.returncode
        record["outputs"] = {name: (out / name).is_file() for name in ("report.html", "VIDEO.md", "breakdown.json", "storyboard.jpg")}
    except subprocess.TimeoutExpired:
        record["exit_code"] = "timeout"
    (out / "invocation.json").write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"run": str(out), "exit_code": record["exit_code"], "outputs": record.get("outputs", {})}))
    return 0 if record["exit_code"] == 0 and all(record["outputs"].values()) else 1

if __name__ == "__main__":
    sys.exit(main())

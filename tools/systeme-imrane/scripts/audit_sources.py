"""Maintainer-only provenance refresh. No skill bodies, secrets or project data exported."""
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

from common import ROOT, now, write_json

REPOS = {
    "dp": "kabde/dp-createur", "seo": "kabde/seo-skills",
    "emil": "emilkowalski/skills", "impeccable": "pbakaus/impeccable",
    "humanizer": "blader/humanizer", "taste-skill": "Leonxlnx/taste-skill",
    "unlazy": "Leonxlnx/unlazy", "graphify": "Graphify-Labs/graphify",
    "canonry": "Canonry/canonry",
    "ui-ux-pro-max": "nextlevelbuilder/ui-ux-pro-max-skill",
}
EMIL = set("animate animate-expo animation-vocabulary apple-design ask-sonner emil-design-eng find-animation-opportunities improve-animations mobile-native pick-ui-library prototype review-animations write-swift".split())


def gh(endpoint):
    result = subprocess.run(["gh", "api", endpoint], check=True, capture_output=True, text=True, encoding="utf-8")
    return json.loads(result.stdout)


def source_for(name):
    if name.startswith("dp-"):
        return "dp", f"skills/{name}"
    if name.startswith("seo"):
        special = {"seo-image-gen": "extensions/banana/skills/seo-image-gen", "seo-dataforseo": "extensions/dataforseo/skills/seo-dataforseo", "seo-firecrawl": "extensions/firecrawl/skills/seo-firecrawl"}
        return "seo", special.get(name, f"skills/{name}")
    if name in EMIL:
        return "emil", f"skills/{name}"
    return {
        "impeccable": ("impeccable", ".agents/skills/impeccable"),
        "humanizer": ("humanizer", "."), "taste-skill": ("taste-skill", "skills/taste-skill"),
        "unlazy": ("unlazy", "."), "graphify": ("graphify", None), "canonry": ("canonry", "skills/canonry"),
        "ui-ux-pro-max": ("ui-ux-pro-max", ".claude/skills/ui-ux-pro-max"),
    }.get(name, (None, None))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--library", required=True, help="Generic skill library, not project contents")
    args = parser.parse_args()
    library = Path(args.library)
    names = sorted(p.name for p in library.iterdir() if (p / "SKILL.md").is_file())
    names = sorted(set(names + ["ui-ux-pro-max"]))
    metadata = {}
    for key, repo in REPOS.items():
        info = gh(f"repos/{repo}")
        ref = "v0.8.13" if key == "graphify" else info["default_branch"]
        commit = gh(f"repos/{repo}/commits/{ref}")["sha"]
        license_info = gh(f"repos/{repo}/license?ref={commit}")
        tree = gh(f"repos/{repo}/git/trees/{commit}?recursive=1")
        if tree.get("truncated"):
            raise ValueError("Truncated source tree; narrow manually")
        metadata[key] = {"repo": repo, "commit": commit, "license": (license_info.get("license") or {}).get("spdx_id"),
                         "paths": {entry["path"] for entry in tree["tree"] if entry["type"] == "blob"}}
    entries = []
    for name in names:
        key, path = source_for(name)
        entry = {"name": name, "status": "unresolved", "reason": "Local installation has no verifiable upstream provenance; not redistributed or auto-installed."}
        if key:
            meta = metadata[key]
            entry.update({k: meta[k] for k in ("repo", "commit", "license")})
            entry["url"] = "https://github.com/" + meta["repo"]
            if path is not None:
                marker = (path + "/" if path != "." else "") + "SKILL.md"
                if marker in meta["paths"]:
                    entry.update(status="github", path=path, reason="Pinned verified public upstream; local adaptations are not silently copied.")
                else:
                    entry["reason"] = "Known source but matching SKILL.md path is absent at the pinned revision."
            else:
                entry.update(status="package", reason="Install through the pinned package/runtime, not an invented SKILL.md path.")
        entries.append(entry)
    # Package Graphify installs host-specific SKILL.md content from its official wheel.
    write_json(ROOT / "config/skills-lock.json", {"schema": 1, "audited_at": now(), "inventory_count": len(names), "skills": entries})
    packages = []
    for name in ("lighthouse", "pa11y", "linkinator", "playwright", "sharp", "@canonry/canonry", "@openai/codex"):
        cmd = "npm.cmd" if __import__("os").name == "nt" else "npm"
        result = subprocess.run([cmd, "view", name, "version", "--json"], check=True, capture_output=True, text=True)
        packages.append({"name": name, "version": json.loads(result.stdout), "profile": "optional-host" if name == "@openai/codex" else "complete"})
    write_json(ROOT / "config/npm-tools-lock.json", {"audited_at": now(), "packages": packages})
    print(json.dumps({"skills": len(names), "github": sum(e["status"] == "github" for e in entries), "packages": len(packages)}))


if __name__ == "__main__":
    main()

# Dependencies and capability boundaries

The bootstrap, workspace/memory commands, routing metadata, work-management CLI
and offline graph code run on Python 3.11+ standard library. They do not require
pip, npm, administrator privileges, API credentials or a network connection.

The following are optional capabilities. Run `python scripts/bootstrap.py doctor`
to inspect this machine. Its `ok` means the diagnostic completed, not that every
optional capability is installed. Review a tool's actual task requirements and
the generated dependency plan before authorizing installation.

| Capability | What you need separately |
| --- | --- |
| Git backup | Git, your private repository access and personal authentication |
| Codex | Supported client, personal login/subscription, account model access and native worker support |
| Claude Code | Supported client and personal login; Claude model choices remain personal |
| Native hooks | Client support, workspace trust and an observed real lifecycle event after reload |
| Media checks | FFmpeg/FFprobe; optional ExifTool and image/PDF tools |
| Remotion/video studio | Node/npm and the selected project's reviewed package manifest; browser/font dependencies |
| Browser QA | Node/npm, Playwright/Chromium or another explicitly chosen browser backend |
| UI skill helpers | Some use Python, Node/npm or optional downloads; read their entrypoint before executing |
| SEO research | Browser access or optional DataForSEO/Firecrawl/other connectors with your own accounts |
| Semantic Graphify | Reviewed package/environment, provider SDK/model, personal credentials and explicit corpus/destination approval |
| Image/voice generation | The actual authorized host tool or provider/account; no paid generation runtime is bundled |

The engine retains dependency manifests and a plan/apply dependency CLI. Bootstrap
never runs its installation mode. Use its plan first if later authorized:

```text
python tools/systeme-imrane/scripts/imrane.py doctor --profile complete --workspace <workspace>
python tools/systeme-imrane/scripts/imrane.py deps --workspace <workspace> --profile complete
```

Some skill instructions reference optional connectors, adjacent skills or vendor
tools that are intentionally absent. Such references are not installed plugins
and do not authorize network calls, downloads or publication. No plugin cache,
Codex/Claude account state, local venv or node_modules is copied into this kit.

Generic skill provenance is in `kit/skills-manifest.json`; source grants remain
beside each skill. The current video production review and static creative review
notes are bundled. The library omits affiliate workflows and the DP production
suite. Generic methods may mention affiliate metrics as an example, which does
not add an affiliate skill or client corpus.

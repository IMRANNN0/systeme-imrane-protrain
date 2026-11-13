# Codex plugins: observed inventory and workflow needs

The October 20, 2026 observation used `codex plugin list --json` with access to the
remote catalogue and found 25 installed/enabled plugins. Observed names,
marketplace references and versions are in
[codex-plugins-observed.json](../config/codex-plugins-observed.json). It contains
no local paths, tokens or personal authorizations. Another account may have
different plugins or versions; verify its current capabilities.

## Exact observed names and purpose

| Installed plugin | Purpose / requirement |
| --- | --- |
| Product Design (`product-design`) | Recommended for canvases, visual fidelity, audits and image-to-code work |
| Browser (`browser`) | Web pages and journeys; choose a host-compatible browser capability |
| Unified Computer Use (`unified-computer-use`) | Another browser-control surface; avoid unnecessary duplication |
| Chrome (`chrome`) | Useful for workflows using Chrome |
| Computer Use (`computer-use`) | Computer-control integration/instructions; capabilities depend on the host |
| Opera Browser Connector | Existing Opera tabs; requires the recipient's own Opera connection |
| Code Review (`code-review`) | Recommended for independent code review |
| Codex App Tools (`codex-app-tools`) | Desktop panels, tasks, worktrees and related features; not a Python engine prerequisite |
| HumanWriting (`humanwriting`) | Optional editorial support, distinct from the GitHub Humanizer skill |
| Documents (`documents`) | Word document creation/review when needed |
| PDF (`pdf`) | PDF inspection, rendering and verification |
| Spreadsheets (`spreadsheets`) | Tables, imports and data checks |
| Presentations (`presentations`) | Slide decks; unnecessary for a simple website |
| Template Creator (`template-creator`) | Reusable artifact templates |
| Vercel (`vercel`) | Only when selected hosting/services use Vercel |
| Sites (`sites`) | Projects built/published with OpenAI Sites; not required for every Astro site |
| Notion (`notion`) | Data/workflows explicitly managed in Notion |
| Pages (`pages`) | ChatGPT spaces/documents; not canonical workspace Markdown memory |
| Canva (`canva`) | Canva design/collaboration with a personal connected account |
| Adobe Acrobat | Advanced document/PDF work when used |
| TaskNotify | Authorized notifications; no shared Telegram address or connection |
| Visualize (`visualize`) | Optional explanatory visualizations |
| OpenAI Templates (`openai-templates`) | Optional host-provided templates |
| Plugin Management (`plugin-management`) | Host inventory, discovery and connection management |
| Work Pets (`work-pets`) | Application personalization; unnecessary for project governance |

The three `app-` names were resolved through public manifests: Opera Browser
Connector, Adobe Acrobat and TaskNotify. Use readable UI titles; exact references
remain in JSON. A historical local Hostinger configuration was observed but was
absent from the remotely accessible installed inventory, so it is not presented
as an installed or required dependency.

## What to install

The portable core requires no Codex plugin. Git/Python, kit files and supported
clients provide governance, memory and hooks. Graphify is a separate package/skill,
not a required Codex plugin; this also supports Claude Code.

For an editorial website workflow, Product Design and Code Review are recommended;
one browser capability is enough for visual checks. Add document tools according
to deliverables and one suitable hosting service, rather than installing all
browsers or both Vercel and Sites by default.

[Profiles](../config/plugin-profiles.json) distinguish core, publisher-design,
editorial, office, vercel-hosting, sites-hosting and notion-operations. AFbooster,
Canonry, OpenSERP, Screaming Frog, DataForSEO and Firecrawl may be MCPs, CLIs or
external accounts. An available tool is not proof of a publicly installable Codex
plugin. Connections and permissions remain personal.

## Inspect the recipient's machine

```text
python scripts/plugins.py inventory
python scripts/plugins.py plan --profile publisher-design
python scripts/plugins.py plan --profile editorial
codex plugin list --json
codex plugin add --help
```

`plugins.py` reads the current client rather than the maintainer's snapshot. It
distinguishes installed, enabled and incomplete remote-catalogue states. It does
not verify OAuth. It supplies a plan without hidden installation or permission
changes. The observed client syntax was `codex plugin add NAME@MARKETPLACE`;
original references are provided, but availability must be rechecked per account.

For runtime/bundled plugins, use the recipient's Codex features instead of copying
another machine's caches. For service plugins, open Plugins in Codex, find the
exact name, install, connect a personal account and choose permissions. If the
client lacks plugin commands, use its UI; do not invent commands.

Claude Code shares the architecture and compatible skills, not the Codex plugin
runtime. Use an authorized equivalent connector/MCP/tool where needed. A plugin
does not include its service subscriptions or authorize changing approval policy.

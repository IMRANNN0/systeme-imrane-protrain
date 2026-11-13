# Detailed installation

## 1. Access and machine

Use an authorized copy of Imrane System with its retained private-collaboration LICENSE and NOTICE. Historical
upstream is `systeme-ashraf/systeme-ashraf`, commit
`e626d1a1b887bae4cf825772a684cc6fd3af09ec`; cloning it does not provide these
adaptations. See [provenance and sharing](SHARING.md). Each recipient uses personal
accounts. The system targets Windows/macOS, local Codex desktop/CLI, and Claude Code.
A remote-container assistant needs dependencies inside its container; software
installed on the PC is not automatically available there.

For the first trial, choose a new folder **separate from the clone**. In existing
workspaces, divergent files remain conflicts. The installer does not blindly merge
AGENTS.md or private configuration.

## 2. Tool checks and dependencies

`bootstrap.ps1` or `bootstrap.sh` finds an executable Python >=3.11. Microsoft Store
aliases are not treated as a working Python installation. Without Python, the plan
proposes Winget Python 3.12 or Homebrew python@3.12. After installation, reopen the
terminal and resume. The global PATH is not changed automatically.

**Core** checks Git, Python, Node.js/npm, ripgrep, jq, and GitHub CLI. **Complete**
adds FFmpeg/FFprobe, ExifTool, Poppler, an isolated Python environment, and local npm
tools. JSON is a data format, not an application to install; `jq` processes it.

Sources/minimum versions: [dependency manifest](../config/dependencies.json).
Exact npm versions: [lock](../config/npm-tools-lock.json).

| Tool family | Location or mechanism |
| --- | --- |
| System commands | Official Winget on Windows, Homebrew on macOS |
| Graphify and Gemini/Ollama SDKs | `<workspace>/.imrane/venv`, no global pip |
| Pillow, pypdf, python-docx, openpyxl, PyYAML, ReportLab | Same venv; exact direct versions in manifest |
| Lighthouse, Pa11y, Linkinator | `<workspace>/.imrane/npm/node_modules/.bin` |
| Playwright/Chromium, Sharp, Canonry | Same local npm library; explicit Chromium download |
| Codex / Claude Code | Official client installation and personal account |
| SEO data / connectors | Personal setup, no shared account |

Installations may request OS confirmation. The tool does not force sudo, disable
the sandbox, or accept agreements for the recipient. If Winget is absent, install
Microsoft App Installer. If Homebrew is absent, follow [brew.sh](https://brew.sh/)
and resume using the authorized procedure.

Bootstrap sequences prerequisites, architecture, and verified catalogue skills.
Ten unresolved origins produce an explicit incomplete result (exit 1) without
undoing valid installations. Core does not prepare Graphify or install optional
skills; use Complete for the known online catalogue or later install targeted
GitHub skills. The complete distribution's separate offline library is installed
using this private kit's root `scripts/bootstrap.py`, not by the historical online catalogue.

```text
python scripts/imrane.py doctor --profile complete
python scripts/imrane.py deps --workspace <workspace> --profile complete
python scripts/imrane.py deps --workspace <workspace> --profile complete --apply
```

With `--workspace`, Complete doctor also checks Graphify/SDKs, local npm versions,
and Playwright Chromium. Personal connections are a separate check. Recheck after
installation; a terminal restart may be necessary.

## 3. Assistant clients

Install Codex using its [official instructions](https://developers.openai.com/codex/cli/)
or the desktop application. The optional `@openai/codex` npm package is recorded in
the lock; it is not silently installed globally. For Claude Code, follow the
[official native setup](https://code.claude.com/docs/en/setup). Log in with your own
account. The kit exports neither authentication nor subscriptions.

Initialization creates `.codex/config.toml` enabling local hooks,
`.codex/hooks.json`, and `.claude/settings.json`, without changing host security
policies. Hook paths are generated for the current machine. The user must trust
the repository in the assistant before its configuration loads. Local hooks are
not promised on cloud-orchestration surfaces that do not support them. References:
[Codex](https://learn.chatgpt.com/docs/config-file/config-reference),
[Claude Code](https://code.claude.com/docs/en/hooks).

## 4. Create and qualify projects

Initialize with `init --apply`, register each project with `project-add --apply`,
then fill its AGENTS.md, mission, stack, and validation commands. `--git-init`
creates an independent repository without committing or publishing. The default
remains null without `--set-default`. Root governance has its descriptor, four
neutral memories, and an initial corpus limited to those memories and AGENTS.md.
No client context or previous consent is copied.

If the workspace has a Git repository, do not accidentally track independent
business folders. Choose an explicit `.gitignore` or submodule strategy.

Generated `.agents/skills` and `.claude/skills` wrappers make the engine discoverable.
The actual engine lives under `tools/systeme-imrane`. Other skills are installed
separately. The shared library and its Claude view stay at governance only.

## 5. Personal models, credentials, and capabilities

Choose models available to your account for all six levels in
`.codex/model-routing-policy.json`. Bindings remain empty until chosen.
[Model routing](MODEL_ROUTING.md) documents the levels and
`scripts/models.py --preset codex-sol-luna-6`, first as a plan, then `--apply`.
Codex reasoning effort varies with complexity; Claude retains its own bindings.
Hooks do not switch the active model or enable unsupported delegation.

Run `scripts/agents.py --workspace <workspace>` and its `--apply` variant to
generate configured native roles. Missing models are not guessed. Personal
policies and generated roles are ignored by Git; neutral shareable templates
remain in `tools/systeme-imrane/config/`.

Only in your interactive terminal:

```text
python scripts/imrane.py secrets --workspace <workspace>
```

Enter personal GEMINI_API_KEY/OLLAMA_API_KEY values without pasting them into chat.
Choose models in `.codex/graphify.json`, inspect each project's corpus, and read
[Graphify](GRAPHIFY.md). Semantic indexing can consume credits and requires explicit
network authorization.

Plugins/MCP servers need separate connections, sometimes paid. The
[capability catalogue](../config/plugin-catalogue.json) explains what cannot be
obtained through `pip install` or by copying the maintainer's settings.

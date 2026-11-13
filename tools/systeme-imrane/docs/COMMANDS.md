# Command reference

From the engine directory, use `python scripts/...`. From an installed workspace,
use `python tools/systeme-imrane/scripts/...`. On macOS, substitute `python3` if
needed. `<workspace>` is the recipient's absolute path. Quote paths containing spaces.

## Installation and projects

```text
python scripts/imrane.py --help
python scripts/imrane.py doctor --profile core
python scripts/imrane.py doctor --profile complete
python scripts/imrane.py deps --workspace <workspace> --profile complete
python scripts/imrane.py deps --workspace <workspace> --profile complete --apply
python scripts/imrane.py init --workspace <workspace>
python scripts/imrane.py init --workspace <workspace> --apply
python scripts/imrane.py project-add --workspace <workspace> --id demo --path projects/demo --name "Demo" --git-init --apply
python scripts/imrane.py project-add --workspace <workspace> --id demo --path projects/demo --name "Demo" --set-default --apply
python scripts/imrane.py select --workspace <workspace> --id demo
python scripts/imrane.py check --workspace <workspace>
python scripts/imrane.py snapshot --workspace <workspace> --id demo
python scripts/imrane.py secrets --workspace <workspace>
```

Without `--apply`, `init`, `project-add`, and `deps` show plans. `select`, `snapshot`,
and `secrets` intentionally write state; they are not simulations. Project names
may contain spaces; IDs remain ASCII slugs. Project paths must stay within the
workspace, without `..`, escaping symlinks, or absolute paths.

The default remains null without `--set-default`, including for the first project.
The root then resolves governance and its four memories unless explicitly selected.
An incomplete snapshot saves available memories and exits 1. Inspect `complete`,
`missing`, `errors`, and `completeness` in its JSON.

## Historical online skill catalogue

```text
python scripts/skills.py list
python scripts/skills.py install --workspace <workspace> --name humanizer
python scripts/skills.py install --workspace <workspace> --name humanizer --apply
python scripts/skills.py install --workspace <workspace> --all --apply
```

`--all` reports unresolved sources and returns 1 while entries remain unavailable;
verified installations already completed are retained. Conflicts or unsafe archives
return 2. Existing unmanaged skills are not overwritten. `.agents/skills` and
`.claude/skills` are created at governance only; projects receive no catalogue copies.
For this curated offline edition, use the distribution-root `scripts/bootstrap.py`
instead, as described in the main README.

## Plugins, models, and agent roles

Read-only Codex plugin inspection:

```text
python scripts/plugins.py inventory
python scripts/plugins.py plan --profile publisher-design
```

[Plugin names and matrix](PLUGINS.md). No plugin is required by the portable core;
profiles only recommend useful capabilities.

After checking account capabilities, explicitly adopt the optional Codex preset:

```text
python scripts/models.py --workspace <workspace> --preset codex-sol-luna-6
python scripts/models.py --workspace <workspace> --preset codex-sol-luna-6 --apply
```

The plan shows six bindings; apply backs up the policy and preserves Claude.
Without a preset, personal bindings stay unchanged. [Complexity routing](MODEL_ROUTING.md).
Then generate roles:

```text
python scripts/agents.py --workspace <workspace>
python scripts/agents.py --workspace <workspace> --apply
```

This prepares up to six configured roles per client in `.codex/agents/*.toml` and
`.claude/agents/*.md`, at governance and existing projects. Empty bindings generate
no role. Reload and inspect the host's roles; support depends on version and host.
No delegation launches. Rerun after adding a lane; `--upgrade` preserves locally
edited managed files as conflicts. Permissions remain inherited from the host.

Automatic delegation starts disabled. After configuring/reviewing all six Codex
models/roles and confirming host support:

```text
python scripts/imrane.py routing --workspace <workspace> --enable
python scripts/imrane.py routing --workspace <workspace> --enable --apply
python scripts/imrane.py routing --workspace <workspace> --disable --apply
```

The CLI records recipient choice without changing the active model or host config
and without launching agents. The installed adapter
`tools/imrane-route.py --workspace <workspace> --cwd <cwd> --session-id <id>` reads
`{"prompt":"..."}` on stdin and emits a decision only. The controller must read
the opt-in policy, start a native worker, wait, and verify. Prompts are not stored.
Missing opt-in, model, or host support produces a visible failure.

## Graphify

```text
python scripts/graphify_runtime.py status --workspace <workspace> --project demo
python scripts/graphify_runtime.py refresh --workspace <workspace> --project demo
python scripts/graphify_runtime.py refresh --workspace <workspace> --project demo --allow-network
python scripts/graphify_runtime.py query --workspace <workspace> --project demo --question "Where is routing defined?" --budget 1200
```

Without authorization, `refresh` previews the corpus without transmitting it.
`status` can mark the index stale. `query` is a bounded local search returning
files to inspect; it does not call an LLM to answer instead of the agent.

## Validation and maintenance

```text
python -m unittest discover -s tests -v
python scripts/release_check.py
python scripts/release_check.py --root <workspace>/tools/systeme-imrane
python scripts/imrane.py init --workspace <workspace> --upgrade
python scripts/imrane.py init --workspace <workspace> --upgrade --apply
```

Upgrades replace only unchanged managed files. Others remain conflicts for manual
merging. [Maintenance](MAINTENANCE.md) covers backups and hook regeneration after
moving directories or changing Python.

The same explicit inventory validates source and installation, including legal
files, bootstrap, tests, and three adapters. `check` parses generated JSON/TOML and
compares known hook targets without executing commands. It reports unverified
custom commands; it does not prove host trust or native hook loading.

Local npm commands do not change global PATH. Invoke them through:

```text
python scripts/tool.py --workspace <workspace> lighthouse --version
python scripts/tool.py --workspace <workspace> pa11y --version
python scripts/tool.py --workspace <workspace> linkinator --version
python scripts/tool.py --workspace <workspace> playwright --version
python scripts/tool.py --workspace <workspace> canonry --help
```

Actions remain limited to the requested scope. Installing a tool does not authorize
crawling, remote writes, or publication.

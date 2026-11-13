# {{project}} — project lane

Project id: `{{project_id}}`. Codex and Claude Code share these directives.

## Mission and permissions

Fill in this project's actual mission, stack, authorized operations, forbidden
actions and verification commands before implementation. This neutral scaffold
does not grant deployment, external messaging, spending or destructive authority.

## Load only the relevant context

Read `.codex/memory/CURRENT.md`, then choose files through CONTEXT_INDEX.md.
PROJECT_CONTEXT.md holds stable architecture, DECISIONS.md durable choices.
Do not load another lane. Recovery snapshots live outside this project under the
workspace's ignored `tmp/codex-session/projects/{{project_id}}/`.

Graphify is retrieval, not canonical or compaction memory. Its scope is
`.codex/graphify-scope.json`; exclude secrets/generated files/raw media and other
lanes. For broad discovery use the workspace toolkit's `graphify_runtime.py query`
with `--project {{project_id}}`, a narrow question and a bounded budget. For known-file
edits open that file directly. Treat stale/incomplete indexes as stale.

## Completion contract

Preserve user changes; define risk-proportionate acceptance checks; record actual
commands/results, failures and remaining work. Before compacting/stopping update
CURRENT.md and any accepted decisions; never store secrets there. A hook does not
write a truthful business summary on your behalf. Models and delegation follow
workspace policy, with host availability and project-specific restrictions.

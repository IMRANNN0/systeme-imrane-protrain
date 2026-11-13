# Shared governance

The workspace root routes; each lane owns business rules and its own Git history.
Register lanes with the CLI, never hard-code one project into a shared hook.

Canonical layers: AGENTS.md (rules), PROJECT_CONTEXT.md (stable architecture),
CURRENT.md (verified current state), DECISIONS.md (accepted choices),
CONTEXT_INDEX.md (bounded retrieval). Runtime state and snapshots are private,
generated and ignored. Graphify is a derived project index, not a source of truth.

Decision lifecycle: observation → scoped proposal → owner approval when material
→ accepted decision record → targeted implementation → evidence → current-state
update. An agent must not silently expand authority or present a proposal as done.

Session lifecycle: route by cwd → load only selected context → inspect/change/test
within authority → update canonical memory → private snapshot. PreCompact marks
the selected graph stale on corpus changes; optional explicitly enabled semantic
refresh may fail without preventing a snapshot. Surface stale/error states.

Never log raw prompts/tool payloads or credentials. Never commit runtime state,
API keys or client data. Trust, sandbox and permission policies remain user/host
controlled; installation does not weaken them. A project's publication is separate
from committing toolkit changes. Reusable mechanisms must remain business-neutral.

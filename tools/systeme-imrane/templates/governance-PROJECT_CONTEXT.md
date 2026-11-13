# Workspace governance context

This scope owns shared routing, installation controls and governance documentation.
It does not aggregate project business memories or corpora. The longest registered
path wins; the root selector/default applies only at the root, otherwise governance
is used when no business lane matches.

Canonical memories: CURRENT.md, DECISIONS.md, CONTEXT_INDEX.md, PROJECT_CONTEXT.md.
Private snapshots are recovery data, never substitutes for an agent's memory update.
Root Graphify initially includes only AGENTS.md and these four memories. Indexing
requires separate corpus review and explicit network authorization.

Local validation: `python tools/systeme-imrane/scripts/imrane.py check --workspace .`.
Check inspects files and known targets; native trust and hook loading remain host checks.

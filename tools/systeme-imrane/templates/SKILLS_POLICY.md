# Skill placement

One canonical library per installation. Default: workspace `.agents/skills` for
Codex, with linked `.agents/skills` views in independent lanes and `.claude/skills`
views for Claude Code; if linking is unavailable,
use a generated hash-tracked mirror, never independently edit it. A shared user
library is optional and requires explicit user choice, not a default global edit.

Install generic skills from reviewed pinned upstream sources. Local overlays hold
project paths/business rules. Keep local extensions distinct from imported code;
do not guess a GitHub origin or redistribute a plugin's runtime package. Preserve
licenses and report unresolved sources. Updates require review and a new lock.

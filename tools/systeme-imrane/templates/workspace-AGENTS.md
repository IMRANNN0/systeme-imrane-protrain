# Workspace router — Codex and Claude Code

Read this router first. Identify the requested project in `.codex/projects.json`.
Resolve the longest matching registered project path from cwd; only at the workspace
root use the ignored runtime selector `tmp/codex-session/ACTIVE_PROJECT.json`, then
the configured default. Ask when the request could materially affect another lane.

## Load order and isolation

1. Router and project registry; no other project's business context.
2. Active project's AGENTS.md and `.codex/memory/CURRENT.md`.
3. Its CONTEXT_INDEX.md selects the smallest sufficient files for this task.
4. Its private runtime snapshot only when recovery is needed.
5. A bounded project-scoped Graphify query for broad architecture/discovery;
   read a known file directly for a narrow correction.

The root governs shared mechanics only. Each project owns its mission, code,
documents, memory, runtime, graph, secrets and publication controls. Never create
a combined business graph. Shared credentials do not authorize shared corpora.

For workspace architecture read `docs/governance/WORKSPACE_GOVERNANCE.md`.
Cross-project transfers require `HANDOFF_POLICY.md`. Reusable skill placement follows
`SKILLS_POLICY.md`. New lanes must satisfy `PROJECT_LANE_BOOTSTRAP_CHECKLIST.md`.

## Work and model policy

Answer/review/diagnose is read-only unless the user also requests changes. Preserve
existing edits. Ask before a meaningful scope expansion. Do not publish, contact
people, weaken approvals or change campaigns on the strength of this router.

Read `.codex/model-routing-policy.json`: six complexity levels map mechanical,
simple, bounded, intermediate, complex and critical work to configured model/effort
pairs. Unknown scope defaults to standard_safe; the optional Codex preset uses
Luna 6 low/medium/high and Sol 6.1 low/medium/high. Inspect actual scope,
uncertainty, dependencies, risk/reversibility and verification; heuristics are not
proof. Short continuations retain the route, new risk can raise it, and two reported
failures in one task escalate to deep_safe. Explicit
`[route:mechanical|simple|focused|balanced|sol|deep]` tags override; legacy luna/terra
aliases remain accepted. Models and Claude effort are personal. Max/Ultra and
service-tier changes are never automatic. Hooks recommend only; they cannot switch
the active model/effort or authorize subagents. Use delegation only when authorized.

## Context and continuity

Read narrowly with rg and bounded excerpts. Do not preload histories, generated
graphs or other lanes. Decisions are canonical in DECISIONS.md, not a transcript.
Before stopping/compaction update the active project's CURRENT.md with verified
state, unresolved failures, next steps and evidence; do not claim hooks can infer it.
Hooks write ignored private snapshots even if semantic indexing fails.

Runtime surfaces: `.codex/` and `.claude/`; generic executables in
`tools/systeme-imrane/scripts/`. Run `imrane.py --help` for commands. Dependencies
and skills are installed only after reviewing their plan. Do not expose secrets.

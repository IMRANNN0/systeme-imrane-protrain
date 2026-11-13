# Maintenance and recovery

## Upgrade the toolkit

Update only from the authorized repository. Review changes, run tests, then inspect
`init --upgrade` before `--apply`. The private `.imrane/managed.json` manifest
records generated files and hashes. Upgrades replace only versions still matching
their managed bytes. Each replacement is backed up under `.imrane/backups/<date>/`.

An owner-edited file is a conflict: the batch stops before writes. Merge manually,
preserving mission, commands, and local rules. Do not suppress the signal with a
force mode. Reinstallation does not reset the existing project registry.

Hooks record absolute local Python/workspace paths. After moving the workspace or
replacing Python, regenerate from the new toolkit with `--upgrade` and inspect
conflicts. Do not copy another person's paths. This version does not automatically
migrate old registry paths after project folders move; verify and edit them deliberately.

## Skills

Reinstalling the same online source commit verifies hashes. Version changes or an
edited mirror block replacement. Back up/review adaptations, then archive only the
affected module before reinstalling. Do not delete the whole library to fix one
conflict. The complete offline library additionally supports explicit managed
`--upgrade` with backups; see the distribution's onboarding contract.

## Resume a session

Read the router, resolve the lane by cwd, and read its CURRENT.md. If recovery is
needed, inspect `tmp/codex-session/projects/<id>/latest-snapshot.json`, then only
relevant history. Do not inject every snapshot. Check dates and evidence; an old
success message is not a current test. Memory rollback is a human decision, not
an automatic effect.

## Repair an index

`graphify_runtime.py status` reports freshness. On failure, retain the last graph
and completed batches, correct key/model/scope, then rerun an authorized refresh.
Cooldowns belong to the lane. Old graphs remain in private runtime; they are not
automatically published or transferred.

## Retention and removal

Snapshots and backups remain local without automatic purging. The owner chooses
retention according to recovery/privacy needs; archive before deleting a specific
item. npm/venv libraries and caches may be large but do not belong on GitHub.

To remove the framework, preserve useful memories/rules, disable only Imrane System
handlers in each client's configuration, then review the managed manifest before
removing its files. The kit provides no global recursive deletion command. Projects,
accounts, keys, and repositories are not deleted.

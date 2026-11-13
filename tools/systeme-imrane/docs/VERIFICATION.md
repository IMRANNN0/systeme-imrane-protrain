# What verification proves

Standard-library tests use synthetic workspaces without keys, business accounts
or publication. They exercise fresh initialization, idempotence, conflicts,
unchanged-managed-version backups, contained paths, cwd/selector resolution,
separate sessions, snapshots despite errors, prompt/tool non-retention, Graphify
scope, quotas/fallback/cooldowns, no fallback for nonquota errors, bounded queries
and hostile skill archives. Failures retain a nonzero exit.

`test_release_regressions.py` also exercises complete source/runtime copying,
inventory acceptance/refusal, four root memories, neutral corpus, explicit default,
real preservation/upgrades, disabled routing followed by opt-in, governance-only
skill placement, historical exclusions and visible incomplete snapshots.
Tests use Python temporary folders. If a sandbox restricts TEMP, point TEMP/TMP to
an authorized fixture folder before running them. Use `PYTHONDONTWRITEBYTECODE=1`
or `python -B` to preserve source files.

`tests/graphify_offline.py` exercises the real pinned Graphify package with a small
synthetic Python file: adapter contract, skill data, AST extraction and validation.
It sends no corpus to Gemini/Ollama. Keyless tests do not certify semantic calls
with real provider accounts.

`release_check.py` checks distributable components, Python/JSON parsing, internal
Markdown links, catalogue pins/provenance and some obvious leaks. It is not a
universal rights or secret audit. The source and installed toolkit use the same
contract with three neighboring adapters. Out-of-inventory files, runtime/cache
and links are rejected. Workspace `check` also parses generated JSON/TOML and
checks the Python runner and known commands without executing them. Custom
commands remain unverified. Host trust and native autoload are not proved.

Distribution CI targets Windows/macOS. Read Actions for the exact commit; a
configuration is not a successful run. Tests do not run Winget/Homebrew system
installation. Their plans are checked, and recipients authorize execution on
their own machines. Assistant clients must also load a synthetic hook after
repository trust is approved in the actual host.

Before delivery, run current tests and distribution checks, try a separate fresh
workspace, review the diff/tracked files and verify repository visibility and
pushed SHA. A Windows run or a generated macOS command is not macOS execution.

# Review and back up the working copy

The repository checkout and installed workspace are independent. After working on
another computer, copy only reviewed ProTrain changes back into the checkout's
`project/ProTrain` before committing. The kit does not perform this sync for you.

1. Close tools that are writing the project. Update the installed lane's checkpoint
   and durable decisions, then save and inspect its explicit snapshot locally.
2. Make a local backup of the checkout. Compare installed `projects/ProTrain` with
   checkout `project/ProTrain` using your editor or directory comparison tool.
3. Review the actual changed files and copy the chosen source, deliverables, assets
   and four canonical memories. Preserve edits already in the checkout. Do not
   delete destination files based only on an absent source file. Resolve conflicts
   explicitly rather than using a blind mirror or overwrite command.
4. Exclude `.git`, `.venv`, `node_modules`, caches, `__pycache__`, `.imrane`, `.work`,
   `tmp`, `secrets`, environment files, authentication and host settings. Keep root
   lane `.codex` limited to the four canonical memories and optional graph scope.
   The bootstrap regenerates Codex/Claude configuration, hooks and roles.
5. In copied UTF-8 text, replace actual installed absolute workspace pointers with
   `{{IMRANE_WORKSPACE_ROOT}}` and project pointers with `{{PROTRAIN_PROJECT_ROOT}}`.
   These tokens are expanded at the next installation. Use forward slashes for
   tokens inside JSON strings. Review code separately: a historical source path or
   third-party tool path is not automatically a portable project pointer.
6. Inspect `git status` and the full diff. Check new binary files, nested archives,
   private data, credentials, media rights and retained approval states. Run a new
   bootstrap `plan` against a fresh external destination to validate the payload.
7. Commit only the reviewed snapshot. Push to the private repository only when the
   owner has authorized that publication. Other PCs can fetch that commit and
   create a fresh installation, then transfer any separate local changes after
   comparison. Bootstrap refuses changed existing installations rather than merging.

Installed `bootstrap.py check` reports changed files against installation hashes.
Changes are expected during authorized work. That report is a comparison aid, not
a merge result, approval, credential scan, source-of-truth decision or backup.
The repository manifest is an integrity record for bundled skills; it is not a
certification of every business artifact.

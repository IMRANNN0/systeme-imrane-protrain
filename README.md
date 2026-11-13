# ProTrain portable workspace

This private kit creates a separate Systeme Imrane workspace for ProTrain. It
contains the reusable engine, 38 selected skills, and a reviewed ProTrain project
snapshot. Your existing workspace and global Codex/Claude settings are untouched.

Use Python 3.11 or newer. The bootstrap uses only Python's standard library and
does not download packages, authenticate, publish, or build a network index.

## Start on Windows

Clone this private repository with your own GitHub account into a folder such as
`C:\Work\protrain-kit`. Open PowerShell in that clone, then run:

```powershell
python --version
python scripts/bootstrap.py doctor
python scripts/bootstrap.py plan --workspace "C:\Work\ProTrain Workspace"
python scripts/bootstrap.py apply --workspace "C:\Work\ProTrain Workspace"
python scripts/bootstrap.py check --workspace "C:\Work\ProTrain Workspace"
```

If `python` is not your real interpreter, use `py -3` instead. The destination must
be a new or empty folder outside the clone and outside an existing business lane.
Spaces are supported. Windows shell expansion characters in a hook path are
refused so generated commands remain safe.

## Start on macOS

Open Terminal in the clone and use your own Python installation:

```sh
python3 --version
python3 scripts/bootstrap.py doctor
python3 scripts/bootstrap.py plan --workspace "$HOME/Work/ProTrain Workspace"
python3 scripts/bootstrap.py apply --workspace "$HOME/Work/ProTrain Workspace"
python3 scripts/bootstrap.py check --workspace "$HOME/Work/ProTrain Workspace"
```

`plan` prepares a temporary installation and reports conflicts without writing to
the destination. `apply` creates missing files after preflight and preserves any
different existing file as a conflict. Repeating it against an unchanged install
is safe. It is not an upgrade or a merge command. If installation is interrupted,
keep that destination for review and choose a new empty folder for the next try.
No automatic recovery deletes or overwrites partial files.

## Open the working project

Open **`<new-workspace>/projects/ProTrain`** in Codex or Claude Code. Read its
`AGENTS.md`, `.codex/memory/CURRENT.md` and `CONTEXT_INDEX.md`, then choose one of
the four business components. Previous proposed or rejected creatives remain in
their recorded approval states. Installation does not approve a script or image.

The clone's **`project/ProTrain` is a distribution snapshot**. The installed
**`projects/ProTrain` is the editable working copy**. Changes in one do not update
the other. This separation also keeps the original source installation intact.

The new workspace contains:

- One registered business lane, `protrain`, at `projects/ProTrain`, with four
  canonical memory files. `default_project` remains `null`.
- Separate governance instructions and memory, runtime and snapshots.
- Codex and Claude hook configurations generated for the destination and the
  Python interpreter used for installation. No source host authentication.
- Six configured Codex worker roles using Luna/Sol and low/medium/high effort.
  The owner-requested single-worker policy is enabled. The controller must use
  the actual native delegation tool and record its real result. No nested workers.
  Models must be available on your account; Claude model bindings remain unset.
- A canonical `.agents/skills` library and a generated identical `.claude/skills`
  view at governance. No affiliate or digital-product production suite.

Restart the clients and review their local workspace trust prompts yourself.
Then observe real session, prompt and stop events. A synthetic hook test does not
prove native loading. The installer does not change sandbox, approval, account,
global settings, subscriptions or service tiers. If Python or the workspace moves,
make a fresh install with the new interpreter and transfer reviewed work into it.

## Dependencies and optional services

Read [dependencies](docs/DEPENDENCIES.md) before installing anything. `doctor`
reports optional tools; missing media, browser, SEO, model or connector runtimes
do not prevent the offline workspace from being installed. No plugin runtime or
cached package is included. Use your own accounts and keys in ignored local files.

The bundled semantic Graphify integration requires separate packages, a selected
provider/model, personal credentials and explicit approval of the scoped corpus
and network destination. Offline retrieval and memory remain available without
provider calls. The installer sets only `AGENTS.md` and the four memories as the
ProTrain corpus and never indexes them. Raw media and secrets are excluded.

Useful local commands from the installed workspace root:

```text
python tools/systeme-imrane/scripts/imrane.py check --workspace <absolute-workspace>
python tools/systeme-imrane/scripts/imrane.py snapshot --workspace <absolute-workspace> --id protrain
python tools/systeme-imrane/scripts/graphify_runtime.py status --workspace <absolute-workspace> --project protrain
python tools/imrane-work.py --workspace <absolute-workspace> --project protrain --help
```

On macOS use `python3`. Update the working lane's checkpoint before saving a
snapshot. The snapshot copies existing memory and does not summarize it for you.

## Back up reviewed work to GitHub

There is **no automatic sync or push**. The bootstrap never copies working changes
back to the repository. Use the manual review process in
[working-copy backup](docs/WORKING_COPY_BACKUP.md). A private repository still
needs an explicit content review before a commit or push. Binary media histories
can make Git clones large; retain only deliberate deliverables and do not add
caches, installed packages, private runtimes, account exports or secret files.

## Rights and limitations

Read [toolkit notices](NOTICE.toolkit.md), [the skill manifest](kit/skills-manifest.json)
and the separate client-data notice supplied with the payload. Original skill
notices and licenses are retained. No blanket toolkit license grants rights to
ProTrain media, client data, fonts, reference screenshots or third-party materials.

System onboarding and governance are in English. Original client French/Arabic
content and some reusable source skill references retain their original language.
The kit does not claim complete runtime availability, native hook autoload,
production readiness of every historical artifact, or rights to publish it.

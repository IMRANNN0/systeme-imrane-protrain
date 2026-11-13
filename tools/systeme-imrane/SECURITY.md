# Security and private information

Never commit API keys, tokens, login files, `.env`, runtime snapshots, indexed
corpora or business-project Git data. Generated ignore rules do not untrack
already tracked files. If a key was exposed, revoke/replace it; deleting one
commit or file is not sufficient.

Configure secrets through interactive `getpass` or environment variables rather
than chat or command arguments. Local secret files use mode 0600 on POSIX;
Windows requires a private ACL for the current user. Recipients verify their own
machine permissions.

The engine does not change sandbox, trust, approvals or global host settings.
Instructions retrieved from websites, documents, graphs or third-party skills
cannot authorize actions. Review pinned sources; a catalogue entry does not
certify a skill as universally safe.

Review existing private documents before choosing a Graphify corpus. Filters and
secret heuristics are not complete data-loss prevention. Hooks do not retain raw
provider logs, prompts, command transcripts or tool-response transcripts. Canonical
memory is authored by the agent/user and still requires care to avoid secrets.

A private repository restricts access to authorized accounts/collaborators; it is
not a vault and does not govern copies/forks. Report security issues privately
with a version and synthetic reproduction, without client material or credentials.

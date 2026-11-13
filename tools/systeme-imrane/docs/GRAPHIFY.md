# Graphify: indexing, credentials and fallback

Graphify turns a scoped corpus into a knowledge graph. It is a retrieval layer;
CURRENT.md remains canonical memory, compaction recovery uses snapshots, and each
project keeps a separate graph.

This kit pins `graphifyy[gemini,ollama]==0.8.13`, the version supported and tested by
the adapter. This is not a claim to ship the latest release. An upgrade requires
rechecking callbacks, caching, extraction and graph formats. Source:
[Graphify-Labs/graphify](https://github.com/Graphify-Labs/graphify), MIT at revision
0.8.13; the license of its current branch may differ.

## Review the corpus before any request

Each project has `.codex/graphify-scope.json` with includes and excludes relative to
its root. The initial scope proposes AGENTS.md, src, docs and canonical memory.
Read and adjust that list; it must not expand to the entire disk. A project can
disable Graphify in the registry. Root governance has a separate descriptor and
starts with AGENTS.md and its four memories only, without combining registered
projects.

The engine always excludes secrets, `.env`, local authentication, Git, dependencies,
generated output, runtime, raw media and other nested lanes. Historical `.imrane`
and `.ashraf` directories are excluded case-insensitively. It skips symlinks and
rejects traversal, non-UTF-8 files and files over 2 MB. The initial budget is 200
files and two million words; exceeding it requires an explicit choice. Sensitive
assignment detection catches some obvious secrets but does not replace corpus
review.

`refresh` without `--allow-network` lists selected files without sending them.
Temporary copies and corpus-specific caches stay in the lane's private runtime,
outside published folders.

## Personal setup

Create the ignored `secrets/graphify.env` through the interactive `secrets` command.
The environment variables GEMINI_API_KEY and OLLAMA_API_KEY take precedence over
that file. Never put a key in a command argument, screenshot, project document or
commit.

Explicitly choose available Gemini and Ollama Cloud models in
`.codex/graphify.json` using your own accounts. Model fields start empty. Cloud
fallback accepts only `https://ollama.com/v1`; it does not treat a Cloud key as
credentials for an unauthenticated local Ollama server. The kit neither creates
keys nor shares the maintainer's keys or guarantees a free quota. Provider limits
depend on the service and account.

## Exact fallback rules

1. Try Gemini when its cooldown has expired.
2. On HTTP 429, RESOURCE_EXHAUSTED or an explicit quota-exceeded response, save a
   cooldown and try Ollama for this project.
3. Invalid authentication, network/configuration errors, timeouts and malformed
   output do not trigger this fallback.
4. If Ollama also exceeds quota, retain the quota state and last validated index.
5. After the Gemini cooldown expires, the next refresh tries Gemini again.

The initial cooldown is one hour and is configurable. Fallback does not increase
the budget or activate an additional paid provider. SDK error bodies can contain
sensitive information; only structured status is saved.

## Cache, validation and promotion

Only complete, non-truncated, nonempty batches populate the semantic cache.
Interrupted batches are not complete results. Validation requires a nonempty
graph, valid edges, a complete semantic cache and represented anchors. Partial
extraction does not replace the previous graph.

Rebuilding uses a stable private corpus. Derived manifests are reevaluated so a
false unchanged state cannot stand in for a valid cache. Successful promotion
keeps the previous output in runtime before installing the validated index in the
project. Provenance records the id, hash, files and provider.

Local queries filter this graph and return sources within an approximate
100–8,000-token budget (characters/4). Changed corpora and failed refreshes are
reported; an old index is not presented as current.

## Compaction and incidents

By default PreCompact marks freshness and saves memory without network access.
Setting `auto_refresh` to true gives ongoing consent for the reviewed corpus and
configured providers; do so only after reviewing both. Hook refreshes remain
bounded to 60 seconds per attempt. A snapshot precedes the call and another saves
the final state; an external interruption still leaves the initial backup.

A crash may leave `graphify.lock`. First check its recorded PID and confirm that
no rebuild is running; only then remove that exact lock. Do not erase caches,
snapshots or old graphs by default to hide an error. Report an index as repaired
only after real validation.

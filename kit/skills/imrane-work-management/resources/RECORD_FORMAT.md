# Work record format, version 1

Use `show` to see the full record and safe defaults. `create --input` starts in qualification; it cannot import a ready-made stage or audit trail. `update --input` takes an object containing only the editable top-level fields to change. Nested objects and arrays replace their previous value completely. Unknown fields are rejected. All text is data: no command, URL or evidence string is executed.

## Editable fields

| Field | Shape / meaning |
| --- | --- |
| `id` | Lowercase slug at creation only; immutable afterward |
| `title`, `owner`, `next_action` | Strings; meaningful values required for forward transitions |
| `mode` | `light` or `standard` |
| `domain` | `general`, `website`, `research`, `financial` or `advertising` |
| `brief` | `goal`, `deliverable` strings; `in_scope`, `out_of_scope`, `inputs`, `acceptance` arrays of nonempty strings; `missing_inputs` as below |
| `priority` | `impact`, `urgency`, `effort` integers 1–5 and `reason` string; the score is a heuristic |
| `blocker` | `{ "active": false, "reason": "" }`; active needs a reason |
| `tasks` | Array of `{id,title,owner,status,depends_on}`; status `todo`, `doing` or `done`; dependencies are task IDs |
| `evidence` | Array of `{id,criterion,kind,source,observed_at,result,notes}` |
| `review` | `{reviewer,independent,required,verdict,notes}`; booleans for independent/required; verdict `pending`, `pass` or `fail` |
| `delivery` | `{summary,artifact,delivered_at,channel}`; local artifact path, actual recorded handoff time and channel |
| `decisions` | Array of `{id,prediction,rationale,test,observation,outcome,decided_at}` |
| `lessons` | Array of `{id,summary,context,limitations,status,reviewer,reviewed_at,sanitized,proposed_change}` |
| `escaped_errors` | `null` when unmeasured; otherwise array of `{id,description,source,observed_at}` |

Missing inputs use `{description,disposition,reason}`. A `blocking` disposition prevents advancement and counts toward blocked time. `nonblocking` and `not-needed` require a reason. This records a justified choice, not an invented answer. Both missing-input blockers and `blocker.active` contribute to the same elapsed blocked intervals.

Evidence `criterion` matches the corresponding acceptance string exactly. Kind is `measured`, `observed`, `reported`, `hypothesis` or `unknown`; result is `pass`, `fail` or `pending`. A pass/fail needs a source and ISO 8601 timestamp including timezone. Hypothesis/unknown cannot be marked pass; reported evidence alone cannot satisfy delivery. Sources are HTTP(S) URLs or selected-lane paths. The tool validates references structurally; it neither fetches URLs nor proves content, causality or independence.

`review.required: true` means an independent review is required; the named reviewer must differ from the owner and attest independence. Research exit requires a source, date and useful notes. Plan exit requires owned tasks with valid dependencies. Review-to-production resets review/evidence results to pending so corrected work is checked again.

Settled decision outcomes (`supported`, `rejected`, `inconclusive`) need prediction, rationale, test, actual observation and date. Otherwise leave `pending`. Lesson statuses are `draft`, `approved` or `rejected`; reviewed states need reviewer/date. Export additionally requires approved, sanitized and meaningful context, limitations and proposed change. These are human/agent attestations requiring real review, not a truth or privacy detector.

All timestamps use ISO 8601 with timezone, for example `2026-11-02T12:00:00Z`. Future observations/handoffs are not evidence of completed work. Keep future measurement dates in `next_action` rather than fabricating observations.

## Safe patch example

This is the complete nested review object in an update payload. Use a real reviewer and actual evidence; the example is not review approval.

```json
{
  "review": {
    "reviewer": "Named reviewer",
    "independent": true,
    "required": true,
    "verdict": "pending",
    "notes": "Inspect the artifact and acceptance evidence before passing."
  },
  "next_action": "Check each acceptance criterion against the actual result."
}
```

## Audit, handoff and metrics

`schema_version`, `project`, `stage`, creation/update timestamps, revision, history and blocked intervals are tool-managed. Manual file changes are not tamper-proof: this is a cooperative local working tool, not an access-control or cryptographic audit service. Locks and content checks protect ordinary simultaneous CLI writes; they do not defeat a malicious process with filesystem access.

Entering **delivery** means the review passed and the result is ready. It does not record an external send. Complete `delivery` with the actual local handoff and then advance to **follow-up**. Only then does `time_to_first_delivery_seconds` use the recorded handoff date minus creation date. Do not backfill an early start time to claim measured productivity. These core fields freeze after acceptance; create a new work item for changed delivered scope. Follow-up decisions, lessons and observed escaped errors remain updateable.

Revision cycles count review-to-production transitions. Blocked time is recorded elapsed time, not an estimate of human effort. Escaped errors remain `null` until explicitly assessed; an empty list means an explicit observation found none, not guaranteed absence. Synthetic pilot metrics verify calculations, not business impact.

Output paths must remain in the selected lane and outside any separately registered child lane. Existing unrelated files are preserved; managed boards can be regenerated. Lesson exports are minimal local files. No cross-client search, remote sending, indexing, campaign execution or skill rewriting exists in this CLI.

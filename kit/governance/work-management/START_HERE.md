# Imrane work management

This is the local working method approved on 2 November 2026. It turns a request into a scoped deliverable, verifies the result and keeps useful learning. It works alongside the existing project router, four canonical memories and domain skills.

Start in the requested project's lane. For shared system work use `governance`. Never choose a business lane from a guess or combine client boards. The command examples below target the real governance scope; use them only for shared system work. The installation pilot uses a separate synthetic workspace under `tmp`, without changing any real client lane.

## Everyday use

Tell Codex or Claude Code:

> Use imrane-work-management for this request. Reuse the available project information, prepare the smallest useful brief, identify the next action and complete the authorized work with verification evidence. Keep the work inside the selected project. Ask only for information that changes the result or for actions that genuinely need separate approval.

For a tiny correction, answer or make the correction directly and verify it. A formal record is optional. Use **light** mode for a small deliverable with clear inputs. Use **standard** mode for work with research, dependencies or material uncertainty. Scope and risk, rather than word count, determine the mode. Consequential work needs independent review; a second AI restating the first answer is not independent evidence.

1. **Brief:** goal, deliverable, scope, known inputs, material unknowns and observable acceptance criteria. Adapt the questions to the client and assignment; do not send the entire library of questions by default.
2. **Work:** resolve blockers, choose the next action, produce the deliverable and record decisions when they affect the result.
3. **Review:** compare the actual result with each acceptance criterion, attach sources or test evidence and fix failures.
4. **Handoff:** explain the result, the evidence and material limits. Record a local handoff as local; email, publishing, campaign changes and deployment keep their own authorization requirements.
5. **Follow-up:** compare predicted and observed outcomes, then propose reusable lessons for review.

## Leave a checkpoint before stopping

For an ongoing project, keep one short checkpoint near the top of its `.codex/memory/CURRENT.md`. Set the outcome before starting work and update the checkpoint when you stop. Reuse the stage and evidence from an existing work record when available.

Project chats in this workspace follow this by default for substantive work. On hosts that load the local hooks, a new chat receives a bounded excerpt from its resolved lane and project prompts receive the checkpoint instruction. The assistant records verified progress in `CURRENT.md` before replying. Stop and PreCompact save the existing notes locally. On hosts without native hooks, the assistant saves the scoped snapshot explicitly. Reopen the same project folder after a restart to resume from the last saved checkpoint.

```markdown
### Restart checkpoint
- Current stage: [the stage supported by the evidence]
- Done when: [one observable result or test]
- Last verified: [date, result and link to the evidence in this project]
- Next action: [one concrete action you can start in 15–30 minutes]
- Blocker: [if any, name what is missing and who can resolve it]
- Review on: [date to revisit]
```

If a result is unsatisfactory, name the specific check that failed and make the smallest useful correction the next action. If you have no evidence yet, say what remains unverified and start with that check. “Improve the dashboard” is too broad. “Import a sample CSV and reconcile its three displayed totals with the source” is a next action with an observable result.

At a weekly check-in, choose one project and read its checkpoint. **Resume** by scheduling the next action, **pause** with a reason and a review date, or **close** with the accepted result or a decision to stop. These are personal review decisions; they do not change the work record's stage. A generic reminder can prompt the review without combining project records.

## The seven stages

| Stage | What it resolves | Exit evidence |
| --- | --- | --- |
| Qualification | What result is wanted and what is in scope? | Owner, useful brief, acceptance criteria, next action; material missing inputs resolved or visibly blocked |
| Research | What do we know, and how do we know it? | Sources, dates, assumptions and unanswered questions sufficient for the plan |
| Plan | What will we do, in what order? | Feasible tasks, dependencies, checks and responsibilities |
| Production | Does the deliverable exist? | Tasks complete, no active blocker, evidence prepared |
| Review | Does the result meet acceptance? | Passed observed/measured evidence for every criterion and recorded review; independent when required |
| Delivery | What was actually handed over? | Summary, scoped artifact, date and real channel; local preparation is not external transmission |
| Follow-up | Did it help, and what should change? | Outcome observations or a dated next measurement; unknown remains unknown |

Standard mode follows the sequence. Light mode may go from qualification directly to production. Failed review returns to production and counts a revision cycle. These stage labels organize work: they do not prove market fit, profitability or campaign performance. A validator checks structure and consistency; reviewers still inspect whether the evidence supports the claim.

## Local commands

Only Python's standard library is needed. Run from the workspace root; the tool also accepts an absolute script path. Read the selected lane's instructions first.

```powershell
python tools/imrane-work.py --help
python tools/imrane-work.py --workspace <workspace> --project governance create --input brief.json
python tools/imrane-work.py --workspace <workspace> --project governance show --id work-item
python tools/imrane-work.py --workspace <workspace> --project governance update --id work-item --input changes.json
python tools/imrane-work.py --workspace <workspace> --project governance check --id work-item
python tools/imrane-work.py --workspace <workspace> --project governance advance --id work-item --to production
python tools/imrane-work.py --workspace <workspace> --project governance board
```

`create` takes a JSON object; use [brief.example.json](templates/brief.example.json) as a starting shape and replace its example values. Relative `--input` paths resolve from the **selected lane**, regardless of the shell's current directory. `update` replaces each supplied top-level field, including entire nested objects or arrays. Read the record first; preserve entries you still need. Stages and audit history change through the tool rather than an update payload. A blocked transition returns a nonzero exit code with the reason. Use `check` before advancing and inspect its readiness report. [Record format](RECORD_FORMAT.md) describes the fields and update shapes.

The store is `<selected-lane>/.imrane/work/`, with one JSON record per work item and a generated offline `board.html`. The CLI creates an internal ignore rule. Work records may still contain private client information: filesystem access and backup policy remain important. The tool does not read every business project from governance, change campaigns, send messages, run evidence strings or publish a board. Do not upload it or add it to Graphify without reviewing its corpus and destination.

## A useful daily board

The board recommends up to three actionable items from the **selected lane**, while displaying blockers separately. Its transparent heuristic is `impact × urgency ÷ effort`, each input from 1 to 5. This is a planning aid, not a forecast. Explain each rating in `priority.reason`. Ties, deadlines, risk and owner commitments still need judgment. See [daily planning](templates/daily-planning.md).

Each active item needs an owner, a specific next action and, if blocked, the missing dependency and resolution action. An item can be high impact and low confidence; say so rather than hiding uncertainty inside a score. Do not silently overwrite the owner's priorities or produce a combined client-content dashboard.

## Evidence and review

Use the [review template](templates/review.md) and only the relevant [domain checks](DOMAIN_CHECKS.md). Evidence records distinguish `measured`, `observed`, `reported`, `hypothesis` and `unknown`. Source, observation date and result stay attached. Reported claims, hypotheses and unknowns are not passed delivery evidence.

A screenshot proves an observed screen, not a successful form submission or a profitable funnel. A command exit code is meaningful only with a relevant assertion. An AI statement that something works is not an independent test. Give limitations and conflicting observations space in the review. An unresolved failed check on an acceptance criterion blocks delivery: after a correction, explicitly replace that failed evidence entry with the fresh check and retain useful failure context in notes or the review artifact.

## Decisions, experiments and lessons

Use [decision and experiment](templates/decision-experiment.md) for choices worth revisiting. Specify prediction, rationale, test and observation before labeling the outcome supported, rejected or inconclusive. Keep routine reversible choices lightweight. Accepted lasting decisions still belong in the lane's canonical `DECISIONS.md`; link the work record rather than copying a transcript.

Lessons stay local and draft until reviewed. Use [lesson](templates/lesson.md), including applicability and limits. Include both successful and rejected approaches with the actual reason. A proposed skill change is a proposal; the tool never edits skills itself.

The [reviewed method library](library/README.md) starts with fully synthetic accepted and rejected examples from the pilot. Use their reasoning and limitations, not their hypothetical numbers as client evidence.

```powershell
python tools/imrane-work.py --workspace <workspace> --project governance lesson-export --id work-item --lesson-id lesson-1 --output <workspace>/.imrane/work/exports/lesson-1.json
```

Only a selected approved, sanitized lesson with a named reviewer and review date may be exported. This is a **local** export. Cross-lane promotion additionally follows [HANDOFF_POLICY.md](../HANDOFF_POLICY.md): explicit purpose, source/destination, authorized data classes and owner approval. Recheck the actual text for client names, identifying details, proprietary numbers, URLs, screenshots and secrets. Setting `sanitized: true` is an attestation, not an automatic confidentiality scan.

## Measure whether the method helps

Start with a baseline and comparable work, not a promised productivity percentage. Track time to first delivery, review-to-production cycles, blocked elapsed time and observed escaped errors. An unmeasured error count remains unknown. Synthetic pilot timings verify the instrument; they do not establish real productivity gains. Use [pilot results](PILOT.md) for the installation exercise.

After several comparable real tasks, review whether the method reduced revisions and blocked time without increasing administrative overhead. Simplify fields or gates that add no decision value. Do not draw a universal client rule from one case.

## Existing skills and continuity

This method organizes the assignment; it does not replace expertise. Use only the relevant media-buying, affiliate, design, engineering or document skill. For example, a targeted offer review does not trigger every media-buying framework. Sources and client facts remain in their own lane.

The four canonical memories retain their roles. At stopping or compaction, update `CURRENT.md` with verified state and the next action, `DECISIONS.md` for accepted choices, and the context index/context when needed. Save the existing scoped snapshot. Work records supplement this continuity; they do not replace it, prove native hook loading or authorize a network index refresh.

The new method is installed locally. The previously sealed GitHub distribution has not been changed or published by this implementation. Windows checks are run locally; macOS uses the same standard-library code but needs its own host validation.

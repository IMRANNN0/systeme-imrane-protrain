# Installation pilot and validation

Date: 2 November 2026. This exercise uses invented data in a separate workspace under `tmp/codex-session/imrane-work-management-20261102/pilot/`. It is not a registered business project and does not establish real productivity or market results.

## End-to-end exercise

`tools/imrane-work-pilot.py` creates an isolated registry and hypothetical pricing brief, then uses the actual CLI to move through qualification, research, plan, production, review, delivery and follow-up. It generates a memo, calculation evidence, a reviewed local lesson export and an offline board. One review-to-production loop exercises fresh evidence and revision counting.

The independent arithmetic oracle checks orders of 80, 70, 60 and 50, with contribution after ads of 8,400, 10,600, 11,800 and 12,000 hypothetical currency units. The maximum contribution occurs at price 400, while maximum revenue is tied at 300 and 350. These are conditional calculations from invented CVR inputs, not net profit forecasts. The memo states excluded costs.

The pilot verifies that these actions are refused:

- Skipping research/plan in standard mode.
- Delivery without a passed review.
- Follow-up without a recorded local handoff.
- Exporting an unreviewed lesson.
- Advancing while material inputs are missing.
- Reading a registered nested client input through governance.

It also verifies HTML escaping of a hostile title and minimal lesson export fields. Timing remains instrument-only; escaped errors are explicitly unmeasured.

## Commands and evidence

```powershell
python -X utf8 -B tools/imrane-work-pilot.py --output <workspace>/tmp/codex-session/work-pilot-new-run
python -X utf8 -B -m unittest discover -s tests -p test_imrane_work.py -v
python -X utf8 -B -m unittest discover -s tools/systeme-imrane/tests -p "test_*.py"
python -X utf8 -B tools/install-imrane-work-skill.py --workspace <workspace>
```

The pilot refuses an existing output directory. For tests on hosts whose default temporary folder is restricted, set TEMP/TMP to an existing workspace-local test directory in the current process. Do not change system-wide environment variables.

Installation evidence is in `tmp/codex-session/imrane-work-management-20261102/verification.json`; pilot details are in its `pilot/verification.json` and `pilot/events.json`. The work-management unit suite covers lifecycle gates, source/date handling, tasks/dependencies, blockers, metrics, scoped paths, output preservation, locks/conflicts, HTML and lesson export. Existing installed-engine tests are run separately. One real symlink-creation test is skipped because this Windows host lacks the required unprivileged creation capability; mocked/path controls still run. That skipped host check is not counted as a pass.

The installed skill passes the bundled skill validator using the already installed Imrane virtual environment. System Python lacks PyYAML, so no new package is installed to run that validator. A separate agent tested the new skill against a tiny guarantee-wording request: it produced a direct correction, kept the assignment narrow and did not open a client lane or force onboarding. Review clarified relative input paths, tiny-task continuity and real versus synthetic command examples.

## Practical limits

This is local Windows validation. macOS execution and native Codex/Claude discovery/autoload have not been demonstrated here. Existing permissions, credentials and client files are not migrated. The sealed GitHub distribution is not updated. The validator checks mechanical consistency; evidence quality, reviewer independence, sanitization and real business benefit still need judgment. Cooperative file locks are not an operating-system security boundary. Graphify freshness is reported separately without an implicit network refresh.

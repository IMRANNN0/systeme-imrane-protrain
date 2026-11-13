# Diagnostic output and synthetic examples

Adapt the following to the request; omit irrelevant branches. All examples below are invented training data, not client results or expected benchmarks.

## Reviewable diagnosis template

**Decision and scope:** business model, question, periods/cohorts, segment, primary metric, sample and target/source if known.

**Data contract:** source/refresh, grain, timezone, currency, attribution, event/status and numerator/denominator definitions, cohort maturity, exclusions and coverage. List unreconciled differences.

| Measure | Baseline numerator / denominator | Current numerator / denominator | Value/change | Comparability or uncertainty |
| --- | --- | --- | --- | --- |
| Relevant measure | Eligible counts/totals | Eligible counts/totals | Units; rate points and/or relative change | Definition, coverage, sample |

**Compatible decomposition:** show formulas and substituted values, or state why a branch is unavailable. Separate arithmetic contributions from causal explanations.

| Observation | Competing hypothesis | Evidence and counterevidence | Gap / next validation | Possible action, owner and dependency |
| --- | --- | --- | --- | --- |
| Measured fact, period and sample | Explanation to test | Source and limits | Specific check or experiment | Conditional recommendation; authorization status |

**Decision:** supported finding or inconclusive result; business impact and confidence; next step; what would change the conclusion. Link project-local evidence without personal data.

## Example 1: two ROAS components move

Two comparable synthetic weekly cohorts use the same attributed paid-order definition, currency and revenue treatment. Baseline: spend 1,000, revenue 2,000, 40 orders, 1,000 eligible clicks. Current: spend 1,200, revenue 1,800, 40 orders, 1,000 eligible clicks.

| Measure | Baseline | Current |
| --- | --- | --- |
| ROAS | 2.00 | 1.50 |
| AOV | 50 | 45 |
| CPS | 25 | 30 |
| CPC | 1.00 | 1.20 |
| Click-to-order CVR | 4% | 4% |

ROAS changes by `(45/50) / (30/25) − 1 = −25%`; AOV falls 10% and CPS rises 20% simultaneously. Compatible arithmetic locates two branches. It does not show whether product mix, discounts, auction mix or other factors caused them. Inspect item-revenue reconciliation and like-for-like mix for AOV, and compatible CPM/CTR for CPC. Without cost coverage and retained revenue, this says nothing conclusive about net profit. No campaign edit follows automatically.

## Example 2: incompatible CVR and a click/view gap

Spend is 600; the platform reports 300 link clicks; site analytics reports 240 sessions and 12 orders. CPC is 2 per platform link click, while session CVR is 5%. `2 / 0.05 = 40` cannot be presented as the CPS identity: the denominators differ. Direct spend/orders is 50 only if the 12 orders legitimately match that spend cohort/attribution. Until reconciled, label source-specific metrics and avoid claiming that 60 people could not load the site. Check definitions, tagging/consent, redirects and accessible loading before diagnosing technical loss.

## Example 3: lead and affiliate decisions

A lead cohort with 20 qualified leads from 100 inquiries is not directly comparable with yesterday's 5 qualified leads from 80 inquiries if qualification is still pending for most recent records. Keep pending status visible, use equal observation age where possible, and report an inconclusive quality comparison rather than declaring a winner from CPL alone. A proposed primary metric could be cost per mature qualified lead if it matches the decision.

For affiliate traffic, pending commission of 900 and approved commission of 500 are different statuses; neither is automatically paid cash or customer revenue. Use acquisition cohort, approval/reversal window, costs and agreed decision metric. Do not reuse the e-commerce AOV map without equivalent order and revenue definitions. These two adaptations are operational examples; the owner's separate sector tracks remain pending.

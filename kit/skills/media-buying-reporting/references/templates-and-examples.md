# Reporting templates and synthetic examples

Adapt sections and rows to the decision. Examples are invented training data, not client results or benchmarks. A template is a specification until populated from authorized evidence.

## Report contract

| Field | Record |
| --- | --- |
| Decision, audience and scope | Business model; question; segment; requested format |
| Reporting and comparison period | Dates; timezone; acquisition cohort vs calendar outcomes; maturity |
| Sources and freshness | Source; extraction/refresh time; grain; coverage; live/tested vs static |
| Financial/measurement basis | Currency; revenue/status/cost basis; attribution; refunds/exclusions |
| Primary metric and target | Numerator; denominator; target value/source/date or unknown |
| Mapping and preparation | Stable IDs; rule version; unmatched/unknown coverage; join/cleaning notes |

## On-platform column specification

| Order / section | Available column or formula | Definition and denominator | Filters / breakdown | Availability or caveat |
| --- | --- | --- | --- | --- |
| Business outcome | Relevant primary metric | Explicit source/status | Scope and attribution | Platform view or reconciled outcome |
| Diagnostics | Compatible secondary metrics | Click/event type and rate basis | Relevant segment | Missing/custom metric limits |
| Volume | Spend, eligible outcomes and exposure | Units and currency | Same period/filter | Overlap/maturity |

**Naming/mapping specification:** stable ID; original name; effective dates; phase/objective and relevant dimensions; mapping rule; verification; unknown reason. Include a fallback unknown category instead of discarding ambiguous names.

## Manual performance report

**Decision answer:** concise supported result and confidence; provisional or inconclusive where warranted.

| Period / cohort / segment | Spend | Eligible outcome count | Revenue or commission/status | Primary metric | Relevant diagnostics | Coverage / maturity |
| --- | --- | --- | --- | --- | --- | --- |
| Comparable period | Currency | Definition | Source/basis | Numerator / denominator | Units, sample | Gaps and as-of time |

Optional sections: outcome/financial diagnostics; volumes/capacity; compatible funnel transitions; traffic/creative context. Add only those needed to answer the question.

| Funnel transition, if defensible | Earlier eligible count | Later eligible count | Rate | Compatible spend / action | Event/sequence and coverage caveat |
| --- | --- | --- | --- | --- | --- |
| Defined stage pair | Population and window | Matched outcomes | Explicit denominator | Only if compatible | Deduplication/repeats/maturity |

**Reconciliation and validation:** source/control totals; join checks; missing/unknown mapping; weighted ratios; attribution differences; refresh and calculation evidence.

| Observation | Competing explanation | Supporting / contrary evidence | Business impact and confidence | Next validation, owner and dependency |
| --- | --- | --- | --- | --- |
| Fact with period/sample | Hypothesis, not fact | Traceable source and limits | Conditional where needed | Recommendation and authorization status |

**Limitations:** unresolved issues that could change the decision; what is still unknown; exact next data/check. Report sharing or campaign edits require the task's authorization.

## Example 1: aggregate ratios and missing coverage

Two synthetic comparable days contain 10 and 90 eligible clicks, with 2 and 9 attributed orders. Daily CVRs are 20% and 10%; the combined rate is `11 / 100 = 11%`, not the unweighted 15%. Spend 20 and 180 gives combined CPC `200 / 100 = 2` and CPS `200 / 11 ≈ 18.18`. Each calculation requires those clicks, orders and spend to belong to the same eligible scope.

If day three has 50 known clicks but unknown orders, the full-period order CVR is unknown. The observed-coverage rate is still 11/100 = 11%, labeled as two of three days with 100 of 150 known clicks covered. Dividing 11 by 150 would silently treat unknown orders as zero. Recover the missing outcomes before presenting a full-period CVR.

## Example 2: competing attribution and mapping gaps

In a synthetic week, platform A attributes revenue 800, platform B attributes 700, while the deduplicated order system records 1,000. Do not report 1,500 as actual revenue or assume the 500 difference has a known explanation. Show each platform's attribution view separately alongside business revenue; reconcile defensible order IDs/window differences where available. Keep separate unmatched results if matching is unavailable.

A campaign named `legacy-promo` with a stable ID but no verified phase remains `phase = unknown`. Include its spend in totals and expose the unknown coverage. Do not infer a funnel phase from an ambiguous historical name or remove it from the report.

## Example 3: a service or affiliate summary

For a synthetic service report, 100 inquiries include 20 qualified, 30 disqualified and 50 pending qualification as of the refresh time. Report all three statuses and the cohort age; 20/100 = 20% is an as-of qualified share, not a mature qualification rate or proof of poor traffic. A comparison requires equivalent maturity and definitions. Cost per qualified lead may be provisional, and paid/retained outcomes may be more relevant to the decision.

For a synthetic affiliate report, show pending 900, approved 500 and paid 300 commission as separately defined source statuses, not automatically additive amounts. Check whether statuses overlap or represent transitions and distinguish cohorts and reversals. Do not label commission/ad spend as net profit or report merchant sales as the affiliate's revenue without an explicit appropriate basis.

---
name: media-buying-ecommerce-analysis
description: Analyze paid e-commerce acquisition using order, delivery, return and retained-revenue cohorts. Use when store outcomes, product mix or contribution must reconcile with ad metrics; booked order ROAS alone is insufficient.
---

# E-commerce analysis

Determine what paid acquisition produces after order processing, fulfillment and returns, and what that result supports commercially. Adapt to prepaid, cash-on-delivery, marketplace or subscription commerce rather than imposing one universal order lifecycle.

## Scope and provenance

This is an original local proposed methodology prepared on 5 November 2026. The owner's sector-specific course material has not been supplied; do not attribute this protocol to that course or claim its e-commerce track is complete. Future reviewed material can refine the protocol with explicit provenance.

Work only in the selected registered lane and use its authorized sources. Keep raw exports, transformations and results there. Shared examples are synthetic. Prefer order/customer pseudonymous IDs and aggregate summaries; addresses, phone numbers and payment credentials are not needed for normal performance analysis.

Analysis does not authorize new source connections, external uploads/indexing, publication, customer contact, spending, refunds, price/inventory changes or campaign/account edits. A proposed optimization remains subject to the task's existing authorization.

## Analyze the relevant path

Read [the protocol](references/protocol.md) for lifecycle definitions, compatible ratios and economics. Read [the illustrative cases](references/illustrative-cases.md) when validating treatment of returns, booked revenue or attribution.

1. **Frame the decision.** Define the business outcome, scope, attribution, comparable cohort/period and revenue basis. Distinguish order acquisition, new-customer acquisition and repeat purchases. Reuse supplied targets and mark their provenance rather than inventing benchmarks.
2. **Reconcile actual outcomes.** Connect spend, analytics/tracker, store, payment and fulfillment records on defensible keys/grain. Separate created, canceled, shipped, delivered, returned/refunded and retained/paid outcomes; keep unresolved orders visible. Platform claims and store totals can be useful separate views without agreeing exactly.
3. **Compare mature and compatible populations.** Match fulfillment/return age, currency, timezone, event/status definitions and attribution. Show coverage, sample and unknowns. Recompute ratios from eligible totals, with clicks and sessions distinguished. A return-period cohort is different from a cohort acquired in that period.
4. **Investigate with competing hypotheses.** Inspect price/discount/product mix, traffic/creative, checkout/payment issues, stock, delivery capacity and returns only as relevant. Decompose compatible metrics without claiming the identity proves a cause. Track measurement changes and evidence against the favored explanation.
5. **Connect revenue to contribution.** Reconcile retained revenue and documented costs once each; distinguish recoverable returned inventory, losses, shipping and refund fees. A high ROAS or AOV does not establish profit or a safe budget increase. State what missing costs, delayed returns or stock/capacity could change.

## Deliver and verify

Provide the decision, source/cohort/status/attribution contract, reconciliation and maturity gaps, relevant volume and metric calculations, observations versus hypotheses, economic scope, uncertainty and a bounded next action. An inconclusive result with a precise collection plan is useful when evidence is missing.

Before delivery, reconcile order/payment/refund control totals, check join cardinality and exclusion counts, verify lifecycle denominators and units, and distinguish recognized/retained revenue from cash and gross order value. Show omitted costs and provisional outcomes. Avoid universal ROAS, return-rate, observation-window or scaling thresholds.

Use [Data Analysis Process](../media-buying-data-analysis-process/SKILL.md) for general preparation, [Analysis Flow](../media-buying-analysis-flow/SKILL.md) for compatible metric diagnosis, [Reporting](../media-buying-reporting/SKILL.md) for dashboards, and [Monetization](../media-buying-monetization/SKILL.md) for cost coverage, pricing and financial scenarios. Do not restart unrelated workflows.

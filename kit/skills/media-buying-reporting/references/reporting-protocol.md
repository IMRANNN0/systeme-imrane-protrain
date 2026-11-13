# Reporting protocol

Select only the parts relevant to the requested report. Reported values are source-defined observations, not automatically complete, real-time, reconciled or causal business outcomes.

## On-platform reporting

Arrange available columns around the objective and diagnostic sequence. A possible e-commerce order is ROAS, revenue, purchases, AOV, cost per purchase, spend, CPC, click-to-purchase CVR and relevant events. Include delivery volumes and platform definitions needed to interpret them. Some platforms cannot supply a compatible custom metric or breakdown: mark unavailable or calculate offline from compatible exports rather than inventing support.

For video, record platform-specific view/ThruPlay/completion eligibility and denominators before comparing creatives. For image ads use relevant click and downstream measures. Keep all-click, link-click and outbound CTR separate. CTR is clicks/impressions; show percent to readers and use decimal form in arithmetic. Do not infer scroll stopping, desire, traffic quality or fatigue from one proxy. Frequency and reach need period/population definitions; reach across overlapping periods or groups is not additive.

Do not silently edit saved columns or report settings during a read-only specification task. If a requested configuration is authorized, verify the resulting columns/filters and availability through readback; otherwise label it a specification.

## Naming and mapping

Use a documented naming convention where useful: funnel phase and objective, plus market, audience, placement, format or language as relevant. Do not impose every dimension on every campaign. Prefer stable platform IDs to names as keys; names can change and historical names can be inaccurate.

Maintain a mapping with: source, stable ID, original name, effective date range, phase, objective, applicable category values, mapping rule/version, validation status and unknown reason. Do not use a parsed name as verified truth. Check ambiguous/missing names and summarize unknown coverage by count and material spend/outcome value. Do not silently drop unmatched rows. Not every platform supports every custom breakdown.

## Manual or multi-source reporting

Keep raw exports and reproducible transforms. Record source, extraction/refresh time, period, timezone, currency, grain, cohort/event/status definitions, attribution and coverage. Reconcile joins with known cardinality, matched/unmatched records and before/after totals. Aggregate each source at the correct grain before joining when necessary to avoid duplicating spend or orders.

Distinguish ad-platform attributed revenue, analytics revenue and actual order/CRM outcomes. Overlapping platform attribution cannot be summed into actual sales. If matching is not defensible, retain side-by-side labeled views with reconciliation differences. Cohort-age and conversion lag matter: compare equally mature acquisition cohorts or label provisional outcomes. Do not compare a calendar week's conversions with a spend cohort as if they were necessarily the same population.

The course calls ROAS/AOV/CPS/CVR/CPC a profitability view and spend/orders/revenue/sessions a scalability view. Use clearer diagnostic/volume labels when useful. ROAS equals revenue/ad spend and excludes costs beyond advertising; assess retained revenue, margins, refunds, fulfillment, fees and other relevant costs for profitability. Capacity and sustained marginal outcomes also matter for scalability. A high reported ROAS alone proves neither.

For lead generation/services, define inquiry, qualified, booked, attended, paid and retained states only as relevant, with denominator and maturity. Pending is not a failed outcome. For affiliate work distinguish clicks, accepted conversions, pending/approved/paid commission, reversals and acquisition cohort; commission is not the merchant's gross revenue. These are local adaptations; the owner's separate sector course material remains pending.

## Calculation and visualization rules

- Sum additive compatible quantities; recompute ratios as total eligible numerator / total eligible denominator. Do not average daily percentages, AOV, CPC or ROAS unweighted. Do not combine different currencies without a documented conversion basis.
- Missing values are unknown, not zero. For a partial-coverage ratio, use numerator/denominator with matching coverage, disclose the excluded volume and avoid presenting it as the full-period rate. Zero denominator means undefined; zero numerator with a positive denominator can legitimately mean zero.
- Define funnel rate as eligible later-stage outcomes / eligible earlier-stage population, including sequence/cohort, deduplication, repeat-event treatment and observation window when needed. Generic event totals may not form a user funnel. Never imply a transition merely because two event names appear in order.
- Define cost per action as compatible spend / eligible actions; cost per purchase, lead or qualified lead need distinct action definitions. Do not substitute session CVR into a click-based CPS identity.
- Chart time series with comparable periods, explicit units, currency, timezone, scales, sample and missing-data treatment. Mark provisional periods, meaningful business/measurement changes and target provenance. Threshold colors and historical averages support reading, not causal or statistical certainty.
- Historical or industry benchmarks require source, date, population and definition. A target is an ambition or model assumption until supported; do not invent achievable lifts. Show absolute and relative changes correctly, including percentage points for rate differences.

## Interpretation and acceptance

Keep factual results, hypotheses and proposed actions visibly distinct. Investigate daily shifts against alternative explanations; do not label the date of a change as its cause. State limitations that could alter the decision, not a generic disclaimer list.

Acceptance evidence should cover the actual source/filter/period, numerator/denominator definitions, reconciled totals or explained differences, mapping unknowns, missing/provisional data, refreshed status and calculation checks. If a live connector, refresh, causal mechanism or commercial effect was not tested, say so. Session recordings, CRM and payment information require authorized access and privacy/consent constraints; reports should contain only the minimum necessary, sanitized evidence.

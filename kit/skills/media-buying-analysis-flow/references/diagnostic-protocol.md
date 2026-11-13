# Diagnostic protocol

Use only relevant branches. The owner's material supplies the diagnostic map and candidate checks below; compatibility, uncertainty, privacy and action boundaries are operational clarifications.

## Metric contract before calculation

For each measure record: source and extraction time; period/timezone; grain; currency; numerator and denominator; event, order or status definition; attribution window/model; exclusions; refunds/cancellations; cohort and maturity; coverage. A shared label does not establish comparability. If sources cannot be reconciled, show separate views and mark the identity unavailable.

For changes, show absolute values and sample counts before relative changes. Percentage-point changes in rates differ from percentage changes. A relative change from a zero baseline is undefined. Zero numerators can yield zero when their denominator is positive; a zero denominator makes the ratio undefined, not zero or an invented finite value.

| Identity | Required definitions and conditions |
| --- | --- |
| ROAS = revenue / spend = AOV / CPS | AOV = revenue / orders; CPS = spend / orders. Same nonzero orders, positive spend, period, cohort, attribution, currency and revenue basis. Orders may be zero while direct revenue/spend remains computable; then do not use the AOV/CPS branch. |
| AOV = ASP × UPO | ASP = item revenue / units; UPO = units / orders. Same nonzero units and orders and revenue basis. Reconcile order-level shipping, taxes, discounts and returns; item revenue need not equal order revenue. |
| CPS = CPC / CVR | CPC = spend / clicks; CVR = conversions / the same clicks. Nonzero clicks and conversions, same eligible cohort, attribution and period. Define conversions as the same orders used for CPS. Site sessions cannot replace platform clicks without a justified model. |
| CPC = CPM / (1,000 × CTR) | CPM = 1,000 × spend / impressions; CTR = the same clicks / impressions as a **decimal**. Nonzero impressions and clicks, same spend and click type. A displayed 2% enters as 0.02. Keep all-click, link-click and outbound CTR separate. |

An algebraic decomposition describes compatible totals; it does not isolate why a customer or auction changed. A directional claim about one variable assumes the other inputs remain fixed. When multiple components move, calculate their combined effect rather than assigning the full outcome change to one branch.

## AOV: ASP and units per order

- Compare realized item prices, discounts and product/category mix; inspect stock availability and stockouts. Compare comparable orders and periods, not only headline catalog prices.
- For units per order inspect top sellers, mix, availability and campaign traffic/budget allocation. A stockout or reallocation can motivate a hypothesis; verify timing, exposure and alternatives.
- Check seasonality, sample and measurement changes. The course's three-day or seven-day examples are possible windows, not sufficient-evidence rules. Recommend an upsell or price test only when the evidence and delivery capacity support it.

## CVR: funnel and traffic context

First define whether counts are events, sessions, unique users or orders. Do not call unrelated aggregate events a sequential user funnel. A transition rate requires a compatible, eligible earlier-stage denominator and matched sequence/cohort where the interpretation requires it; state repeats, deduplication, observation window and measurement loss. Counts can differ because of tracking, consent, redirects, browser loss and attribution.

| Candidate transition | Checks to select when relevant |
| --- | --- |
| Link click → page view | Click/view definitions, time windows, redirects, destination accessibility, load performance on relevant devices/networks, tagging and consent coverage. A discrepancy alone does not prove failed loading. |
| Page view → content view | Landing-page type and event implementation first; then listing, sorting, stock, price presentation, thumbnails and naming. A landing page can already be a product page. |
| Content view → cart | Product clarity, benefits, evidence, offer, delivery, price, effort and perceived risk. A price change does not establish price-caused abandonment. |
| Cart → checkout | Visibility/usability of the next action and observed friction. Authorized session recordings can illustrate friction, but are not automatically representative or causal evidence. |
| Checkout → purchase | Form usability, fees, delivery expectations, payment methods, valid codes, confirmation and measurement. Use an authorized test/sandbox flow; real charges, fulfillment or customer messages need separate authorization. |

Session duration, pages per session and bounce/engagement measures depend on page purpose, intention, platform definitions and coverage. Treat them as contextual signals, not direct measures of traffic quality. Inspect traffic mix alongside site friction and instrumentation. For recordings and payment data, use only authorized access with applicable consent/privacy constraints, redact personal/payment details and retain the minimum necessary evidence.

## CPC: creative, CTR and CPM

For video, select platform-defined three-second views, ThruPlay, percentage watched or completion only after recording eligibility, denominator, video length, placement and window. These measures and clicks are not necessarily sequential stages; CTR all is not a direct measure of scroll stopping, completion is not proof of desire, and a click may occur at different moments. Images need relevant click and downstream measures, not video retention.

Frequency, trend, reach, estimated audience size and overlap may motivate creative/audience-fatigue hypotheses. Verify exposure, mix, periods and downstream outcomes; these signals do not establish fatigue, saturation or harmful self-competition. Audience exclusions, new creative, budgets and structures are proposed tests rather than automatic remedies.

For CPM inspect campaign objective, delivery, placement and audience/auction mix and applicable platform-specific quality signals. Small audiences, destination issues or conversion-event problems are hypotheses to investigate, not universal explanations of CPM. A cheaper upper-funnel objective is useful only when it serves a defined business/measurement goal. Do not replace pixels, pages or accounts to evade restrictions.

## From diagnosis to decision

Use: observation → competing explanations → evidence/counterevidence → unresolved uncertainty → next validation → possible action if supported. Choose an observational comparison or authorized experiment suited to the decision. State practical effect, sample, uncertainty, stopping method where relevant and dependencies. Neither significance nor a funnel pattern alone proves causality; a causal claim requires a defensible design and assumptions. Prioritize impact, urgency, feasibility and confidence without promising a financial result.

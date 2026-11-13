# Method and evidence checks

Read the sections needed for the current question. These checks expand the six stages in the entrypoint; they do not define the course's pending frameworks or a universal dashboard.

## Objective and competing explanations

Frame a decision-specific question instead of simply asking to improve performance. For a measured View Content to Add to Cart decline, establish the event definitions, denominator, period and tracking quality before interpreting the rate. Record the baseline and desired target only if provided or supported; an unknown target stays unknown.

Relevant business context can include campaign objectives, audience, price, offers, stock, new collections and site changes. Distinguish stakeholder-reported context from independently verified records. Consult already supplied context first; new outreach requires its own authorization.

Guard against confirmation bias and anchoring. Low CPM does not establish campaign success without the objective and downstream outcomes. Repeated "why" questions can expose testable explanations, but a chain of plausible statements is not evidence that one event caused another. Look for alternatives, instrument errors and contradictory evidence.

## Collection and reconciliation

Choose a source by what it records, not by its label:

| Candidate source | Possible use | Definition to verify |
| --- | --- | --- |
| Advertising platform | Spend, impressions, creative clicks and attributed outcomes | Campaign objective, click type, attribution window, reporting basis and coverage |
| GA4 or supplied site analytics | Tracked sessions, users and on-site behaviour | Event setup, identity, consent/measurement coverage, session and user definitions |
| Store backend/CMS | Recorded orders, revenue and customers | Payment/order status, cancellations, refunds and reporting basis |
| Payment records or CRM, when relevant and available | Reconcile paid outcomes or later statuses | Record identity, status timing, coverage and amount definition |

Clicks, sessions and users are different events. A difference between clicks and sessions alone cannot quantify lost tracking. GA4 users depend on the property's identity and measurement setup; they are not necessarily distinct people across devices. Platform-attributed conversions and total recorded or paid orders answer different questions. Do not sum competing platforms' attributed sales as independent actual sales.

For each dataset, record source, extraction date, period, timezone, currency, grain, event/status definitions, attribution windows and material gaps. Assess accuracy, completeness, consistency and relevance. Segment different objectives such as traffic and purchase campaigns when mixing them would distort the answer.

For a merge, retain raw inputs and source totals; define a common schema and defensible keys. Normalize dates/identifiers, inspect join cardinality and unmatched rows, then reconcile counts and amounts. A daily spend row joined to several order rows can multiply spend; use the appropriate aggregation or separate view. Unjoinable sources remain separate with their limitations.

## Cleaning and a transformation record

Record each rule, reason, affected rows, exclusions, assumptions and before/after counts and relevant totals. Preserve enough lineage to reproduce the result.

- **Missing data:** identify affected fields/periods and coverage. Exclude only from measures the gap invalidates. Missing purchase values may block revenue analysis while valid click analysis remains possible. Do not fill unknowns with zero. If an estimate is justified, label it and compare conclusions with and without it; prefer original reliable records.
- **Duplicates:** distinguish duplicated records from legitimate repeated activity using suitable event/order identifiers, source and time scope. Retain raw records and document the reconciliation.
- **Outliers:** investigate error versus genuine observation. Keep valid values by default for totals; use segmentation, robust summaries or sensitivity comparisons where useful. A large real order is not a cleaning error merely because it is extreme.
- **Formatting:** normalize numeric types, dates with known locale/timezone, currency labels, text and names. A label change is not a currency conversion. Normalize contact data only if necessary and authorized.
- **Inconsistencies:** use traceable alias/mapping rules. Ambiguous entities remain unresolved rather than silently merged. Suggest maintained choices/input validation when that would prevent a demonstrated recurrence.

Cleaning improves consistency; it does not prove that the dataset represents all real activity. Report remaining gaps and their effect on the question.

## Processing and comparison

Define each calculation's unit, numerator, denominator, source, time/cohort and status before using it. For example, revenue and ad spend need compatible definitions for ROAS; cost per sale requires a defined sale count, and units per order requires both units and orders. Do not use incompatible attributed and actual totals as if they shared a basis.

Aggregate at the grain the question requires. Pivots can group campaign, creative, month, product, country or audience. Recompute ratios from the appropriate summed numerators and denominators rather than indiscriminately averaging row percentages. Users and reach can overlap and generally cannot be summed across such groups as independent people.

Preserve a dated context record for material promotions, prices, stock, collections, site and campaign changes. A 3% / 6% / 3% conversion series with an offer in the middle suggests a hypothesis; three observations do not define a normal baseline or establish the offer's effect.

Charts, heat maps and conditional formatting should show period, units, sample sizes, scales and missing-data treatment. A color or pattern is an investigation aid, not statistical or causal proof.

Use benchmarks only when relevant to the question: historical performance, prior campaigns, business targets or suitably comparable industry data. Record their source, date, population, metric definition and limitations. An industry average is not an automatically attainable target. If an external benchmark must be researched, follow the task's network authorization and source requirements; do not upload private data.

For time comparisons, assess comparable periods, seasonality, cohort maturity, offer/price, traffic mix, economic context and measurement changes. Same-season year-over-year comparisons are not automatically equivalent. Comparing different seasons can answer a seasonality question if differences are explicit.

## Insights, uncertainty and priority

Record exposures, conversions, sample, period and uncertainty before declaring an advantage. One order from one session or two purchases in an hour cannot alone establish a durable winner. Any practical minimum-data threshold must fit the decision; an operational threshold is not statistical significance.

When a formal experiment is needed, specify the comparison, assignment, metric, effect of interest, sample and stopping method before interpreting it. Report effect size and uncertainty. Statistical significance alone does not establish business importance, causality in observational comparisons, or the probability that a hypothesis is true. Do not invent universal sample or significance cutoffs. When evidence is inadequate, say inconclusive and identify whether more data or a bounded reversible action is useful.

Label findings distinctly: observed symptom; possible explanation; evidence supporting/contradicting it; unresolved limitation; proposed action or test. Higher cost per purchase may be observed; CPM, CTR, conversion, tracking and business changes are candidates to investigate, not automatically proven causes.

Prioritize with explained impact, urgency, feasibility, dependencies, resources and confidence. The owner's matrix is a flexible aid:

| Situation | Possible treatment |
| --- | --- |
| High impact, urgent, feasible | Top priority |
| High impact, urgent, low feasibility | Critical resource/dependency decision |
| High impact, less urgent, feasible | Candidate quick win |
| High impact, less urgent, low feasibility | Longer-term plan |
| Low impact, feasible | Fill-in if capacity permits |
| Low impact, low feasibility | Lower priority |

Explain each choice; do not make categories automatic rankings. A tracking issue can be urgent if it materially affects the decision, after checking its actual scope and remedy. Identify an owner and next step if known, without assigning people or executing external actions without authorization.

## Provenance and boundary

Adapted in English from owner material received on 5 November 2026: `docs/templates/media-buying/DATA_ANALYSIS_IN_PROGRESS.md` in the governance workspace. The source filename reflects incremental collection; the owner has declared the **Data Analysis Process portion** finished. This skill covers that portion only. The source remains the canonical note for later course material.

The entrypoint's flexible workflow, lane/access boundary and minimum evidence contract are local operational adaptations, not claimed verbatim course rules. No complete polar/secondary-metric framework, macro/micro-funnel method, analysis/reporting system or vertical-specific track is supplied here.

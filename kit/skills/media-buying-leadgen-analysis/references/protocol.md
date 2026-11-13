# Lead generation protocol

## Establish a usable contract

Reuse supplied definitions and ask for material gaps. Record the decision, offer/segment/GEO, source and extraction date, period/timezone/currency, spend scope, attribution model/window and conversion event. Then define:

| Input | Minimum decision-relevant definition |
| --- | --- |
| Acquisition | Click/form/lead IDs as needed; source/campaign/creative IDs; creation timestamp; spend at its actual grain |
| Identity | Deduplication key and lookback; separate lead, person, account and customer; treatment of repeat inquiries and existing customers |
| Validity/quality | Invalid/spam/duplicate rules; qualification criteria and version; accepted/rejected reasons; unknown classifications |
| CRM history | Stage/status transitions with event time, as-of time and relevant owner; definition of a terminal outcome |
| Appointment | Booking and appointment IDs, reschedules, cancellations, attendance and timing; avoid counting a reschedule as another unique lead |
| Sales/payment | Contract/customer IDs, signature date, payment/refund/cancellation status, revenue convention and business outcome |
| Cost/capacity | Media, eligible sales/fulfillment/payment costs, refunds/bad debt, response workload and capacity where available |

Do not require direct identifiers or conversation content when scoped IDs, timestamps and classifications suffice. Report small/sensitive segments at an appropriate aggregate level. Do not silently send data to an outside analysis tool.

## Reconcile before comparing

Preserve raw inputs and log exclusions and mapping changes. Reconcile submissions to unique valid leads; retain the duplicate, invalid and unknown counts rather than deleting them from the evidence. A deduplication rule can change CPL substantially and must stay stable across comparisons.

Check one-to-many joins: a lead can have several calls, stage changes, appointments, contracts and payments. Aggregate those to the intended unit before joining a campaign/day spend table. Never repeat daily spend on each lead row and then sum it. Keep unassigned records visible; do not allocate their outcomes proportionally without a labeled assumption.

Platform-attributed leads, tracker leads and CRM acquisition cohorts may have different windows, timezones and identity coverage. Keep separate views if a reconciliation cannot be defended. Overlapping platform claims cannot be added to obtain actual unique leads or sales. Verify whether offline outcome uploads already include a lead's form event to avoid counting both as unique acquisitions.

## Model the real pipeline

Map the relevant transitions, eligibility rules and branches. `Lead -> contact -> qualify -> book -> attend -> pay` is illustrative: qualification may precede contact; direct sales may skip appointments. Count unique entities at each stage and count activities separately. A current-status snapshot cannot reconstruct historical transition rates without history or suitable timestamps.

For every rate show numerator, denominator, unit and window:

| Measure | Compatible calculation |
| --- | --- |
| Valid lead CPL | Allocated acquisition spend / unique eligible valid acquired leads |
| Qualification rate | Unique qualified leads / leads assessed under those criteria; show unassessed leads separately |
| Coverage rate | Unique leads attempted / eligible leads assigned for follow-up |
| Contact rate | Unique leads reached / eligible attempted leads, or / all eligible leads; label the chosen base |
| Booking rate | Unique leads booked / eligible contacted or qualified leads, with the chosen base explicit |
| Attendance rate | Attended appointments / appointments eligible to have occurred; exclude future appointments and define reschedules |
| Close rate | Unique paid or won entities / eligible opportunities or attendees; label event and base |
| Cost per paid acquisition | Cohort acquisition spend / attributable unique paid acquisitions on that cohort basis |
| New customer CAC | Defined acquisition costs / attributable new customers; not orders, contracts or existing customers |

Zero eligible denominator means undefined, not zero performance. Unknown status is not failure. Ratios from totals take precedence over averages of campaign ratios. Stage-rate products only reproduce an end-to-end rate for compatible nested populations and windows; never multiply a convenient collection of unrelated dashboard rates.

## Preserve time and selection

Compare leads acquired in comparable periods at equal elapsed follow-up age, or explicitly show the maturity difference. Define as-of date, time-to-contact/qualification/payment, open counts and the lag distribution where available. Report calendar-period bookings or cash separately from acquisition-cohort yield. Historical CRM history must support an as-of reconstruction; today's status cannot prove what was known on day seven.

Look for changes in source mix, offer, qualification criteria, sales staffing/hours, response coverage, assignment rules, price and availability. A quality comparison among contacted leads can be selected by sales teams' choice of whom to call. Segment only where volumes and definitions remain interpretable; do not treat many exploratory slices as confirmed winners.

Do not use an early pipeline stage as a surrogate for paid value without evidence that it predicts it in this setting. If cohorts are immature, report early signals and pending outcomes, then specify the follow-up needed. A forecast using historical conversion or collection is a conditional estimate with visible assumptions, not observed revenue.

## Make an economic decision

Choose the revenue basis: billed contract value, recognized revenue or cash collected; distinguish taxes and pass-through amounts. Match refunds, cancellations, bad debt and costs to the cohort or period without double counting. Revenue/media spend can be reported as a defined revenue ROAS when the revenue is attributable; it does not establish profit.

Contribution after acquisition = compatible retained revenue minus documented non-acquisition variable costs minus included acquisition costs. State omitted fixed costs and missing costs; unknown costs are not zero. A customer-level acquisition ceiling requires compatible new-customer value, margin, collection, time horizon and capacity. Do not infer lifetime value from one payment or project indefinite repeat sales.

For lead resale, use accepted/payable/paid lead statuses and buyer clawbacks, caps, exclusivity and permitted traffic conditions where documented. Do not treat all submitted leads as billable or assume responsibility/control over the buyer's sales process.

End with a decision proportionate to evidence: reconcile missing CRM links; observe equal maturity; investigate response coverage; test a defined qualification/offer hypothesis within existing permission. A recommendation to raise budget requires supported downstream contribution and operational capacity, not merely a cheap form lead.

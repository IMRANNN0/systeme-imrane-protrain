# E-commerce protocol

## Define the data contract

Record question/decision, source and extraction time, timezone/currency, acquisition and observation periods, event/status definitions, revenue and cost conventions, attribution model/window and coverage. Select only relevant sources:

| Source | Useful evidence |
| --- | --- |
| Ad/tracker/analytics | Spend, impressions, link clicks, sessions and acquisition IDs at known grain; attribution definitions |
| Store/order lines | Unique order and customer IDs; creation time; SKU/quantity; item price, discounts, tax/shipping and status history |
| Payment/refund | Captured/settled/failed/refunded amounts and event dates; payment fees and chargebacks |
| Fulfillment/returns | Shipment/delivery/failure/return events, quantities and dispositions; restocked/recovered versus damaged/lost |
| Costs/capacity | COGS basis, outbound/return/failed delivery, packaging, payment/platform costs, acquisition scope, stock and fulfillment constraints |

Preserve raw inputs. Maintain stable keys and explicit unknown categories. One order can have many lines, transactions, shipments and returns; aggregate each source to the intended grain before joining. Order revenue and campaign spend must not multiply across line/shipment joins. Reconcile records, amounts and exclusion totals. A failed payment attempt is not automatically a unique failed order.

## Follow status and time

Build the actual lifecycle and define mutually exclusive current states separately from historical event counts. A delivered order can later be returned; historical delivered and returned counts therefore overlap. Partial refunds/returns require amount and unit evidence, not only an order count. Canceled-before-shipping, delivery failure and post-delivery return have different cost and denominator bases.

Compare acquisition cohorts at comparable fulfillment and return maturity. State as-of date, unresolved orders and applicable return observation horizon, without inventing a universal waiting period. Report calendar-period cash/refunds separately; an old order refunded this week should not silently reduce only this week's acquisition cohort. Reversals and chargebacks need a documented matching policy.

Keep platform-attributed revenue, analytics revenue and store/payment outcomes separately labeled unless a defensible reconciliation exists. Differences can reflect attribution, timing, view-through credit, deduplication, taxes/shipping, consent/coverage or refunds. Do not sum overlapping platform-attributed revenue to claim actual store sales. A platform result cannot establish incrementality.

## Use compatible units and denominators

| Measure | Calculation and condition |
| --- | --- |
| Created-order CPS | Defined acquisition spend / attributable unique created orders |
| Retained-order CPS | Same compatible spend / attributable retained orders at stated maturity |
| Cancellation rate | Canceled-before-shipping orders / eligible created orders |
| Delivery failure rate | Failed deliveries / eligible shipped orders; define attempts versus unique orders |
| Post-delivery return rate | Returned orders / eligible delivered orders, or returned units / delivered units; label the unit |
| Retained net AOV | Defined retained net sales / orders represented by those sales; partial refunds need a stated convention |
| New-customer CAC | Defined acquisition costs / attributable new customers; distinguish returning customers and repeat orders |
| Revenue ROAS | Compatible attributed revenue / ad spend, with revenue basis and attribution explicit |
| Contribution after media | Compatible net sales minus documented non-media variable costs minus media spend |

Unknown or zero denominators cannot be filled with a plausible rate. Recompute aggregate ratios from totals. If using a diagnostic identity, verify its bases: revenue ROAS = AOV / CPS only when revenue, orders and spend are compatible; CPS = CPC / order-per-click CVR only for the same clicks and orders. Session conversion cannot silently replace order-per-click conversion. ASP multiplied by units/order matches item-revenue AOV only for compatible weighted item prices/quantities and the same discount/tax/shipping convention; an unweighted product price average will not do.

## Reconcile economics without double counting

Choose what revenue includes: discounts, sales taxes, shipping revenue, refunds and chargebacks. Keep booked gross order value, recognized/retained net sales and cash collected distinct. For COD, an order submitted or even delivered does not automatically prove retained collected revenue; document reconciliation to settlement. Never subtract a refund twice when net sales already exclude it.

Match COGS to the accounting/economic scope. Recoverable returned stock is inventory, not automatically an additional total COGS loss. Retained goods, damaged/lost units, unrecoverable return costs, write-downs, return handling and failed-delivery charges may have different treatments. Document stock recovery and avoid expensing a returned unit both as sold COGS and as a second loss. Include outbound charges incurred on orders that never become retained sales.

List included acquisition, payment, marketplace, packaging, support, shipping and other variable costs and state missing/fixed costs. Revenue ROAS is not contribution or net profit. A contribution model may support a conditional acquisition ceiling or break-even ROAS; its mix, cost, return and maturity assumptions must stay visible. Nonpositive contribution before acquisition does not allow positive acquisition spend to make that same static model profitable.

Check stock in units, product mix, supplier/fulfillment capacity, delivery geography and cash-cycle constraints before suggesting scale. A higher AOV can come from more low-margin products, a discount or tax/shipping changes. Repeat purchase and lifetime contribution require customer-level cohorts and a defensible observation horizon; do not extrapolate indefinitely from early repeat orders.

## Decide what evidence is next

Separate measured change, candidate cause, counterevidence and unresolved gap. Examine relevant offer, checkout, traffic, delivery and measurement changes. A visible funnel drop localizes a problem; it does not establish the cause. Conclude with a supported action or an inconclusive diagnosis and a precise reconciliation/collection/test plan, including decision rule and stop/observation condition proportional to the task. Do not turn arithmetic decomposition into an automatic campaign adjustment.

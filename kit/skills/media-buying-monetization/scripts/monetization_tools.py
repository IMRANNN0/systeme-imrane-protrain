"""Scoped, deterministic Monetization calculations. No network or dependencies."""
import argparse
import copy
import html
import json
import math
from pathlib import Path
import sys


class ModelError(ValueError):
    pass


def num(data, key, minimum=0, maximum=None, positive=False):
    value = data.get(key)
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ModelError(f'{key}: finite numeric value required; missing is not zero')
    if value < minimum or (positive and value <= 0) or (maximum is not None and value > maximum):
        raise ModelError(f'{key}: out of range')
    return float(value)


def text_value(data, key):
    value = data.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ModelError(f'{key}: non-empty text required')
    return value


def context(data):
    value = data.get('context')
    if not isinstance(value, dict):
        raise ModelError('context object required')
    for key in ('currency', 'period', 'source', 'cost_scope'):
        text_value(value, key)
    excluded = value.get('excluded_costs')
    if not isinstance(excluded, list) or not all(isinstance(item, str) for item in excluded):
        raise ModelError('context.excluded_costs: explicit list required, possibly empty')
    return copy.deepcopy(value)


def ratio(a, b):
    return a / b if b else None


def margin(price, cost):
    return {'amount': price - cost, 'margin_on_sales': ratio(price - cost, price),
            'markup_on_cost': ratio(price - cost, cost)}


def constraints(data, orders, units):
    failures = []
    if 'stock_units' in data and units > num(data, 'stock_units') + 1e-9:
        failures.append('stock_units')
    if 'capacity_orders' in data and orders > num(data, 'capacity_orders') + 1e-9:
        failures.append('capacity_orders')
    return failures


def _order_row(data, discount):
    n = num(data, 'placed_orders')
    upo = num(data, 'upo', positive=True)
    price = num(data, 'price_unit') * (1 - discount)
    cancelled = n * num(data, 'cancel_rate_of_placed', maximum=1)
    shipped = n - cancelled
    failed = shipped * num(data, 'fail_rate_of_shipped', maximum=1)
    delivered = shipped - failed
    post_returns = delivered * num(data, 'post_return_rate_of_delivered', maximum=1)
    retained = delivered - post_returns
    all_returns = failed + post_returns
    damaged_return_units = all_returns * upo * num(data, 'damaged_fraction_of_return_units', maximum=1)
    other_damage = num(data, 'other_damaged_units')
    cogs = num(data, 'cogs_unit')
    retained_units = retained * upo
    consumed_units = retained_units + damaged_return_units + other_damage
    product_revenue = retained_units * price
    shipping_revenue = retained * num(data, 'shipping_revenue_per_retained')
    revenue = product_revenue + shipping_revenue
    ledger = {
        'sold_cogs': retained_units * cogs,
        'unrecoverable_return_cogs': damaged_return_units * cogs,
        'other_inventory_damage': other_damage * cogs,
        'forward_shipping': shipped * num(data, 'forward_shipping_per_shipped'),
        'reverse_shipping': all_returns * num(data, 'reverse_shipping_per_return'),
        'packaging': shipped * num(data, 'packaging_per_shipped'),
        'payment_fees_fixed': retained * num(data, 'payment_fee_per_retained'),
        'payment_fees_proportional': product_revenue * num(data, 'payment_fee_rate_of_product_revenue', maximum=1),
        'cancellation_fees': cancelled * num(data, 'cancellation_fee_per_cancelled'),
        'return_handling': all_returns * num(data, 'handling_per_return'),
        'other_marketing_period': num(data, 'other_marketing_period'),
        'overhead_period': num(data, 'overhead_period'),
        'other_period_costs': num(data, 'other_period_costs'),
    }
    non_ad = sum(ledger.values())
    ad = num(data, 'ad_spend')
    max_ads = revenue - non_ad
    failures = constraints(data, shipped, consumed_units)
    target = None
    if 'target_roas' in data:
        t = num(data, 'target_roas', positive=True)
        spend = revenue / t
        target = {'target_roas': t, 'ad_spend_at_target': spend,
                  'cps_placed_at_target': ratio(spend, n),
                  'cps_retained_at_target': ratio(spend, retained),
                  'scoped_result_at_target': revenue - non_ad - spend,
                  'assumption': 'same order flow and non-ad costs; acquisition response not predicted'}
    return {
        'discount_rate': discount, 'sale_price_unit': price, 'upo': upo,
        'expected_counts': {'placed': n, 'cancelled': cancelled, 'shipped': shipped,
                            'failed_delivery': failed, 'delivered': delivered,
                            'post_delivery_returns': post_returns, 'retained': retained,
                            'all_returns': all_returns, 'retained_units': retained_units,
                            'damaged_return_units': damaged_return_units, 'consumed_units': consumed_units},
        'success_delivery_of_placed': ratio(delivered, n),
        'success_retained_of_placed': ratio(retained, n),
        'product_revenue': product_revenue, 'shipping_revenue': shipping_revenue,
        'recognized_revenue': revenue, 'non_ad_cost_ledger': ledger,
        'non_ad_cost_total': non_ad, 'ad_spend': ad, 'total_cost': non_ad + ad,
        'scoped_result': revenue - non_ad - ad,
        'scoped_result_per_retained_order': ratio(revenue - non_ad - ad, retained),
        'aov_retained_products': ratio(product_revenue, retained),
        'aov_retained_including_shipping': ratio(revenue, retained),
        'media_cps_placed': ratio(ad, n), 'media_cps_retained': ratio(ad, retained),
        'recognized_revenue_roas': ratio(revenue, ad),
        'break_even_ad_budget': max_ads if max_ads > 0 else None,
        'break_even_cps_placed': ratio(max_ads, n) if max_ads > 0 else None,
        'break_even_cps_retained': ratio(max_ads, retained) if max_ads > 0 else None,
        'break_even_recognized_roas': ratio(revenue, max_ads) if max_ads > 0 else None,
        'positive_ad_break_even_possible': max_ads > 0,
        'feasible_terminal_stock_and_capacity': not failures, 'constraint_failures': failures,
        'target': target,
    }


def order_model(data):
    ctx = context(data)
    rates = data.get('discount_rates', [])
    if not isinstance(rates, list):
        raise ModelError('discount_rates: list required')
    discounts = [0.0]
    for value in rates:
        checked = num({'discount': value}, 'discount', maximum=1)
        if checked not in discounts:
            discounts.append(checked)
    rows = [_order_row(data, d) for d in discounts]
    return {'mode': 'order_model', 'context': ctx, 'rows': rows,
            'interpretation': 'Expected period flow; scoped result, not a guarantee or statutory net income.',
            'assumptions': ['rates conditional on named event, fractional counts are expectations',
                            'price and UPO homogeneous within retained and returned orders',
                            'failed deliveries and post-delivery returns fully reverse product revenue',
                            'all return units recoverable except explicit damaged fraction',
                            'stock constraint checks terminal consumption only, not dispatch concurrency or cash',
                            'discount rows keep orders, UPO and cost inputs unchanged; proportional product-revenue fees recalculate; no uplift predicted',
                            'fixed amounts entered once for the same period; no automatic allocation']}


def _best(rows, metric):
    valid = [r for r in rows if r['feasible']]
    if not valid:
        return []
    maximum = max(r[metric] for r in valid)
    return [r['scenario_id'] for r in valid if math.isclose(r[metric], maximum, rel_tol=1e-12, abs_tol=1e-9)]


def forecast(data):
    ctx = context(data)
    budget = num(data, 'ad_budget')
    cpc = num(data, 'cpc', positive=True)
    cost = num(data, 'non_ad_cost_per_order')
    fixed = num(data, 'period_fixed_costs')
    upo = num(data, 'upo', positive=True)
    event = text_value(data, 'conversion_event')
    if event not in ('retained_order', 'sale_in_simplified_model'):
        raise ModelError('forecast conversion_event must be retained_order or sale_in_simplified_model; use order_model for placed-order failures')
    points = data.get('scenarios')
    if not isinstance(points, list) or not points:
        raise ModelError('scenarios: non-empty list required')
    rows = []
    ids = set()
    clicks = budget / cpc
    for point in points:
        if not isinstance(point, dict):
            raise ModelError('each scenario must be an object')
        sid = text_value(point, 'id')
        if sid in ids:
            raise ModelError('scenario IDs must be unique')
        ids.add(sid)
        price = num(point, 'price_unit')
        cvr = num(point, 'cvr', maximum=1)
        orders = clicks * cvr
        units = orders * upo
        revenue = price * units
        cps = cpc / cvr if cvr else None
        result = revenue - orders * cost - fixed - budget
        before_ads = price * upo - cost
        failures = constraints(data, orders, units)
        rows.append({'scenario_id': sid, 'price_unit': price, 'cvr': cvr, 'upo': upo,
                     'clicks': clicks, 'orders': orders, 'units': units, 'cps': cps,
                     'scoped_result_per_order': ratio(result, orders),
                     'non_ad_variable_cost_total': orders * cost, 'period_fixed_costs': fixed,
                     'ad_spend': budget, 'revenue': revenue, 'scoped_result': result,
                     'roas': ratio(revenue, budget),
                     'break_even_cps_before_period_fixed_costs': before_ads if before_ads > 0 else None,
                     'feasible': not failures, 'constraint_failures': failures})
    best_profit = _best(rows, 'scoped_result')
    valid = [r for r in rows if r['feasible']]
    warnings = ['CVRs are inputs, not estimated price response; no true continuous optimum established',
                'infeasible rows are unconstrained arithmetic, not executable plans or capped-spend simulations']
    if not valid:
        warnings.append('no feasible supplied scenario')
    elif max(r['scoped_result'] for r in valid) <= 0:
        warnings.append('no positive-result feasible scenario; best ranking is at most break-even or least loss')
    return {'mode': 'forecast', 'context': ctx, 'conversion_event': event, 'rows': rows,
            'best_supplied_feasible': {'scoped_result': best_profit, 'revenue': _best(rows, 'revenue'),
                                       'orders': _best(rows, 'orders')},
            'warnings': warnings,
            'cost_definition': 'non_ad_cost_per_order excludes media and period_fixed_costs; result includes both once'}


def competitive(data):
    own = num(data, 'own_price')
    basis = data.get('comparison_basis')
    if not isinstance(basis, dict):
        raise ModelError('comparison_basis required')
    keys = ('currency', 'tax_basis', 'unit_basis', 'shipping_basis', 'observation_date')
    for k in keys:
        text_value(basis, k)
    entries = data.get('competitors')
    if not isinstance(entries, list):
        raise ModelError('competitors list required')
    included, excluded = [], []
    for entry in entries:
        if not isinstance(entry, dict):
            raise ModelError('each competitor must be an object')
        label = text_value(entry, 'id')
        if not isinstance(entry.get('comparable'), bool):
            raise ModelError('comparable must be explicitly true or false')
        if not entry['comparable']:
            excluded.append({'id': label, 'reason': 'declared non-comparable'})
            continue
        if entry.get('price') is None:
            excluded.append({'id': label, 'reason': 'missing price, not zero'})
            continue
        price = num(entry, 'price')
        if any(entry.get(k) != basis[k] for k in keys):
            excluded.append({'id': label, 'reason': 'comparison basis differs or missing; normalize before inclusion'})
            continue
        included.append({'id': label, 'price': price})
    average = sum(e['price'] for e in included) / len(included) if included else None
    return {'mode': 'competitive', 'comparison_basis': copy.deepcopy(basis), 'own_price': own,
            'included': included, 'excluded': excluded, 'sample_count': len(included),
            'sample_mean': average, 'own_minus_sample_mean': own - average if average is not None else None,
            'relative_difference': (own - average) / average if average else None,
            'classification': None,
            'limitation': 'unweighted comparable sample, not whole-market reference or customer perceived price; no approved classification thresholds implemented'}


def calculate(data):
    if not isinstance(data, dict):
        raise ModelError('input must be a JSON object')
    mode = data.get('mode')
    handlers = {'order_model': order_model, 'forecast': forecast, 'competitive': competitive}
    if mode not in handlers:
        raise ModelError('mode must be order_model, forecast or competitive')
    result = handlers[mode](data)
    # Reject arithmetic overflow as well as non-finite inputs.
    json.dumps(result, allow_nan=False)
    return result


def forecast_html(result):
    if result.get('mode') != 'forecast':
        raise ModelError('chart supports forecast only')
    rows = result['rows']
    values = [0.0] + [r[key] for r in rows for key in ('revenue', 'scoped_result')]
    low, high = min(values), max(values)
    span = high - low or 1
    x = lambda i: 70 + i * 780 / max(1, len(rows) - 1)
    y = lambda value: 320 - (value - low) * 240 / span
    line = lambda key: ' '.join(f'{x(i):.2f},{y(row[key]):.2f}' for i, row in enumerate(rows))
    ticks = ''.join(f'<text x="{x(i):.2f}" y="350" text-anchor="middle">{r["price_unit"]:g}</text>' for i, r in enumerate(rows))
    table = ''.join('<tr>' + ''.join(f'<td>{html.escape(str(r[k]))}</td>' for k in ('scenario_id', 'price_unit', 'cvr', 'orders', 'revenue', 'scoped_result', 'feasible')) + '</tr>' for r in rows)
    return f'''<!doctype html><html lang="fr"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Scénarios de prix</title><style>body{{font:16px system-ui;margin:32px;color:#182434;background:#f7f9fc}}main{{max-width:1100px;margin:auto}}svg{{width:100%;background:white;border:1px solid #ccd5e0}}text{{font:13px system-ui}}table{{width:100%;border-collapse:collapse;font-size:14px}}th,td{{padding:9px;text-align:right;border-bottom:1px solid #cdd5df}}th:first-child,td:first-child{{text-align:left}}.revenue{{color:#136eb0}}.profit{{color:#a24b19}}</style><main><h1>Scénarios de prix</h1><p>{html.escape(result['context']['currency'])} · {html.escape(result['context']['period'])} · hypothèses, pas résultats garantis.</p><p><b class="revenue">Revenu</b> et <b class="profit">résultat du périmètre</b>. Les points infaisables sont exclus du classement, sans modifier leur arithmétique.</p><p>« True » signifie seulement qu’aucune contrainte numérique fournie n’est dépassée. Stock ou capacité absents restent non évalués ; ce statut ne valide pas la faisabilité opérationnelle.</p><svg viewBox="0 0 920 380" role="img" aria-label="Revenu et résultat selon les prix fournis"><line x1="70" x2="850" y1="{y(0):.2f}" y2="{y(0):.2f}" stroke="#8895a6"/><polyline fill="none" stroke="#136eb0" stroke-width="3" points="{line('revenue')}"/><polyline fill="none" stroke="#a24b19" stroke-width="3" points="{line('scoped_result')}"/><text x="12" y="70">{high:,.0f}</text><text x="12" y="320">{low:,.0f}</text>{ticks}<text x="450" y="375">Prix unitaire</text></svg><table><thead><tr><th>Scénario</th><th>Prix</th><th>CVR</th><th>Commandes</th><th>Revenu</th><th>Résultat</th><th>Contraintes fournies satisfaites</th></tr></thead><tbody>{table}</tbody></table><p>Coûts : {html.escape(result['context']['cost_scope'])}. Exclusions : {html.escape(', '.join(result['context']['excluded_costs']) or 'aucune déclarée')}.</p></main></html>'''


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, help='JSON input; otherwise stdin')
    parser.add_argument('--output', type=Path, help='JSON output; otherwise stdout')
    parser.add_argument('--html', type=Path, help='optional offline forecast chart')
    args = parser.parse_args()
    try:
        raw = args.input.read_text(encoding='utf-8') if args.input else sys.stdin.read()
        data = json.loads(raw)
        result = calculate(data)
        body = json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False)
        if args.html:
            chart = forecast_html(result)
        if args.output:
            args.output.write_text(body + '\n', encoding='utf-8')
        else:
            print(body)
        if args.html:
            args.html.write_text(chart, encoding='utf-8')
    except (ValueError, TypeError, KeyError, OSError, OverflowError) as exc:
        print(json.dumps({'error': str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

"""Numerical contract checks; no external services or client data."""
import copy
import unittest
from monetization_tools import ModelError, calculate, forecast_html, margin


def ctx():
    return {'currency': 'DH', 'period': 'fictional month', 'source': 'fictional exercise',
            'cost_scope': 'explicit costs only', 'excluded_costs': ['taxes', 'finance']}


def order():
    return {'mode': 'order_model', 'context': ctx(), 'placed_orders': 100,
            'price_unit': 200, 'upo': 2, 'cancel_rate_of_placed': .1,
            'fail_rate_of_shipped': .2, 'post_return_rate_of_delivered': .25,
            'damaged_fraction_of_return_units': .1, 'other_damaged_units': 2,
            'cogs_unit': 50, 'forward_shipping_per_shipped': 10,
            'reverse_shipping_per_return': 4, 'packaging_per_shipped': 2,
            'payment_fee_per_retained': 3, 'payment_fee_rate_of_product_revenue': 0,
            'cancellation_fee_per_cancelled': 1,
            'handling_per_return': 2, 'shipping_revenue_per_retained': 5,
            'ad_spend': 1000, 'other_marketing_period': 200,
            'overhead_period': 500, 'other_period_costs': 0}


def forecast():
    return {'mode': 'forecast', 'context': ctx(), 'ad_budget': 200000, 'cpc': 1,
            'non_ad_cost_per_order': 120, 'period_fixed_costs': 0, 'upo': 1,
            'conversion_event': 'sale_in_simplified_model',
            'scenarios': [{'id': str(p), 'price_unit': p, 'cvr': c} for p, c in
                          [(250,.04),(300,.035),(350,.03),(400,.025),(450,.02),(500,.015),(550,.01),(600,.005)]]}


class NumericTests(unittest.TestCase):
    def test_course_forecast_and_tied_revenue(self):
        result = calculate(forecast())
        r = {row['scenario_id']: row for row in result['rows']}
        self.assertAlmostEqual(r['250']['scoped_result'], 840000)
        self.assertAlmostEqual(r['350']['scoped_result'], 1180000)
        self.assertAlmostEqual(r['400']['scoped_result'], 1200000)
        self.assertAlmostEqual(r['600']['scoped_result'], 280000)
        self.assertEqual(result['best_supplied_feasible']['scoped_result'], ['400'])
        self.assertEqual(result['best_supplied_feasible']['revenue'], ['300','350'])

    def test_cvr_zero_keeps_spend_loss(self):
        data = forecast(); data['scenarios'] = [{'id':'zero','price_unit':400,'cvr':0}]
        row = calculate(data)['rows'][0]
        self.assertEqual(row['orders'], 0); self.assertIsNone(row['cps'])
        self.assertEqual(row['scoped_result'], -200000)
        self.assertIsNone(row['scoped_result_per_order'])

    def test_order_flow_conditional_bases(self):
        row = calculate(order())['rows'][0]
        c = row['expected_counts']
        self.assertEqual([c[k] for k in ('cancelled','shipped','failed_delivery','delivered','post_delivery_returns','retained')],
                         [10,90,18,72,18,54])
        self.assertAlmostEqual(row['success_delivery_of_placed'], .72)
        self.assertAlmostEqual(row['success_retained_of_placed'], .54)

    def test_ledger_and_return_inventory_not_double_counted(self):
        row = calculate(order())['rows'][0]
        # 108 sold units, 7.2 unrecoverable return units, 2 separately damaged units.
        self.assertAlmostEqual(row['non_ad_cost_ledger']['sold_cogs'], 5400)
        self.assertAlmostEqual(row['non_ad_cost_ledger']['unrecoverable_return_cogs'], 360)
        self.assertAlmostEqual(row['non_ad_cost_total'], 8028)
        self.assertAlmostEqual(row['recognized_revenue'], 21870)
        self.assertAlmostEqual(row['scoped_result'], 12842)

    def test_fixed_cost_added_once(self):
        data = order(); base = calculate(data)['rows'][0]
        data['overhead_period'] += 75
        changed = calculate(data)['rows'][0]
        self.assertAlmostEqual(base['scoped_result'] - changed['scoped_result'], 75)

    def test_break_even_budget_reconciles(self):
        data = order(); row = calculate(data)['rows'][0]
        data['ad_spend'] = row['break_even_ad_budget']
        self.assertAlmostEqual(calculate(data)['rows'][0]['scoped_result'], 0)
        self.assertAlmostEqual(row['break_even_recognized_roas'], 21870 / 13842)

    def test_no_positive_ad_break_even_for_negative_contribution(self):
        data = order(); data['price_unit'] = 1
        row = calculate(data)['rows'][0]
        self.assertFalse(row['positive_ad_break_even_possible'])
        self.assertIsNone(row['break_even_cps_retained'])

    def test_margin_and_markup_different_denominators(self):
        m = margin(150,100)
        self.assertEqual(m['amount'], 50)
        self.assertAlmostEqual(m['margin_on_sales'], 1/3)
        self.assertEqual(m['markup_on_cost'], .5)

    def test_stock_units_and_capacity_not_orders(self):
        data = order(); data['stock_units'] = 116
        row = calculate(data)['rows'][0]
        self.assertAlmostEqual(row['expected_counts']['consumed_units'], 117.2)
        self.assertFalse(row['feasible_terminal_stock_and_capacity'])
        data['stock_units'] = 118; data['capacity_orders'] = 80
        self.assertIn('capacity_orders', calculate(data)['rows'][0]['constraint_failures'])

    def test_discount_no_invented_uplift(self):
        data = order(); data['discount_rates'] = [.1]
        a,b = calculate(data)['rows']
        self.assertEqual(a['expected_counts'], b['expected_counts'])
        self.assertAlmostEqual(a['scoped_result'] - b['scoped_result'], 2160)

    def test_target_roas_changes_ad_allowance_only(self):
        data = order(); data['target_roas'] = 5
        row = calculate(data)['rows'][0]
        self.assertAlmostEqual(row['target']['ad_spend_at_target'], 4374)
        self.assertAlmostEqual(row['target']['scoped_result_at_target'], 9468)

    def test_discount_recomputes_proportional_fees(self):
        data = order(); data['discount_rates'] = [.1]
        data['payment_fee_rate_of_product_revenue'] = .02
        a,b = calculate(data)['rows']
        self.assertAlmostEqual(a['non_ad_cost_ledger']['payment_fees_proportional'], 432)
        self.assertAlmostEqual(b['non_ad_cost_ledger']['payment_fees_proportional'], 388.8)
        self.assertAlmostEqual(a['scoped_result'] - b['scoped_result'], 2116.8)

    def test_forecast_upo_price_and_fixed_cost(self):
        data = forecast(); data['upo'] = 2; data['period_fixed_costs'] = 100
        row = calculate(data)['rows'][0]
        self.assertEqual(row['units'], 16000)
        self.assertAlmostEqual(row['revenue'], 4000000)
        self.assertAlmostEqual(row['scoped_result'], 2839900)

    def test_feasibility_excludes_unfulfillable_not_silently_capped(self):
        data = forecast(); data['capacity_orders'] = 4500
        r = calculate(data)
        self.assertEqual(r['rows'][3]['orders'], 5000)
        self.assertFalse(r['rows'][3]['feasible'])
        self.assertEqual(r['best_supplied_feasible']['scoped_result'], ['450'])

    def test_loss_ranking_not_profit_recommendation(self):
        data = forecast(); data['non_ad_cost_per_order'] = 1000
        r = calculate(data)
        self.assertTrue(any('no positive-result' in s for s in r['warnings']))
        self.assertTrue(all(row['scoped_result'] < 0 for row in r['rows']))

    def test_comparable_sample_missing_price_not_zero(self):
        basis = {'currency':'DH','tax_basis':'included','unit_basis':'one shirt','shipping_basis':'excluded','observation_date':'2026-10-25'}
        entries = [{**basis,'id':'a','comparable':True,'price':300},
                   {**basis,'id':'b','comparable':True,'price':330},
                   {**basis,'id':'c','comparable':True,'price':None},
                   {**basis,'id':'d','comparable':False,'price':50},
                   {**basis,'id':'e','comparable':True,'price':200,'currency':'USD'}]
        r = calculate({'mode':'competitive','own_price':340,'comparison_basis':basis,'competitors':entries})
        self.assertEqual(r['sample_mean'],315); self.assertEqual(r['sample_count'],2)
        self.assertEqual(len(r['excluded']),3); self.assertIsNone(r['classification'])

    def test_empty_comparison_not_zero_market(self):
        r = calculate({'mode':'competitive','own_price':10,'comparison_basis':{
            'currency':'DH','tax_basis':'included','unit_basis':'unit','shipping_basis':'excluded','observation_date':'2026-10-25'},'competitors':[]})
        self.assertIsNone(r['sample_mean']); self.assertIsNone(r['relative_difference'])

    def test_missing_nonfinite_and_range_rejected(self):
        for key, value in [('cpc',0),('cpc',float('nan')),('ad_budget',float('inf')),('upo',True)]:
            data = forecast(); data[key] = value
            with self.assertRaises(ModelError): calculate(data)
        data = order(); del data['overhead_period']
        with self.assertRaises(ModelError): calculate(data)
        data = order(); data['cancel_rate_of_placed'] = 10
        with self.assertRaises(ModelError): calculate(data)

    def test_fully_cancelled_no_shipping_or_sales(self):
        data = order(); data['cancel_rate_of_placed'] = 1; data['other_damaged_units'] = 0
        row = calculate(data)['rows'][0]
        self.assertEqual(row['recognized_revenue'],0)
        self.assertEqual(row['non_ad_cost_ledger']['forward_shipping'],0)
        self.assertIsNone(row['media_cps_retained'])
        self.assertEqual(row['scoped_result'], -1800)

    def test_html_two_series_no_external_or_script(self):
        data = forecast(); data['context']['period'] = '<unsafe>'
        body = forecast_html(calculate(data))
        self.assertEqual(body.count('<polyline'),2)
        self.assertIn('&lt;unsafe&gt;',body)
        self.assertNotIn('<script',body); self.assertNotIn('https://',body)


if __name__ == '__main__':
    unittest.main()

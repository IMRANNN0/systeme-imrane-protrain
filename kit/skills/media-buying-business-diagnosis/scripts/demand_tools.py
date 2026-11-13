"""Offline assessment, midpoint elasticity and baseline time-series analysis."""
from __future__ import annotations
import argparse
import csv
from datetime import date, timedelta
import html
import io
import json
import math
from pathlib import Path
import statistics
import sys

FACTORS = {
    'product_nature': ('expiration', 'essentiality', 'dependency', 'seasonality', 'price_elasticity', 'versatility', 'urgency'),
    'market': ('competition', 'size', 'supply'),
    'consumer': ('preferences', 'expectations', 'loyalty'),
    'economic_conditions': ('purchase_power', 'economic_cycle', 'income_distribution', 'inflation'),
}
LABELS = {'product_nature': 'Product Nature', 'market': 'Market', 'consumer': 'Consumer', 'economic_conditions': 'Economic Conditions'}

def number(value, field, low=None, high=None):
    if isinstance(value, bool) or not isinstance(value, (float, int)) or not math.isfinite(value):
        raise ValueError(field + ': finite number required')
    if low is not None and value < low or high is not None and value > high:
        raise ValueError(field + ': out of range')
    return float(value)

def integer(value, field, low=1, high=10000):
    x=number(value, field, low, high)
    if not x.is_integer():
        raise ValueError(field + ': integer required')
    return int(x)

def assessment(data, demo=False):
    rubric=data.get('rubric', {})
    status=rubric.get('status')
    if status not in ('draft_local', 'screenshot_demo', 'owner_confirmed'):
        raise ValueError('Explicit rubric status required')
    if not demo and status != 'owner_confirmed':
        raise ValueError('Draft/screenshot ratings require --demo; owner review remains pending')
    if status == 'owner_confirmed' and not (rubric.get('approved_by') and rubric.get('approved_at')):
        raise ValueError('Owner confirmation name and date required')
    if rubric.get('formula') != 'weighted_max_v1':
        raise ValueError('Unsupported formula; do not silently substitute an aggregation')
    lo=number(rubric.get('score_min'), 'score_min', 0)
    hi=number(rubric.get('score_max'), 'score_max', 0.000001)
    if lo >= hi:
        raise ValueError('score_min must be smaller than score_max')
    axes=data.get('axes', [])
    if len(axes)!=4 or {a.get('id') for a in axes} != set(FACTORS):
        raise ValueError('Exactly four unique assessment axes required')
    result={'scope':data.get('scope', {}), 'rubric_status':status, 'demonstration':bool(demo),
            'formula':'100 * sum(weight * score) / (score_max * sum(rated weights))',
            'meaning':'Percentage of maximum entered rubric points, not probability or market demand volume',
            'overall_score':None, 'overall_reason':'No owner-approved cross-axis aggregation supplied', 'axes':[]}
    for axis_id, expected in FACTORS.items():
        axis=next(a for a in axes if a['id']==axis_id)
        rows=axis.get('factors', [])
        ids=[f.get('id') for f in rows]
        if len(ids)!=len(set(ids)) or set(ids)-set(expected):
            raise ValueError('Unknown or duplicate factor in '+axis_id)
        weighted=total_weight=0.0
        unknown_weight=0.0;unknown_weights_known=True
        rated=[]; unknown=[]; na=[]
        for fid in expected:
            row=next((f for f in rows if f.get('id')==fid), {'status':'unknown'})
            s=row.get('status', 'unknown')
            if s=='not_applicable':
                if not row.get('reason') or row.get('score') is not None:
                    raise ValueError('N/A requires reason and no score: '+fid)
                na.append(fid)
            elif s=='unknown':
                if row.get('score') is not None:
                    raise ValueError('Unknown factor cannot carry a score: '+fid)
                if row.get('weight') is None:
                    unknown_weights_known=False
                else:
                    missing_weight=number(row['weight'],fid+'.weight',1,5)
                    if not missing_weight.is_integer():raise ValueError('Ordinal weight must be integer: '+fid)
                    unknown_weight+=missing_weight
                unknown.append(fid)
            elif s=='rated':
                w=number(row.get('weight'), fid+'.weight', 0.000001, 5)
                score=number(row.get('score'), fid+'.score', lo, hi)
                if not w.is_integer() or not score.is_integer():
                    raise ValueError('Ordinal weights and scores must be integers: '+fid)
                if not row.get('evidence') or not row.get('reason'):
                    raise ValueError('Rated factor needs evidence and rationale: '+fid)
                weighted+=w*score; total_weight+=w
                rated.append(fid)
            else:
                raise ValueError('Unknown factor status: '+fid)
        pct=100*weighted/(hi*total_weight) if total_weight else None
        if pct is not None and not math.isfinite(pct):
            raise ValueError('Assessment overflow')
        applicable=len(expected)-len(na)
        result['axes'].append({'id':axis_id, 'label':LABELS[axis_id], 'percent':pct,
            'status':'partial' if unknown else ('complete' if rated else 'not_applicable'),
            'rated':rated, 'unknown':unknown, 'not_applicable':na,
            'factor_coverage':len(rated)/applicable if applicable else None,
            'weighted_coverage':(total_weight/(total_weight+unknown_weight)
                if unknown_weights_known and total_weight+unknown_weight else None),
            'weighted_coverage_note':('Fraction of applicable weight represented' if unknown_weights_known
                else 'Indeterminate: some unknown factors have no assigned weight'),
            'weighted_sum':weighted, 'rated_weight_sum':total_weight})
    result['status']=('partial' if any(a['unknown'] for a in result['axes']) else
                      ('complete' if any(a['rated'] for a in result['axes']) else 'not_applicable'))
    result['warnings']=['Ratings are supplied judgments; arithmetic does not verify their evidence or rubric validity.',
        'No automatic GO/STOP thresholds. A low subtotal is not proof of no market.',
        'Unknown factors are excluded from the subtotal and remain visible; partial coverage is not a complete assessment.']
    if demo:
        result['warnings'].insert(0, 'DEMONSTRATION ONLY — local rubric/original scoring anchors are not approved for client use.')
    return result

def radar_svg(result):
    cx=340; cy=255; radius=165
    def pt(i, value):
        angle=-math.pi/2+i*math.pi/2
        return cx+radius*value*math.cos(angle),cy+radius*value*math.sin(angle)
    parts=['<svg xmlns="http://www.w3.org/2000/svg" width="680" height="520" viewBox="0 0 680 520" role="img" aria-labelledby="title desc">',
        '<title id="title">Demand Assessment</title><desc id="desc">Four axes, known weighted subtotals and coverage; missing values are not zero.</desc>',
        '<rect width="680" height="520" fill="white"/>',
        '<text x="340" y="28" text-anchor="middle" font-family="sans-serif" font-size="18">Demand Assessment — '+('DEMO' if result['demonstration'] else 'entered ratings')+'</text>']
    for level in (.2,.4,.6,.8,1):
        points=' '.join('%.2f,%.2f'%pt(i,level) for i in range(4))
        parts.append('<polygon points="'+points+'" fill="none" stroke="#cbd5e1"/>')
        parts.append(f'<text x="{cx+5}" y="{cy-radius*level-3:.2f}" font-family="sans-serif" font-size="11">{int(level*100)}%</text>')
    known=[]
    for i,axis in enumerate(result['axes']):
        x,y=pt(i,1); lx,ly=pt(i,1.3)
        horizontal=i in (1,3)
        if horizontal: ly-=15
        parts.append(f'<line x1="{cx}" y1="{cy}" x2="{x:.2f}" y2="{y:.2f}" stroke="#94a3b8"/>')
        label=html.escape(axis['label'])
        pct='?' if axis['percent'] is None else f"{axis['percent']:.2f}%"
        parts.append(f'<text x="{lx:.2f}" y="{ly:.2f}" text-anchor="middle" font-family="sans-serif" font-size="12">{label}</text>')
        parts.append(f'<text x="{lx:.2f}" y="{ly+(35 if horizontal else 17):.2f}" text-anchor="middle" font-family="sans-serif" font-size="12">{pct} · {axis["status"]} ({len(axis["rated"])}/{len(axis["rated"])+len(axis["unknown"])})</text>')
        if axis['percent'] is not None:
            px,py=pt(i,axis['percent']/100)
            known.append((px,py))
            parts.append(f'<circle cx="{px:.2f}" cy="{py:.2f}" r="5" fill="'+('#fff' if axis['status']=='partial' else '#0f766e')+'" stroke="#0f766e" stroke-width="2"/>')
    if len(known)==4 and all(a['status']=='complete' for a in result['axes']):
        parts.insert(3,'<polygon points="'+' '.join('%.2f,%.2f'%p for p in known)+'" fill="#0f766e" fill-opacity=".12" stroke="#0f766e" stroke-width="2"/>')
    parts.append('<text x="340" y="505" text-anchor="middle" font-family="sans-serif" font-size="11">Partial axes: points only; no invented area, overall score or probability.</text></svg>')
    return ''.join(parts)

def elasticity(p1,p2,q1,q2):
    p1=number(p1,'p1',0.000001);p2=number(p2,'p2',0.000001)
    q1=number(q1,'q1',0);q2=number(q2,'q2',0)
    if p1==p2 or q1+q2==0:
        raise ValueError('Price change and positive average quantity required')
    dp=(p2-p1)/((p2+p1)/2)
    dq=(q2-q1)/((q2+q1)/2)
    signed=dq/dp; magnitude=abs(signed)
    category='unitary' if math.isclose(magnitude,1,rel_tol=1e-9,abs_tol=1e-12) else ('elastic' if magnitude>1 else 'inelastic')
    if not math.isfinite(signed): raise ValueError('Elasticity overflow')
    return {'method':'midpoint arc elasticity','signed':signed,'absolute':magnitude,'category':category,
        'price_change_pct':100*dp,'quantity_change_pct':100*dq,
        'warnings':['Descriptive comparison, not a causal estimate; check time, exposure, availability and other changes.']+
        (['Price and quantity changed in the same direction; this is not a validated downward demand curve.'] if signed>0 else [])}

def advance(d,frequency,steps=1):
    if frequency=='day': return d+timedelta(days=steps)
    if frequency=='week': return d+timedelta(days=7*steps)
    if frequency=='month':
        if d.day!=1: raise ValueError('Monthly observations must use first day of month')
        idx=d.year*12+d.month-1+steps
        return date(idx//12,idx%12+1,1)
    raise ValueError('frequency must be day, week or month')

def predict(values,method,horizon,m=None):
    if method=='naive': return [values[-1]]*horizon
    if method=='drift':
        slope=(values[-1]-values[0])/(len(values)-1)
        return [values[-1]+slope*h for h in range(1,horizon+1)]
    if method=='seasonal_naive': return [values[-m+(h%m)] for h in range(horizon)]
    raise ValueError('Unknown model')

def timeseries(data):
    for key in ('metric','unit','source','frequency'):
        if not data.get(key): raise ValueError('Missing '+key)
    obs=data.get('observations',[])
    if not 4<=len(obs)<=100000: raise ValueError('Need 4 to 100000 observations')
    dates=[date.fromisoformat(o['date']) for o in obs]
    values=[number(o['value'],'observation.value',0) for o in obs]
    for a,b in zip(dates,dates[1:]):
        if advance(a,data['frequency'])!=b:
            raise ValueError('Dates must be chronological, unique and regular; do not fill missing dates with zero')
    advance(dates[-1],data['frequency'])
    horizon=integer(data.get('horizon'),'horizon',1,60)
    holdout=integer(data.get('holdout'),'holdout',1,len(values)-3)
    m=data.get('seasonal_period')
    if m is not None: m=integer(m,'seasonal_period',2,10000)
    methods=['naive','drift']
    warnings=['Baseline forecasts only. One-step rolling evaluation is not validation of every future horizon.',
              'No causal advertising effect or prediction interval is estimated.']
    if m and len(values)-holdout>=2*m:
        methods.append('seasonal_naive')
    elif m:
        warnings.append('Seasonal naive excluded: tool requires two complete training seasons before holdout.')
    metrics={}
    for method in methods:
        errors=[values[t]-predict(values[:t],method,1,m)[0] for t in range(len(values)-holdout,len(values))]
        metrics[method]={'MAE':statistics.fmean(abs(e) for e in errors),
                         'RMSE':math.sqrt(statistics.fmean(e*e for e in errors)),'test_points':holdout}
    selected=min(methods,key=lambda name:metrics[name]['MAE'])
    forecasts=predict(values,selected,horizon,m)
    if not all(math.isfinite(v) for v in forecasts): raise ValueError('Forecast overflow')
    negative=any(v<0 for v in forecasts)
    if negative: warnings.append('Negative baseline forecast: review; values were not silently clipped to zero.')
    return {'scope':data.get('scope',{}),'metric':data['metric'],'unit':data['unit'],'source':data['source'],
        'frequency':data['frequency'],'observations':obs,'evaluation':'expanding-window one-step holdout',
        'metrics':metrics,'selected_model':selected,'selection':'lowest holdout MAE; ties prefer naive then drift',
        'forecasts':[{'date':advance(dates[-1],data['frequency'],i+1).isoformat(),'value':v} for i,v in enumerate(forecasts)],
        'status':'requires_review' if negative else 'baseline_forecast','warnings':warnings}

def series_svg(result):
    obs=result['observations'];fc=result['forecasts']; values=[o['value'] for o in obs]+[o['value'] for o in fc]
    low=min(0,min(values)); high=max(values)
    if high==low: high=low+1
    def point(i,v): return 65+650*i/max(1,len(values)-1),365-295*(v-low)/(high-low)
    def path(start,vals): return ' '.join('%.2f,%.2f'%point(start+i,v) for i,v in enumerate(vals))
    split=point(len(obs)-1,values[len(obs)-1])[0]
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="800" height="450" viewBox="0 0 800 450" role="img" aria-label="Observed series and baseline forecast">'
        '<rect width="800" height="450" fill="white"/><g font-family="sans-serif" fill="#172033">'
        '<text x="40" y="25" font-size="18">'+html.escape(str(result['metric']))+' — baseline forecast</text>'
        f'<path d="M65,60 V365 H740" fill="none" stroke="#64748b"/><text x="5" y="65">{high:.2f}</text>'
        f'<text x="5" y="365">{low:.2f}</text><line x1="{split:.2f}" x2="{split:.2f}" y1="55" y2="365" stroke="#94a3b8" stroke-dasharray="4 4"/>'
        '<polyline points="'+path(0,values[:len(obs)])+'" fill="none" stroke="#2563eb" stroke-width="2"/>'
        '<polyline points="'+path(len(obs)-1,values[len(obs)-1:])+'" fill="none" stroke="#b45309" stroke-dasharray="6 4" stroke-width="2"/>'
        '<text x="65" y="390">'+obs[0]['date']+'</text><text x="590" y="390">'+fc[-1]['date']+'</text>'
        '<text x="65" y="415">Blue: observed · Dashed: forecast · '+html.escape(result['selected_model'])+'</text>'
        '<text x="65" y="439">No prediction interval; no causal claim about ad spend.</text></g></svg>')

def emit(out,stem,result,svg):
    out=Path(out).resolve()
    files={stem+'.json':json.dumps(result,ensure_ascii=False,indent=2,allow_nan=False)+'\n',stem+'.svg':svg}
    if stem=='assessment':
        buf=io.StringIO(newline='');writer=csv.writer(buf);writer.writerow(['axis','percent','status','rated','unknown','N/A'])
        for a in result['axes']:writer.writerow([a['label'],a['percent'],a['status'],len(a['rated']),len(a['unknown']),len(a['not_applicable'])])
        files[stem+'.csv']=buf.getvalue()
    title=html.escape(stem)
    note='DEMONSTRATION — rubric pending review' if result.get('demonstration') else result.get('status','')
    details=html.escape(json.dumps(result,ensure_ascii=False,indent=2,allow_nan=False))
    if stem=='assessment':
        overview='<table><thead><tr><th>Axe</th><th>Sous-total</th><th>Facteurs notés</th><th>Inconnus</th><th>Sans objet</th><th>État</th></tr></thead><tbody>'
        for a in result['axes']:
            pct='Non calculable' if a['percent'] is None else f"{a['percent']:.2f}%"
            overview+=f'<tr><td>{html.escape(a["label"])}</td><td>{pct}</td><td>{len(a["rated"])}</td><td>{len(a["unknown"])}</td><td>{len(a["not_applicable"])}</td><td>{a["status"]}</td></tr>'
        overview+='</tbody></table><p>Les valeurs sont des sous-totaux de points saisis, pas des probabilités de vente. Pas de note globale ni de seuil GO/STOP.</p>'
    else:
        overview='<table><thead><tr><th>Modèle testé</th><th>MAE</th><th>RMSE</th><th>Points test</th></tr></thead><tbody>'
        for method,values in result['metrics'].items():
            overview+=f'<tr><td>{method}</td><td>{values["MAE"]:.3f}</td><td>{values["RMSE"]:.3f}</td><td>{values["test_points"]}</td></tr>'
        overview+='</tbody></table><p>Modèle retenu : '+html.escape(result['selected_model'])+'. Validation à un pas ; la précision future reste à vérifier.</p>'
    files[stem+'.html']=(f'<!doctype html><html lang="fr"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title}</title>'
        '<style>body{max-width:960px;margin:24px auto;padding:0 16px;font:16px system-ui;color:#172033}svg{max-width:100%;height:auto}pre{white-space:pre-wrap;overflow-wrap:anywhere}strong{color:#92400e}table{border-collapse:collapse;width:100%}th,td{text-align:left;border:1px solid #cbd5e1;padding:8px}</style>'
        f'<h1>{title}</h1><p><strong>{html.escape(note)}</strong></p>'+svg+'<h2>Overview</h2>'+overview+'<details><summary>Données, provenance et limites du calcul</summary><pre>'+details+'</pre></details></html>')
    if any((out/name).exists() for name in files): raise ValueError('Output exists; choose a new directory rather than overwrite')
    out.mkdir(parents=True,exist_ok=True)
    for name,content in files.items():
        with (out/name).open('x',encoding='utf-8',newline='') as stream:stream.write(content)

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    sub=parser.add_subparsers(dest='command',required=True)
    for name in ('assessment','timeseries'):
        p=sub.add_parser(name);p.add_argument('--input',required=True);p.add_argument('--out',required=True)
        if name=='assessment':p.add_argument('--demo',action='store_true')
    p=sub.add_parser('elasticity')
    for name in ('p1','p2','q1','q2'):p.add_argument('--'+name,type=float,required=True)
    args=parser.parse_args()
    if args.command=='elasticity':
        result=elasticity(args.p1,args.p2,args.q1,args.q2)
        print(json.dumps(result,ensure_ascii=False,allow_nan=False));return
    data=json.loads(Path(args.input).read_text(encoding='utf-8-sig'))
    if args.command=='assessment':
        result=assessment(data,args.demo);svg=radar_svg(result);stem='assessment'
    else:
        result=timeseries(data);svg=series_svg(result);stem='timeseries'
    emit(args.out,stem,result,svg)
    print(json.dumps({'command':args.command,'status':result['status'],'output':str(Path(args.out).resolve())}))

if __name__=='__main__':
    try:main()
    except (ValueError,KeyError,TypeError,OSError,OverflowError) as exc:
        print('INPUT_ERROR: '+str(exc),file=sys.stderr);raise SystemExit(2)

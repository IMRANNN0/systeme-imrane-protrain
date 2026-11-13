from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import unquote, urlparse
import hashlib
import json

root = Path(__file__).resolve().parent
inventory = json.loads((root/'inventory-measurements.json').read_text(encoding='utf-8'))
proposal = json.loads((root/'template-proposal.json').read_text(encoding='utf-8'))
checks = {}
checks['20_originals_hash_preserved'] = len(inventory['inventory']) == 20 and all(hashlib.sha256(Path(f['path']).read_bytes()).hexdigest() == f['sha256_before'] for f in inventory['inventory'])
checks['reference_hash_matches'] = hashlib.sha256(Path(proposal['reference']['path']).read_bytes()).hexdigest() == proposal['reference']['sha256']
checks['single_reference_not_reconstructed'] = proposal['reference']['id'] == 32 and proposal['production_performed'] is False
for f in root.glob('*.json'):
    json.loads(f.read_text(encoding='utf-8'))
checks['all_json_parses'] = True

class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
    def handle_starttag(self, tag, attrs):
        for key, value in attrs:
            if key in ('src','href'):
                self.links.append(value)

page = (root/'design-system-analysis.html').read_text(encoding='utf-8')
parser = Links()
parser.feed(page)
missing = []
for link in parser.links:
    parsed = urlparse(link)
    target = Path(unquote(parsed.path).lstrip('/')) if parsed.scheme == 'file' else root/link
    if not target.exists():
        missing.append(link)
checks['all_report_links_exist'] = not missing
checks['exact_copy_documented'] = all(v['text'] in page for k,v in proposal['variable_slots'].items() if k in ('hook','promise','cta'))
result = {'checks':checks, 'missing_links':missing, 'status':'PASS' if all(checks.values()) else 'FAIL', 'scope':'Analysis document/data integrity only. No V4 output or RTL/mobile creative QA performed.'}
(root/'verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,ensure_ascii=False))
assert result['status'] == 'PASS'

"""Render an offline, source-linked view of a scoped Graphify index."""
from collections import defaultdict
from html import escape


def source_link(url, label):
    return f'<a href="{escape(url)}">{escape(label)}</a>'


def render_viewer(meta, sources, nodes, links):
    labels = {node["id"]: node["label"] for node in nodes}
    neighbors = defaultdict(list)
    for edge in links:
        start, end, relation = edge["source"], edge["target"], edge["relation"]
        neighbors[start].append(("Outgoing", labels[end], relation, edge["source_url"]))
        if start != end:
            neighbors[end].append(("Incoming", labels[start], relation, edge["source_url"]))

    entries = []
    for node in nodes:
        relationships = "".join(
            f"<li>{direction} · {escape(label)} · {source_link(url, relation or 'Relationship source')}</li>"
            for direction, label, relation, url in neighbors[node["id"]]
        )
        entries.append(
            f'<details class="node"><summary>{escape(node["label"])}</summary>'
            f'<p>{source_link(node["source_url"], node["source"])}</p>'
            f'<p>{escape(node["summary"])}</p><ul>{relationships}</ul></details>'
        )
    file_list = "".join(f'<li>{source_link(source["url"], source["path"])}</li>' for source in sources)
    project = escape(meta["project"])
    status = escape(meta["status"])
    built = escape(meta["last_build"] or "Unknown")
    mode = "Local Markdown structure" if meta.get("mode") == "local-markdown" else "Semantic index"
    empty_text = "No saved nodes with sources in the current scope." if not nodes else "No matching nodes."
    return fr"""<!doctype html>
<html lang="en">
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'unsafe-inline'; script-src 'unsafe-inline'">
<title>Graphify · {project}</title>
<style>
:root {{ color-scheme: light dark; font: 1rem/1.5 system-ui, sans-serif }}
body {{ max-width: 58rem; margin: 2rem auto; padding: 0 1rem 3rem }}
h1 {{ font-size: clamp(1.8rem, 4vw, 2.6rem); margin-bottom: .5rem }}
dl {{ display: grid; grid-template-columns: max-content 1fr; gap: .25rem 1rem }}
dt {{ font-weight: 650 }}
dd {{ margin: 0; overflow-wrap: anywhere }}
input {{ font: inherit; width: min(26rem, 100%); padding: .4rem; box-sizing: border-box }}
details {{ border-top: 1px solid GrayText; padding: .55rem 0 }}
summary {{ cursor: pointer; font-weight: 600 }}
ul {{ padding-inline-start: 1.5rem }}
a {{ overflow-wrap: anywhere }}
</style>
<main>
<h1>Graphify · {project}</h1>
<dl>
<dt>Scope</dt><dd>{project}</dd>
<dt>Freshness</dt><dd>{status}</dd>
<dt>Index</dt><dd>{mode}</dd>
<dt>Last build</dt><dd>{built}</dd>
<dt>Saved graph</dt><dd>{len(nodes)} nodes · {len(links)} relationships in the current scope</dd>
</dl>
<p>Freshness and scope were checked when this view was generated. Open the source files to verify the saved graph.</p>
<h2>Saved nodes</h2>
<label for="search">Filter by node, source or relationship</label><br>
<input id="search" type="search" autocomplete="off">
<p id="empty" role="status"{' hidden' if nodes else ''}>{empty_text}</p>
{''.join(entries)}
<h2>Current scope sources</h2>
<ul>{file_list}</ul>
</main>
<script>
const search = document.querySelector('#search');
const empty = document.querySelector('#empty');
const nodes = Array.from(document.querySelectorAll('.node'));
const searchable = value => value.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '');
search.addEventListener('input', () => {{
  const terms = searchable(search.value).trim().split(/\s+/);
  let matches = 0;
  for (const node of nodes) {{
    const text = searchable(node.textContent);
    node.hidden = !terms.every(term => text.includes(term));
    if (!node.hidden) matches++;
  }}
  empty.hidden = matches > 0;
}});
</script>
</html>
"""

"""Build a deterministic offline graph from an already approved corpus.

Each source gets a file node. For Markdown, this extracts ATX headings and
inline links from the first 64 KiB, up to 24 headings and 128 distinct link
destinations per file. It skips fenced/indented code and inline code in link
search. Setext headings, reference links, nested link syntax, and fragment
resolution are outside this parser's scope.
"""
from __future__ import annotations

import posixpath
import re
from collections.abc import Mapping
from pathlib import PurePosixPath
from urllib.parse import unquote, urlsplit


MAX_BYTES = 64 * 1024
MAX_HEADINGS = 24
MAX_LINKS = 128
HEADING = re.compile(r"^ {0,3}(#{1,6})[ \t]+(.+)$")
FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")
INLINE_CODE = re.compile(r"(?<!`)(`+)(?!`).*?\1(?!`)")
LINK = re.compile(r'''(?<![!\\])\[[^\[\]\n]*\]\([ \t]*(?:<([^<>\n]+)>|([^\s()<>]+))(?:[ \t]+(?:"[^"\n]*"|'[^'\n]*'))?[ \t]*\)''')


def markdown_lines(content: bytes):
    fence = ""
    for line in content[:MAX_BYTES].decode("utf-8-sig", errors="ignore").splitlines():
        marker = FENCE.match(line)
        if fence:
            if marker and marker[1][0] == fence[0] and len(marker[1]) >= len(fence) and not marker[2].strip():
                fence = ""
            yield None
        elif marker:
            fence = marker[1]
            yield None
        elif line.startswith(("    ", "\t")):
            yield None
        else:
            yield line


def clip(text: str, limit: int) -> str:
    return text if len(text) <= limit else text[:limit - 1].rstrip() + "…"


def adjacent_excerpt(lines, start):
    chunks = []
    for line in lines[start:start + 8]:
        if line is None or HEADING.match(line):
            break
        text = " ".join(line.split())
        if not text:
            if chunks:
                break
            continue
        chunks.append(text[:240])
    return clip(" ".join(chunks), 240)


def link_target(source, destination, approved):
    try:
        url = urlsplit(destination)
    except ValueError:
        return None
    if url.scheme or url.netloc or url.query or not url.path:
        return None
    path = unquote(url.path)
    if path.startswith("/") or "\\" in path or any(ord(char) < 32 for char in path):
        return None
    target = posixpath.normpath(posixpath.join(posixpath.dirname(source), path))
    return target if target in approved else None


def build_graph(paths: Mapping[str, bytes]) -> dict:
    """Return the nodes and links consumed by the saved Graphify reader."""
    nodes = []
    links = []
    file_ids = {source: f"file:{source}" for source in sorted(paths)}

    def connect(source_id, target_id, relation, source_file):
        links.append({"source": source_id, "target": target_id, "relation": relation,
                      "source_file": source_file})

    for source, file_id in file_ids.items():
        path = PurePosixPath(source)
        nodes.append({"id": file_id, "label": path.name, "source_file": source, "description": ""})
        if path.suffix.casefold() not in {".md", ".markdown"}:
            continue
        lines = list(markdown_lines(paths[source]))
        parents = [(0, file_id)]
        heading_count = 0
        linked = set()
        for i, line in enumerate(lines):
            if line is None:
                continue
            heading = HEADING.match(line)
            if heading and heading_count < MAX_HEADINGS:
                level = len(heading[1])
                label = re.sub(r"[ \t]+#+[ \t]*$", "", heading[2]).strip()
                if label:
                    node_id = f"heading:{source}#{i + 1}"
                    nodes.append({"id": node_id, "label": clip(label, 160), "source_file": source,
                                  "description": adjacent_excerpt(lines, i + 1)})
                    while parents[-1][0] >= level:
                        parents.pop()
                    connect(parents[-1][1], node_id, "contains", source)
                    parents.append((level, node_id))
                    heading_count += 1
            if len(linked) >= MAX_LINKS:
                continue
            for match in LINK.finditer(INLINE_CODE.sub("", line)):
                target = link_target(source, match[1] or match[2], file_ids)
                if target is None or target in linked:
                    continue
                connect(file_id, file_ids[target], "links_to", source)
                linked.add(target)
                if len(linked) >= MAX_LINKS:
                    break
    return {"nodes": nodes, "links": links}

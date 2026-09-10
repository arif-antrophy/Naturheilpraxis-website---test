#!/usr/bin/env python3
"""Inline referenced assets as data URIs -> index.inlined.html (self-contained single file).

Covers src= and poster=, anywhere under assets/ — not just assets/clean/ and not
just images. The hero is a <video> with a poster frame, and both were being left
as external paths, which quietly broke the whole point of this build.
"""
import base64, re, os, sys

src, out = 'index.html', 'index.inlined.html'
html = open(src, encoding='utf-8').read()
mime = {
    '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.png': 'image/png',
    '.gif': 'image/gif',  '.webp': 'image/webp', '.svg': 'image/svg+xml',
    '.mp4': 'video/mp4',  '.webm': 'video/webm', '.woff2': 'font/woff2',
}
seen = {}

def repl(m):
    attr, path = m.group(1), m.group(2)
    if path not in seen:
        if not os.path.exists(path):
            sys.exit('missing asset: ' + path)
        ext = os.path.splitext(path)[1].lower()
        if ext not in mime:
            sys.exit('no mime type for %s — add it to build-inline.py' % ext)
        blob = open(path, 'rb').read()
        seen[path] = ('data:%s;base64,%s' % (mime[ext], base64.b64encode(blob).decode()), len(blob))
    return '%s="%s"' % (attr, seen[path][0])

html = re.sub(r'(src|poster)="(assets/[^"]+)"', repl, html)

# Nothing under assets/ may survive as a path, or the file is not standalone.
left = sorted(set(re.findall(r'(?:src|href|poster)="(assets/[^"]+)"', html)))
if left:
    sys.exit('still external, not self-contained: ' + ', '.join(left))

open(out, 'w', encoding='utf-8').write(html)
raw = sum(size for _, size in seen.values())
print('inlined %d unique assets (%.0f KB raw) -> %s (%.0f KB)'
      % (len(seen), raw / 1024, out, os.path.getsize(out) / 1024))
for path, (_, size) in sorted(seen.items(), key=lambda kv: -kv[1][1])[:3]:
    print('  largest: %s (%.0f KB)' % (path, size / 1024))

#!/usr/bin/env python3
"""Inline assets/clean/* as data URIs -> index.inlined.html (self-contained single file)."""
import base64, re, os, sys

src, out = 'index.html', 'index.inlined.html'
html = open(src, encoding='utf-8').read()
mime = {'.jpg':'image/jpeg', '.jpeg':'image/jpeg', '.png':'image/png'}
seen = {}

def repl(m):
    path = m.group(1)
    if path in seen:
        return 'src="%s"' % seen[path]
    if not os.path.exists(path):
        sys.exit('missing asset: ' + path)
    ext = os.path.splitext(path)[1].lower()
    uri = 'data:%s;base64,%s' % (mime[ext], base64.b64encode(open(path,'rb').read()).decode())
    seen[path] = uri
    return 'src="%s"' % uri

html = re.sub(r'src="(assets/clean/[^"]+)"', repl, html)
open(out, 'w', encoding='utf-8').write(html)
print('inlined %d unique assets -> %s (%.0f KB)' % (len(seen), out, os.path.getsize(out)/1024))

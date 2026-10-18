#!/usr/bin/env python3
"""Build the public site (index.html) from src/template.html.

Run from the repo root:  python3 src/build_public.py
Then commit index.html together with any src/ change.

The public build deliberately contains NO officer names, Monitor text, drills or law book.
Those are stored in Supabase (docs table, coll 'offpre' and 'ref') and loaded by the app
for signed-in, card-verified members. Edit src/template.html, never index.html directly:
index.html is generated and will be overwritten by the next build.
"""
import re, json, datetime, os, sys
try:
    import zoneinfo; now = datetime.datetime.now(zoneinfo.ZoneInfo('America/Chicago'))
except Exception:
    now = datetime.datetime.now()
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src = os.path.join(root, 'src')
rd = lambda *p: open(os.path.join(src, *p), encoding='utf-8').read()
stubs = json.loads(rd('data', 'stubs.json'))
t = rd('template.html')
t = t.replace('__BUILD__', now.strftime('%b %-d %-I:%M %p'))
t = (t.replace('__LODGES__', rd('data', 'lodges.json'))
      .replace('__BODIES__', rd('data', 'bodies.json'))
      .replace('__LODGEINFO__', rd('data', 'lodgeinfo.json'))
      .replace('__CONTACTS__', rd('data', 'contacts.json'))
      .replace('__JSQR__', rd('vendor', 'jsqr.min.js'))
      .replace('__OFFICERS__', '{}')
      .replace('__DRILLS__', stubs['DRILLDATA'])
      .replace('__MONITOR__', stubs['MON'])
      .replace('__LAWS__', stubs['LAWS']))
t = t.replace('https://trucktraders.github.io/freemasonry/', 'https://mytrestleboard.org/')
for k in ('__LODGES__','__BODIES__','__LODGEINFO__','__CONTACTS__','__JSQR__','__OFFICERS__','__DRILLS__','__MONITOR__','__LAWS__','__BUILD__'):
    assert k not in t, 'placeholder left in build: ' + k
open(os.path.join(root, 'index.html'), 'w', encoding='utf-8').write(t)
js = max(re.findall(r'<script>(.*?)</script>', t, re.S), key=len)
open(os.path.join(root, '.build-check.js'), 'w', encoding='utf-8').write(js)
print('wrote index.html (%d bytes). Syntax check: node --check .build-check.js' % len(t))

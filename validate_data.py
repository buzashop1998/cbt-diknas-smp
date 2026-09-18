# -*- coding: utf-8 -*-
"""Validate webapp/data/*.js -> check syntax (node) and structure (json parse)."""
import json, os, re, subprocess, sys

OUT = 'webapp/data'
ok = True
total_q = 0
for f in sorted(os.listdir(OUT)):
    if not f.endswith('.js'):
        continue
    p = os.path.join(OUT, f)
    r = subprocess.run(['node', '--check', p], capture_output=True, text=True)
    if r.returncode != 0:
        ok = False
        print('SYNTAX', f, r.stderr[:200])
        continue
    src = open(p, encoding='utf-8').read()
    m = re.search(r'window\.KSM_PACKAGES\["([^"]+)"\] = (\{.*\});?\s*$', src, re.S)
    if not m:
        ok = False
        print('PARSE', f, 'header tidak cocok'); continue
    data = json.loads(m.group(2))
    if m.group(1) != data['id']:
        ok = False; print('ID mismatch', f)
    n_pg = n_isi = 0
    for q in data['questions']:
        if q['type'] == 'pg':
            n_pg += 1
            if len(q.get('o', {})) < 3:
                ok = False; print('PG opsi <3:', f, 'no', q['n'])
            if q['a'] not in q.get('o', {}):
                ok = False; print('PG kunci tak ada di opsi:', f, 'no', q['n'], q['a'])
        else:
            n_isi += 1
            if not str(q.get('a', '')).strip():
                ok = False; print('Isian tanpa kunci:', f, 'no', q['n'])
        if not q['t'].strip():
            ok = False; print('Soal tanpa teks:', f, 'no', q['n'])
        for img in q.get('img', []):
            fp = os.path.join('webapp', img.replace('/', os.sep))
            if not os.path.exists(fp):
                ok = False; print('Gambar hilang:', img)
    total_q += len(data['questions'])
    print(f'{m.group(1)}: {len(data["questions"])} soal (PG {n_pg}, isian {n_isi})')
print('TOTAL:', total_q, '| status:', 'OK' if ok else 'ADA MASALAH')


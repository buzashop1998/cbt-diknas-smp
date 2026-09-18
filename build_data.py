# -*- coding: utf-8 -*-
"""Assemble final webapp/data/<pkg>.js from draft + manual overrides."""
import json, os, sys

DRAFT = 'draft'
OUT = 'data'
os.makedirs(OUT, exist_ok=True)

def build(pkg, meta, include, fixes=None, drops=None, draft=None):
    """include: list of question nums to keep. fixes: {num: {t, o, a, img, pemb, type}}"""
    d = json.load(open(os.path.join(DRAFT, (draft or pkg) + '.json'), encoding='utf-8'))
    bynum = {}
    for q in d['questions']:
        bynum.setdefault(q['num'], q)
    fixes = fixes or {}
    drops = drops or []
    questions = []
    for num in include:
        if num in drops or num not in bynum:
            continue
        q = bynum[num]
        f = fixes.get(num, {})
        text = f.get('t', q['text'])
        opts = f.get('o', q['options'])
        opts = {k: v for k, v in opts.items() if str(v).strip() != ''} if opts else {}
        key = f.get('a', q.get('key'))
        imgs = f.get('img', q.get('images', []))
        imgs = [p.replace('img2/', 'img/') for p in imgs]
        typ = f.get('type', 'isian' if q.get('isian') else ('pg' if len(opts) >= 3 else 'pg'))
        pemb = f.get('pemb', '')
        if key is None:
            print(f'!! {pkg} Q{num} TANPA KUNCI - dilewati')
            continue
        item = {'n': num, 'type': typ, 't': text, 'a': key, 'pemb': pemb}
        if typ == 'pg':
            item['o'] = opts
        if imgs:
            item['img'] = imgs
        questions.append(item)
    data = {
        'id': pkg, 'title': meta['title'], 'year': meta['year'],
        'mapel': meta['mapel'], 'tingkat': meta['tingkat'],
        'duration': meta.get('duration', 120), 'questions': questions,
    }
    js = ('window.KSM_PACKAGES = window.KSM_PACKAGES || {};\n'
          'window.KSM_PACKAGES["%s"] = %s;\n' % (pkg, json.dumps(data, ensure_ascii=False)))
    path = os.path.join(OUT, pkg + '.js')
    with open(path, 'w', encoding='utf-8') as fh:
        fh.write(js)
    pg = sum(1 for q in questions if q['type'] == 'pg')
    isi = len(questions) - pg
    print(f'OK {path} | {len(questions)} soal (pg {pg}, isian {isi})')



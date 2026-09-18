# -*- coding: utf-8 -*-
import json, sys
pkg = sys.argv[1]
maxlen = int(sys.argv[2]) if len(sys.argv) > 2 else 180
only = set(int(x) for x in sys.argv[3].split(',')) if len(sys.argv) > 3 else None
d = json.load(open(f'draft/{pkg}.json', encoding='utf-8'))
for q in d['questions']:
    if only and q['num'] not in only:
        continue
    key = q.get('key', '-')
    opts = ' | '.join(f'{k}:{str(v)[:60]}' for k, v in q['options'].items())
    print(f"Q{q['num']} k={key} img={len(q['images'])} :: {q['text'][:maxlen]}")
    print('   ', opts[:260])

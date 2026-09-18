# -*- coding: utf-8 -*-
"""Ekspansi otomatis: semua soal berkunci + kunci dari pembahasan defantri."""
import json, re
from build_data import build

META_YEAR = {'2020': 2020, '2021': 2021, '2022': 2022, '2023': 2023, '2024': 2024, '2025': 2025}
KEY_PAT = re.compile(
    r'(?:jawaban(?:nya)?(?:\s*(?:yang\s*)?(?:benar|tepat))?|pilihan|opsi)\s*(?:adalah|adalah:|:|-)?\s*\(?\s*([A-E])\s*\)?(?![A-Za-z])',
    re.I)

def usable(q):
    if len(q.get('options', {})) < 3:
        return False
    if not q.get('key'):
        return False
    if len(q.get('text', '').strip()) < 30:
        return False
    for v in q['options'].values():
        if len(str(v).strip()) < 2:
            return False
    return True

def build_auto(draft, pkg, mapel, tingkat, auto_key_from_pemb=False):
    d = json.load(open('draft/%s.json' % draft, encoding='utf-8'))
    bynum = {}
    for q in d['questions']:
        if q['num'] in bynum:
            continue
        qq = dict(q)
        if not qq.get('key') and auto_key_from_pemb:
            m = KEY_PAT.search(qq.get('pemb', ''))
            if m:
                qq['key'] = m.group(1).upper()
        if usable(qq):
            bynum[q['num']] = qq
    fixes = {}
    include = sorted(bynum)
    year = META_YEAR[pkg[:4]]
    build(pkg, {'title': f'OSN {mapel} SMP {year} - {tingkat}', 'year': year,
                'mapel': mapel, 'tingkat': tingkat, 'duration': 120},
          include=include, fixes=fixes, draft=draft)
    return len(include)

if __name__ == '__main__':
    n1 = build_auto('2021-mat-pembahasan', '2021-mat-kabkota', 'Matematika', 'Kabupaten/Kota')
    n2 = build_auto('2022-mat-pembahasan', '2022-mat-kabkota', 'Matematika', 'Kabupaten/Kota')
    n3 = build_auto('2023-mat-pembahasan-b', '2023-mat-kabkota', 'Matematika', 'Kabupaten/Kota')
    n4 = build_auto('2020-mat-pembahasan-a', '2020-mat-kabkota', 'Matematika', 'Kabupaten/Kota')
    n5 = build_auto('2025-ipa-kabkota', '2025-ipa-kabkota', 'IPA', 'Kabupaten/Kota', auto_key_from_pemb=True)
    n6 = build_auto('2025-ipa-prov', '2025-ipa-prov', 'IPA', 'Provinsi', auto_key_from_pemb=True)
    n7 = build_auto('2025-ipa-semifinal', '2025-ipa-semifinal', 'IPA', 'Nasional (Semifinal)', auto_key_from_pemb=True)
    n8 = build_auto('2025-ipa-final', '2025-ipa-final', 'IPA', 'Nasional (Final)', auto_key_from_pemb=True)
    print('auto:', n1, n2, n3, n4, n5, n6, n7, n8)

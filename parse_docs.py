# -*- coding: utf-8 -*-
"""Parse src/*.txt (Google Docs OSN 2021) v2: pisah seksi SOAL & KUNCI."""
import os, re, json

SRC, DRAFT = 'src', 'draft'
QNUM_RE = re.compile(r'^\s*(\d{1,3})\s*[.)]\s*(.*)$')
KUNCI_HDR = re.compile(r'^[^\n]*KUNCI[^\n]*$', re.I | re.M)

META = {
    '2021-ipa-kabkota-a': ('IPA', 'Kabupaten/Kota', 'Paket A'), '2021-ipa-kabkota-b': ('IPA', 'Kabupaten/Kota', 'Paket B'), '2021-ipa-kabkota-c': ('IPA', 'Kabupaten/Kota', 'Paket C'),
    '2021-ipa-prov-a': ('IPA', 'Provinsi', 'Paket A'), '2021-ipa-prov-b': ('IPA', 'Provinsi', 'Paket B'), '2021-ipa-prov-c': ('IPA', 'Provinsi', 'Paket C'),
    '2021-ipa-nas-a': ('IPA', 'Nasional', 'Paket A'), '2021-ipa-nas-b': ('IPA', 'Nasional', 'Paket B'), '2021-ipa-nas-c': ('IPA', 'Nasional', 'Paket C'),
    '2021-ips-kabkota-a': ('IPS', 'Kabupaten/Kota', 'Paket A'), '2021-ips-kabkota-b': ('IPS', 'Kabupaten/Kota', 'Paket B'), '2021-ips-kabkota-c': ('IPS', 'Kabupaten/Kota', 'Paket C'),
    '2021-ips-prov-a': ('IPS', 'Provinsi', 'Paket A'), '2021-ips-prov-b': ('IPS', 'Provinsi', 'Paket B'), '2021-ips-prov-c': ('IPS', 'Provinsi', 'Paket C'),
    '2021-ips-nas-a': ('IPS', 'Nasional', 'Paket A'), '2021-ips-nas-b': ('IPS', 'Nasional', 'Paket B'), '2021-ips-nas-c': ('IPS', 'Nasional', 'Paket C'),
}

def parse(name):
    raw = open(os.path.join(SRC, name + '.txt'), encoding='utf-8').read()
    km = KUNCI_HDR.search(raw)
    kunci = {}
    soal_text = raw
    if km:
        soal_text = raw[:km.start()]
        after = raw[km.end():]
        for m in re.finditer(r'(?m)^\s*(\d{1,3})\s*[.):\-]\s*([A-Ea-e])\s*\.?\s*$', after):
            kunci[int(m.group(1))] = m.group(2).upper()
        if not kunci:
            for m in re.finditer(r'\b(\d{1,3})\s*[.):\-]\s*([A-Ea-e])\b', after):
                n = int(m.group(1))
                if n not in kunci:
                    kunci[n] = m.group(2).upper()
    lines = [l.rstrip() for l in soal_text.split('\n')]
    questions, cur, expected = [], None, 1
    for ln in lines:
        m = QNUM_RE.match(ln)
        if m:
            num = int(m.group(1))
            if num == expected:
                cur = {'num': num, 'text': m.group(2).strip(), 'images': [], 'key': None,
                       'pemb': '', 'options': {}, 'isian': False}
                questions.append(cur)
                expected = num + 1
                continue
        if cur is not None:
            cur['text'] += '\n' + ln
    for q in questions:
        rawq = q['text']
        q['key'] = kunci.get(q['num'])
        parts = re.split(r'(?:^|\n)\(?([A-Ea-e])[).]\s*', '\n' + re.sub(r'\n+', '\n', rawq))
        opts = {}
        if len(parts) >= 7:
            q['text'] = parts[0].strip()
            for i in range(1, len(parts) - 1, 2):
                L = parts[i].upper()
                if L not in opts:
                    opts[L] = re.sub(r'\s+', ' ', parts[i + 1]).strip()
        q['options'] = opts
        q['text'] = re.sub(r'[ \t]+', ' ', q['text']).strip()
        q['isian'] = len(q['options']) < 3
    draft = {'id': name, 'meta': META.get(name), 'questions': questions}
    with open(os.path.join(DRAFT, name + '.json'), 'w', encoding='utf-8') as f:
        json.dump(draft, f, ensure_ascii=False, indent=1)
    n_pg = sum(1 for q in questions if len(q['options']) >= 3)
    n_k = sum(1 for q in questions if q['key'])
    print(f'{name}: {len(questions)} soal | PG {n_pg} | kunci {n_k}')

def main():
    os.makedirs(DRAFT, exist_ok=True)
    for name in META:
        try:
            parse(name)
        except Exception as e:
            print('ERR', name, repr(e)[:120])

if __name__ == '__main__':
    main()

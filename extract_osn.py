# -*- coding: utf-8 -*-
"""Extraction OSN v2: sequential question split, font watermark filter, kunci, pembahasan, gambar."""
import os, re, json, sys
import pdfplumber

PDF_DIR, DRAFT_DIR = 'pdf', 'draft'
IMG_DIR, PAGE_DIR = 'img2', 'pages'
QNUM_RE = re.compile(r'^\s*(\d{1,3})\s*[.)]\s*(.*)$')
NOMOR_RE = re.compile(r'^\s*Nomor\s+(\d{1,3})\b\s*[.:]?\s*(.*)$', re.I)
OPT_RE = re.compile(r'^\(?([A-Ea-e])[).]\s*(.*)$')
KEY_RE = re.compile(r'(?:Jawab(?:an(?:nya)?)?\s*[:\-]|Jawabannya adalah|Kunci(?:\s*jawaban)?)\s*[:\-]?\s*\(?\s*([A-Ea-e])\s*\)?\s*(?![A-Za-z0-9])', re.I)
PEMB_RE = re.compile(r'(Alasan jawaban|Solusi|Pembahasan|Penyelesaian|Jawaban dan Pembahasan)\s*[:\-]?', re.I)

def page_filtered(page):
    """Return (page_to_use, singlefont_mode)."""
    groups = {}
    for c in page.chars:
        groups.setdefault(c['fontname'], []).append(c)
    bad = set()
    for fname, chs in groups.items():
        text = ''.join(ch['text'] for ch in chs)
        if ('https://' in text or 'https:/' in text.replace(' ', '')
                or len(re.findall(r'KWWS|defantri|calonguru', text)) >= 1
                or re.search(r'[A-Z]{12,}', text)):
            bad.add(fname)
    bad_chars = sum(len(groups[f]) for f in bad if f in groups)
    total = max(1, len(page.chars))
    if bad and bad_chars / total <= 0.5:
        f = page.filter(lambda obj: not (obj.get('object_type') == 'char' and obj.get('fontname') in bad))
        return f, False
    return page, True  # single-font: bersihkan teks saja

def clean_line(s):
    s = re.sub(r'\(cid:\d+\)', '', s)
    s = re.sub(r'KWWSVVLGRVQPPVPS|KWWSVVLGRVQPPVS', '', s)
    return s

def extract_package(path):
    name = os.path.splitext(os.path.basename(path))[0]
    img_out = os.path.join(IMG_DIR, name)
    page_out = os.path.join(PAGE_DIR, name)
    os.makedirs(img_out, exist_ok=True)
    os.makedirs(page_out, exist_ok=True)
    questions, cur = [], None
    expected = 1
    img_idx = 0
    txt_pages = []
    with pdfplumber.open(path) as pdf:
        for pi, page in enumerate(pdf.pages):
            try:
                f, single = page_filtered(page)
            except Exception:
                f, single = page, True
            text = clean_line(f.extract_text() or '')
            txt_pages.append(f'<<<PAGE {pi+1}>>>\n{text}')
            lines = [dict(top=l['top'], text=clean_line(l['text'])) for l in (f.extract_text_lines() or [])]
            lines.sort(key=lambda l: l['top'])
            imgs = []
            for im in sorted(page.images, key=lambda x: x['top']):
                try:
                    bbox = (im['x0'], page.height - im['bottom'], im['x1'], page.height - im['top'])
                    pil = page.crop(bbox).to_image(resolution=170).original
                    img_idx += 1
                    fn = f'{name}_p{pi+1}_{img_idx:04d}.png'
                    pil.save(os.path.join(img_out, fn))
                    imgs.append({'file': f'img2/{name}/{fn}', 'top': im['top']})
                except Exception:
                    pass
            try:
                page.to_image(resolution=150).save(os.path.join(page_out, f'{name}_p{pi+1}.png'))
            except Exception:
                pass
            for ln in lines:
                m = QNUM_RE.match(ln['text'])
                nm = NOMOR_RE.match(ln['text'])
                num = None
                rest = ln['text']
                if nm:
                    num = int(nm.group(1)); rest = nm.group(2)
                elif m:
                    num = int(m.group(1)); rest = m.group(2)
                if num is not None and (num == expected or num == 1):
                    cur = {'num': num, 'top': ln['top'], 'page': pi + 1,
                           'text': rest.strip(), 'images': [], 'key': None, 'pemb': ''}
                    questions.append(cur)
                    expected = num + 1
                    continue
                if cur is not None:
                    cur['text'] += '\n' + ln['text']
            for im in imgs:
                cands = [q for q in questions if q['page'] == pi + 1 and q['top'] < im['top']]
                tgt = cands[-1] if cands else (questions[-1] if questions else None)
                if tgt is not None:
                    tgt['images'].append(im['file'])

    for q in questions:
        raw = q['text']
        q.pop('top', None)
        q.pop('page', None)
        km = KEY_RE.search(raw)
        pemb = ''
        if km:
            q['key'] = km.group(1).upper()
            pemb = raw[km.end():].strip()
            raw = raw[:km.start()]
            km2 = KEY_RE.search(pemb)
            if km2:
                q['key'] = km2.group(1).upper()
                pemb = pemb[:km2.start()] + pemb[km2.end():]
        else:
            pm0 = PEMB_RE.search(raw)
            if pm0:
                pemb = raw[pm0.end():].strip()
                raw = raw[:pm0.start()]
                km2 = KEY_RE.search(pemb)
                if km2:
                    q['key'] = km2.group(1).upper()
                    pemb = pemb[:km2.start()] + pemb[km2.end():]
        q['pemb'] = re.sub(r'\s+', ' ', pemb)[:1500]
        q['isian'] = '<@isian>' in raw
        raw2 = re.sub(r'\s*\n\s*', '\n', raw)
        parts = re.split(r'(?:^|\n)\(?([A-Ea-e])[).]\s*', '\n' + raw2)
        if len(parts) < 7:
            parts = re.split(r'\(([A-Ea-e])\)\s+', raw)
        opts = {}
        if len(parts) >= 3:
            q['text'] = parts[0].strip()
            for i in range(1, len(parts) - 1, 2):
                letter = parts[i].upper()
                if letter not in opts:
                    opts[letter] = re.sub(r'\s+', ' ', parts[i + 1]).strip()
            q['options'] = opts
        else:
            q['options'] = {}
            q['text'] = re.sub(r'\s+', ' ', raw).strip()
    draft = {'id': name, 'questions': questions}
    with open(os.path.join(DRAFT_DIR, name + '.json'), 'w', encoding='utf-8') as fh:
        json.dump(draft, fh, ensure_ascii=False, indent=1)
    n_key = sum(1 for q in questions if q['key'])
    n_opts = sum(1 for q in questions if len(q['options']) >= 3)
    print(f'{name}: {len(questions)} soal | kunci: {n_key} | opsi>=3: {n_opts}')

def main():
    os.makedirs(DRAFT_DIR, exist_ok=True)
    os.makedirs(IMG_DIR, exist_ok=True)
    os.makedirs(PAGE_DIR, exist_ok=True)
    only = sys.argv[1:] if len(sys.argv) > 1 else None
    for f in sorted(os.listdir(PDF_DIR)):
        if not f.lower().endswith('.pdf'):
            continue
        if only and not any(o in f for o in only):
            continue
        try:
            extract_package(os.path.join(PDF_DIR, f))
        except Exception as e:
            print('ERR', f, repr(e)[:120])

if __name__ == '__main__':
    main()

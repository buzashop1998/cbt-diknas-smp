# -*- coding: utf-8 -*-
"""Extraction v2: clean text (drop watermark font), page renders, image association, draft JSON."""
import os, re, json
import pdfplumber

PDF_DIR, TXT_DIR, DRAFT_DIR = 'pdf', 'txt2', 'draft'
IMG_DIR, PAGE_DIR = 'img2', 'pages'

QNUM_RE = re.compile(r'^\s*(\d{1,2})\.\s*')

def is_watermark(obj):
    return obj.get('object_type') == 'char' and 'ArialMT' in obj.get('fontname', '') and obj.get('size', 0) > 20

def extract_package(path):
    name = os.path.splitext(os.path.basename(path))[0]
    img_out = os.path.join(IMG_DIR, name)
    page_out = os.path.join(PAGE_DIR, name)
    os.makedirs(img_out, exist_ok=True)
    os.makedirs(page_out, exist_ok=True)

    questions = []          # list of dicts
    cur = None
    open_questions = []
    img_idx = 0
    txt_pages = []

    with pdfplumber.open(path) as pdf:
        for pi, page in enumerate(pdf.pages):
            f = page.filter(lambda obj: not is_watermark(obj))
            text = f.extract_text() or ''
            txt_pages.append(f'<<<PAGE {pi+1}>>>\n{text}')
            lines = f.extract_text_lines() or []
            lines.sort(key=lambda l: l['top'])
            # embedded images on this page, sorted top-to-bottom
            imgs = sorted(page.images, key=lambda im: im['top'])
            page_imgs = []
            for im in imgs:
                try:
                    bbox = (im['x0'], page.height - im['bottom'], im['x1'], page.height - im['top'])
                    pil = page.crop(bbox).to_image(resolution=180).original
                    img_idx += 1
                    fn = f'{name}_p{pi+1}_{img_idx:04d}.png'
                    pil.save(os.path.join(img_out, fn))
                    page_imgs.append({'file': f'img2/{name}/{fn}', 'top': im['top']})
                except Exception:
                    pass
            # render full page for reference
            try:
                page.to_image(resolution=150).save(os.path.join(page_out, f'{name}_p{pi+1}.png'))
            except Exception:
                pass

            # walk lines, split questions; attach images to the question active at their position
            for ln in lines:
                m = QNUM_RE.match(ln['text'])
                if m:
                    num = int(m.group(1))
                    cur = {'num': num, 'top': ln['top'], 'page': pi + 1,
                           'text': QNUM_RE.sub('', ln['text']).strip(), 'images': []}
                    questions.append(cur)
                elif cur is not None:
                    cur['text'] += '\n' + ln['text'].strip()
            # attach images: to the last question whose start is above the image (same page), else last question overall
            for im in page_imgs:
                cands = [q for q in questions if q['page'] == pi + 1 and q['top'] < im['top']]
                tgt = cands[-1] if cands else (questions[-1] if questions else None)
                if tgt is not None:
                    tgt['images'].append(im['file'])

    txt_path = os.path.join(TXT_DIR, name + '.txt')
    with open(txt_path, 'w', encoding='utf-8') as fh:
        fh.write('\n\n'.join(txt_pages))

    # parse options / isian per question
    for q in questions:
        q['isian'] = '<@isian>' in q['text']
        opts = {}
        text_wo_img = q['text'].replace('[img]', ' ')
        parts = re.split(r'\n?\(?([A-Ea-e])\)\s*', '\n' + text_wo_img)
        # parts: [lead, 'A', opttext, 'B', opttext, ...]
        if len(parts) >= 3:
            q['text'] = parts[0].strip()
            for i in range(1, len(parts) - 1, 2):
                letter = parts[i].upper()
                if letter in 'ABCDE' and letter not in opts:
                    opts[letter] = parts[i + 1].strip()
        q['options'] = opts
        q['text'] = q['text'].replace('<@isian>', '').strip()
        q['text'] = re.sub(r'\s+', ' ', q['text'])
        for k in q['options']:
            q['options'][k] = re.sub(r'\s+', ' ', q['options'][k])

    draft = {'id': name, 'questions': questions}
    with open(os.path.join(DRAFT_DIR, name + '.json'), 'w', encoding='utf-8') as fh:
        json.dump(draft, fh, ensure_ascii=False, indent=1)
    n_opts = sum(1 for q in questions if len(q['options']) >= 3)
    n_isian = sum(1 for q in questions if q['isian'])
    n_imgs = sum(len(q['images']) for q in questions)
    print(f'{name}: {len(questions)} soal | pg>=3opsi: {n_opts} | isian: {n_isian} | img ter-attach: {n_imgs}')

def main():
    os.makedirs(TXT_DIR, exist_ok=True)
    os.makedirs(DRAFT_DIR, exist_ok=True)
    os.makedirs(IMG_DIR, exist_ok=True)
    os.makedirs(PAGE_DIR, exist_ok=True)
    for f in sorted(os.listdir(PDF_DIR)):
        if not f.lower().endswith('.pdf'):
            continue
        try:
            extract_package(os.path.join(PDF_DIR, f))
        except Exception as e:
            print('ERR', f, repr(e)[:150])

if __name__ == '__main__':
    main()

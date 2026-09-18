# -*- coding: utf-8 -*-
"""Retry download via alternate endpoints."""
import os, re, requests

UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124 Safari/537.36'}

FAILED_PDF = {
    '2020-ipa-kabkota':   '1l-HxLqnqUM0ktEtGxDNaTV0RWXVVNY1y',
    '2025-ips-final':     '1PU6LvaObUAJsHFZiWEozcjdejC55rw8w',
    '2024-ips-kabkota':   '1777gQAJ857Cyb6gRsoPSSi6cRFAyI45j',
    '2024-ips-prov':      '1THD2fs_z3KN8CIbeciW0EfReCcF-GgqM',
    '2024-ips-nas':       '1gxjC7U9fMYW-8g9jH0KEDAmpL_k-YdrG',
    '2023-ips-kabkota':   '1Wsz6rCWBEni_BghomVWPBV7Jx7_bpcGF',
    '2023-ips-prov':      '1ZbjP42nX7UXrU_bQ5Mx43nUc7Rg2hIC0',
    '2023-ips-nas':       '1jRpqwikE2a5biMP5kzSfRohut1YHzkGA',
    '2022-ips-kabkota-a': '1572xJlAz0WpnV0DlsdA0EdycVUvulFN7',
    '2022-ips-kabkota-b': '1bdqr9fV9YN11J4g-E4u5OpNOsYcBE6Tt',
    '2022-ips-nas':       '1F3c7x7-nS3arx0foSsAmZIcG_20X1PZH',
    '2020-ips-kabkota':   '1iGkPHGDt0tdYWF_oeQaFEzI_Vr4CpPIf',
}

DOCS = {
    '2022-ipa-kabkota':   ('doc',   '15SwpK1i6ltebP7oqNQxBzZ0Xeu4oQYRRSBLtiYWEw2c'),
    '2022-ipa-kunci-a':   ('doc',   '1ccERUx76ezmpP4cx9RxwjPr18fC1VHLnpOGLD98-lN4'),
    '2022-ipa-kunci-b':   ('doc',   '1fdSpv3cEUeRI5V514EqPU_a4xIHwNuBdeY1xP4d41iE'),
    '2022-ipa-nas-a':     ('doc',   '1tXrGHGIzzqAa1_0hHxP6FaQlO2RqEnpv-RlA4xEXQ84'),
    '2022-ipa-nas-b':     ('doc',   '1U59oAwS_hv7Ngl4iytnZlncwEeVZAnwg9tztsSGWh_Y'),
    '2022-ipa-kunci-nas': ('sheet', '1dxU7xLIIXV6PlFq79mGq31Njb_YA_-A8PkIn_RRx6qU'),
}

def dl_pdf(name, fid):
    out = os.path.join('pdf', name + '.pdf')
    if os.path.exists(out) and os.path.getsize(out) > 20000:
        print('SKIP', name); return
    url = f'https://drive.usercontent.google.com/download?id={fid}&export=download&confirm=t'
    r = requests.get(url, headers=UA, timeout=120)
    if r.content[:4] == b'%PDF':
        open(out, 'wb').write(r.content); print('OK  ', name, len(r.content)); return
    # perlukan token confirm dari form html
    m = re.search(r'name="uuid" value="([^"]+)"', r.text)
    m2 = re.search(r'name="at" value="([^"]+)"', r.text)
    if m:
        params = {'id': fid, 'export': 'download', 'confirm': 't', 'uuid': m.group(1)}
        if m2: params['at'] = m2.group(1)
        r2 = requests.get('https://drive.usercontent.google.com/download', params=params, headers=UA, timeout=180)
        if r2.content[:4] == b'%PDF':
            open(out, 'wb').write(r2.content); print('OK2 ', name, len(r2.content)); return
    print('FAIL', name, r.status_code, len(r.content), r.text[:80].replace('\n', ' '))

def strip_html(html):
    html = re.sub(r'<script.*?</script>', ' ', html, flags=re.S)
    html = re.sub(r'<style.*?</style>', ' ', html, flags=re.S)
    html = re.sub(r'<br[^>]*>', '\n', html)
    html = re.sub(r'</(p|div|tr|h\d)>', '\n', html)
    html = re.sub(r'</td>', ' | ', html)
    html = re.sub(r'<[^>]+>', '', html)
    import html as H
    return H.unescape(html)

def dl_doc(name, kind, did):
    out = os.path.join('src', name + '.txt' if kind == 'doc' else '.csv')
    if os.path.exists(out) and os.path.getsize(out) > 200:
        print('SKIP', name); return
    if kind == 'doc':
        urls = [f'https://docs.google.com/document/d/{did}/export?format=txt',
                f'https://docs.google.com/document/d/{did}/mobilebasic']
    else:
        urls = [f'https://docs.google.com/spreadsheets/d/{did}/export?format=csv',
                f'https://docs.google.com/spreadsheets/d/{did}/htmlview']
    for u in urls:
        r = requests.get(u, headers=UA, timeout=120)
        if r.status_code == 200 and len(r.content) > 500 and b'accounts.google.com' not in r.content[:2000]:
            if 'mobilebasic' in u or 'htmlview' in u:
                txt = strip_html(r.text)
                if len(txt) < 500: continue
                open(out, 'w', encoding='utf-8').write(txt)
            else:
                open(out, 'wb').write(r.content)
            print('OK  ', name, len(r.content), '<-', u.split("/")[-1][:30]); return
    print('FAIL', name, r.status_code if 'r' in dir() else '-', len(r.content) if 'r' in dir() else 0)

def main():
    for n, fid in FAILED_PDF.items():
        try: dl_pdf(n, fid)
        except Exception as e: print('ERR ', n, str(e)[:100])
    for n, (k, d) in DOCS.items():
        try: dl_doc(n, k, d)
        except Exception as e: print('ERR ', n, str(e)[:100])

if __name__ == '__main__':
    main()

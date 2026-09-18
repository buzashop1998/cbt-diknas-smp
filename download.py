# -*- coding: utf-8 -*-
"""Download semua soal OSN SMP/MTs 2020-2025 (PDF Drive + Google Docs/Sheets export)."""
import os, sys, csv, io
import requests
import gdown

PDFS = {
    # IPA
    '2025-ipa-kabkota':      '1P1sDuWg0XSTSdBY9B9zNZDF6_FD7NTes',
    '2025-ipa-prov':         '17XGloH_DFgbEJv1LkZEk6p2tq0VYu1uu',
    '2025-ipa-semifinal':    '1EwSrdWldbNd2KdscClJ5U7Ruh1RSPBkS',
    '2025-ipa-final':        '1EwZ8MpwN07z1B9OLQ-tiQ1g0BiRbljpv',
    '2024-ipa-kabkota':      '1zsxIufn83XalWrS9upis0uVTNToIwlT4',
    '2024-ipa-prov':         '1TIR7-INamLIqGIfN_aod4K2dTFQoKdEx',
    '2024-ipa-nas-tulis':    '1BI7kQNbT52B2QF5ETRw3PMXtc_DvLBiM',
    '2024-ipa-nas-praktikum':'1uEIPOChwvc_XkB5v7n8ICCv1pfMdRRzS',
    '2023-ipa-kabkota':      '1K_PWweZUmbz8IoNakn09ufQJTLCh4uQx',
    '2023-ipa-prov':         '1aDoShKqKX9Cnxc_qQebqPkQyZGSqWuIa',
    '2023-ipa-nas-fisika':   '1E4fO8aQPVmmKtial087x1zACcGHPU1Wp',
    '2023-ipa-nas-biologi':  '1MIDCG4-cFHARYfhEzKJc-AZtq1koi84H',
    '2020-ipa-kabkota':      '1l-HxLqnqUM0ktEtGxDNaTV0RWXVVNY1y',
    # Matematika
    '2025-mat-kabkota':      '1igDr7Vl-F1CerjiF2wVUk8Jt14VoAeTm',
    '2025-mat-prov':         '1Bv_PIKc0Ep-XWcC3n3LaPTaAbV6P1phm',
    '2025-mat-semifinal':    '1sfdHDHKIkLfJPRzaEbvff9FsONACYuER',
    '2025-mat-final':        '1EwHxyfIasyup0ID1hlsJ-6PCb7bSlLib',
    '2024-mat-kabkota':      '147RwcO7PlAzohTwj4GQb_N4g9kCk33jp',
    '2024-mat-pembahasan':   '1GH4s10PgPO43OQjn8OPkn3ukcfQlphVy',
    '2024-mat-prov':         '1hC7nO_Cd-7YRnHwO22NTLXf_M_9Se9m_',
    '2024-mat-nas':          '1OzWTXGNx0AxkXMjlG3qALEfkNHhRPB4q',
    '2023-mat-kabkota':      '1mLuc9-8yrmvu_XC2lHTMs9FQkbR4BZyA',
    '2023-mat-pembahasan-a': '1apUEkaeD80FTiiFf4pkVwzpVBLwo7wVY',
    '2023-mat-pembahasan-b': '13iE675nhmxPmjpJTgt7TTHC-Ou0Yc0Um',
    '2023-mat-pembahasan-prov': '1Ow5BQWBttcUS42YlTxx1qLNA2CUP1cNh',
    '2022-mat-pembahasan':   '1zTJ7waWRrDaXH14kodCZv8xUju4qJnGe',
    '2021-mat-pembahasan':   '1Ut6vUmxT3KHZ0j6TYvGNoJ5y_FtE0IGj',
    '2020-mat-kabkota':      '1YfM_f3ssqtwRRGBsFABcyg8BIhUZgQVs',
    '2020-mat-pembahasan-a': '1UosxO5EDHdbutyEcTquK7k5d9rWLojMU',
    '2020-mat-pembahasan-b': '1ioQJGOLKhOG65XdbrC62fb4xvDK0QGAq',
    '2020-mat-pembahasan-nas': '1984yrwm3bqtZ5QBAWUYZ-2riVNOspoB_',
    # IPS
    '2025-ips-kabkota':      '1yFo6HRtXah0KKYMjyw35bxez9P3W-8Vw',
    '2025-ips-prov':         '1Bv_PIKc0Ep-XWcC3n3LaPTaAbV6P1phm',
    '2025-ips-semifinal':    '1V6uRaYwlTSqiuVwe68_h28HUjnnGsrq8',
    '2025-ips-final':        '1PU6LvaObUAJsHFZiWEozcjdejC55rw8w',
    '2024-ips-kabkota':      '1777gQAJ857Cyb6gRsoPSSi6cRFAyI45j',
    '2024-ips-prov':         '1THD2fs_z3KN8CIbeciW0EfReCcF-GgqM',
    '2024-ips-nas':          '1gxjC7U9fMYW-8g9jH0KEDAmpL_k-YdrG',
    '2023-ips-kabkota':      '1Wsz6rCWBEni_BghomVWPBV7Jx7_bpcGF',
    '2023-ips-prov':         '1ZbjP42nX7UXrU_bQ5Mx43nUc7Rg2hIC0',
    '2023-ips-nas':          '1jRpqwikE2a5biMP5kzSfRohut1YHzkGA',
    '2022-ips-kabkota-a':    '1572xJlAz0WpnV0DlsdA0EdycVUvulFN7',
    '2022-ips-kabkota-b':    '1bdqr9fV9YN11J4g-E4u5OpNOsYcBE6Tt',
    '2022-ips-nas':          '1F3c7x7-nS3arx0foSsAmZIcG_20X1PZH',
    '2020-ips-kabkota':      '1iGkPHGDt0tdYWF_oeQaFEzI_Vr4CpPIf',
}

# Google Docs / Sheets: name -> (type, id)
DOCS = {
    '2022-ipa-kabkota':      ('doc', '15SwpK1i6ltebP7oqNQxBzZ0Xeu4oQYRRSBLtiYWEw2c'),
    '2022-ipa-kunci-a':      ('doc', '1ccERUx76ezmpP4cx9RxwjPr18fC1VHLnpOGLD98-lN4'),
    '2022-ipa-kunci-b':      ('doc', '1fdSpv3cEUeRI5V514EqPU_a4xIHwNuBdeY1xP4d41iE'),
    '2022-ipa-nas-a':        ('doc', '1tXrGHGIzzqAa1_0hHxP6FaQlO2RqEnpv-RlA4xEXQ84'),
    '2022-ipa-nas-b':        ('doc', '1U59oAwS_hv7Ngl4iytnZlncwEeVZAnwg9tztsSGWh_Y'),
    '2022-ipa-kunci-nas':    ('sheet', '1dxU7xLIIXV6PlFq79mGq31Njb_YA_-A8PkIn_RRx6qU'),
    '2021-ipa-kabkota-a':    ('doc', '164B4O4aHH23NI93Tf2EteNsTiwXDbkQq'),
    '2021-ipa-kabkota-b':    ('doc', '1VR4rucmoDpcRt8t71G3HLQT5p4H_10FK'),
    '2021-ipa-kabkota-c':    ('doc', '19nFY7Wvu3Jbd_xKv_neyxdxjvkJBYVef'),
    '2021-ipa-prov-a':       ('doc', '14qKKQyUXROgvsOSPYhGzm9T6A1v7GjVU'),
    '2021-ipa-prov-b':       ('doc', '1pJiazrrXXETDsfTwliU6jhOoMpT1S9tf'),
    '2021-ipa-prov-c':       ('doc', '1UVUYBTkCTmqvwBrZtnxS73Mz7yBi0jtd'),
    '2021-ipa-nas-a':        ('doc', '1sDmu-msrEGquc9n5Jx571wdTD3pBEbk8'),
    '2021-ipa-nas-b':        ('doc', '1D5aNG7H218OuQDJ6bNepZhF_m-Kxrw4l'),
    '2021-ipa-nas-c':        ('doc', '1E1zHNB1mNxIufz80zohhFH3yHZreoNPA'),
    '2021-ips-kabkota-a':    ('doc', '1V1t0IHmOHSfdGVBatnzg-mP-HUtKkiFC'),
    '2021-ips-kabkota-b':    ('doc', '1BUoaNTzTuGlkAIZ1En7239wqrBQOJegl'),
    '2021-ips-kabkota-c':    ('doc', '1AcuoKhElAT96Py4kCIPQXddMP985VSDl'),
    '2021-ips-prov-a':       ('doc', '1Vjv-T-kWyU6VvJ_FyyIncgcYJVGqxB1w'),
    '2021-ips-prov-b':       ('doc', '1c9GtKyHbEVc0uDnJqcsyxzKuY4uJ--MJ'),
    '2021-ips-prov-c':       ('doc', '1JdghRulcZc1hJU6Y-C1TMGX5CWMVy_eL'),
    '2021-ips-nas-a':        ('doc', '1MkG6cTptbetmFWgao9rnfCO6Y_3Rxqnl'),
    '2021-ips-nas-b':        ('doc', '1YGajL5oUap-GSBkcSuhcfdLx6AUwMPjG'),
    '2021-ips-nas-c':        ('doc', '1jOl_0_e0ZxQbjWB6ivyQAl1S7EUw69_q'),
}

def fetch_doc(name, kind, did):
    out = os.path.join('src', name + '.txt' if kind == 'doc' else '.csv')
    if os.path.exists(out) and os.path.getsize(out) > 200:
        print('SKIP', name); return
    url = (f'https://docs.google.com/document/d/{did}/export?format=txt' if kind == 'doc'
           else f'https://docs.google.com/spreadsheets/d/{did}/export?format=csv')
    r = requests.get(url, timeout=60)
    if r.status_code == 200 and len(r.content) > 200 and b'<html' not in r.content[:400]:
        with open(out, 'wb') as f: f.write(r.content)
        print('OK  ', name, len(r.content))
    else:
        print('BAD ', name, r.status_code, len(r.content))

def main():
    os.makedirs('pdf', exist_ok=True)
    os.makedirs('src', exist_ok=True)
    only = sys.argv[1] if len(sys.argv) > 1 else None
    for name, fid in PDFS.items():
        if only and only not in name: continue
        out = os.path.join('pdf', name + '.pdf')
        if os.path.exists(out) and os.path.getsize(out) > 20000:
            print('SKIP', name); continue
        try:
            gdown.download(f'https://drive.google.com/uc?id={fid}', out, quiet=True)
            size = os.path.getsize(out) if os.path.exists(out) else 0
            head = open(out, 'rb').read(5) if size else b''
            print(('OK ' if head.startswith(b'%PDF') else 'BAD'), name, size)
        except Exception as e:
            print('ERR ', name, str(e)[:100])
    for name, (kind, did) in DOCS.items():
        if only and only not in name: continue
        try:
            fetch_doc(name, kind, did)
        except Exception as e:
            print('ERR ', name, str(e)[:100])

if __name__ == '__main__':
    main()

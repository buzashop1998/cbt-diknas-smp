# -*- coding: utf-8 -*-
from build_data import build

KEYS = {1:'B',2:'B',4:'B',5:'A',6:'C',7:'C',8:'C',9:'B',10:'D',11:'B',12:'A',13:'C',14:'B',15:'C'}
PEMB = {
    1: 'Pembentukan rantai peptida tanpa enzim/DNA menunjukkan reaksi kimia spontan terjadi di laut purba.',
    2: 'Cahaya tinggi di danau terbuka mendukung fotosintesis -> keanekaragaman lebih tinggi.',
    4: 'Perbedaan jenis ikan antar danau = keanekaragaman tingkat spesies.',
    5: 'Perubahan warna kulit populasi menyesuaikan habitat = adaptasi fisiologis.',
    6: 'Gen resisten diwarisi; individu adaptif bertahan (seleksi alam), bukan mutasi serempak.',
    7: 'Barcode DNA membedakan spesies yang mirip secara morfologis.',
    8: 'Stomata sedikit, kutikula tebal, akar panjang = adaptasi xerofit (kering).',
    9: 'Floem mengangkut hasil fotosintesis; kerusakan floem menghambatnya.',
    10: 'Rongga aerenkim pada tangkai hidrofit memudahkan pertukaran gas.',
    11: 'Salinitas tinggi mengganggu pertukaran gas dan pengangkutan air pada eceng gondok.',
    12: 'Salinitas memicu penebalan dinding sel korteks akar untuk menahan masuknya garam.',
    13: 'Nucleolus pembentuk ribosom; rusak -> translasi terhambat (ribosom kurang).',
    14: 'Mikrotubulus spindle diperlukan anafase; dihambat -> sel tertahan metafase.',
    15: 'Pertumbuhan 20%/bulan: 144 -> 172,8 -> 207,4; pembulatan sesuai kunci = 206.',
}

build('2025-ipa-prov',
    {'title': 'OSN IPA SMP 2025 - Provinsi', 'year': 2025,
     'mapel': 'IPA', 'tingkat': 'Provinsi', 'duration': 120},
    include=sorted(KEYS),
    draft='2025-ipa-prov',
    fixes={n: dict([('a', k)] + ([('pemb', PEMB[n])] if n in PEMB else [])) for n, k in KEYS.items()},
)

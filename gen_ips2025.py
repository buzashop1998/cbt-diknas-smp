# -*- coding: utf-8 -*-
from build_data import build

KEYS = {3:'C',5:'A',7:'C',9:'A',11:'A',13:'A',16:'C',17:'D',18:'B',19:'C',23:'B',24:'C',
        28:'D',29:'B',31:'B',33:'C',34:'C',35:'A',36:'B',37:'B',38:'A',39:'B',41:'A',
        42:'A',44:'B',46:'C',47:'A',49:'B',50:'B'}
PEMB = {
    3: 'Cendana (Santalum) khas NTT, wilayah di antara Garis Wallace dan Weber.',
    7: 'Penyebab utama deforestasi: konversi hutan menjadi lahan perkebunan.',
    9: 'Abrasi memutus mata pencaharian nelayan -> adaptasi menjadi pedagang cenderak mata.',
    11: 'Akar mangrove menahan gelombang sehingga melindungi pesisir (A-B benar dan berkaitan).',
    18: 'Faktor eksternal perundungan: lemahnya sanksi/kebijakan pemerintah.',
    28: 'Dampak mendasar pariwisata: perubahan orientasi pola hidup masyarakat Baduy Dalam.',
    31: 'Proto-Melayu & Deutro-Melayu mendukung teori Yunan (datang dari Yunan/Asia Tenggara darat).',
    33: 'Dakwah Walisongo lewat seni: Sunan Bonang menggubah tembang.',
    34: 'Rute barat dipilih untuk menghindari Portugis yang menguasai Malaka.',
    35: 'Kereta api 1867 dibangun untuk mengangkut hasil bumi tanam paksa.',
    36: 'Dampak positif cultuurstelsel: mengenal tanaman industri dan pengolahannya.',
    37: 'Organisasi pergerakan didirikan golongan terpelajar (penerima pendidikan Barat).',
    38: 'KMB 1949 menghasilkan penyerahan kedaulatan oleh Belanda.',
    39: 'Teknik pengecoran logam yang hilang = a cire perdue.',
    41: 'Renville memperkecil wilayah RI (garis Van Mook).',
    42: 'Trias van Deventer: edukasi, irigasi, emigrasi (Politik Etis).',
    44: 'Sosialisme menginspirasi perjuangan kelas dan keadilan sosial.',
    47: 'Danantara membawahi BUMN besar: Bank Mandiri, BNI, BRI, dll.',
    50: 'Penawaran nyaris tetap saat permintaan melonjak -> penawaran inelastis.',
}

build('2025-ips-kabkota',
    {'title': 'OSN IPS SMP 2025 - Kabupaten/Kota', 'year': 2025,
     'mapel': 'IPS', 'tingkat': 'Kabupaten/Kota', 'duration': 120},
    include=sorted(KEYS),
    draft='2025-ips-kabkota',
    fixes={n: dict([('a', k)] + ([('pemb', PEMB[n])] if n in PEMB else [])) for n, k in KEYS.items()},
)

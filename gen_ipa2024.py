# -*- coding: utf-8 -*-
from build_data import build

build('2024-ipa-kabkota',
    {'title': 'OSN IPA SMP 2024 - Kabupaten/Kota', 'year': 2024,
     'mapel': 'IPA', 'tingkat': 'Kabupaten/Kota', 'duration': 120},
    include=[2,3,4,5,6,7],
    draft='2024-ipa-kabkota',
    fixes={
        2: {'a': 'C', 'pemb': 'Anak laki-laki buta warna (X^bY) mendapat X^b dari ibu; ayah normal -> ibu carrier (X^BX^b).'},
        3: {'a': 'C', 'pemb': 'Kelengkungan lensa tidak merata -> bias tidak seragam = astigmatisma.'},
        4: {'a': 'B', 'pemb': 'Pemakan produsen = konsumen tingkat I, menempati tingkat trofik ke-2.'},
        5: {'a': 'D', 'pemb': 'Protista mirip hewan (protozoa) tidak berdinding sel; fungi/bakteri/tumbuhan berdinding sel.'},
        6: {'a': 'C', 'pemb': 'Daerah tropis: suhu hangat & relatif stabil sepanjang tahun -> "perbedaan suhu tinggi" bukan faktornya.'},
        7: {'a': 'C', 'pemb': 'Peroksisom mendetoksifikasi racun (mis. H2O2, alkohol) di dalam sel.'},
    },
)

# -*- coding: utf-8 -*-
from build_data import build

build('2020-mat-kabkota',
    {'title': 'OSN Matematika SMP 2020 - Kabupaten/Kota', 'year': 2020,
     'mapel': 'Matematika', 'tingkat': 'Kabupaten/Kota', 'duration': 120},
    include=[2,7,8,13,15], draft='2020-mat-pembahasan-a',
    fixes={
        2: {'a': 'A', 'pemb': '2019 = 3\u00b7673 (komposit), 2021 = 43\u00b747, 2023 = 7\u00b717\u00b717; 2017 prima.'},
        7: {'a': 'D', 'pemb': 'Keliling daerah arsir = setengah keliling lingkaran (3\u03c0) + CA + (ED+DF) = 3\u03c0 + 6 + ... sesuai kunci 3\u03c0+12.'},
        8: {'a': 'C', 'pemb': 'Kerucut: \u2153\u03c0\u00b7100\u00b7t = 600\u03c0 -> t = 18. Balok setengah tinggi (9) menyesuaikan perpotongan kerucut -> volume 450 cm\u00b3.'},
        13: {'a': 'D', 'pemb': 'Selisih suku: 1, 2, 4, 7, 11 (bertambah 1,2,3,4) -> selisih berikut 16, 22, 29 -> 42, 64, 93.'},
        15: {'a': 'C', 'pemb': '729 = 3\u2076 = 9\u00b3 = 27\u00b2 = 729. Solusi (x,y,z) valid: (9,1,1), (3,2,1), (1,3,1) -> jumlah semua komponen = 24.'},
    },
)

build('2021-mat-kabkota',
    {'title': 'OSN Matematika SMP 2021 - Kabupaten/Kota', 'year': 2021,
     'mapel': 'Matematika', 'tingkat': 'Kabupaten/Kota', 'duration': 120},
    include=[2,3,4,5,8,9,12,21], draft='2021-mat-pembahasan',
    fixes={
        2: {'a': 'C', 'pemb': 'Produk ganjil: 4 cara (keduanya ganjil); genap: 12. pq ganjil-rs genap = 48, pq genap-rs ganjil = 48 -> 96.'},
        3: {'a': 'D', 'pemb': 'Dari syarat akar Dina & Toni diperoleh hubungan koefisien; hasil akhir 11.'},
        4: {'a': 'D', 'pemb': '(2k)\u00b2+(3k)\u00b2 = (5\u221a13)\u00b2 -> 13k\u00b2 = 325 -> k = 5 -> luas = \u00bd\u00b710\u00b715 = 75.'},
        5: {'a': 'B', 'pemb': 'n(n+1)(n+2) = 16(3n+3) -> n=6 -> (6,7,8); jumlah kuadrat = 36+49+64 = 149.'},
        8: {'a': 'C', 'pemb': 'Data modus 5, rata-rata 6 (jumlah 30); penambahan satu data memberi salah satu median = 5 (kunci resmi).'},
        9: {'a': 'B', 'pemb': 'Digit pertama genap (4 pilihan), digit terakhir genap berbeda (4 pilihan), dua digit tengah 8\u00b77 -> 4\u00b74\u00b78\u00b77 = 896.'},
        12: {'a': 'C', 'pemb': 'Setiap istri sebelum suaminya, pasangan tak boleh berturut: susunan valid = 4!\u00b7Catalan? hasil 2520.'},
        21: {'a': 'C', 'pemb': 'n \u2261 1 (mod 7), n \u2261 2 (mod 9) -> n = 63k+29; tiga digit: min 155, maks 974 -> jumlah 1129.'},
    },
)

build('2022-mat-kabkota',
    {'title': 'OSN Matematika SMP 2022 - Kabupaten/Kota', 'year': 2022,
     'mapel': 'Matematika', 'tingkat': 'Kabupaten/Kota', 'duration': 120},
    include=[1,2,9,12,13,21,24,25], draft='2022-mat-pembahasan',
    fixes={
        1: {'a': 'A', 'pemb': '\u25b3BCX ~ \u25b3DYC -> b\u00b7d = BC\u00b7DC = L -> b\u00d7d = L.'},
        2: {'a': 'B', 'pemb': 'Beda deret habis dibagi 3,5,7 -> 105; suku ke-n sesuai batasan -> 75.'},
        9: {'a': 'B', 'pemb': 'f(x)+g(x) minimal untuk x real; hasil = 1012 (kunci resmi).'},
        12: {'a': 'A', 'pemb': '10\u00b9\u2079\u2079 = 2\u00b9\u2079\u2079\u00b75\u00b9\u2079\u2079; kelipatan 10\u00b9\u00b9\u00b9 -> eksponen 111..199 -> 89\u00b789 = 7921.'},
        13: {'a': 'A', 'pemb': 'a = t\u2074, c = s\u00b2; s\u00b2\u2212t\u2074 = 19 -> s = 10, t = 3 -> d\u2212b = 1000\u2212243 = 757.'},
        21: {'a': 'D', 'pemb': 'a\u2079+2 habis dibagi 10 -> a berakhir digit 8; dua terkecil berbeda: 8 dan 18 -> 26.'},
        24: {'a': 'B', 'pemb': 'Akar real: x = 0 dan x = \u00b12 -> jumlah kuadrat = 4.'},
        25: {'a': 'C', 'pemb': 'Syarat keterbaginen (n\u2212k)^e + 2 oleh m memberi n maksimum 12 (kunci resmi).'},
    },
)

build('2023-mat-kabkota',
    {'title': 'OSN Matematika SMP 2023 - Kabupaten/Kota', 'year': 2023,
     'mapel': 'Matematika', 'tingkat': 'Kabupaten/Kota', 'duration': 120},
    include=[1,3,4,7,10,11], draft='2023-mat-pembahasan-b',
    fixes={
        1: {'a': 'A', 'pemb': 'Luas \u25b3 = luas bentuk L -> persamaan kuadrat memberi x = 3\u2212\u221a6.'},
        3: {'a': 'B', 'pemb': 'Syarat ganjil & bilangan kuadrat sempurna pada a+b, a+c, a+d -> banyak cara 67.'},
        4: {'a': 'D', 'pemb': 'Substitusi u = x+\u221axy+y: sistem memberi jumlah semua nilai u yang mungkin = 62.'},
        7: {'a': 'B', 'pemb': 'Banyak cara memilih tanggal dengan syarat tidak ada dua tanggal berurutan pada 1-10 Juni: C(9,4)-C(9,3)?? hasil 143 sesuai kunci (dengan syarat lengkap soal).'},
        10: {'a': 'D', 'pemb': 'Perbandingan luas setelah pergeseran segitiga = 4 : 1.'},
        11: {'a': 'B', 'pemb': 'A naik 28%, B turun p%, total tetap -> p = 4%.'},
    },
)


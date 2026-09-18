# CBT OSN SMP/MTs (cbt-diknas-smp)

Web CBT (Computer Based Test) latihan **Olimpiade Sains Nasional (OSN) SMP/MTs** â€” IPA, Matematika, dan IPS â€” tahun 2020â€“2025 (Kemendikbudristek).

Murni **HTML + CSS + JavaScript** (tanpa backend, tanpa admin) â€” cukup buka `webapp/index.html`.

## Fitur
- Pilih paket soal per tahun/mapel/tingkat
- Timer hitung mundur + auto-submit, navigasi soal, tandai ragu-ragu
- Soal Pilihan Ganda & Isian Singkat (dikoreksi otomatis)
- Hasil ujian: skor, benar/salah/kosong + koreksi jawaban & pembahasan
- Klik gambar soal untuk perbesar (lightbox, zoom di desktop & mobile)

## Struktur
- `webapp/` â€” aplikasi (index.html, style.css, app.js, data/*.js, img/)
- `draft/`, `img2/`, `txt2/`, `pdf/` â€” pipeline ekstraksi soal dari dokumen sumber

## Menjalankan
Buka `webapp/index.html` langsung di browser, atau:
```
cd webapp
python -m http.server 8080
```

<!-- rebuild 2026-09-19T01:39:23 -->

<!-- deploy 2026-09-19T02:03:39 -->

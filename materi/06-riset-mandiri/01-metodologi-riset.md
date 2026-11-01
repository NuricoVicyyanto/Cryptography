# 🔬 Metodologi Riset Kriptografi

Riset kriptografi bukan sekadar membuat program yang "jalan". Ia membutuhkan pertanyaan yang jelas, model ancaman yang eksplisit, eksperimen yang bisa diulang, dan kesimpulan yang jujur tentang batasannya. Dokumen ini adalah kerangka kerja untuk melakukan riset mandiri yang layak dipublikasikan.

---

## 1. Memilih Pertanyaan Riset

Pertanyaan yang baik memenuhi empat syarat:

1. **Spesifik.** "Apakah BLAKE3 lebih cepat dari SHA-256 pada CPU tanpa AES-NI untuk data 10 MB" lebih baik daripada "apakah BLAKE3 bagus".
2. **Terukur.** Ada metrik yang jelas: waktu, memori, ukuran bukti, tingkat keberhasilan serangan.
3. **Terbatas.** Bisa diselesaikan dalam waktu yang tersedia dengan sumber daya yang ada.
4. **Bernilai.** Menjawab sesuatu yang belum jelas, atau menguji ulang klaim yang ada.

### Tiga jenis kontribusi

| Jenis | Contoh |
|---|---|
| Replikasi | Mengulang benchmark atau serangan yang sudah dipublikasikan |
| Ekstensi | Menguji parameter baru, ukuran data baru, atau platform baru |
| Eksplorasi | Menggabungkan dua teknik atau menguji asumsi yang jarang diperiksa |

Untuk peneliti mandiri, replikasi yang rapi sering lebih berharga daripada klaim kebaruan yang lemah.

---

## 2. Studi Literatur

Langkah minimal:

1. Baca spesifikasi resmi: FIPS, RFC, dan paper asli.
2. Baca analisis keamanan terbaru, bukan hanya pengumuman rilis.
3. Cari paper serangan, lalu catat asumsi yang dibutuhkan.
4. Periksa implementasi referensi, tetapi jangan menganggapnya bebas bug.
5. Catat versi dan tanggal, karena status keamanan berubah.

### Sumber yang layak

- IACR ePrint untuk preprint kriptografi.
- NIST CSRC untuk standar.
- RFC Editor untuk protokol.
- Conference: CRYPTO, EUROCRYPT, ASIACRYPT, CHES, USENIX Security.
- Dokumentasi library resmi.

### Yang perlu diwaspadai

1. Blog tanpa sumber primer.
2. Klaim "tidak bisa dipecahkan" tanpa model ancaman.
3. Benchmark tanpa menyebutkan hardware dan versi library.
4. Paper yang tidak menyertakan kode atau data.

---

## 3. Model Ancaman

Setiap klaim keamanan harus menyebutkan:

```
Siapa penyerangnya?
Apa yang bisa dia lakukan?
Apa yang ingin dia capai?
Apa asumsinya?
```

Contoh model ancaman:

| Elemen | Contoh |
|---|---|
| Penyerang | Pengguna jaringan pasif |
| Kemampuan | Merekam lalu lintas, tidak bisa mengubah |
| Tujuan | Mendapatkan plaintext |
| Asumsi | Tidak ada kebocoran kunci, implementasi constant time |

Tanpa model ancaman, pertanyaan "apakah ini aman" tidak bisa dijawab.

---

## 4. Merancang Eksperimen

### Variabel

- **Independen**: yang diubah, misalnya algoritma, ukuran data, parameter.
- **Dependen**: yang diukur, misalnya waktu, memori, throughput.
- **Kontrol**: yang dijaga tetap, misalnya hardware, versi Python, sumber data.

### Prinsip

1. **Ulangi pengukuran.** Minimal 5 sampai 10 kali, laporkan median atau minimum.
2. **Acak urutan.** Hindari efek cache dan pemanasan.
3. **Pisahkan pemanasan.** Buang iterasi pertama.
4. **Ukur yang relevan.** Waktu total belum tentu penting; latensi per operasi bisa lebih penting.
5. **Catat lingkungan.** CPU, RAM, OS, versi library, dan beban sistem.
6. **Simpan data mentah.** Jangan hanya menyimpan ringkasan.

### Contoh tabel hasil

| Ukuran | Algoritma | Waktu (ms) | Throughput (MB/detik) |
|---|---|---|---|
| 1 MB | SHA-256 | 2.242 | 446.1 |
| 1 MB | BLAKE3 | 0.371 | 2694.7 |

---

## 5. Validasi

Sebelum menyimpulkan, pastikan:

1. **Benar secara fungsional.** Hasil cocok dengan vektor uji resmi.
2. **Benar secara statistik.** Perbedaan di luar noise.
3. **Bisa diulang.** Skrip tersedia dan parameter terdokumentasi.
4. **Tidak ada bias.** Data uji tidak dibuat agar hasil terlihat bagus.
5. **Batas jelas.** Sebutkan kasus yang tidak diuji.

### Vektor uji

Selalu pakai vektor resmi:

- FIPS-197 untuk AES.
- RFC 8439 untuk ChaCha20.
- FIPS 180-4 untuk SHA.
- RFC 4231 untuk HMAC.
- RFC 6979 untuk ECDSA deterministik.

Jika hasil tidak cocok, jangan "menyesuaikan" vektor. Perbaiki implementasi.

---

## 6. Analisis Hasil

### Statistik dasar

- **Mean**: mudah terpengaruh outlier.
- **Median**: lebih tahan outlier.
- **Minimum**: berguna untuk benchmark karena noise cenderung menambah waktu.
- **Standar deviasi**: menunjukkan stabilitas.
- **Interval kepercayaan**: menunjukkan ketidakpastian.

### Menghindari kesalahan interpretasi

1. Korelasi bukan kausalitas.
2. Perbedaan 5 persen bisa jadi noise.
3. Benchmark mikro tidak selalu mencerminkan beban nyata.
4. Optimasi yang mempercepat satu operasi bisa memperlambat operasi lain.
5. Angka throughput puncak bukan angka yang dialami pengguna.

---

## 7. Etika dan Tanggung Jawab

1. **Jangan menguji sistem tanpa izin.** Uji hanya sistem sendiri atau lab.
2. **Koordinasikan kerentanan.** Hubungi vendor sebelum publikasi.
3. **Jangan menyertakan data pribadi.** Anonimkan dan agregasi.
4. **Jangan melebih-lebihkan klaim.** Tulis batasan dengan jujur.
5. **Hormati lisensi.** Cantumkan sumber kode dan data.
6. **Jangan mempublikasikan eksploit yang membahayakan tanpa mitigasi.**

---

## 8. Struktur Laporan

1. Abstrak.
2. Pendahuluan dan motivasi.
3. Tinjauan pustaka.
4. Model ancaman.
5. Metodologi.
6. Hasil.
7. Analisis.
8. Keterbatasan.
9. Kesimpulan dan riset lanjutan.
10. Referensi dan lampiran kode.

Template lengkap ada di `02-whitepaper-template.md`.

---

## 9. Alur Kerja yang Disarankan

```
1. Pilih pertanyaan
2. Baca spesifikasi dan paper
3. Tulis model ancaman
4. Bangun implementasi kecil
5. Uji dengan vektor resmi
6. Rancang eksperimen
7. Jalankan, simpan data mentah
8. Analisis dan buat grafik
9. Tulis laporan dengan batasan
10. Minta review
11. Publikasikan kode dan data
```

---

## 10. Jebakan Umum

1. Langsung menulis kode sebelum memahami spesifikasi.
2. Tidak menulis model ancaman.
3. Mengukur satu kali lalu menyimpulkan.
4. Mengabaikan versi library.
5. Menyembunyikan hasil yang tidak sesuai harapan.
6. Menganggap implementasi referensi bebas bug.
7. Membandingkan algoritma dengan implementasi yang tidak setara.
8. Menulis kesimpulan lebih kuat dari data.

---

## 11. Latihan

1. Ambil satu paper, tulis ulang model ancamannya dalam satu halaman.
2. Ulangi benchmark di `hasil-eksperimen` pada mesin sendiri dan bandingkan.
3. Rancang eksperimen untuk mengukur biaya PBKDF2 pada berbagai iterasi.
4. Buat tabel hasil dengan median, minimum, dan standar deviasi.
5. Tulis bagian keterbatasan untuk eksperimen yang baru Anda lakukan.

---

## 12. Referensi

- Boneh dan Shoup, *A Graduate Course in Applied Cryptography*.
- [IACR ePrint](https://eprint.iacr.org/)
- [NIST CSRC](https://csrc.nist.gov/)
- [How to Write a Paper, Simon Peyton Jones](https://www.microsoft.com/en-us/research/academic-program/write-great-research-paper/)
- [Art of Problem Solving: research guidelines](https://artofproblemsolving.com/)

# ✍️ Panduan Publikasi Blog Teknis

Menulis artikel adalah cara terbaik untuk menguji pemahaman sendiri. Jika Anda tidak bisa menjelaskan sesuatu dengan sederhana, kemungkinan Anda belum memahaminya cukup dalam. Panduan ini membantu mengubah eksperimen menjadi artikel yang berguna.

---

## 1. Tujuan dan Pembaca

Sebelum menulis, tentukan:

1. **Siapa pembacanya?** Pemula, praktisi, atau peneliti.
2. **Apa yang ingin mereka lakukan setelah membaca?** Memahami konsep, menjalankan kode, atau mengambil keputusan.
3. **Apa yang harus mereka ingat?** Satu ide utama per artikel.

Artikel yang mencoba melayani semua pembaca biasanya tidak melayani siapa pun.

---

## 2. Struktur Artikel yang Efektif

```
1. Judul yang spesifik
2. Pembuka: masalah nyata dalam 2 sampai 3 paragraf
3. Janji: apa yang akan dibaca
4. Isi: konsep, kode, dan hasil
5. Kesalahan umum
6. Ringkasan
7. Referensi
```

### Judul

Buruk: "Belajar Kriptografi"
Baik: "Mengapa AES-GCM Gagal Total Saat Nonce Diulang"

Judul yang baik memuat subjek, masalah, dan kadang angka.

### Pembuka

Mulai dari masalah, bukan dari definisi. Contoh:

> "Suatu pagi, semua sesi pengguna di aplikasi kami tiba-tiba bisa dibaca penyerang. Penyebabnya bukan AES yang lemah, melainkan satu baris kode yang memakai ulang nonce."

Setelah itu baru masuk teori.

---

## 3. Menulis Penjelasan Teknis

### Aturan sederhana

1. **Satu paragraf, satu ide.**
2. **Definisikan istilah saat pertama muncul.**
3. **Gunakan contoh konkret sebelum generalisasi.**
4. **Tunjukkan angka, bukan hanya kata "cepat".**
5. **Sertakan batasan.**

### Analogi

Analogi membantu, tetapi harus diberi batas:

> "AES seperti brankas yang sangat kuat. Masalahnya, orang sering meninggalkan kuncinya di bawah keset."

Setelah analogi, jelaskan bagian yang tidak sama dengan kenyataan.

### Kode

Aturan kode dalam artikel:

1. Kode harus bisa dijalankan.
2. Sertakan versi bahasa dan library.
3. Potong bagian yang tidak relevan, tetapi tunjukkan cara mendapatkannya.
4. Beri komentar pada baris penting.
5. Tampilkan output nyata, bukan output karangan.
6. Tautkan repositori untuk kode lengkap.

Contoh:

```python
# Menghitung HMAC dengan benar dan membandingkan secara constant time
import hmac, hashlib

tag = hmac.new(key, message, hashlib.sha256).digest()
valid = hmac.compare_digest(tag, received_tag)
```

---

## 4. Menyajikan Hasil Eksperimen

Tabel yang baik:

| Ukuran | Algoritma | Waktu | Throughput |
|---|---|---|---|
| 10 MB | SHA-256 | 28.1 ms | 356 MB/detik |
| 10 MB | BLAKE3 | 3.6 ms | 2784 MB/detik |

Selalu sebutkan:

1. Hardware dan OS.
2. Versi library.
3. Jumlah pengulangan.
4. Metode pengukuran.
5. Apakah angka adalah minimum, median, atau rata-rata.

Tanpa itu, angka tidak bisa dibandingkan.

---

## 5. Menjelaskan Keamanan dengan Bertanggung Jawab

1. **Jangan menakut-nakuti tanpa dasar.** Sebutkan model ancaman.
2. **Jangan menulis "tidak bisa dipecahkan".** Tulis "tidak ada serangan praktis yang diketahui".
3. **Jangan mempublikasikan eksploit pada sistem yang tidak Anda miliki.**
4. **Beri konteks waktu.** Status keamanan berubah.
5. **Sebutkan ketidakpastian.** Kriptografi penuh nuansa.

---

## 6. Alur Penulisan

### Tahap 1: Kerangka

Tulis heading dan satu kalimat per bagian. Jangan mengedit saat menyusun kerangka.

### Tahap 2: Draf kasar

Tulis cepat, jangan pedulikan gaya. Fokus pada kelengkapan.

### Tahap 3: Perbaikan struktur

Periksa alur. Apakah setiap bagian menjawab pertanyaan yang muncul dari bagian sebelumnya?

### Tahap 4: Perbaikan kalimat

1. Pendekkan kalimat panjang.
2. Hapus kata yang tidak perlu.
3. Ganti kalimat pasif yang membingungkan.
4. Pastikan istilah konsisten.

### Tahap 5: Verifikasi

1. Jalankan ulang semua kode.
2. Cocokkan semua angka dengan data.
3. Periksa tautan.
4. Minta satu orang membaca.

---

## 7. Gaya Penulisan

| Hindari | Gunakan |
|---|---|
| "Sangat aman" | "Aman terhadap serangan X dengan asumsi Y" |
| "Jelas sekali" | "Perhatikan bahwa" |
| "Sangat cepat" | "Sekitar 2.700 MB/detik pada mesin uji" |
| "Selalu" | "Pada konfigurasi yang diuji" |
| "Tidak mungkin" | "Tidak praktis dengan sumber daya saat ini" |

Hindari juga:

1. Jargon tanpa definisi.
2. Singkatan yang tidak diperkenalkan.
3. Emoji berlebihan di teks teknis.
4. Kalimat lebih dari 30 kata tanpa jeda.

---

## 8. Panjang dan Format

| Jenis | Panjang | Catatan |
|---|---|---|
| Catatan cepat | 400 sampai 700 kata | Satu temuan |
| Tutorial | 1.200 sampai 2.000 kata | Satu alur kerja |
| Analisis mendalam | 2.500 sampai 4.000 kata | Satu sistem |
| Seri | Beberapa artikel | Topik besar |

Gunakan heading setiap 300 sampai 500 kata. Pembaca memindai, bukan membaca linear.

---

## 9. Publikasi

### Platform

| Platform | Kelebihan | Kekurangan |
|---|---|---|
| Blog pribadi | Kontrol penuh, arsip | Sedikit pembaca awal |
| Medium | Jangkauan | Kurang kontrol format |
| dev.to | Komunitas developer | Fokus umum |
| Substack | Newsletter | Perlu konsistensi |
| GitHub Pages | Dekat dengan kode | Perlu setup |

### Checklist sebelum publikasi

- [ ] Judul spesifik dan jujur.
- [ ] Pembuka memuat masalah nyata.
- [ ] Semua kode sudah dijalankan.
- [ ] Semua angka sesuai data.
- [ ] Lingkungan uji disebutkan.
- [ ] Keterbatasan ditulis.
- [ ] Referensi lengkap dan bisa diakses.
- [ ] Kode lengkap tersedia di repositori.
- [ ] Lisensi jelas.
- [ ] Tidak ada data pribadi atau rahasia.
- [ ] Sudah dibaca ulang dengan suara keras.
- [ ] Satu orang lain sudah meninjau.

---

## 10. Setelah Publikasi

1. Bagikan ke komunitas yang relevan, jangan spam.
2. Tanggapi koreksi dengan terbuka.
3. Perbarui artikel jika ada kesalahan.
4. Simpan versi dan tanggal perubahan.
5. Kumpulkan pertanyaan pembaca sebagai ide artikel berikutnya.

---

## 11. Kerangka Contoh

```
Judul: Mengapa Nonce GCM Tidak Boleh Diulang

1. Insiden: ciphertext bisa dibaca setelah server restart
2. Cara kerja GCM dalam 5 paragraf
3. Apa yang terjadi saat nonce sama
   3.1 XOR dua ciphertext
   3.2 Kebocoran kunci autentikasi
4. Demonstrasi kode: dua enkripsi dengan nonce sama
5. Cara memperbaiki
   5.1 Nonce acak 96 bit
   5.2 Penghitung per kunci
   5.3 Rotasi kunci
6. Kesalahan umum lain
7. Ringkasan
8. Referensi
```

---

## 12. Kesalahan Umum Penulis Teknis

1. Menulis untuk diri sendiri, bukan pembaca.
2. Terlalu banyak teori sebelum ada masalah yang jelas.
3. Kode tidak bisa dijalankan.
4. Angka tanpa konteks.
5. Tidak menyebut batasan.
6. Klaim keamanan yang berlebihan.
7. Tidak ada kesimpulan yang bisa ditindaklanjuti.
8. Artikel terlalu panjang tanpa heading.
9. Tidak memperbarui artikel yang sudah usang.
10. Tidak menyimpan data mentah eksperimen.

---

## 13. Latihan

1. Ambil satu file dari repositori ini, tulis artikel 800 kata tentang satu konsep di dalamnya.
2. Tulis ulang abstrak laporan eksperimen menjadi pembuka blog yang menarik.
3. Buat satu diagram untuk menjelaskan CBC bit flipping.
4. Minta seseorang membaca draf dan catat di mana ia berhenti memahami.
5. Ubah satu kalimat "sangat aman" menjadi klaim yang presisi.

---

## 14. Referensi

- Simon Peyton Jones, *How to Write a Great Research Paper*.
- Ann Handley, *Everybody Writes*.
- [Google Technical Writing Course](https://developers.google.com/tech-writing)
- [OWASP: Writing Secure Code Documentation](https://owasp.org/)

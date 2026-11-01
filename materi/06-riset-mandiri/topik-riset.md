# 💡 Ide Topik Riset Kriptografi

Daftar topik yang bisa dikerjakan secara mandiri, diurutkan dari yang paling ringan. Setiap topik mencantumkan prasyarat, pertanyaan riset, metrik, dan tingkat kesulitan.

Keterangan tingkat: ⭐ pemula, ⭐⭐ menengah, ⭐⭐⭐ lanjutan.

---

## 1. Benchmark Fungsi Hash Modern ⭐

**Pertanyaan:** Seberapa besar perbedaan throughput SHA-256, SHA-3, BLAKE2, dan BLAKE3 pada perangkat tanpa akselerasi hardware?

**Prasyarat:** dasar hashing, Python.

**Metrik:** MB/detik, latensi untuk data kecil, penggunaan memori.

**Kontribusi:** data pembanding yang bisa diulang untuk platform tertentu, misalnya Raspberry Pi atau laptop lama.

**Referensi:** FIPS 180-4, FIPS 202, RFC 7693, spesifikasi BLAKE3.

---

## 2. Analisis Padding Oracle pada Aplikasi Nyata ⭐⭐

**Pertanyaan:** Pola implementasi apa yang membuat aplikasi rentan padding oracle meskipun memakai library standar?

**Prasyarat:** AES-CBC, PKCS#7, dasar web.

**Metrik:** waktu pemulihan per byte, jumlah request, tingkat keberhasilan.

**Kontribusi:** daftar pola kode rawan dan panduan mitigasi.

**Catatan etika:** uji hanya aplikasi buatan sendiri atau lab lokal.

---

## 3. Perbandingan KDF Password pada Perangkat Terbatas ⭐⭐

**Pertanyaan:** Bagaimana trade-off memori, waktu, dan ketahanan Argon2id, scrypt, bcrypt, dan PBKDF2 pada perangkat dengan RAM terbatas?

**Prasyarat:** password hashing, dasar sistem operasi.

**Metrik:** waktu verifikasi, puncak memori, Throughput serangan kamus.

**Kontribusi:** rekomendasi parameter untuk perangkat kelas bawah.

---

## 4. Deteksi Nonce Reuse pada Tanda Tangan ECDSA ⭐⭐

**Pertanyaan:** Seberapa mudah nonce reuse terdeteksi dari kumpulan tanda tangan publik, dan bagaimana pola distribusinya?

**Prasyarat:** ECDSA, statistik dasar.

**Metrik:** jumlah collision, akurasi deteksi, waktu analisis.

**Kontribusi:** alat analisis dan laporan kasus pada data sintetis atau blockchain publik.

---

## 5. Kriptanalisis Cipher Klasik dengan Machine Learning ⭐⭐

**Pertanyaan:** Seberapa baik model sederhana memecahkan Vigenere dengan panjang kunci bervariasi dibandingkan metode Kasiski dan Index of Coincidence?

**Prasyarat:** cipher klasik, dasar machine learning.

**Metrik:** akurasi pemulihan kunci, panjang teks minimum, waktu.

**Kontribusi:** perbandingan metode klasik dan statistik modern pada dataset terkontrol.

---

## 6. Kinerja AES-GCM vs ChaCha20-Poly1305 di Berbagai Platform ⭐⭐

**Pertanyaan:** Kapan ChaCha20-Poly1305 mengungguli AES-GCM, dan seberapa besar pengaruh ada tidaknya AES-NI?

**Prasyarat:** mode AEAD, dasar CPU.

**Metrik:** throughput, latensi, konsumsi daya.

**Kontribusi:** panduan pemilihan cipher berdasarkan platform.

---

## 7. Analisis Implementasi Kriptografi di Library Open Source ⭐⭐

**Pertanyaan:** Kesalahan umum apa yang muncul pada implementasi AES, RSA, dan ECDSA di library kecil?

**Prasyarat:** membaca kode, dasar kriptografi.

**Metrik:** jumlah temuan per kategori, tingkat keparahan.

**Kontribusi:** taksonomi kesalahan dan checklist review.

**Catatan etika:** laporkan temuan ke maintainer sebelum publikasi.

---

## 8. Serangan Length Extension pada API Nyata ⭐⭐

**Pertanyaan:** Berapa banyak API yang memakai `H(secret || message)` sebagai tanda tangan?

**Prasyarat:** SHA-256, HMAC, dasar HTTP.

**Metrik:** jumlah endpoint rentan, tingkat keberhasilan pemalsuan.

**Kontribusi:** survei dan panduan migrasi ke HMAC.

---

## 9. Perbandingan Ukuran dan Waktu Tanda Tangan: RSA vs ECDSA vs Ed25519 ⭐

**Pertanyaan:** Bagaimana trade-off ukuran kunci, ukuran tanda tangan, waktu tanda tangan, dan waktu verifikasi pada tiga skema?

**Prasyarat:** dasar tanda tangan digital.

**Metrik:** byte, milidetik, operasi per detik.

**Kontribusi:** tabel keputusan untuk aplikasi dengan bandwidth terbatas.

---

## 10. Implementasi ECDSA Deterministik (RFC 6979) ⭐⭐

**Pertanyaan:** Apakah ECDSA deterministik benar-benar menghilangkan risiko nonce reuse tanpa mengorbankan performa?

**Prasyarat:** ECDSA, HMAC.

**Metrik:** waktu tanda tangan, konsistensi output, ketahanan terhadap RNG rusak.

**Kontribusi:** implementasi referensi dan analisis risiko residual.

---

## 11. Analisis Performa Homomorphic Encryption untuk Agregasi Statistik ⭐⭐⭐

**Pertanyaan:** Seberapa besar biaya CKKS untuk menghitung rata-rata dan varians atas data terenkripsi dibanding komputasi biasa?

**Prasyarat:** aljabar linear, dasar FHE.

**Metrik:** waktu, memori, ukuran ciphertext, galat numerik.

**Kontribusi:** tolok ukur praktis dan rekomendasi parameter.

---

## 12. Zero-Knowledge Proof untuk Autentikasi Tanpa Password ⭐⭐⭐

**Pertanyaan:** Bagaimana kinerja Schnorr proof dan zk-SNARK untuk autentikasi dibanding TLS biasa?

**Prasyarat:** protokol kriptografi, dasar ZKP.

**Metrik:** latensi, ukuran pesan, biaya verifikasi.

**Kontribusi:** prototipe dan analisis kelayakan.

---

## 13. Serangan Side Channel pada Implementasi AES Python ⭐⭐⭐

**Pertanyaan:** Seberapa besar kebocoran timing pada implementasi AES dengan tabel S-box dibanding implementasi constant time?

**Prasyarat:** AES, statistik, dasar cache.

**Metrik:** korelasi waktu dengan data rahasia, jumlah sampel untuk pemulihan kunci.

**Kontribusi:** demonstrasi edukatif dan panduan mitigasi.

---

## 14. MPC untuk Private Set Intersection ⭐⭐⭐

**Pertanyaan:** Bagaimana trade-off komunikasi dan komputasi antara protokol PSI berbasis OT dan berbasis hashing?

**Prasyarat:** MPC, oblivious transfer.

**Metrik:** bandwidth, jumlah ronde, waktu total.

**Kontribusi:** perbandingan implementasi pada dataset realistis.

---

## 15. Kesiapan Post-Quantum pada Protokol Populer ⭐⭐⭐

**Pertanyaan:** Sejauh mana library populer mendukung ML-KEM dan ML-DSA, dan bagaimana dampaknya pada ukuran handshake?

**Prasyarat:** TLS, dasar lattice.

**Metrik:** ukuran pesan, latensi handshake, kompatibilitas.

**Kontribusi:** matriks kesiapan dan rekomendasi migrasi.

---

## 16. Deteksi Pola ECB pada Data Biner ⭐

**Pertanyaan:** Seberapa andal deteksi blok berulang untuk membedakan ECB dari mode lain pada berbagai jenis data?

**Prasyarat:** mode operasi, dasar statistik.

**Metrik:** akurasi, false positive, false negative.

**Kontribusi:** alat deteksi sederhana dan ambang batas yang disarankan.

---

## 17. Analisis Entropi Kunci pada Proyek Open Source ⭐⭐

**Pertanyaan:** Apakah proyek kecil memakai CSPRNG dengan benar untuk kunci dan nonce?

**Prasyarat:** dasar RNG, membaca kode.

**Metrik:** jumlah temuan, jenis kesalahan.

**Kontribusi:** panduan pemakaian RNG yang aman.

---

## 18. Perbandingan Format Penyimpanan Sandi ⭐

**Pertanyaan:** Bagaimana format penyimpanan password (bcrypt, scrypt, Argon2, PHC string) memengaruhi kemudahan migrasi parameter?

**Prasyarat:** password hashing.

**Metrik:** kemudahan rehash, kompatibilitas, risiko kesalahan.

**Kontribusi:** rekomendasi format dan strategi migrasi.

---

## Cara Memilih Topik

1. Pilih yang bisa selesai dalam 2 sampai 4 minggu.
2. Pastikan ada data atau kode yang bisa diakses.
3. Pastikan ada metrik yang jelas.
4. Hindari topik yang membutuhkan perangkat mahal kecuali tersedia.
5. Pilih topik yang hasilnya berguna meskipun hipotesis awal salah.

---

## Format Proposal Singkat

```
Judul:
Pertanyaan riset:
Mengapa penting:
Metode:
Data atau sistem yang dipakai:
Metrik:
Batas waktu:
Risiko:
Etika:
```

---

## Referensi

- [IACR ePrint](https://eprint.iacr.org/)
- [NIST Post-Quantum Cryptography](https://csrc.nist.gov/projects/post-quantum-cryptography)
- [Cryptopals Challenges](https://cryptopals.com/)
- [Awesome Crypto Papers](https://github.com/pFarb/awesome-crypto-papers)

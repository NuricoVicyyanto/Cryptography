# 📰 Kumpulan Artikel Teknis Penting

Daftar artikel, esai, dan tulisan teknis yang layak dibaca, disertai alasan mengapa penting dan apa yang bisa dipelajari. Diurutkan berdasarkan tema, bukan tahun.

---

## 1. Dasar dan Cara Berpikir

### The Process of Science Applied to Cryptography
**Sumber:** IACR ePrint

Membahas bagaimana riset kriptografi dilakukan dan dievaluasi. Berguna untuk memahami mengapa klaim keamanan harus disertai model ancaman.

### Kerckhoffs' Principle
**Sumber:** berbagai artikel pengantar

Prinsip bahwa keamanan harus bergantung pada kunci, bukan pada kerahasiaan algoritma. Sederhana, tetapi sering dilanggar dalam desain sistem.

### Why Cryptographic Software Is Hard
**Sumber:** IACR ePrint dan blog peneliti

Menjelaskan mengapa implementasi kriptografi benar-benar sulit: timing, cache, compiler, dan perilaku hardware.

---

## 2. Serangan yang Mengubah Industri

### Bleichenbacher's Attack on PKCS#1 v1.5
**1998**

Menunjukkan bahwa pesan error yang tampak tidak berbahaya bisa membocorkan seluruh plaintext. Dasar dari banyak serangan oracle modern, termasuk ROBOT.

### Padding Oracle Attacks
**Robert Heaton, 2013**

Penjelasan paling mudah dipahami tentang padding oracle pada CBC, lengkap dengan langkah demi langkah. Wajib dibaca sebelum menulis kode yang menangani error dekripsi.

### POODLE
**2014**

Serangan terhadap SSL 3.0 yang memanfaatkan cara padding dan fallback. Pelajaran: protokol lama yang dibiarkan hidup bisa menghancurkan keamanan sistem modern.

### Heartbleed
**2014**

Bug pada OpenSSL yang membaca memori di luar batas. Bukan serangan matematis pada TLS, tetapi pengingat bahwa implementasi bisa jauh lebih rapuh dari algoritmanya.

### ROBOT
**2017**

Pengulangan serangan Bleichenbacher pada implementasi TLS modern. Menunjukkan bahwa kesalahan lama bisa bertahan puluhan tahun.

### SHAttered
**2017**

Collision SHA-1 pertama yang dipublikasikan. Menandai akhir SHA-1 untuk collision resistance.

### Logjam
**2015**

Serangan pada Diffie-Hellman dengan parameter lemah dan penggunaan ulang grup. Pelajaran: parameter publik juga bisa menjadi titik lemah.

---

## 3. Implementasi yang Benar

### How to Safely Store a Password
**Berbagai penulis, termasuk OWASP**

Panduan praktis salt, KDF, parameter biaya, dan migrasi. Lebih berguna daripada teori panjang.

### Cryptographic Right Answers
**Latacora**

Daftar jawaban langsung untuk pertanyaan umum: cipher apa, panjang kunci berapa, mode apa, library apa. Bagus untuk memeriksa keputusan desain.

### Nonce Disrespect
**Various security blogs**

Kumpulan insiden nyata nonce reuse pada GCM, CTR, dan ECDSA. Menunjukkan bahwa kesalahan satu bit bisa menghancurkan seluruh sistem.

### The Design of Rijndael
**Daemen dan Rijmen**

Buku oleh pencipta AES yang menjelaskan alasan di balik setiap keputusan desain. Membantu memahami mengapa AES terlihat sederhana tetapi kuat.

---

## 4. Protokol

### TLS 1.3 Explained
**RFC 8446 dan berbagai ringkasan**

Menjelaskan mengapa TLS 1.3 lebih sederhana dan lebih aman dari TLS 1.2: menghapus cipher lemah, mewajibkan forward secrecy, dan menyederhanakan handshake.

### Signal Protocol
**Dokumentasi Signal**

Contoh nyata protokol double ratchet, forward secrecy, dan post-compromise security. Sangat berharga untuk memahami kriptografi pesan.

### Noise Protocol Framework
**noiseprotocol.org**

Kerangka untuk membangun protokol handshake yang aman. Dipakai WireGuard dan banyak sistem lain.

### WireGuard Whitepaper
**Jason Donenfeld**

Contoh desain protokol yang minimalis dan mudah diaudit. Pelajaran tentang menghindari kompleksitas yang tidak perlu.

---

## 5. Kriptografi Modern

### A Graduate Course in Applied Cryptography
**Boneh dan Shoup**

Buku daring gratis yang mencakup hampir semua topik penting. Setiap bab punya latihan yang menantang.

### Twenty Years of Attacks on the RSA Cryptosystem
**Dan Boneh, 1999**

Katalog serangan RSA dan pelajaran tentang pentingnya padding dan implementasi.

### The ChaCha Family of Stream Ciphers
**Daniel J. Bernstein**

Penjelasan desain ChaCha langsung dari penciptanya. Ringkas dan padat.

### BLAKE3 Specification
**BLAKE3 Team**

Spesifikasi yang jelas, disertai alasan desain. Bagus sebagai contoh dokumen teknis yang baik.

### Post-Quantum Cryptography
**NIST dan IACR**

Kumpulan paper tentang ML-KEM, ML-DSA, dan SLH-DSA. Penting untuk memahami arah industri.

---

## 6. Zero-Knowledge dan MPC

### zk-SNARKs: Under the Hood
**Vitalik Buterin**

Penjelasan intuitif tentang QAP dan polynomial commitment. Titik awal yang baik sebelum membaca paper asli.

### PLONK
**Ariel Gabizon, Zachary Williamson, Oana Ciobotaru**

Paper yang memperkenalkan universal setup dan menjadi dasar banyak sistem zkEVM.

### A Pragmatic Introduction to Secure Multi-Party Computation
**Evans, Kolesnikov, Rosulek**

Buku daring yang menjelaskan MPC tanpa terlalu banyak formalisme. Cocok untuk praktisi.

---

## 7. Blog dan Situs yang Konsisten Bagus

| Sumber | Fokus |
|---|---|
| [Trail of Bits Blog](https://blog.trailofbits.com/) | Audit dan implementasi |
| [Cryptography Dispatches](https://buttondown.email/cryptography-dispatches) | Esai teknis oleh Filippo Valsorda |
| [Latacora](https://www.latacora.com/blog/) | Praktik kriptografi terapan |
| [Matthew Green](https://blog.cryptographyengineering.com/) | Analisis kebijakan dan serangan |
| [Dan Boneh](https://crypto.stanford.edu/~dabo/) | Paper dan kuliah |
| [Bristol Cryptography Blog](https://bristolcrypto.blogspot.com/) | Riset dan kriptanalisis |
| [Google Project Zero](https://googleprojectzero.blogspot.com/) | Bug keamanan nyata |
| [NCC Group Research](https://research.nccgroup.com/) | Audit dan eksploitasi |
| [Sophie Schmieg](https://sophieschmieg.com/) | Implementasi kriptografi dan bug |
| [Filippo Valsorda](https://filippo.io/) | Go, TLS, dan kriptografi praktis |

---

## 8. Artikel yang Sering Dikutip

1. **"The Security of the AES"** oleh berbagai penulis, ringkasan kriptanalisis AES.
2. **"On the Security of the CBC Mode"** tentang padding dan bit flipping.
3. **"How to Break MD5 and Other Hash Functions"** oleh Wang dan Yu.
4. **"The First 10 Years of Blockchain"** untuk perspektif kriptografi terapan.
5. **"SoK: Research Perspectives and Challenges for Bitcoin and Cryptocurrencies"**.
6. **"A Taxonomy of Attacks on Cryptographic Implementations"**.

---

## 9. Cara Membaca Artikel Teknis

1. Baca judul, abstrak, dan kesimpulan.
2. Tandai klaim utama.
3. Cari model ancaman dan asumsi.
4. Periksa apakah ada bukti atau hanya argumen.
5. Baca bagian metodologi dengan kritis.
6. Catat pertanyaan yang muncul.
7. Cari diskusi atau kritik dari peneliti lain.
8. Implementasikan versi kecil jika memungkinkan.

---

## 10. Menyimpan Catatan

Format catatan yang berguna:

```
Judul:
Penulis:
Tahun:
Tautan:
Klaim utama:
Model ancaman:
Metode:
Hasil:
Batasan:
Yang saya pelajari:
Pertanyaan lanjutan:
```

Simpan di repositori yang sama dengan kode eksperimen, agar mudah dirujuk saat menulis laporan.

---

## 11. Catatan

1. Artikel blog bisa salah. Verifikasi dengan standar atau paper.
2. Status keamanan berubah. Periksa tanggal.
3. Jangan mengambil nasihat produksi dari artikel tanpa konteks.
4. Jika artikel bertentangan dengan dokumentasi resmi, periksa keduanya dengan hati-hati.
5. Semakin kuat klaim, semakin besar bukti yang dibutuhkan.

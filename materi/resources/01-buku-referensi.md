# 📚 Buku dan Sumber Referensi

Daftar buku, kursus, dan sumber belajar kriptografi yang layak dibaca, disertai catatan siapa yang cocok membacanya dan bab mana yang paling relevan.

---

## 1. Buku Pengantar

### Understanding Cryptography
**Christof Paar dan Jan Pelzl, Springer, 2010**

Buku pengantar terbaik untuk pemula yang ingin memahami cara kerja algoritma tanpa tenggelam dalam formalisme. Setiap bab punya contoh angka, diagram, dan latihan.

Bab penting:

- Bab 1: pengantar dan model ancaman.
- Bab 4: AES.
- Bab 6: RSA.
- Bab 7: RSA lanjutan.
- Bab 8: Diffie-Hellman.
- Bab 9: ECC.
- Bab 10: tanda tangan digital.
- Bab 11: fungsi hash.
- Bab 12: protokol kriptografi.

Cocok untuk: mahasiswa, engineer, siapa pun yang baru mulai.

### Serious Cryptography
**Jean-Philippe Aumasson, No Starch Press, 2018**

Ditulis oleh salah satu pencipta BLAKE2 dan BLAKE3. Fokus pada praktik dan jebakan implementasi, bukan hanya teori. Banyak nasihat nyata tentang apa yang sering salah.

Cocok untuk: engineer yang akan menulis kode kriptografi.

### Cryptography Engineering
**Niels Ferguson, Bruce Schneier, Tadayoshi Kohno, Wiley, 2010**

Membahas cara membangun sistem, bukan hanya algoritma. Bab tentang manajemen kunci, protokol, dan kesalahan implementasi sangat berharga.

Cocok untuk: arsitek sistem dan praktisi keamanan.

---

## 2. Buku Lanjutan

### Introduction to Modern Cryptography
**Jonathan Katz dan Yehuda Lindell, CRC Press, edisi ketiga, 2020**

Buku standar untuk mata kuliah kriptografi. Memperkenalkan definisi keamanan formal dan pembuktian. Jika ingin serius di bidang ini, buku ini wajib.

Topik: pseudorandomness, CPA dan CCA security, PRF, MAC, hash, number theory, RSA, DH, ECC, TLS.

Cocok untuk: mahasiswa pascasarjana dan peneliti.

### A Graduate Course in Applied Cryptography
**Dan Boneh dan Victor Shoup, versi daring**

Gratis dan sangat lengkap. Setiap bab punya latihan. Versi daring sering diperbarui.

Topik: stream cipher, block cipher, message integrity, collision resistance, key exchange, public key encryption, digital signature, MPC, ZKP.

Cocok untuk: belajar mandiri tingkat lanjut.

### Handbook of Applied Cryptography
**Alfred Menezes, Paul van Oorschot, Scott Vanstone, 1996**

Referensi klasik yang masih berguna untuk algoritma dan protokol. Beberapa bagian sudah usang, tetapi strukturnya sangat sistematis.

Cocok untuk: referensi cepat.

---

## 3. Buku Matematika Pendukung

### Elementary Number Theory
**David Burton**

Dasar teori bilangan: keterbagian, kongruensi, primality, fungsi aritmetika. Membantu memahami RSA dan DH.

### A Course in Number Theory and Cryptography
**Neal Koblitz, Springer**

Menghubungkan teori bilangan dengan kriptografi secara langsung. Lebih padat dari Burton.

### Introduction to Algorithms
**Cormen, Leiserson, Rivest, Stein**

Untuk memahami kompleksitas algoritma, termasuk algoritma faktorisasi dan uji primalitas. Bab number theory relevan.

### Abstract Algebra
**Dummit dan Foote**

Untuk memahami grup, ring, dan field yang mendasari ECC dan AES.

---

## 4. Buku Keamanan Sistem

### Real-World Cryptography
**David Wong, Manning, 2021**

Menjelaskan bagaimana kriptografi dipakai di sistem nyata: TLS, Noise, Signal, Bitcoin, dan lainnya. Sangat berguna untuk menghubungkan teori dengan produk.

### Security Engineering
**Ross Anderson, Wiley, edisi ketiga, 2020**

Tidak hanya kriptografi, tetapi konteks sistem tempat kriptografi hidup. Bab tentang protokol dan kegagalan sistem sangat relevan.

### The Tangled Web
**Michal Zalewski**

Tentang keamanan web dan cara browser menangani kriptografi. Bagus untuk memahami ancaman nyata.

---

## 5. Sumber Daring Gratis

| Sumber | Isi | Tingkat |
|---|---|---|
| [Cryptohack](https://cryptohack.org/) | Tantangan interaktif | Pemula sampai lanjut |
| [CryptoPals](https://cryptopals.com/) | Tantangan implementasi | Menengah |
| [Dan Boneh Coursera](https://www.coursera.org/learn/crypto) | Kuliah kriptografi | Menengah |
| [Khan Academy Cryptography](https://www.khanacademy.org/computing/computer-science/cryptography) | Dasar | Pemula |
| [IACR ePrint](https://eprint.iacr.org/) | Paper terbaru | Lanjut |
| [NIST CSRC](https://csrc.nist.gov/) | Standar resmi | Referensi |
| [RFC Editor](https://www.rfc-editor.org/) | Spesifikasi protokol | Referensi |

---

## 6. Paper Klasik

1. Diffie dan Hellman, *New Directions in Cryptography*, 1976.
2. Rivest, Shamir, Adleman, *A Method for Obtaining Digital Signatures and Public-Key Cryptosystems*, 1978.
3. ElGamal, *A Public Key Cryptosystem and a Signature Scheme Based on Discrete Logarithms*, 1985.
4. Koblitz, *Elliptic Curve Cryptosystems*, 1987.
5. Miller, *Use of Elliptic Curves in Cryptography*, 1986.
6. Goldwasser dan Micali, *Probabilistic Encryption*, 1984.
7. Bellare dan Rogaway, *Random Oracles are Practical*, 1993.
8. Boneh, *Twenty Years of Attacks on the RSA Cryptosystem*, 1999.
9. Bernstein, *ChaCha, a variant of Salsa20*, 2008.
10. Gentry, *Fully Homomorphic Encryption Using Ideal Lattices*, 2009.

---

## 7. Kursus dan Video

1. **Cryptography I dan II, Dan Boneh, Coursera.** Penjelasan paling jelas untuk definisi keamanan.
2. **MIT 6.875 Cryptography.** Kuliah lengkap dengan catatan.
3. **Christof Paar, Introduction to Cryptography.** Seri video yang mengikuti bukunya.
4. **ZKP MOOC.** Kursus zero-knowledge proof yang komprehensif.
5. **Real World Cryptography Conference.** Rekaman konferensi tahunan.

---

## 8. Urutan Belajar yang Disarankan

```
Tahap 1: Dasar
  - Understanding Cryptography, bab 1 sampai 2
  - Khan Academy
  - Cryptohack level pemula

Tahap 2: Simetris
  - Understanding Cryptography, bab 3 sampai 5
  - Serious Cryptography, bab 4 sampai 6
  - Implementasikan AES dari nol

Tahap 3: Asimetris
  - Understanding Cryptography, bab 6 sampai 10
  - Implementasikan RSA dan DH dari nol
  - CryptoPals Set 5

Tahap 4: Hash dan protokol
  - Understanding Cryptography, bab 11 sampai 12
  - Implementasikan HMAC
  - CryptoPals Set 1 sampai 4

Tahap 5: Lanjutan
  - Katz-Lindell atau Boneh-Shoup
  - ECC dan ZKP
  - Baca paper asli

Tahap 6: Riset
  - Pilih topik dari `03-topik-riset.md`
  - Tulis laporan
  - Publikasikan
```

---

## 9. Cara Membaca Paper

1. Baca abstrak dan kesimpulan.
2. Baca pendahuluan untuk konteks.
3. Lihat definisi dan model ancaman.
4. Lewati pembuktian pada bacaan pertama.
5. Catat asumsi yang dipakai.
6. Cari paper yang mengutip untuk melihat kritik.
7. Implementasikan versi kecil jika memungkinkan.

---

## 10. Catatan

1. Buku lama tetap berguna untuk konsep, tetapi status keamanan berubah.
2. Selalu periksa tahun terbit untuk rekomendasi parameter.
3. Jangan mengambil nasihat kriptografi dari sumber tanpa nama penulis yang jelas.
4. Dokumentasi resmi dan standar lebih tinggi otoritasnya daripada blog.
5. Jika buku bertentangan dengan standar terbaru, ikuti standar.

# 🧮 Homomorphic Encryption: Gambaran Umum

Homomorphic encryption (HE) memungkinkan komputasi langsung pada data terenkripsi. Hasil komputasi tetap terenkripsi, dan hanya pemilik kunci yang bisa membukanya. Ini menyelesaikan masalah lama: untuk mengolah data, biasanya kita harus mendekripsinya lebih dulu.

---

## 1. Ide Dasar

Enkripsi biasa:

```
D( E(a) + E(b) ) tidak ada hubungannya dengan a + b
```

Enkripsi homomorfik:

```
D( E(a) + E(b) ) = a + b
D( E(a) * E(b) ) = a * b
```

Operasi dilakukan pada ciphertext, tanpa kunci privat.

---

## 2. Jenis Homomorfik

| Jenis | Operasi didukung | Contoh |
|---|---|---|
| Partially HE | Satu operasi, biasanya penjumlahan | Paillier, ElGamal |
| Somewhat HE | Penjumlahan dan perkalian, kedalaman terbatas | BGV, BFV dengan parameter kecil |
| Leveled HE | Kedalaman terbatas yang diketahui | BGV, BFV |
| Fully HE | Operasi tak terbatas | TFHE, BGV dengan bootstrapping |

Perbedaan utama terletak pada **noise**. Setiap operasi menambah noise. Jika noise melewati batas, dekripsi gagal.

---

## 3. Contoh: Paillier

Paillier adalah skema partially homomorphic yang sudah dipakai di industri.

### Key generation

```
pilih prima p dan q
n = p*q
lambda = lcm(p-1, q-1)
g = n + 1
mu = (L(g^lambda mod n^2))^(-1) mod n
L(x) = (x - 1) / n
```

Kunci publik `(n, g)`, kunci privat `(lambda, mu)`.

### Enkripsi

```
c = g^m * r^n mod n^2
```

Dengan `r` acak, sehingga enkripsi probabilistik.

### Sifat homomorfik

```
D( c1 * c2 mod n^2 ) = m1 + m2 mod n
```

Perkalian ciphertext setara penjumlahan plaintext. Ini memungkinkan penjumlahan nilai terenkripsi, misalnya total suara atau total transaksi.

### Aplikasi

1. **E-voting.** Menjumlahkan suara tanpa membuka satu pun.
2. **Private set intersection.** Menghitung irisan tanpa mengungkap data.
3. **Iklan dan analitik.** Agregasi metrik tanpa melihat data individual.

---

## 4. ElGamal: Multiplikatif

ElGamal bersifat homomorfik terhadap perkalian:

```
D( c1 * c2 ) = m1 * m2 mod p
```

Ini dipakai dalam protokol yang membutuhkan perkalian, misalnya beberapa skema voting dan mixnet.

---

## 5. Fully Homomorphic Encryption

### Sejarah singkat

| Tahun | Peristiwa |
|---|---|
| 1978 | Rivest, Adleman, Dertouzos mengusulkan konsep |
| 2005 | Boneh-Goh-Nissim: beberapa operasi terbatas |
| 2009 | Craig Gentry: konstruksi FHE pertama dengan bootstrapping |
| 2011 | BGV, leveling dan modulus switching |
| 2012 | BFV, NTRU-based |
| 2013 | LTV, FHE over the integers |
| 2016 | CKKS, aritmetika aproksimasi untuk angka riil |
| 2016 | TFHE, bootstrapping cepat per gerbang |
| 2017 sampai sekarang | Optimasi besar, implementasi praktis |

### Bootstrapping

Masalah FHE: noise tumbuh setiap operasi. Bootstrapping adalah proses menyegarkan ciphertext:

```
ciphertext_baru = E( D( ciphertext_lama ) )
```

Proses ini dijalankan tanpa membuka ciphertext, dengan mengevaluasi sirkuit dekripsi secara homomorfik. Hasilnya ciphertext dengan noise kecil, siap untuk operasi berikutnya.

Bootstrapping mahal, tetapi memungkinkan operasi tak terbatas.

---

## 6. Skema Modern

| Skema | Tipe data | Kekuatan | Catatan |
|---|---|---|---|
| BFV | Integer | Penjumlahan dan perkalian | Populer, mudah dipahami |
| BGV | Integer | Penjumlahan dan perkalian | Mirip BFV, modulus switching |
| CKKS | Bilangan riil atau kompleks | Aritmetika aproksimasi | Cocok untuk machine learning |
| TFHE | Bit atau integer kecil | Gerbang boolean cepat | Bootstrapping per gerbang |

### BFV dan BGV

Bekerja pada ring polinomial `Z_q[x] / (x^n + 1)`. Plaintext adalah polinomial dengan koefisien integer kecil. Operasi dilakukan koefisien demi koefisien.

### CKKS

Mengenkripsi bilangan riil dengan menganggapnya sebagai polinomial dengan noise aproksimasi. Hasilnya mendekati nilai sebenarnya, dengan presisi yang bisa diatur. Sangat cocok untuk:

1. Inferensi machine learning.
2. Statistik dan agregasi.
3. Analisis sinyal.

### TFHE

Mengenkripsi setiap bit sebagai Learning With Errors. Mendukung gerbang boolean, sehingga bisa membangun rangkaian logika apa pun. Fleksibel, tetapi ciphertext per bit lebih besar.

---

## 7. Performa

Perbandingan kasar:

| Operasi | Komputasi biasa | FHE |
|---|---|---|
| Penjumlahan | Nanodetik | Mikrodetik sampai milidetik |
| Perkalian | Nanodetik | Milidetik |
| Operasi non-linear | Nanodetik | Milidetik sampai detik |
| Transfer data | Kecil | Jauh lebih besar, bisa KB per angka |

Rasio perlambatan bisa mencapai 10.000 kali atau lebih, tergantung skema dan operasi.

Perkembangan hardware dan algoritma terus menurunkan biaya ini, tetapi FHE belum cocok untuk semua beban kerja.

---

## 8. Aplikasi yang Realistis

1. **Kesehatan.** Rumah sakit mengirim data terenkripsi, penyedia cloud menjalankan model prediksi, hasilnya dikembalikan terenkripsi.
2. **Keuangan.** Deteksi penipuan lintas bank tanpa berbagi data nasabah.
3. **Periklanan.** Mengukur konversi tanpa membuka data pribadi.
4. **Pemerintahan.** Agregasi statistik tanpa membuka data individu.
5. **Machine learning sebagai layanan.** Pengguna tidak perlu mempercayai penyedia model.

---

## 9. Keterbatasan

1. **Biaya komputasi tinggi.**
2. **Ukuran ciphertext besar.**
3. **Keterbatasan operasi.** Banyak skema tidak mendukung pembagian, perbandingan, atau fungsi non-linear dengan mudah.
4. **Kebocoran akses pola.** Skema HE menyembunyikan isi, tetapi pola akses memori atau ukuran hasil bisa membocorkan informasi.
5. **Kompleksitas parameter.** Salah memilih parameter bisa membuat data tidak bisa didekripsi.
6. **Standarisasi belum selesai.** HomomorphicEncryption.org sudah menerbitkan standar, tetapi ekosistem masih berkembang.

---

## 10. Kesalahan Umum

1. Menganggap HE menyembunyikan metadata. Ia tidak.
2. Memakai parameter terlalu kecil sehingga noise meluap.
3. Tidak memperhitungkan biaya bootstrapping.
4. Mengira CKKS memberi hasil eksak. Ia aproksimasi.
5. Membandingkan ciphertext dengan `==` untuk logika, padahal enkripsi probabilistik.
6. Mengabaikan kebutuhan autentikasi. HE tidak otomatis memberi integritas.

---

## 11. Latihan

1. Implementasikan Paillier dan tunjukkan bahwa perkalian ciphertext menghasilkan penjumlahan plaintext.
2. Tunjukkan bahwa ElGamal bersifat multiplikatif.
3. Jelaskan mengapa noise tumbuh dan mengapa bootstrapping diperlukan.
4. Bandingkan ukuran ciphertext BFV dan CKKS untuk parameter tertentu.
5. Rancang protokol e-voting sederhana dengan Paillier.
6. Cari library open source seperti Microsoft SEAL, OpenFHE, atau TFHE-rs, lalu jalankan contoh dasar.

---

## 12. Referensi

- Craig Gentry, *A Fully Homomorphic Encryption Scheme*, disertasi Stanford, 2009.
- [HomomorphicEncryption.org standards](https://homomorphicencryption.org/standard/)
- [Microsoft SEAL](https://github.com/microsoft/SEAL)
- [OpenFHE](https://www.openfhe.org/)
- [TFHE-rs](https://github.com/zama-ai/tfhe-rs)
- [Awesome Homomorphic Encryption](https://github.com/jonaschn/awesome-he)

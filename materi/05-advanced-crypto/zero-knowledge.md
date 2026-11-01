# 🕵️ Zero-Knowledge Proofs

Zero-Knowledge Proof (ZKP) adalah protokol di mana satu pihak, **prover**, meyakinkan pihak lain, **verifier**, bahwa sebuah pernyataan benar, tanpa mengungkap **mengapa** pernyataan itu benar. Prover membuktikan pengetahuan tanpa membocorkan pengetahuannya.

Contoh intuitif: membuktikan bahwa Anda tahu password sebuah akun tanpa mengirim password itu, atau membuktikan bahwa Anda cukup umur tanpa mengungkap tanggal lahir.

---

## 1. Tiga Sifat Wajib

| Sifat | Arti |
|---|---|
| Completeness | Jika pernyataan benar dan kedua pihak jujur, verifier menerima |
| Soundness | Jika pernyataan salah, prover tidak bisa meyakinkan verifier, kecuali dengan peluang sangat kecil |
| Zero-knowledge | Verifier tidak belajar apa pun selain fakta bahwa pernyataan itu benar |

Zero-knowledge berarti ada **simulator** yang bisa menghasilkan transkrip yang tidak bisa dibedakan dari transkrip asli. Jika transkrip bisa dipalsukan tanpa pengetahuan rahasia, maka transkrip itu tidak membocorkan pengetahuan.

---

## 2. Gua Ali Baba

Analogi klasik oleh Quisquater dan Guillou:

Sebuah gua berbentuk lingkaran dengan dua pintu, A dan B, yang hanya bisa dibuka dengan kata sandi ajaib. Peggy mengklaim tahu kata sandi. Victor berdiri di luar.

1. Victor menunggu di luar, tidak tahu Peggy masuk lewat pintu mana.
2. Peggy masuk dan memilih salah satu pintu secara acak.
3. Victor berteriak meminta Peggy keluar lewat pintu A atau B, acak.
4. Jika Peggy tahu kata sandi, ia selalu bisa memenuhi permintaan, karena bisa berpindah lewat pintu rahasia.
5. Jika Peggy tidak tahu, peluang ia bisa memenuhi hanya 1/2.
6. Ulangi 20 kali, peluang penipu lolos menjadi 2^-20.

Victor akhirnya yakin Peggy tahu kata sandi, tetapi tidak belajar apa pun tentang kata sandi itu sendiri.

---

## 3. Bukti Interaktif: Graph Isomorphism

Dua graf `G1` dan `G2` disebut isomorfik jika ada permutasi simpul yang mengubah `G1` menjadi `G2`. Menemukan permutasi itu sulit.

Prover tahu isomorfisme `phi`. Protokol:

1. Prover memilih permutasi acak `pi`, membentuk `H = pi(G1)`, lalu mengirim `H`.
2. Verifier memilih tantangan acak: `b = 0` atau `b = 1`.
3. Jika `b = 0`, prover mengirim `pi`.
4. Jika `b = 1`, prover mengirim `pi` dikomposisikan dengan `phi`.
5. Verifier memeriksa bahwa hasilnya memetakan graf yang sesuai ke `H`.

Prover yang tidak tahu `phi` hanya bisa menipu dengan peluang 1/2 per ronde.

---

## 4. Schnorr Proof of Knowledge

Schnorr adalah protokol ZKP paling praktis dan menjadi dasar banyak sistem.

### Setup

Grup siklik berorder prima `q` dengan generator `g`. Prover tahu `x` dan mengumumkan `y = g^x`.

### Protokol

```
Prover                         Verifier
pilih r acak
t = g^r          ----------->  simpan t
                 <-----------  pilih c acak (challenge)
s = r + c*x      ----------->  periksa g^s == t * y^c
```

### Kenapa benar

```
g^s = g^(r + c*x) = g^r * (g^x)^c = t * y^c
```

### Kenapa zero-knowledge

Simulator bisa membuat `(t, c, s)` palsu dengan memilih `c` dan `s` lebih dulu, lalu menghitung `t = g^s * y^(-c)`. Distribusinya identik dengan transkrip asli, sehingga transkrip tidak membocorkan `x`.

### Kenapa soundness kuat

Prover yang bisa menjawab dua tantangan berbeda `c1` dan `c2` dengan `r` yang sama bisa menghitung:

```
x = (s1 - s2) / (c1 - c2) mod q
```

Artinya ia memang tahu `x`.

---

## 5. Fiat-Shamir: Membuat Non-Interaktif

Protokol interaktif merepotkan. Fiat-Shamir mengubahnya menjadi non-interaktif dengan mengganti tantangan acak verifier dengan hash:

```
c = H(t || message || context)
```

Prover mengirim `(t, s)`. Verifier menghitung sendiri `c` dari hash dan memeriksa persamaan.

Konsekuensi keamanan: hash harus dianggap sebagai random oracle. Kesalahan dalam domain separation atau urutan input bisa menciptakan kerentanan, seperti yang terjadi pada beberapa implementasi yang lupa memasukkan pesan ke dalam hash.

---

## 6. Jenis ZKP Modern

| Jenis | Bukti | Setup | Asumsi | Catatan |
|---|---|---|---|---|
| Sigma protocol | Interaktif atau Fiat-Shamir | Tidak perlu | Discrete log | Ringan, untuk pernyataan sederhana |
| zk-SNARK | Sangat kecil | Trusted setup (sebagian skema) | Pairing, knowledge of exponent | Verifikasi cepat |
| zk-STARK | Lebih besar | Transparan | Hash | Tahan kuantum, bukti besar |
| Bulletproofs | Logaritmik | Transparan | Discrete log | Cocok untuk range proof |
| PLONK | Kecil | Universal trusted setup | Pairing | Fleksibel, dipakai zkEVM |
| Halo2 | Kecil | Transparan | Inner product | Rekursif tanpa trusted setup |

---

## 7. Aplikasi

1. **Privasi blockchain.** Zcash membuktikan transaksi valid tanpa mengungkap jumlah dan pihak.
2. **zkRollup.** Ethereum Layer 2 membuktikan ribuan transaksi dengan satu bukti murah.
3. **Autentikasi.** Membuktikan tahu password tanpa mengirimnya.
4. **Usia dan kewarganegaraan.** Membuktikan syarat tanpa mengungkap identitas.
5. **Range proof.** Membuktikan saldo dalam rentang tanpa mengungkap nilainya.
6. **Verifiable computation.** Membuktikan hasil komputasi tanpa menjalankan ulang.
7. **Machine learning.** Membuktikan model dijalankan benar tanpa membuka bobot.

---

## 8. Keterbatasan

1. **Biaya komputasi.** Membuat bukti SNARK bisa jauh lebih mahal dari verifikasi.
2. **Trusted setup.** Jika toxic waste tidak dihancurkan, penyerang bisa membuat bukti palsu.
3. **Kompleksitas implementasi.** Bug pada circuit berarti pernyataan yang dibuktikan bukan yang dimaksud.
4. **Asumsi kriptografis.** SNARK berbasis pairing akan rentan terhadap komputer kuantum.
5. **Ukuran circuit.** Semakin kompleks pernyataan, semakin besar circuit dan semakin mahal.

---

## 9. Kesalahan Umum

1. Memakai Fiat-Shamir tanpa memasukkan seluruh konteks ke hash.
2. Memakai nonce yang sama dua kali dalam sigma protocol.
3. Salah merancang circuit, sehingga constraint tidak menangkap semua aturan.
4. Menganggap bukti ZK otomatis menyembunyikan metadata. Waktu, ukuran, dan pola akses tetap bocor.
5. Memakai trusted setup tanpa upacara multi-partai.
6. Tidak menguji soundness terhadap input jahat.

---

## 10. Latihan

1. Implementasikan Schnorr proof of knowledge dan verifikasi.
2. Ubah menjadi non-interaktif dengan Fiat-Shamir.
3. Tunjukkan simulator untuk Schnorr.
4. Buktikan ekstraksi `x` dari dua transkrip dengan challenge berbeda.
5. Jelaskan mengapa peluang penipu turun secara eksponensial dengan jumlah ronde.
6. Rancang skema pembuktian usia tanpa mengungkap tanggal lahir.

---

## 11. Referensi

- [Original paper: The Knowledge Complexity of Interactive Proof Systems](https://dl.acm.org/doi/10.1145/22145.22178)
- Vitalik Buterin, *zk-SNARKs: Under the Hood*, 2021.
- [Schnorr identification protocol](https://en.wikipedia.org/wiki/Schnorr_signature)
- Boneh dan Shoup, *A Graduate Course in Applied Cryptography*, bab 19 dan 20.
- [ZKP MOOC](https://zk-learning.org/)

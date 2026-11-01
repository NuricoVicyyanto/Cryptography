# 🤝 Secure Multi-Party Computation (MPC)

MPC memungkinkan beberapa pihak menghitung fungsi bersama atas data rahasia masing-masing, tanpa ada pihak yang perlu membuka datanya. Contoh: dua bank ingin tahu total nasabah bersama tanpa saling memberi daftar nasabah.

---

## 1. Definisi Formal

Ada `n` pihak, masing-masing memegang input privat `x_i`. Mereka ingin menghitung:

```
y = f(x_1, x_2, ..., x_n)
```

Tanpa membocorkan `x_i` kepada pihak lain, selain apa yang bisa disimpulkan dari `y`.

Keamanan biasanya dinyatakan dengan **ideal world**: hasil nyata tidak bisa dibedakan dari dunia ideal di mana ada pihak ketiga tepercaya yang menerima semua input dan mengembalikan hasil.

---

## 2. Model Keamanan

| Model | Perilaku penyerang | Catatan |
|---|---|---|
| Semi-honest | Mengikuti protokol, tetapi mencoba belajar dari transkrip | Titik awal, paling mudah |
| Malicious | Bisa menyimpang dari protokol | Butuh verifikasi dan konsistensi |
| Covert | Menyimpang, tetapi takut ketahuan | Kompromi praktis |
| Adaptive | Memilih korupsi setelah melihat data | Lebih kuat dari static |

Jumlah korupsi:

- **Honest majority**: kurang dari separuh pihak jahat. Protokol information-theoretic mungkin.
- **Dishonest majority**: sampai `n-1` pihak jahat. Biasanya butuh asumsi komputasi.

---

## 3. Secret Sharing

Fondasi MPC adalah membagi rahasia menjadi beberapa bagian, di mana sebagian saja tidak berguna.

### Shamir Secret Sharing

Rahasia `s` dibagi menjadi `n` bagian dengan threshold `t`:

1. Pilih polinomial acak derajat `t-1`:

```
f(x) = s + a1*x + a2*x^2 + ... + a(t-1)*x^(t-1) mod p
```

2. Bagian ke-`i` adalah `(i, f(i))`.
3. Untuk merekonstruksi, kumpulkan minimal `t` bagian lalu interpolasi Lagrange.

Kurang dari `t` bagian tidak memberi informasi apa pun tentang `s`, karena ada banyak polinomial derajat `t-1` yang melewati titik-titik tersebut.

### Sifat aditif

Untuk MPC, sering dipakai **additive sharing**:

```
s = s1 + s2 + ... + sn mod p
```

Setiap pihak memegang satu bagian. Penjumlahan rahasia mudah: cukup jumlahkan bagian secara lokal. Perkalian membutuhkan interaksi.

---

## 4. Garbled Circuits (Yao)

Dua pihak, satu pihak menyiapkan circuit, pihak lain mengevaluasi.

1. Penggagas menyusun circuit boolean untuk `f`.
2. Setiap kabel diberi dua label acak, satu untuk bit 0, satu untuk bit 1.
3. Setiap gerbang dienkripsi menjadi tabel empat baris, diacak urutannya (garbled table).
4. Penggagas mengirim circuit terenkripsi plus label untuk input-nya sendiri.
5. Pihak lain memperoleh label input-nya lewat **Oblivious Transfer**.
6. Pihak lain mengevaluasi gerbang satu per satu, hanya bisa membuka satu baris tabel per gerbang.
7. Hasil akhir diterjemahkan bersama.

Kelebihan: hanya butuh beberapa ronde komunikasi.
Kekurangan: biaya sebanding dengan ukuran circuit, dan circuit harus dibangun ulang untuk setiap evaluasi.

---

## 5. Oblivious Transfer (OT)

OT adalah primitif dasar. Varian 1-2 OT:

- Pengirim punya dua pesan `m0` dan `m1`.
- Penerima punya pilihan `b`.
- Penerima mendapat `m_b`, tanpa tahu `m_(1-b)`.
- Pengirim tidak tahu `b`.

OT sering diimplementasikan dengan Diffie-Hellman atau kurva eliptik, dan bisa diperluas menjadi ribuan OT dengan biaya rendah lewat **OT extension**.

---

## 6. MPC Berbasis Secret Sharing

Protokol seperti BGW, GMW, dan SPDZ bekerja dengan membagi setiap nilai menjadi shares.

Untuk sirkuit aritmetika:

- **Penjumlahan:** gratis, jumlahkan shares secara lokal.
- **Perkalian:** butuh interaksi untuk menghitung perkalian silang antar shares.

### Beaver Triples

Persiapan offline menghasilkan triple `(a, b, c)` dengan `c = a*b`, semuanya dalam bentuk shares.

Untuk mengalikan `x` dan `y`:

```
e = x - a
f = y - b
buka e dan f
z = c + e*b + f*a + e*f
```

Dengan triple yang sudah disiapkan, perkalian hanya butuh dua pembukaan nilai, bukan komunikasi berat. Ini membuat MPC praktis.

---

## 7. Protokol Modern

| Protokol | Pihak | Model | Catatan |
|---|---|---|---|
| GMW | Banyak | Semi-honest atau malicious | Berbasis shares, cocok untuk boolean |
| BGW | Banyak | Honest majority | Information-theoretic |
| SPDZ | Banyak | Dishonest majority | Preprocessing, malicious |
| Yao | 2 | Semi-honest | Garbled circuit |
| MASCOT | 2 | Malicious | OT-based |
| TinyOT | 2 | Malicious | Boolean, efisien |

### Framework populer

1. **MP-SPDZ**: banyak protokol, riset dan benchmark.
2. **EMP-toolkit**: dua pihak, garbled circuit dan OT.
3. **ABY**: campuran arithmetic, boolean, dan Yao.
4. **Frigate**: circuit compiler.
5. **CrypTen**: MPC untuk machine learning di PyTorch.

---

## 8. Aplikasi

1. **Private set intersection.** Menemukan kontak bersama tanpa membuka daftar.
2. **Threshold signature.** Kunci tanda tangan dibagi, butuh `t` pihak untuk menandatangani.
3. **Auction.** Lelang tertutup tanpa membuka penawaran.
4. **Analitik lintas organisasi.** Total pasien atau transaksi tanpa berbagi data.
5. **Kripto kustodian.** Dompet multisig tingkat lanjut.
6. **Machine learning kolaboratif.** Melatih model tanpa memusatkan data.
7. **Audit pajak.** Membuktikan kepatuhan tanpa membuka angka detail.

---

## 9. Keterbatasan

1. **Biaya komunikasi.** Setiap perkalian butuh beberapa ronde dan bandwidth.
2. **Latensi.** Semakin banyak pihak, semakin banyak ronde.
3. **Kompleksitas implementasi.** Protokol malicious sangat rumit.
4. **Kebutuhan sinkronisasi.** Pihak yang lambat memperlambat semua.
5. **Kebocoran metadata.** Pola komunikasi dan ukuran data tetap terlihat.
6. **Tidak melindungi input yang salah.** MPC menjamin privasi, bukan kebenaran data.

---

## 10. Perbandingan dengan FHE

| Aspek | MPC | FHE |
|---|---|---|
| Pihak yang menghitung | Beberapa pihak berinteraksi | Satu pihak menghitung sendiri |
| Komunikasi | Intensif | Hanya data terenkripsi |
| Latensi | Beberapa ronde | Satu putaran |
| Kecocokan | Lintas organisasi | Cloud dan outsourcing |
| Kematangan | Lebih matang untuk produksi | Berkembang cepat |
| Biaya komputasi | Lebih rendah dari FHE | Tinggi |

Sering kali keduanya digabung: MPC untuk menyiapkan kunci, FHE untuk komputasi.

---

## 11. Kesalahan Umum

1. Menganggap MPC menyembunyikan jumlah pihak atau ukuran data.
2. Memakai protokol semi-honest di lingkungan yang tidak tepercaya.
3. Tidak mengautentikasi pihak, sehingga penyerang bisa ikut serta.
4. Mengabaikan serangan denial of service dari pihak yang berhenti di tengah.
5. Memakai randomness yang tidak aman untuk shares.
6. Lupa menghapus nilai antara dari memori.
7. Mengira MPC menjamin hasil benar jika input salah.

---

## 12. Latihan

1. Implementasikan Shamir Secret Sharing untuk `t = 3`, `n = 5`, lalu rekonstruksi.
2. Tunjukkan bahwa dua shares tidak memberi informasi tentang rahasia.
3. Implementasikan penjumlahan rahasia dengan additive sharing.
4. Implementasikan Beaver triple sederhana untuk perkalian dua nilai rahasia.
5. Simulasikan oblivious transfer dengan Diffie-Hellman.
6. Rancang protokol lelang tertutup dua pihak dengan MPC.
7. Bandingkan biaya komunikasi garbled circuit dan secret sharing untuk fungsi yang sama.

---

## 13. Referensi

- [Yao's Millionaires' Problem](https://en.wikipedia.org/wiki/Yao%27s_Millionaires%27_Problem)
- [MP-SPDZ](https://github.com/data61/MP-SPDZ)
- [EMP-toolkit](https://github.com/emp-toolkit)
- [ABY framework](https://github.com/encryptogroup/ABY)
- Evans, Kolesnikov, Rosulek, *A Pragmatic Introduction to Secure Multi-Party Computation*
- Boneh dan Shoup, *A Graduate Course in Applied Cryptography*, bab 22.

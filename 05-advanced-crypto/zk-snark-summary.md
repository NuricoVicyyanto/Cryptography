# 📐 Ringkasan zk-SNARK

zk-SNARK adalah singkatan dari **Zero-Knowledge Succinct Non-interactive Argument of Knowledge**. Ia membuktikan bahwa sebuah pernyataan benar tanpa mengungkap datanya, dengan bukti yang **pendek** dan **cepat diverifikasi**.

Dokumen ini merangkum cara kerjanya pada level yang cukup teknis untuk dipahami, tanpa tenggelam dalam notasi aljabar.

---

## 1. Arti Setiap Kata

| Kata | Arti |
|---|---|
| Zero-Knowledge | Verifier tidak belajar apa pun selain kebenaran pernyataan |
| Succinct | Bukti berukuran sangat kecil, verifikasi super cepat |
| Non-interactive | Cukup satu pesan bukti, tidak perlu bolak-balik |
| Argument | Soundness bergantung pada asumsi komputasi, bukan kekuatan tak terbatas |
| of Knowledge | Prover benar-benar tahu witness, bukan sekadar hitungan untung |

Bukti Groth16 berukuran sekitar 200 byte dan bisa diverifikasi dalam hitungan milidetik, berapa pun besarnya komputasi yang dibuktikan.

---

## 2. Masalah yang Diselesaikan

Misalkan kita ingin membuktikan pernyataan seperti:

```
"Saya tahu x dan y sehingga x * y = 391 dan x + y = 40."
```

Verifier tidak perlu tahu `x` dan `y`, cukup yakin bahwa pasangan itu ada dan memenuhi syarat.

Untuk program komputer:

```
"Saya menjalankan program P dengan input publik I dan saya tahu input privat W
sehingga P(I, W) menghasilkan output yang diumumkan."
```

Ini disebut **verifiable computation**.

---

## 3. Alur Besar

```
Program atau pernyataan
        |
        v
Arithmetic Circuit
        |
        v
R1CS (Rank-1 Constraint System)
        |
        v
QAP (Quadratic Arithmetic Program)
        |
        v
Polynomial Commitment
        |
        v
Proof (ratusan byte)
```

---

## 4. R1CS

R1CS adalah kumpulan constraint berbentuk:

```
(a . w) * (b . w) = (c . w)
```

Dengan `w` adalah vektor witness, yaitu semua nilai variabel dalam circuit, termasuk input publik dan privat. Setiap gerbang aritmetika menjadi satu constraint.

Contoh: membuktikan `z = x * y` dan `z = 42`:

```
constraint 1: x * y = z
constraint 2: z * 1 = 42
```

Setiap operasi perkalian membutuhkan constraint. Penjumlahan biasanya gratis karena bisa digabung ke dalam vektor.

---

## 5. QAP

QAP mengubah kumpulan constraint menjadi polinomial. Idenya:

1. Setiap constraint diberi titik evaluasi `r_i`.
2. Untuk setiap variabel, dibentuk polinomial yang menginterpolasi nilainya di titik-titik tersebut.
3. Constraint terpenuhi di semua titik jika dan hanya jika polinomial tertentu habis dibagi oleh **vanishing polynomial** `Z(x) = product (x - r_i)`.

Secara informal:

```
A(x) * B(x) - C(x) = H(x) * Z(x)
```

Prover harus membuktikan ia tahu `H(x)` yang membuat persamaan ini benar.

Untuk mengeceknya tanpa mengungkap polinomial, dipakai **polynomial commitment**: prover mengirim komitmen, verifier meminta evaluasi di titik acak, dan memeriksa persamaan.

---

## 6. Polynomial Commitment

Skema populer:

| Skema | Ukuran komitmen | Setup | Asumsi |
|---|---|---|---|
| KZG | Satu grup elemen | Trusted, universal atau per-circuit | Pairing, q-SDH |
| Bulletproofs | Logaritmik | Transparan | Discrete log |
| FRI | Logaritmik kuadratik | Transparan, hanya hash | Collision resistance |

KZG sangat kecil dan cepat, tetapi butuh **trusted setup**. FRI transparan dan tahan kuantum, tetapi bukti lebih besar.

---

## 7. Trusted Setup

Beberapa SNARK membutuhkan **structured reference string** yang dibangkitkan dari rahasia `tau`. Jika `tau` bocor, penyerang bisa membuat bukti palsu.

Upacara yang benar:

1. Banyak peserta masing-masing menyumbang kerahasiaan.
2. Selama minimal satu peserta jujur dan menghancurkan kontribusinya, parameter aman.
3. Hasil akhir bisa diverifikasi publik.

Contoh: upacara Zcash dan banyak proyek lain melibatkan ribuan peserta.

PLONK memakai **universal setup**, sehingga satu upacara bisa dipakai untuk semua circuit sampai ukuran tertentu. Ini jauh lebih praktis daripada setup per circuit seperti Groth16.

---

## 8. Groth16 vs PLONK vs STARK

| Aspek | Groth16 | PLONK | STARK |
|---|---|---|---|
| Ukuran bukti | Sangat kecil, sekitar 200 byte | Kecil, sekitar 400 sampai 800 byte | Besar, puluhan KB |
| Waktu prove | Cepat | Sedang | Lambat |
| Waktu verify | Sangat cepat | Cepat | Cepat, tetapi lebih lambat dari SNARK |
| Setup | Per circuit | Universal | Transparan |
| Asumsi | Pairing | Pairing | Hash |
| Tahan kuantum | Tidak | Tidak | Ya |
| Recursion | Sulit | Mudah | Mudah |
| Kecocokan | Aplikasi tetap | zkEVM, sistem umum | Sistem transparan |

---

## 9. Aplikasi

1. **zkRollup.** Menggabungkan ribuan transaksi menjadi satu bukti.
2. **Zcash.** Transaksi shielded tanpa mengungkap pengirim, penerima, dan jumlah.
3. **zkEVM.** Membuktikan eksekusi kontrak Ethereum.
4. **Identitas.** Membuktikan atribut tanpa mengungkap dokumen.
5. **Verifiable ML.** Membuktikan inferensi dijalankan dengan model tertentu.
6. **Cross-chain bridge.** Membuktikan state chain lain tanpa mempercayai relayer.

---

## 10. Keterbatasan Praktis

1. **Biaya prove tinggi.** Membuat bukti bisa memakan waktu puluhan detik sampai menit untuk circuit besar.
2. **Memori besar.** Circuit besar butuh RAM signifikan.
3. **Kompleksitas audit.** Bug pada compiler circuit atau constraint bisa membuat pernyataan yang dibuktikan berbeda dari yang dimaksud.
4. **Trusted setup.** Beban operasional dan risiko sosial.
5. **Bukan solusi privasi menyeluruh.** Metadata seperti waktu dan ukuran tetap terlihat.

---

## 11. Istilah Penting

| Istilah | Arti |
|---|---|
| Witness | Data privat yang dipakai prover |
| Public input | Data yang diketahui verifier |
| Circuit | Representasi komputasi sebagai gerbang aritmetika |
| Constraint | Persamaan yang harus dipenuhi witness |
| Toxic waste | Rahasia dari trusted setup yang harus dihancurkan |
| Recursive proof | Bukti yang membuktikan bukti lain valid |
| Fiat-Shamir | Mengubah protokol interaktif menjadi non-interaktif |
| Soundness error | Peluang prover palsu diterima |

---

## 12. Ringkasan Satu Paragraf

zk-SNARK mengubah pernyataan komputasi menjadi circuit aritmetika, lalu menjadi sistem persamaan polinomial. Prover menunjukkan bahwa ia tahu witness yang memenuhi persamaan tersebut, dengan mengirim komitmen polinomial yang sangat kecil. Verifier memeriksa beberapa evaluasi di titik acak dan menerima atau menolak. Semua ini bisa dilakukan tanpa verifier mengetahui witness, dan biaya verifikasinya konstan.

---

## 13. Referensi

- [Groth16 paper](https://eprint.iacr.org/2016/260)
- [PLONK paper](https://eprint.iacr.org/2019/953)
- [STARK paper](https://eprint.iacr.org/2018/046)
- [KZG polynomial commitments](https://www.iacr.org/archive/asiacrypt2010/6477178/6477178.pdf)
- Vitalik Buterin, *zk-SNARKs: Under the Hood*, 2017.
- [ZKProof community](https://zkproof.org/)

# 🏛️ Cipher Klasik: Catatan Analisis

Cipher klasik adalah kriptografi sebelum era komputer. Nilainya bukan pada keamanan hari ini, tetapi pada **pola berpikir**: bagaimana menyerang sistem, bagaimana mengukur kekuatan, dan bagaimana prinsip-prinsipnya masih hidup di algoritma modern. Banyak konsep di sini, seperti confusion, diffusion, dan known plaintext attack, pertama kali dipahami lewat cipher klasik.

---

## 1. Peta Cipher Klasik

| Kategori | Cara kerja | Contoh | Kunci |
|---|---|---|---|
| Substitusi monoalfabetik | Satu huruf diganti satu huruf | Caesar, Atbash, Affine | Pergeseran atau pemetaan |
| Substitusi polialfabetik | Huruf diganti bergantung posisi | Vigenere, Beaufort, Autokey | Kata kunci |
| Transposisi | Posisi huruf diacak, huruf tetap | Rail Fence, Columnar | Jumlah rail atau kata kunci |
| Poligrafik | Beberapa huruf sekaligus | Playfair, Hill | Matriks kunci |
| Homofonik | Satu huruf punya banyak simbol | Cipher nomenklator | Buku kode |

Dua keluarga besar yang paling penting untuk dipahami adalah **substitusi** dan **transposisi**. Hampir semua cipher klasik adalah kombinasi keduanya.

---

## 2. Caesar Cipher

### Definisi

```
C = (P + k) mod 26
P = (C - k) mod 26
```

### Analisis

- **Ukuran ruang kunci:** hanya 25 kemungkinan (selain 0). Brute force sepenuhnya sepele.
- **Ketahanan frekuensi:** nol. Distribusi huruf bergeser utuh, sehingga huruf yang paling sering di ciphertext adalah huruf paling sering di plaintext, hanya digeser.
- **Kriptanalisis:** cukup hitung huruf terbanyak, bandingkan dengan frekuensi `E` (12.7%) atau `T` (9.1%) dalam bahasa Inggris. Untuk bahasa Indonesia, huruf terbanyak biasanya `A` (sekitar 19%) atau `N` (sekitar 8.5%).
- **Varian Affine:** `C = (aP + b) mod 26` dengan syarat `gcd(a, 26) = 1`. Ruang kunci menjadi 12 * 26 = 312, masih sangat kecil.

Pelajaran: **kunci yang bisa ditebak dalam hitungan detik bukan kunci.**

---

## 3. Vigenere Cipher

### Definisi

```
C_i = (P_i + K_i) mod 26
```

Kunci diulang sepanjang pesan. Jika kunci sepanjang pesan dan benar-benar acak, hasilnya adalah one time pad yang aman sempurna. Karena kunci diulang, keamanannya runtuh.

### Kenapa lebih kuat dari Caesar

Setiap huruf plaintext bisa dipetakan ke beberapa huruf ciphertext berbeda, sehingga frekuensi terlihat lebih rata. Contoh: `E` bisa menjadi `F`, `G`, atau `H` tergantung posisi.

### Kriptanalisis

1. **Cari panjang kunci.**
   - Kasiski Examination: cari substring berulang di ciphertext. Jarak antar kemunculan cenderung kelipatan panjang kunci.
   - Index of Coincidence: untuk setiap dugaan panjang `L`, pecah ciphertext menjadi `L` kolom, hitung IC setiap kolom. Jika `L` benar, IC kolom mendekati 0.066 (bahasa alami). Jika salah, IC mendekati 0.038 (acak).
2. **Pecah ciphertext menjadi L kolom.** Setiap kolom sekarang hanyalah Caesar cipher.
3. **Selesaikan setiap kolom dengan chi-squared** terhadap distribusi frekuensi bahasa target.
4. **Gabungkan pergeseran** menjadi kunci.

### Angka penting Index of Coincidence

| Teks | IC |
|---|---|
| Bahasa Inggris alami | 0.0667 |
| Bahasa Indonesia (perkiraan) | 0.0700 |
| Teks acak seragam | 0.0385 |
| Caesar cipher | 0.0667 (tidak berubah) |
| Vigenere dengan kunci panjang L | sekitar 0.038 + 0.028/L |

Rumus IC:

```
IC = sum(n_i * (n_i - 1)) / (N * (N - 1))
```

dengan `n_i` frekuensi huruf ke-i dan `N` total huruf.

Pelajaran: **pengulangan kunci menciptakan struktur yang bisa dideteksi.**

---

## 4. Transposition Cipher

### Definisi

Huruf tidak diganti, hanya dipindah. Contoh columnar: tulis plaintext dalam grid selebar kunci, lalu baca kolom sesuai urutan abjad kunci.

```
Plain : SERANGFAJARBAWABEKAL
Key   : ZEBRA  -> urutan kolom: B(1), E(0), R(4), A(3), Z(2)
```

### Analisis

- **Frekuensi huruf identik** dengan plaintext. Ini kelemahan sekaligus kelebihan: analisis frekuensi biasa gagal, tetapi anagram tetap terlihat.
- **Kriptanalisis** memakai skor bigram atau trigram. Dengan panjang kunci kecil, brute force permutasi kolom bisa menemukan teks yang "terlihat bahasa".
- Panjang kunci membatasi ruang pencarian: `L!` permutasi. Untuk `L = 10`, ada 3.6 juta kemungkinan, masih bisa diatasi dengan hill climbing.

### Varian

- **Rail Fence:** pola zigzag, jumlah rail sebagai kunci.
- **Double Transposition:** lakukan dua kali dengan dua kunci, jauh lebih kuat.
- **Myszkowski:** kunci dengan huruf berulang dipecah untuk mengubah urutan kolom.

Pelajaran: **menyembunyikan pola statistik tidak cukup jika struktur posisi bisa dipulihkan.**

---

## 5. Playfair Cipher (Poligrafik)

### Cara kerja

1. Buat matriks 5x5 dari kata kunci, buang huruf berulang, isi sisanya dengan abjad (I dan J digabung).
2. Pecah plaintext menjadi pasangan huruf. Jika ada pasangan kembar, sisipkan `X`.
3. Aturan enkripsi per pasangan:
   - Huruf sama baris: geser ke kanan.
   - Huruf sama kolom: geser ke bawah.
   - Berbeda baris dan kolom: tukar kolom (bentuk persegi panjang).

### Analisis

- 676 kemungkinan pasangan, lebih tahan frekuensi tunggal, tetapi frekuensi bigram masih bocor.
- Dipakai Inggris dalam Perang Boer dan Perang Dunia I.
- Kriptanalisis modern membutuhkan sekitar 100 sampai 200 huruf ciphertext.

---

## 6. Hill Cipher (Aljabar Linear)

### Definisi

```
C = K * P mod 26
P = K^(-1) * C mod 26
```

`K` adalah matriks persegi berukuran `n x n` dengan `gcd(det(K), 26) = 1`.

### Analisis

- Rentan **known plaintext attack**: dengan `n` pasangan plaintext dan ciphertext, matriks kunci bisa dihitung langsung lewat aljabar linear.
- Ini contoh awal cipher yang secara matematis elegan tetapi operasionalnya rapuh.

Pelajaran: **keamanan tidak berasal dari kerumitan rumus, tetapi dari ukuran ruang kunci dan ketiadaan struktur yang bisa dieksploitasi.**

---

## 7. Tabel Perbandingan

| Cipher | Ruang kunci | Tahan frekuensi | Serangan efektif | Status |
|---|---|---|---|---|
| Caesar | 25 | Tidak | Brute force, frekuensi | Usang |
| Affine | 312 | Tidak | Brute force, frekuensi | Usang |
| Vigenere | 26^L | Sebagian | Kasiski, IC, chi-squared | Usang |
| Rail Fence | rails | Ya (huruf) | Brute force pola | Usang |
| Columnar | L! | Ya (huruf) | Anagram scoring, hill climbing | Usang |
| Playfair | 25! matriks | Sebagian | Analisis bigram | Usang |
| Hill | matriks mod 26 | Sebagian | Known plaintext | Usang |
| One Time Pad | tak terbatas | Ya | Tidak ada jika kunci benar | Aman secara teori |

---

## 8. Prinsip Yang Diwariskan ke Kriptografi Modern

1. **Confusion** (Shannon): hubungan antara plaintext dan ciphertext harus dibuat serumit mungkin. Ini alasan AES memakai S-box non-linear.
2. **Diffusion** (Shannon): satu bit plaintext harus memengaruhi banyak bit ciphertext. Ini alasan AES memakai MixColumns dan ShiftRows.
3. **Kunci harus besar.** Caesar dengan 25 kunci kalah oleh brute force. AES dengan 2^128 kunci tidak.
4. **Jangan mengulang kunci.** Vigenere gagal karena pengulangan. AES-GCM gagal jika nonce diulang.
5. **Asumsi Kerckhoffs.** Algoritma boleh diketahui publik, hanya kunci yang rahasia. Cipher klasik dengan kunci rahasia algoritma tetap bisa dibongkar.
6. **Known plaintext attack itu nyata.** Hill cipher hancur olehnya, dan di dunia modern serangan ini muncul dalam bentuk crib dragging dan chosen plaintext.

---

## 9. Latihan

1. Dekripsi `WKH VHFUHW LV VDIH` tanpa mengetahui pergeseran. Jelaskan langkahnya.
2. Enkripsi `KRIPTOGRAFI` dengan Vigenere kunci `BUNGA`, lalu coba tebak panjang kuncinya dari ciphertext.
3. Hitung IC dari kalimat `THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG`.
4. Untuk columnar dengan kunci `ZEBRA`, tuliskan urutan kolom yang dipakai dan jelaskan cara menangani huruf kembar.
5. Bangun matriks Playfair dari kunci `MONARCHY` dan enkripsi pasangan `BA`.
6. Jelaskan mengapa transposition cipher tidak bisa dipecahkan dengan analisis frekuensi huruf tunggal, tetapi bisa dengan analisis bigram.
7. Bandingkan keamanan Vigenere dengan kunci 3 huruf dan kunci 20 huruf. Gunakan konsep IC.

---

## 10. Referensi

- William Stallings, *Cryptography and Network Security*, bab cipher klasik.
- Simon Singh, *The Code Book*, sejarah dan kriptanalisis.
- [Practical Cryptography: Vigenere](http://practicalcryptography.com/ciphers/classical-era/vigenere/)
- [Crypto Corner](https://crypto.interactive-maths.com/) untuk playground interaktif.
- [Cryptopals Set 1](https://cryptopals.com/sets/1) untuk latihan implementasi dan serangan.

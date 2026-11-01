# ✍️ DSA (Digital Signature Algorithm)

DSA adalah standar tanda tangan digital Pemerintah Amerika Serikat, diadopsi NIST pada 1994 sebagai FIPS 186. Ia menjadi dasar DSS (Digital Signature Standard) dan kemudian berkembang menjadi ECDSA dan EdDSA. DSA tidak dipakai untuk enkripsi, hanya untuk **tanda tangan digital**.

---

## 1. Tujuan Tanda Tangan Digital

Tanda tangan digital memberi tiga jaminan:

1. **Autentikasi.** Pesan benar berasal dari pemilik kunci privat.
2. **Integritas.** Pesan tidak berubah setelah ditandatangani.
3. **Non-repudiation.** Penandatangan tidak bisa menyangkal, karena hanya dia yang punya kunci privat.

Berbeda dari MAC yang memakai kunci simetris, tanda tangan bisa diverifikasi siapa saja memakai kunci publik.

---

## 2. Parameter Domain

DSA membutuhkan tiga parameter publik:

```
p : bilangan prima besar
q : bilangan prima yang membagi p - 1
g : generator subgrup berorder q, yaitu g = h^((p-1)/q) mod p
```

Ukuran standar:

| Tingkat keamanan | p | q |
|---|---|---|
| Lama | 1024 bit | 160 bit |
| FIPS 186-3 | 2048 bit | 224 bit |
| FIPS 186-4 | 3072 bit | 256 bit |

Kunci privat `x` adalah bilangan acak `1 <= x <= q-1`. Kunci publik:

```
y = g^x mod p
```

---

## 3. Algoritma Tanda Tangan

Untuk pesan `m`:

1. Hitung `z`, yaitu `q` bit paling kiri dari hash pesan. Untuk SHA-256 dan q 160 bit, buang 96 bit terakhir.
2. Pilih nonce `k` acak di `1..q-1`.
3. Hitung `r = (g^k mod p) mod q`. Jika `r = 0`, ulangi dengan `k` baru.
4. Hitung `s = k^(-1) * (z + x*r) mod q`. Jika `s = 0`, ulangi.
5. Tanda tangan adalah pasangan `(r, s)`.

---

## 4. Algoritma Verifikasi

Diberikan `(r, s)`, pesan `m`, dan kunci publik `y`:

1. Tolak jika `r` atau `s` di luar rentang `1..q-1`.
2. Hitung `z` dari hash pesan.
3. Hitung `w = s^(-1) mod q`.
4. Hitung `u1 = z * w mod q`.
5. Hitung `u2 = r * w mod q`.
6. Hitung `v = ((g^u1 * y^u2) mod p) mod q`.
7. Tanda tangan valid jika `v == r`.

### Kenapa benar

Substitusi `s`:

```
w = k * (z + x*r)^(-1)
u1 = z * k * (z + x*r)^(-1)
u2 = r * k * (z + x*r)^(-1)
```

Maka:

```
g^u1 * y^u2 = g^(z*k*inv) * g^(x*r*k*inv) = g^(k*(z + x*r)*inv) = g^k
```

Setelah modulo `q`, hasilnya sama dengan `r`.

---

## 5. Nonce Reuse: Kesalahan Fatal

Ini adalah serangan paling terkenal pada DSA dan ECDSA.

Jika dua pesan `m1` dan `m2` ditandatangani dengan `k` yang sama:

```
s1 = k^(-1) * (z1 + x*r) mod q
s2 = k^(-1) * (z2 + x*r) mod q
```

Kurangkan:

```
s1 - s2 = k^(-1) * (z1 - z2) mod q
k = (z1 - z2) * (s1 - s2)^(-1) mod q
```

Setelah `k` diketahui:

```
x = (s1 * k - z1) * r^(-1) mod q
```

Kunci privat hilang sepenuhnya.

### Kasus nyata: Sony PlayStation 3

Pada 2010, grup fail0verflow menemukan bahwa Sony memakai nilai `k` statis pada firmware PS3. Kunci privat penandatangan firmware bisa dihitung dari dua tanda tangan, dan homebrew bisa ditandatangani agar diterima konsol.

### Kasus lain

- Bitcoin wallet dengan RNG bug.
- Android SecureRandom bug pada 2013, menyebabkan kunci ECDSA bocor.
- Berbagai library kripto dengan nonce bias.

### Mitigasi

**RFC 6979** mendefinisikan **deterministic ECDSA**: `k` diturunkan dari kunci privat dan hash pesan dengan HMAC-DRBG. Hasilnya:

- Tidak butuh RNG saat menandatangani.
- `k` tetap berbeda untuk setiap pesan.
- Tidak ada risiko RNG buruk.
- Tidak ada risiko nonce reuse.

Bitcoin dan banyak sistem modern memakai pendekatan ini.

---

## 6. Nonce Bias

Bahkan jika `k` tidak persis sama, bias kecil sudah cukup. Jika beberapa bit dari `k` cenderung nol, penyerang bisa memakai **lattice attack** (hidden number problem) untuk memulihkan kunci privat.

Kasus nyata: analisis tanda tangan ECDSA di blockchain menunjukkan banyak kunci privat bisa dipulihkan karena nonce tidak sepenuhnya acak.

Aturan: nonce harus seragam acak di seluruh rentang, atau deterministik sesuai RFC 6979.

---

## 7. DSA vs RSA vs ECDSA

| Aspek | DSA | RSA | ECDSA |
|---|---|---|---|
| Berbasis | Discrete log modulo p | Faktorisasi | Discrete log kurva eliptik |
| Enkripsi | Tidak bisa | Bisa | Tidak bisa |
| Ukuran tanda tangan | 2 kali q | seukuran n | 2 kali ukuran kurva |
| Keygen | Cepat | Lambat | Cepat |
| Verifikasi | Sedang | Cepat | Cepat |
| Ukuran kunci | Besar | Besar | Kecil |
| Standar | FIPS 186 | PKCS#1 | FIPS 186-4, SEC1 |
| Popularitas | Menurun | Tinggi | Tinggi |

DSA klasik jarang dipakai untuk sistem baru. ECDSA dan Ed25519 lebih umum. NIST bahkan mendorong transisi ke algoritma post-quantum.

---

## 8. ECDSA dan EdDSA

### ECDSA

Sama seperti DSA, tetapi grupnya adalah titik pada kurva eliptik:

```
r = (k * G).x mod n
s = k^(-1) * (z + x*r) mod n
```

Verifikasi memakai penjumlahan titik:

```
u1 = z * w mod n
u2 = r * w mod n
v = (u1 * G + u2 * Q).x mod n
```

Kurva populer: P-256, P-384, secp256k1.

### EdDSA (Ed25519)

EdDSA menghindari banyak jebakan ECDSA:

1. Nonce deterministik, tidak butuh RNG.
2. Tidak ada malleability tanda tangan.
3. Implementasi lebih sederhana dan constant time.
4. Verifikasi batch lebih mudah.

Ed25519 menjadi pilihan default di SSH, Signal, dan banyak protokol modern.

---

## 9. Implementasi Manual

File `dsa-digital-signature.py` berisi:

- Parameter domain `p` 1024 bit dan `q` 160 bit yang dibangkitkan khusus.
- Generator `g` dihitung dari `h^((p-1)/q) mod p`.
- Key generation, sign, verify.
- Fungsi `hash_to_int` yang memotong hash sesuai ukuran `q`.
- Demonstrasi serangan nonce reuse lengkap dengan pemulihan kunci privat.
- Demonstrasi bahaya nonce kecil.

Contoh keluaran:

```
p bits = 1024
q bits = 160
g berorder q: True
verifikasi pesan asli : True
verifikasi pesan ubah : False
pemulihan berhasil: True
```

Peringatan: parameter dan implementasi ini untuk belajar. DSA 1024 bit sudah dianggap lemah. Gunakan library seperti `cryptography` untuk produksi.

---

## 10. Kesalahan Umum

1. Memakai `k` yang sama atau `k` dari RNG lemah.
2. Memakai `k` dengan bias, misalnya mengambil modulo rentang yang tidak habis dibagi.
3. Lupa memeriksa `r = 0` atau `s = 0`.
4. Tidak memotong hash sesuai ukuran `q`.
5. Memverifikasi hanya sebagian tanda tangan, misalnya hanya `r`.
6. Memakai parameter domain yang tidak standar.
7. Mengabaikan kebutuhan CSPRNG.
8. Memakai DSA 1024 bit untuk data baru.

---

## 11. Latihan

1. Hitung tanda tangan DSA dengan `p = 23`, `q = 11`, `g = 2`, `x = 3`, `k = 5`, `z = 4`. Verifikasi hasilnya.
2. Tunjukkan bahwa mengganti `z` mengubah `s` tetapi tidak `r`.
3. Implementasikan pemulihan kunci dari dua tanda tangan dengan `k` sama.
4. Implementasikan ECDSA dengan `cryptography` dan bandingkan ukuran tanda tangan dengan RSA-3072.
5. Terapkan RFC 6979 untuk ECDSA dan tunjukkan bahwa dua tanda tangan pesan sama identik.
6. Jelaskan mengapa EdDSA tidak rentan terhadap nonce reuse.
7. Cari tahu bagaimana lattice attack memakai nonce yang bias.

---

## 12. Referensi

- [FIPS 186-5: Digital Signature Standard](https://csrc.nist.gov/publications/detail/fips/186/5/final)
- [RFC 6979: Deterministic ECDSA and DSA](https://www.rfc-editor.org/rfc/rfc6979)
- [RFC 8032: EdDSA](https://www.rfc-editor.org/rfc/rfc8032)
- [fail0verflow: PS3 ECDSA nonce reuse](https://fahrplan.events.ccc.de/congress/2010/Fahrplan/events/4087.en.html)
- Christof Paar dan Jan Pelzl, *Understanding Cryptography*, bab 10.

# 🧂 ElGamal

ElGamal adalah skema kunci publik yang diperkenalkan Taher Elgamal pada 1985. Ia menyediakan **enkripsi** dan **tanda tangan digital** sekaligus, keduanya berbasis Discrete Logarithm Problem. Banyak ide di dalamnya dipakai ulang oleh DSA, ECDSA, dan skema berbasis kurva eliptik.

---

## 1. Latar Belakang

ElGamal dibangun di atas Diffie-Hellman. Jika DH hanya bisa menyepakati kunci, ElGamal menambahkan mekanisme untuk mengenkripsi pesan dan menandatangani dokumen memakai struktur grup yang sama.

Sifat penting:

- Enkripsi **probabilistik**, karena setiap enkripsi memakai nonce acak.
- Ciphertext berukuran dua kali modulus.
- Bersifat **malleable**, ciphertext bisa diubah secara terkontrol.
- Tidak dipakai langsung untuk data besar, biasanya dipakai hybrid.

---

## 2. Parameter dan Kunci

```
p : bilangan prima besar
g : generator grup modulo p
x : kunci privat, 1 <= x <= p-2
y = g^x mod p : kunci publik
```

Seperti DH, sebaiknya pakai safe prime dan generator subgrup prima agar aman dari small subgroup attack.

---

## 3. Enkripsi

Untuk pesan `m` dengan `1 <= m <= p-1`:

1. Pilih `k` acak di `1..p-2`.
2. Hitung `c1 = g^k mod p`.
3. Hitung `s = y^k mod p`.
4. Hitung `c2 = m * s mod p`.
5. Ciphertext adalah `(c1, c2)`.

## 4. Dekripsi

1. Hitung `s = c1^x mod p`. Perhatikan bahwa:

```
c1^x = (g^k)^x = g^(k*x) = (g^x)^k = y^k = s
```

2. Hitung `m = c2 * s^(-1) mod p`.

Contoh kecil:

```
p = 23, g = 5, x = 6, y = 5^6 mod 23 = 8
m = 7, k = 3
c1 = 5^3 mod 23 = 10
s  = 8^3 mod 23 = 6
c2 = 7 * 6 mod 23 = 19

Dekripsi:
s  = 10^6 mod 23 = 6
m  = 19 * 6^(-1) mod 23 = 19 * 4 mod 23 = 7
```

---

## 5. Probabilistik

ElGamal memakai nonce `k` baru setiap enkripsi. Akibatnya:

```
E(m, k1) != E(m, k2)
```

Ini mencegah serangan tebakan langsung: penyerang tidak bisa mengenkripsi kandidat pesan dan membandingkan ciphertext, karena setiap enkripsi berbeda.

Bandingkan dengan textbook RSA yang deterministik. Inilah keunggulan desain ElGamal.

---

## 6. Malleability

ElGamal bersifat multiplikatif:

```
c2' = c2 * t mod p
```

Dekripsi `(c1, c2')` menghasilkan:

```
m' = m * t mod p
```

Penyerang yang tidak tahu kunci bisa mengubah plaintext dengan faktor yang dipilihnya. Jika `m` adalah nominal transfer, penyerang bisa mengalikannya.

Karena itu ElGamal **harus** dipasangkan dengan autentikasi, misalnya tanda tangan atau MAC, atau dipakai dalam konstruksi AEAD.

---

## 7. Nonce Reuse

Jika `k` yang sama dipakai untuk dua pesan:

```
c1 sama untuk kedua ciphertext
c2a / c2b = ma / mb mod p
```

Jika salah satu plaintext diketahui, plaintext lain bisa dihitung:

```
mb = ma * c2b * c2a^(-1) mod p
```

Ini sebabnya `k` harus unik dan tidak boleh diprediksi. Kesalahan ini juga muncul pada DSA dan ECDSA dengan akibat yang lebih parah, yaitu kebocoran kunci privat.

---

## 8. Tanda Tangan ElGamal

ElGamal juga bisa menandatangani. Untuk pesan dengan hash `H(m)`:

```
r = g^k mod p
s = (H(m) - x*r) * k^(-1) mod (p-1)
```

Verifikasi:

```
y^r * r^s mod p == g^H(m) mod p
```

Syarat: `gcd(k, p-1) = 1`, agar `k` punya invers modulo `p-1`.

### Kenapa verifikasi berhasil

```
r^s = g^(k*s) = g^(H(m) - x*r)
y^r * r^s = g^(x*r) * g^(H(m) - x*r) = g^H(m)
```

### Perbedaan dengan DSA

| Aspek | ElGamal | DSA |
|---|---|---|
| Modulus | p-1 | q, subgrup prima |
| Ukuran tanda tangan | 2 kali p | 2 kali q |
| Efisiensi | Lebih lambat | Lebih cepat |
| Aman dari subgroup | Perlu hati-hati | Ya, karena q prima |

DSA lahir sebagai perbaikan ElGamal signature agar lebih efisien dan aman.

---

## 9. ElGamal di Era Modern

ElGamal klasik sudah jarang dipakai langsung, tetapi idenya hidup di:

1. **DSA dan ECDSA**, yang mengambil struktur tanda tangan ElGamal.
2. **Cramer-Shoup**, varian ElGamal yang aman terhadap chosen ciphertext.
3. **Sistem voting elektronik**, karena sifat homomorfiknya berguna.
4. **Mixnet dan protokol privasi**, yang memanfaatkan re-randomisasi ciphertext.
5. **Kurva eliptik**, dalam bentuk ECIES.

### ECIES (Elliptic Curve Integrated Encryption Scheme)

ECIES adalah versi modern dari pola hybrid ElGamal:

1. Pihak pengirim membuat pasangan kunci ephemeral.
2. Menghitung shared secret dengan ECDH.
3. Menurunkan kunci simetris dengan HKDF.
4. Mengenkripsi data dengan AES-GCM atau ChaCha20-Poly1305.

Ini adalah cara yang benar untuk memakai ide ElGamal di dunia nyata.

---

## 10. Implementasi Manual

File `kode/03-asymmetric-encryption/elgamal.py` berisi:

- Enkripsi dan dekripsi integer dengan `(c1, c2)`.
- Demonstrasi sifat probabilistik.
- Demonstrasi malleability.
- Demonstrasi nonce reuse.
- Mode hybrid untuk data panjang: kunci sesi dienkripsi ElGamal, data di-XOR dengan keystream turunan hash.
- Tanda tangan dan verifikasi ElGamal.

Contoh keluaran:

```
dua enkripsi pesan sama berbeda: True
dekripsi ciphertext yang diubah = 35
hasilnya m * 5 = 35
c1 sama: True
verifikasi pesan asli : True
verifikasi pesan ubah : False
```

Catatan: implementasi memakai modulus 256 bit untuk kecepatan. Untuk keamanan nyata butuh minimal 2048 bit atau ECC.

---

## 11. Kesalahan Umum

1. Memakai `k` yang sama untuk dua enkripsi.
2. Memakai `k` dari RNG non-kriptografis.
3. Memakai ElGamal tanpa autentikasi, lalu menjadi korban malleability.
4. Memakai modulus terlalu kecil atau grup tanpa subgrup prima.
5. Mengenkripsi data besar langsung per blok tanpa mode yang benar.
6. Memakai `p-1` sebagai modulus tanda tangan padahal `p-1` komposit dan `k` mungkin tidak invertibel.
7. Menganggap ElGamal memberi integritas. Ia tidak.

---

## 12. Latihan

1. Enkripsi `m = 9` dengan `p = 23`, `g = 5`, `x = 4`, `k = 7`, lalu dekripsi.
2. Tunjukkan bahwa `c1^x == y^k mod p`.
3. Kalikan `c2` dengan 3 dan tunjukkan plaintext hasilnya juga dikali 3.
4. Ulangi enkripsi dengan `k` sama dan pulihkan plaintext yang tidak diketahui.
5. Tandatangani pesan dengan ElGamal dan verifikasi, lalu ubah satu bit pesan.
6. Bandingkan ukuran ciphertext ElGamal dengan RSA untuk modulus setara.
7. Implementasikan ECIES memakai library dan jelaskan mengapa ia lebih aman dari ElGamal mentah.

---

## 13. Referensi

- Taher Elgamal, *A Public Key Cryptosystem and a Signature Scheme Based on Discrete Logarithms*, 1985.
- [RFC 2631: Diffie-Hellman Key Agreement Method](https://www.rfc-editor.org/rfc/rfc2631)
- [SEC 1: Elliptic Curve Cryptography](https://www.secg.org/sec1-v2.pdf)
- Christof Paar dan Jan Pelzl, *Understanding Cryptography*, bab 8 dan 10.

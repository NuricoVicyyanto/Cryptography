# 🌀 Elliptic Curve Cryptography (ECC)

ECC adalah kriptografi kunci publik yang memakai struktur aljabar kurva eliptik. Keunggulannya sederhana tetapi sangat penting: **keamanan setara RSA dengan kunci jauh lebih kecil**. Kunci 256 bit ECC setara 3072 bit RSA, sehingga ECC mendominasi TLS modern, perangkat mobile, dan protokol kripto baru.

---

## 1. Persamaan Kurva

Bentuk yang paling umum untuk kriptografi adalah **short Weierstrass**:

```
y^2 = x^3 + a*x + b   (mod p)
```

Dengan `p` bilangan prima besar dan `a`, `b` konstanta. Kurva harus **non-singular**, yaitu diskriminan tidak nol:

```
4a^3 + 27b^2 != 0 (mod p)
```

Jika singular, titik-titiknya membentuk struktur yang mudah diserang.

Contoh kurva kecil `y^2 = x^3 + 2x + 2 mod 17` memiliki 18 titik afinitas plus satu titik infinity, total 19 titik.

---

## 2. Hukum Grup

Himpunan titik pada kurva plus titik infinity membentuk grup abelian dengan operasi penjumlahan.

### Aturan penjumlahan

Untuk `P = (x1, y1)` dan `Q = (x2, y2)` dengan `P != Q`:

```
lambda = (y2 - y1) / (x1 - x2) mod p
x3 = lambda^2 - x1 - x2
y3 = lambda * (x1 - x3) - y1
```

Untuk `P = Q` (doubling):

```
lambda = (3*x1^2 + a) / (2*y1) mod p
```

Untuk `P = -Q`, hasilnya titik infinity, yaitu elemen identitas.

Pembagian di sini adalah perkalian dengan invers modular, bukan pembagian biasa.

### Sifat grup

1. **Tertutup.** Hasil penjumlahan selalu titik pada kurva.
2. **Asosiatif.** `(P + Q) + R = P + (Q + R)`.
3. **Identitas.** `P + O = P`.
4. **Invers.** `P + (-P) = O`.
5. **Komutatif.** `P + Q = Q + P`.

---

## 3. Perkalian Skalar dan ECDLP

Perkalian skalar berarti menjumlahkan titik dengan dirinya sendiri `k` kali:

```
k * P = P + P + ... + P
```

Dihitung dengan **double and add**, kompleksitas `O(log k)`:

```
result = O
addend = P
while k:
    if k & 1: result += addend
    addend += addend
    k >>= 1
```

Keamanan ECC bertumpu pada **Elliptic Curve Discrete Logarithm Problem**:

```
Diberi P dan Q = k*P, temukan k.
```

Tidak ada algoritma klasik yang efisien untuk ini pada kurva yang baik. Berbeda dengan grup modulo prima, tidak ada indeks kalkulus yang efisien di kurva eliptik, sehingga ukuran kunci bisa jauh lebih kecil.

---

## 4. Kurva yang Umum

| Kurva | Ukuran | Bentuk | Dipakai di |
|---|---|---|---|
| secp256k1 | 256 bit | Weierstrass | Bitcoin, Ethereum |
| P-256 (secp256r1) | 256 bit | Weierstrass | TLS, FIPS, banyak sistem |
| P-384 | 384 bit | Weierstrass | TLS tingkat tinggi |
| Curve25519 | 255 bit | Montgomery | X25519, Signal, WireGuard |
| Ed25519 | 255 bit | Edwards | SSH, signature modern |

### secp256k1

```
p = 2^256 - 2^32 - 977
a = 0
b = 7
Gx = 79BE667E F9DCBBAC 55A06295 CE870B07 029BFCDB 2DCE28D9 59F2815B 16F81798
Gy = 483ADA77 26A3C465 5DA4FBFC 0E1108A8 FD17B448 A6855419 9C47D08F FB10D4B8
n  = FFFFFFFF FFFFFFFF FFFFFFFF FFFFFFFE BAAEDCE6 AF48A03B BFD25E8C D0364141
```

Parameter ini dipilih agar efisien, bukan karena alasan rahasia. Bitcoin memilihnya karena tersedia dan efisien.

### P-256

Kurva standar NIST dengan parameter yang dipilih lewat proses publik. Banyak dipakai di TLS. Beberapa pihak mengkhawatirkan kemungkinan parameter tersembunyi, meskipun tidak ada bukti serangan praktis.

### Curve25519 dan Ed25519

Dirancang Daniel J. Bernstein dengan fokus pada keamanan implementasi:

1. Tidak ada titik dengan order kecil yang bermasalah.
2. Rumus lengkap, tidak ada kasus khusus.
3. Constant time secara alami.
4. Tidak memakai tabel lookup besar.

Karena itu X25519 dan Ed25519 sangat disarankan untuk sistem baru.

---

## 5. ECDH

```
Alice: a acak, A = a*G
Bob  : b acak, B = b*G

Alice: S = a*B = a*b*G
Bob  : S = b*A = b*a*G
```

Keduanya mendapat titik `S`. Koordinat `x` dari `S` kemudian di-hash (biasanya dengan HKDF) menjadi kunci simetris.

Kenapa hanya `x`? Karena `y` bisa dihitung dari `x` dan pilihan tanda, sehingga tidak menambah entropi. Standar seperti X25519 menggunakan seluruh hasil pertukaran sebagai input KDF.

---

## 6. ECDSA

```
r = (k*G).x mod n
s = k^(-1) * (z + r*d) mod n
```

Verifikasi:

```
w = s^(-1) mod n
u1 = z*w mod n
u2 = r*w mod n
P = u1*G + u2*Q
valid jika P.x mod n == r
```

Sama seperti DSA, ECDSA bergantung pada nonce `k`:

- `k` berulang, kunci privat bocor.
- `k` bias, kunci privat bisa dipulihkan dengan lattice attack.
- `k` dari RNG lemah, bencana.

**RFC 6979** menurunkan `k` secara deterministik dari kunci privat dan hash pesan, menghilangkan ketergantungan pada RNG.

EdDSA (Ed25519) mengambil pendekatan berbeda dan secara desain menghindari masalah ini.

---

## 7. Kompresi Titik

Titik membutuhkan dua koordinat, tetapi `y` bisa dihitung dari `x`:

```
y^2 = x^3 + a*x + b mod p
```

Ada dua kemungkinan `y`, yaitu `y` dan `p - y`. Cukup simpan satu bit tanda, disebut **parity** atau sign bit.

```
Uncompressed: 04 || x (32 byte) || y (32 byte) = 65 byte
Compressed  : 02 atau 03 || x (32 byte)     = 33 byte
```

Menghemat hampir setengah ukuran kunci publik, penting untuk blockchain dan sertifikat.

---

## 8. Serangan pada Implementasi ECC

Matematika kurva kuat, implementasinya yang rapuh.

| Serangan | Kondisi | Mitigasi |
|---|---|---|
| Invalid curve attack | Implementasi tidak memvalidasi titik | Periksa titik pada kurva |
| Small subgroup | Kurva dengan cofactor besar | Periksa order, kalikan cofactor |
| Twist attack | Kurva menerima titik dari twist | Validasi kurva dan subgroup |
| Timing attack | Perkalian skalar bercabang | Montgomery ladder, constant time |
| Fault attack | Kesalahan hardware saat perkalian | Verifikasi hasil |
| Nonce reuse | ECDSA dengan k buruk | RFC 6979 |
| Invalid point pada ECDH | Peer mengirim titik di luar kurva | Validasi dan KDF |

Contoh invalid curve: penyerang mengirim titik pada kurva berbeda dengan order kecil. Jika implementasi tidak memeriksa, shared secret terurai menjadi bagian-bagian kecil dan bisa direkonstruksi.

---

## 9. ECC vs RSA

| Aspek | ECC | RSA |
|---|---|---|
| Ukuran kunci | 256 bit | 3072 bit |
| Ukuran tanda tangan | 64 byte | 384 byte |
| Keygen | Cepat | Lambat |
| Enkripsi | Tidak langsung, butuh ECIES | Langsung |
| Bandwidth | Hemat | Boros |
| Kematangan | Matang | Sangat matang |
| Resistensi kuantum | Rendah | Rendah |

Untuk perangkat dengan baterai, memori, dan bandwidth terbatas, ECC adalah pilihan yang jelas.

---

## 10. Implementasi di Folder Ini

`elliptic-curve.py` berisi:

- Kelas `Curve` dengan `add`, `double`, `mul`, `order_of`, `all_points`.
- Kurva kecil `y^2 = x^3 + 2x + 2 mod 17` untuk eksplorasi.
- Parameter secp256k1 lengkap.
- ECDH dengan validasi titik.
- ECDSA dengan nonce acak.
- Uji mandiri: `n*G = infinity` dan order titik kecil.

Contoh keluaran:

```
jumlah titik afinitas: 18 (termasuk infinity: 19)
order G = 19
19G = None (titik infinity)
n * G = infinity: True
verifikasi asli : True
verifikasi ubah : False
```

---

## 11. Kesalahan Umum

1. Membuat kurva sendiri tanpa audit. Gunakan kurva standar.
2. Tidak memvalidasi titik yang diterima dari pihak lain.
3. Memakai nonce ECDSA dari RNG lemah.
4. Mengabaikan cofactor pada kurva dengan cofactor besar.
5. Menggunakan perkalian skalar yang tidak constant time pada perangkat dengan penyerang fisik.
6. Memakai shared secret langsung sebagai kunci tanpa KDF.
7. Menyimpan kunci privat tanpa enkripsi.
8. Menganggap ECC aman dari komputer kuantum. Algoritma Shor memecahkan ECDLP.

---

## 12. Latihan

1. Enumerasi semua titik pada `y^2 = x^3 + 2x + 2 mod 17` dan hitung order setiap titik.
2. Implementasikan penjumlahan titik tanpa memakai library, lalu cocokkan dengan kode ini.
3. Hitung `k*G` untuk `k = 1..19` pada kurva kecil dan tunjukkan siklusnya.
4. Implementasikan kompresi dan dekompresi titik.
5. Rancang ECIES: ECDH, HKDF, lalu AES-GCM.
6. Tunjukkan bahwa nonce ECDSA yang sama pada dua pesan membocorkan kunci privat.
7. Bandingkan ukuran kunci dan tanda tangan ECC dengan RSA.
8. Jelaskan mengapa X25519 lebih mudah diimplementasikan dengan aman.

---

## 13. Referensi

- [SEC 1: Elliptic Curve Cryptography](https://www.secg.org/sec1-v2.pdf)
- [SEC 2: Recommended Curve Parameters](https://www.secg.org/sec2-v2.pdf)
- [RFC 7748: Curve25519 and Curve448](https://www.rfc-editor.org/rfc/rfc7748)
- [RFC 8032: EdDSA](https://www.rfc-editor.org/rfc/rfc8032)
- [SafeCurves](https://safecurves.cr.yp.to/)
- Christof Paar dan Jan Pelzl, *Understanding Cryptography*, bab 9.

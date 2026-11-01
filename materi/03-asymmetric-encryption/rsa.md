# 🔓 RSA (Rivest, Shamir, Adleman)

RSA adalah algoritma kriptografi kunci publik pertama yang praktis, dipublikasikan pada 1977. Namanya diambil dari Ron Rivest, Adi Shamir, dan Leonard Adleman. Selama hampir lima dekade ia menjadi tulang punggung keamanan internet: sertifikat TLS, tanda tangan kode, SSH, dan dokumen digital. RSA bertahan karena keamanannya mereduksi ke satu masalah matematika yang sangat sulit: **faktorisasi bilangan besar**.

---

## 1. Ide Dasar

Kriptografi kunci publik memisahkan dua kemampuan:

- **Kunci publik** untuk mengenkripsi dan memverifikasi.
- **Kunci privat** untuk mendekripsi dan menandatangani.

RSA bekerja karena perkalian dua bilangan prima besar mudah, tetapi mengembalikan hasil kali menjadi faktor-faktornya sangat sulit.

```
p dan q prima  ->  n = p * q    (mudah)
n              ->  p, q          (sulit)
```

Dengan `n` 2048 bit, `p` dan `q` masing-masing sekitar 1024 bit. Algoritma faktorisasi terbaik saat ini, General Number Field Sieve, membutuhkan waktu yang tidak praktis untuk ukuran tersebut.

---

## 2. Matematika di Baliknya

### Euler's Theorem

Jika `gcd(a, n) = 1`:

```
a^phi(n) ≡ 1 (mod n)
```

dengan `phi(n)` adalah totient Euler.

### Totient untuk modulus semiprima

Jika `n = p * q` dengan `p` dan `q` prima berbeda:

```
phi(n) = (p - 1) * (q - 1)
```

### Konstruksi kunci

1. Pilih dua prima besar `p` dan `q`.
2. Hitung `n = p * q`.
3. Hitung `phi(n) = (p - 1)(q - 1)`.
4. Pilih `e` dengan `1 < e < phi(n)` dan `gcd(e, phi(n)) = 1`. Biasanya `e = 65537`.
5. Hitung `d = e^(-1) mod phi(n)`.

Maka:

```
e * d ≡ 1 (mod phi(n))
```

### Kenapa dekripsi berhasil

```
c = m^e mod n
c^d = m^(e*d) = m^(1 + k*phi(n)) = m * (m^phi(n))^k ≡ m * 1^k ≡ m (mod n)
```

Kesetaraan terakhir memakai Euler's Theorem, dengan catatan `gcd(m, n) = 1`. Untuk kasus `m` berbagi faktor dengan `n`, hasilnya tetap berlaku melalui Chinese Remainder Theorem.

---

## 3. Contoh Angka Kecil

```
p = 61, q = 53
n = 3233
phi = 60 * 52 = 3120
e = 17                (gcd(17, 3120) = 1)
d = 2753              (17 * 2753 mod 3120 = 1)

Enkripsi m = 65:
c = 65^17 mod 3233 = 2790

Dekripsi:
m = 2790^2753 mod 3233 = 65
```

Angka ini hanya untuk ilustrasi. Keamanan nyata membutuhkan `n` minimal 2048 bit.

---

## 4. Enkripsi dan Dekripsi

```
Enkripsi : c = m^e mod n
Dekripsi : m = c^d mod n
```

Keduanya memakai eksponensial modular dengan kompleksitas `O(log d)`.

### Optimasi CRT

Dekripsi langsung dengan `d` 2048 bit lambat. Dengan Chinese Remainder Theorem, kita bekerja di modulo `p` dan `q` yang masing-masing 1024 bit:

```
dp = d mod (p - 1)
dq = d mod (q - 1)
qinv = q^(-1) mod p

m1 = c^dp mod p
m2 = c^dq mod q
h = qinv * (m1 - m2) mod p
m = m2 + h * q
```

Percepatan sekitar 3 sampai 4 kali lipat. Inilah sebabnya kunci privat RSA di dunia nyata selalu menyimpan `p`, `q`, `dp`, `dq`, dan `qinv`.

---

## 5. Padding: Bagian yang Wajib

RSA murni, disebut **textbook RSA**, bersifat deterministik dan multiplikatif. Tanpa padding, ia tidak aman.

### Masalah textbook RSA

1. **Deterministik.** Pesan sama menghasilkan ciphertext sama, sehingga penyerang tahu dua pesan identik.
2. **Multiplikatif.** `E(m1) * E(m2) = E(m1 * m2)`. Penyerang bisa memanipulasi ciphertext.
3. **Eksponen kecil.** Jika `e = 3` dan `m^3 < n`, ciphertext adalah kubik sempurna, dan pesan bisa diambil dengan akar pangkat tiga biasa.
4. **Tebakan.** Untuk pesan dari ruang kecil, penyerang cukup mengenkripsi semua kemungkinan.

### OAEP (Optimal Asymmetric Encryption Padding)

OAEP menambahkan keacakan sebelum enkripsi:

```
EM = 0x00 || maskedSeed || maskedDB
```

Prosesnya memakai dua hash (MGF1) dan seed acak. Hasilnya:

- Enkripsi menjadi probabilistik.
- Keacakan menyebar ke seluruh blok.
- Serangan chosen ciphertext menjadi jauh lebih sulit.

### PKCS#1 v1.5

Format lama yang masih banyak dipakai:

```
00 02 PS 00 M
```

`PS` adalah byte acak bukan nol minimal 8 byte. Lebih sederhana dari OAEP, tetapi lebih rentan, terutama pada implementasi yang membocorkan perbedaan error (Bleichenbacher attack).

Untuk enkripsi baru, gunakan **OAEP**. PKCS#1 v1.5 hanya dipertahankan untuk kompatibilitas.

---

## 6. Tanda Tangan Digital

RSA juga dipakai untuk tanda tangan. Urutannya dibalik:

```
Tanda tangan : s = H(m)^d mod n
Verifikasi   : H(m) == s^e mod n
```

### Skema padding untuk tanda tangan

**PKCS#1 v1.5**:

```
00 01 FF FF ... FF 00 DigestInfo(hash)
```

**PSS (Probabilistic Signature Scheme)**:

Menambahkan salt acak sehingga dua tanda tangan atas pesan sama menghasilkan nilai berbeda. PSS adalah pilihan modern dan direkomendasikan untuk protokol baru.

### Kenapa hash dulu

1. Pesan bisa lebih panjang dari modulus.
2. Hash mengurangi data menjadi ukuran tetap.
3. Hash mencegah pemalsuan dengan multiplikativitas.

### Kesalahan klasik

**Serangan Bleichenbacher 2006 pada tanda tangan PKCS#1 v1.5**: implementasi yang hanya memeriksa prefix `00 01 FF` tanpa memverifikasi panjang padding dan posisi separator bisa dipalsukan. Verifikasi harus memeriksa seluruh struktur, bukan sebagian.

---

## 7. Serangan Terhadap RSA

| Serangan | Kondisi | Mitigasi |
|---|---|---|
| Faktorisasi | `n` terlalu kecil | Gunakan 2048 bit atau lebih |
| Common modulus | Dua kunci berbagi `n` | Jangan bagikan modulus |
| Small exponent, no padding | `m^e < n` | Gunakan OAEP atau PSS |
| Hastad broadcast | `e` kecil, pesan sama ke banyak penerima | Padding acak |
| Wiener | `d` sangat kecil | `d` harus besar |
| Boneh-Durfee | `d < n^0.292` | `d` harus penuh |
| Fault attack | Kesalahan saat dekripsi CRT | Verifikasi hasil |
| Timing attack | Implementasi tidak constant time | Blinding, constant time |
| Bleichenbacher | Oracle pada PKCS#1 v1.5 | OAEP, pesan error seragam |
| Shared prime | RNG lemah, dua modulus berbagi prima | RNG kriptografis yang baik |

### Shared prime

Jika dua modulus `n1` dan `n2` berbagi satu prima, maka:

```
gcd(n1, n2) = p
```

Satu pemanggilan GCD membongkar kedua kunci. Serangan ini nyata pada perangkat IoT dengan RNG buruk. Pemeriksaan GCD massal terhadap kunci publik di internet pernah menemukan puluhan ribu kunci rentan.

---

## 8. Ukuran Kunci

| Ukuran | Status | Catatan |
|---|---|---|
| 512 bit | Tidak aman | Bisa difaktorkan dalam hitungan jam |
| 1024 bit | Tidak disarankan | Di luar batas NIST sejak 2013 |
| 2048 bit | Minimum saat ini | Standar industri |
| 3072 bit | Disarankan | Setara AES-128 dalam kekuatan |
| 4096 bit | Aman | Lebih lambat, manfaat terbatas |

Perbandingan NIST:

| Simetris | RSA | ECC |
|---|---|---|
| AES-128 | RSA-3072 | P-256 |
| AES-192 | RSA-7680 | P-384 |
| AES-256 | RSA-15360 | P-521 |

Karena itu ECC lebih populer untuk perangkat terbatas.

---

## 9. RSA vs ECC

| Aspek | RSA | ECC |
|---|---|---|
| Ukuran kunci | Besar | Kecil |
| Kecepatan keygen | Lambat | Cepat |
| Kecepatan enkripsi | Cepat | Sedang |
| Kecepatan dekripsi | Lambat | Cepat |
| Ukuran tanda tangan | Besar | Kecil |
| Kematangan | Sangat matang | Matang |
| Resistensi kuantum | Rendah | Rendah |

RSA mudah dipahami dan didukung di mana-mana. ECC lebih efisien. Keduanya akan digantikan oleh algoritma post-quantum seperti ML-KEM dan ML-DSA, yang sudah distandarkan NIST pada 2024.

---

## 10. Implementasi Manual

File `kode/03-asymmetric-encryption/rsa-from-scratch.py` memuat:

- Miller-Rabin dengan basis deterministik untuk bilangan di bawah 2^64.
- Pembangkitan prima yang memastikan `gcd(p-1, e) = 1`.
- Key generation dengan pemeriksaan panjang modulus.
- Enkripsi dan dekripsi integer.
- Dekripsi CRT dengan benchmark.
- Padding PKCS#1 v1.5 untuk enkripsi.
- Tanda tangan dan verifikasi PKCS#1 v1.5 dengan SHA-256.
- Demonstrasi determinisme, sifat multiplikatif, dan serangan eksponen kecil.

Jalankan:

```bash
python kode/03-asymmetric-encryption/rsa-from-scratch.py
```

Contoh keluaran:

```
RSAPublicKey(n_bits=1024, e=65537)
RSAPrivateKey(n_bits=1024, d_bits=1024)
waktu pembangkitan: 0.31 detik
dekripsi CRT sekitar 3x lebih cepat pada Python
verifikasi pesan asli : True
verifikasi pesan salah: False
```

---

## 11. Pemakaian di Dunia Nyata

Enkripsi langsung dengan RSA jarang dipakai karena lambat dan terbatas ukurannya. Pola yang benar adalah **hybrid encryption**:

1. Bangkitkan kunci simetris acak (AES-256 atau ChaCha20).
2. Enkripsi data dengan kunci simetris.
3. Enkripsi kunci simetris dengan RSA-OAEP.
4. Kirim kunci terenkripsi bersama data.

Ini adalah pola yang dipakai TLS, PGP, S/MIME, dan hampir semua sistem.

Dengan PyCryptodome:

```python
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.Random import get_random_bytes

key = RSA.generate(3072)
cipher_rsa = PKCS1_OAEP.new(key.publickey())

session_key = get_random_bytes(32)
encrypted_key = cipher_rsa.encrypt(session_key)

cipher_aes = AES.new(session_key, AES.MODE_GCM)
ciphertext, tag = cipher_aes.encrypt_and_digest(b"data besar")
```

---

## 12. Kesalahan Umum

1. Memakai RSA tanpa padding.
2. Memakai PKCS#1 v1.5 untuk enkripsi pada sistem baru.
3. Menggunakan modulus 1024 bit.
4. Membangkitkan `p` dan `q` dengan `random` biasa, bukan CSPRNG.
5. Memakai ulang `p` atau `q` untuk kunci berbeda.
6. Membocorkan perbedaan error antara padding salah dan data salah.
7. Menyimpan kunci privat tanpa enkripsi dan tanpa kontrol akses.
8. Membandingkan tanda tangan dengan `==` yang tidak constant time.
9. Menganggap RSA bisa menggantikan AES untuk data besar.

---

## 13. Latihan

1. Implementasikan OAEP dengan MGF1 dan bandingkan hasilnya dengan PyCryptodome.
2. Bangkitkan dua kunci RSA dan tunjukkan bahwa `gcd(n1, n2)` biasanya 1.
3. Simulasikan serangan common modulus.
4. Buktikan mengapa `d` kecil berbahaya dengan mempelajari serangan Wiener.
5. Ukur waktu pembangkitan kunci untuk 1024, 2048, dan 4096 bit.
6. Implementasikan hybrid encryption: RSA-OAEP membungkus kunci AES-GCM.
7. Verifikasi tanda tangan PSS memakai library dan jelaskan perbedaannya dengan v1.5.

---

## 14. Referensi

- [RFC 8017: PKCS#1 v2.2](https://www.rfc-editor.org/rfc/rfc8017), spesifikasi RSA, OAEP, dan PSS.
- [NIST SP 800-56B Rev 2](https://csrc.nist.gov/publications/detail/sp/800-56b/rev-2/final), key establishment.
- Dan Boneh, [Twenty Years of Attacks on the RSA Cryptosystem](https://crypto.stanford.edu/~dabo/papers/RSA-survey.pdf)
- Christof Paar dan Jan Pelzl, *Understanding Cryptography*, bab 7.
- [RSA Security Inc. PKCS#1](https://www.emc.com/collateral/white-papers/h11300-pkcs-1v2-2-rsa-cryptography-standard-wp.pdf)

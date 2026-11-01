# 📚 Materi Teori

Folder ini berisi seluruh bahan bacaan: teori, analisis, catatan, template, dan laporan. Tidak ada kode di sini. Semua implementasi ada di folder `kode/` pada tingkat yang sama.

## Aturan penomoran

1. **Angka di depan nama folder** menunjukkan urutan modul, misalnya `01-fondasi-matematika` sampai `06-riset-mandiri`.
2. **Angka di depan nama file** menunjukkan urutan baca di dalam modul.
3. Angka `01`, `02`, `03` dan seterusnya selalu dibaca berurutan, sehingga urutan materi tidak berubah meskipun diurutkan berdasarkan abjad.
4. Subfolder yang punya nomor, seperti `03-cipher-klasik` dan `05-hasil-eksperimen`, menempati posisi sesuai nomornya di dalam modul.

## Cara memakai

1. Baca materi sesuai nomor file.
2. Buka folder `kode/` dengan nama modul yang sama untuk menjalankan implementasinya.
3. Setiap materi yang punya kode akan menyebutkan path file kodenya.

## Urutan baca

### 01-fondasi-matematika

| No | File | Isi |
|---|---|---|
| 01 | [01-teori-bilangan.md](01-fondasi-matematika/01-teori-bilangan.md) | Bilangan prima, GCD, modulo, invers, eksponensial modular |
| 02 | [02-operasi-modular.md](01-fondasi-matematika/02-operasi-modular.md) | Aritmatika modular, EEA, CRT, generator, GF(2^8) |
| 03 | [03-cipher-klasik/cipher-klasik.md](01-fondasi-matematika/03-cipher-klasik/cipher-klasik.md) | Caesar, Vigenere, transposition, Playfair, Hill |

### 02-symmetric-encryption

| No | File | Isi |
|---|---|---|
| 01 | [01-aes.md](02-symmetric-encryption/01-aes.md) | Struktur AES, S-box, key expansion, mode operasi |
| 02 | [02-mode-cbc-vs-ecb.md](02-symmetric-encryption/02-mode-cbc-vs-ecb.md) | ECB dan CBC, bit flipping, padding oracle |
| 03 | [03-chacha20.md](02-symmetric-encryption/03-chacha20.md) | ChaCha20, Poly1305, AEAD |
| 04 | [04-padding-iv.md](02-symmetric-encryption/04-padding-iv.md) | PKCS#7, IV, nonce, nonce reuse |

### 03-asymmetric-encryption

| No | File | Isi |
|---|---|---|
| 01 | [01-rsa.md](03-asymmetric-encryption/01-rsa.md) | RSA, OAEP, tanda tangan, serangan |
| 02 | [02-diffie-hellman.md](03-asymmetric-encryption/02-diffie-hellman.md) | Pertukaran kunci, MITM, forward secrecy |
| 03 | [03-dsa.md](03-asymmetric-encryption/03-dsa.md) | DSA, nonce reuse, ECDSA, EdDSA |
| 04 | [04-elgamal.md](03-asymmetric-encryption/04-elgamal.md) | Enkripsi dan tanda tangan ElGamal |

### 04-hashing-authentication

| No | File | Isi |
|---|---|---|
| 01 | [01-hash-function.md](04-hashing-authentication/01-hash-function.md) | Properti hash, birthday, SHA-2, SHA-3, BLAKE |
| 02 | [02-hmac.md](04-hashing-authentication/02-hmac.md) | HMAC, length extension, HKDF |
| 03 | [03-password-hashing.md](04-hashing-authentication/03-password-hashing.md) | Salt, PBKDF2, bcrypt, scrypt, Argon2 |

### 05-advanced-crypto

| No | File | Isi |
|---|---|---|
| 01 | [01-ecc.md](05-advanced-crypto/01-ecc.md) | Kurva eliptik, ECDH, ECDSA |
| 02 | [02-zero-knowledge.md](05-advanced-crypto/02-zero-knowledge.md) | Sifat ZKP, Schnorr, Fiat-Shamir |
| 03 | [03-zk-snark-summary.md](05-advanced-crypto/03-zk-snark-summary.md) | R1CS, QAP, trusted setup, PLONK |
| 04 | [04-homomorphic-overview.md](05-advanced-crypto/04-homomorphic-overview.md) | Paillier, BFV, CKKS, TFHE |
| 05 | [05-mpc-overview.md](05-advanced-crypto/05-mpc-overview.md) | Secret sharing, garbled circuit, MPC |

### 06-riset-mandiri

| No | File | Isi |
|---|---|---|
| 01 | [01-metodologi-riset.md](06-riset-mandiri/01-metodologi-riset.md) | Merancang riset, model ancaman, validasi |
| 02 | [02-whitepaper-template.md](06-riset-mandiri/02-whitepaper-template.md) | Template laporan riset |
| 03 | [03-topik-riset.md](06-riset-mandiri/03-topik-riset.md) | 18 ide topik dengan metrik |
| 04 | [04-publikasi-blog.md](06-riset-mandiri/04-publikasi-blog.md) | Menulis dan menerbitkan artikel |
| 05 | [05-hasil-eksperimen/perbandingan-sha256-vs-blake3.md](06-riset-mandiri/05-hasil-eksperimen/perbandingan-sha256-vs-blake3.md) | Laporan benchmark dengan data nyata |

### resources

| No | File | Isi |
|---|---|---|
| 01 | [01-buku-referensi.md](resources/01-buku-referensi.md) | Buku dan sumber belajar beranotasi |
| 02 | [02-link-tools.md](resources/02-link-tools.md) | Library, playground, standar, CTF |
| 03 | [03-artikel-favorit.md](resources/03-artikel-favorit.md) | Artikel dan blog penting |

## Pasangan materi dan kode

| Modul | Materi | Kode |
|---|---|---|
| 01 | `materi/01-fondasi-matematika/` | `kode/01-fondasi-matematika/` |
| 02 | `materi/02-symmetric-encryption/` | `kode/02-symmetric-encryption/` |
| 03 | `materi/03-asymmetric-encryption/` | `kode/03-asymmetric-encryption/` |
| 04 | `materi/04-hashing-authentication/` | `kode/04-hashing-authentication/` |
| 05 | `materi/05-advanced-crypto/` | `kode/05-advanced-crypto/` |
| 06 | `materi/06-riset-mandiri/` | Tidak ada, modul dokumentasi |

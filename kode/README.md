# 💻 Kode Implementasi

Folder ini berisi seluruh implementasi Python. Semua teori dan penjelasan ada di folder `materi/` pada tingkat yang sama, dengan nama subfolder modul yang sama.

## Cara menjalankan

Jalankan dari akar repositori agar path konsisten.

```bash
python kode/01-fondasi-matematika/operasi-modular.py
python kode/01-fondasi-matematika/cipher-klasik/caesar.py
python kode/01-fondasi-matematika/cipher-klasik/vigenere.py
python kode/01-fondasi-matematika/cipher-klasik/transposition.py

python kode/02-symmetric-encryption/aes.py
python kode/02-symmetric-encryption/chacha20.py

python kode/03-asymmetric-encryption/rsa-from-scratch.py
python kode/03-asymmetric-encryption/diffie-hellman.py
python kode/03-asymmetric-encryption/dsa-digital-signature.py
python kode/03-asymmetric-encryption/elgamal.py

python kode/04-hashing-authentication/sha256-example.py
python kode/04-hashing-authentication/blake3-example.py
python kode/04-hashing-authentication/hmac.py
python kode/04-hashing-authentication/password-hashing.py

python kode/05-advanced-crypto/elliptic-curve.py
```

## Daftar file

| File | Isi | Uji internal |
|---|---|---|
| `01-fondasi-matematika/operasi-modular.py` | GCD, EEA, invers modular, eksponensial modular, CRT, generator | Ya |
| `01-fondasi-matematika/cipher-klasik/caesar.py` | Caesar cipher, chi-squared, brute force | Ya |
| `01-fondasi-matematika/cipher-klasik/vigenere.py` | Vigenere, Kasiski, Index of Coincidence | Ya |
| `01-fondasi-matematika/cipher-klasik/transposition.py` | Rail fence, columnar, route, brute force | Ya |
| `02-symmetric-encryption/aes.py` | AES-128/192/256, CBC, CTR, PKCS#7, vektor FIPS-197 | Ya |
| `02-symmetric-encryption/chacha20.py` | ChaCha20, Poly1305, vektor RFC 8439 | Ya |
| `03-asymmetric-encryption/rsa-from-scratch.py` | Miller-Rabin, RSA, CRT, PKCS#1 v1.5, tanda tangan | Ya |
| `03-asymmetric-encryption/diffie-hellman.py` | DH pada safe prime, MITM, forward secrecy | Ya |
| `03-asymmetric-encryption/dsa-digital-signature.py` | DSA, verifikasi, serangan nonce reuse | Ya |
| `03-asymmetric-encryption/elgamal.py` | Enkripsi, tanda tangan, malleability, hybrid | Ya |
| `04-hashing-authentication/sha256-example.py` | SHA-256 dari nol, length extension | Ya |
| `04-hashing-authentication/blake3-example.py` | BLAKE3 dari nol, tree hashing, XOF | Ya |
| `04-hashing-authentication/hmac.py` | HMAC, constant time compare, vektor RFC 4231 | Ya |
| `04-hashing-authentication/password-hashing.py` | PBKDF2 dan scrypt dari nol | Ya |
| `05-advanced-crypto/elliptic-curve.py` | Kurva eliptik, ECDH, ECDSA pada secp256k1 | Ya |

## Dependensi

Tidak ada dependensi wajib. Semua file berjalan dengan Python 3.10 atau lebih baru.

Opsional:

```bash
pip install pycryptodome   # perbandingan di 02-symmetric-encryption/aes.py
pip install blake3         # perbandingan library di 04-hashing-authentication/blake3-example.py
```

## Catatan

- File `04-hashing-authentication/hmac.py` bernama sama dengan modul standar Python. Skrip ini memuat modul standar lewat `importlib`, tetapi untuk proyek nyata sebaiknya gunakan nama file lain.
- Kode ini untuk pembelajaran, bukan produksi.

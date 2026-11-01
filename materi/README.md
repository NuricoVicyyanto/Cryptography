# 📚 Materi Teori

Folder ini berisi seluruh bahan bacaan: teori, analisis, catatan, template, dan laporan. Tidak ada kode di sini. Semua implementasi ada di folder `kode/` pada tingkat yang sama.

## Cara memakai

1. Baca materi sesuai urutan modul.
2. Buka folder `kode/` dengan nama modul yang sama untuk menjalankan implementasinya.
3. Setiap materi yang punya kode akan menyebutkan path file kodenya.

## Daftar materi

### 01-fondasi-matematika

- [teori-bilangan.md](01-fondasi-matematika/teori-bilangan.md): bilangan prima, GCD, modulo, invers, eksponensial modular.
- [operasi-modular.md](01-fondasi-matematika/operasi-modular.md): aritmatika modular, EEA, CRT, generator, aritmatika GF(2^8).
- [cipher-klasik/cipher-klasik.md](01-fondasi-matematika/cipher-klasik/cipher-klasik.md): Caesar, Vigenere, transposition, Playfair, Hill, dan kriptanalisisnya.

### 02-symmetric-encryption

- [aes.md](02-symmetric-encryption/aes.md): struktur AES, S-box, key expansion, mode operasi, keamanan.
- [mode-cbc-vs-ecb.md](02-symmetric-encryption/mode-cbc-vs-ecb.md): perbandingan ECB dan CBC, bit flipping, padding oracle.
- [chacha20.md](02-symmetric-encryption/chacha20.md): stream cipher ChaCha20, Poly1305, AEAD.
- [padding-iv.md](02-symmetric-encryption/padding-iv.md): PKCS#7, IV, nonce, nonce reuse.

### 03-asymmetric-encryption

- [rsa.md](03-asymmetric-encryption/rsa.md): teori RSA, padding OAEP, tanda tangan, serangan.
- [diffie-hellman.md](03-asymmetric-encryption/diffie-hellman.md): pertukaran kunci, MITM, forward secrecy, ECDH.
- [dsa.md](03-asymmetric-encryption/dsa.md): DSA, nonce reuse, ECDSA, EdDSA.
- [elgamal.md](03-asymmetric-encryption/elgamal.md): enkripsi dan tanda tangan ElGamal, malleability.

### 04-hashing-authentication

- [hash-function.md](04-hashing-authentication/hash-function.md): properti hash, birthday, SHA-2, SHA-3, BLAKE.
- [hmac.md](04-hashing-authentication/hmac.md): HMAC, length extension, HKDF, Encrypt-then-MAC.
- [password-hashing.md](04-hashing-authentication/password-hashing.md): salt, PBKDF2, bcrypt, scrypt, Argon2.

### 05-advanced-crypto

- [ecc.md](05-advanced-crypto/ecc.md): kurva eliptik, ECDH, ECDSA, serangan implementasi.
- [zero-knowledge.md](05-advanced-crypto/zero-knowledge.md): sifat ZKP, Schnorr, Fiat-Shamir.
- [zk-snark-summary.md](05-advanced-crypto/zk-snark-summary.md): R1CS, QAP, trusted setup, Groth16, PLONK.
- [homomorphic-overview.md](05-advanced-crypto/homomorphic-overview.md): Paillier, BFV, CKKS, TFHE.
- [mpc-overview.md](05-advanced-crypto/mpc-overview.md): secret sharing, garbled circuit, Beaver triple.

### 06-riset-mandiri

- [metodologi-riset.md](06-riset-mandiri/metodologi-riset.md): merancang riset, model ancaman, validasi.
- [whitepaper-template.md](06-riset-mandiri/whitepaper-template.md): template laporan riset.
- [topik-riset.md](06-riset-mandiri/topik-riset.md): 18 ide topik dengan metrik dan tingkat kesulitan.
- [publikasi-blog.md](06-riset-mandiri/publikasi-blog.md): menulis dan menerbitkan artikel teknis.
- [hasil-eksperimen/perbandingan-sha256-vs-blake3.md](06-riset-mandiri/hasil-eksperimen/perbandingan-sha256-vs-blake3.md): laporan benchmark dengan data nyata.

### resources

- [buku-referensi.md](resources/buku-referensi.md): buku dan sumber belajar beranotasi.
- [link-tools.md](resources/link-tools.md): library, playground, standar, CTF.
- [artikel-favorit.md](resources/artikel-favorit.md): artikel dan blog penting.

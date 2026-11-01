# 🛠️ Tools, Library, dan Playground

Daftar alat yang berguna untuk belajar, mengimplementasikan, menguji, dan menganalisis kriptografi. Semua tautan mengarah ke sumber resmi.

---

## 1. Library Python

| Library | Kegunaan | Catatan |
|---|---|---|
| [cryptography](https://cryptography.io/) | High-level dan low-level | Pilihan utama untuk produksi |
| [PyCryptodome](https://www.pycryptodome.org/) | Cipher, mode, KDF | API mudah, dipakai di materi ini |
| [pyca/bcrypt](https://github.com/pyca/bcrypt) | Password hashing | Bindings bcrypt |
| [argon2-cffi](https://argon2-cffi.readthedocs.io/) | Argon2 | Pilihan utama password |
| [PyNaCl](https://pynacl.readthedocs.io/) | libsodium binding | X25519, Ed25519, secretbox |
| [blake3](https://pypi.org/project/blake3/) | BLAKE3 | Cepat, dengan SIMD |
| [py_ecc](https://github.com/ethereum/py_ecc) | Kurva eliptik | Edukatif, dipakai Ethereum |
| [gmpy2](https://pypi.org/project/gmpy2/) | Aritmatika presisi tinggi | Cepat untuk bilangan besar |
| [sympy](https://www.sympy.org/) | Matematika simbolik | Berguna untuk eksplorasi |
| [pwntools](https://pwntools.com/) | Eksploitasi dan CTF | Termasuk util kripto |

### Instalasi cepat

```bash
pip install cryptography pycryptodome argon2-cffi bcrypt pynacl blake3
```

---

## 2. Library Bahasa Lain

### C dan C++

| Library | Catatan |
|---|---|
| [OpenSSL](https://www.openssl.org/) | Standar de facto, lengkap |
| [libsodium](https://libsodium.org/) | API aman, sulit disalahgunakan |
| [mbed TLS](https://tls.mbed.org/) | Ringan untuk embedded |
| [BoringSSL](https://boringssl.googlesource.com/boringssl/) | Fork Google, dipakai Chrome |
| [wolfSSL](https://www.wolfssl.com/) | Kecil, untuk perangkat terbatas |

### Rust

| Library | Catatan |
|---|---|
| [RustCrypto](https://github.com/RustCrypto) | Kumpulan crate per algoritma |
| [ring](https://github.com/briansmith/ring) | Fokus keamanan dan performa |
| [aws-lc-rs](https://github.com/awslabs/aws-lc-rs) | Berbasis AWS-LC |

### Go

| Library | Catatan |
|---|---|
| [crypto standard library](https://pkg.go.dev/crypto) | Lengkap dan stabil |
| [golang.org/x/crypto](https://pkg.go.dev/golang.org/x/crypto) | Algoritma tambahan |

### JavaScript

| Library | Catatan |
|---|---|
| [Web Crypto API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Crypto_API) | Bawaan browser |
| [libsodium.js](https://github.com/jedisct1/libsodium.js) | libsodium di browser |
| [tweetnacl-js](https://tweetnacl.js.org/) | Kecil dan auditabel |

### Java dan Kotlin

| Library | Catatan |
|---|---|
| [JCA/JCE](https://docs.oracle.com/javase/8/docs/technotes/guides/security/crypto/CryptoSpec.html) | Bawaan JDK |
| [Bouncy Castle](https://www.bouncycastle.org/) | Lengkap, termasuk post-quantum |
| [Tink](https://developers.google.com/tink) | API aman dari Google |

---

## 3. Playground dan Alat Visual

| Alat | Kegunaan |
|---|---|
| [CyberChef](https://gchq.github.io/CyberChef/) | Encode, decode, cipher, analisis |
| [CrypTool](https://www.cryptool.org/) | Edukasi interaktif |
| [AES Animation](https://formaestudio.com/rijndaelinspector/archivos/Rijndael_Animation_v4_eng-html5.html) | Visualisasi AES langkah demi langkah |
| [SHA-256 Visualization](https://sha256algorithm.com/) | Visualisasi kompresi SHA-256 |
| [ECDSA Visualization](https://www.desmos.com/calculator) | Eksplorasi kurva eliptik |
| [Desmos](https://www.desmos.com/calculator) | Plot kurva eliptik |
| [Wolfram Alpha](https://www.wolframalpha.com/) | Perhitungan matematika |

---

## 4. Alat Analisis dan Debug

| Alat | Kegunaan |
|---|---|
| [Wireshark](https://www.wireshark.org/) | Analisis lalu lintas TLS |
| [openssl s_client](https://www.openssl.org/docs/man1.1.1/man1/s_client.html) | Inspeksi handshake TLS |
| [testssl.sh](https://testssl.sh/) | Audit konfigurasi TLS |
| [sslyze](https://github.com/nabla-c0d3/sslyze) | Scanner TLS berbasis Python |
| [nmap ssl-enum-ciphers](https://nmap.org/) | Enumerasi cipher |
| [hashcat](https://hashcat.net/) | Pemulihan password, audit |
| [John the Ripper](https://www.openwall.com/john/) | Audit password |
| [binwalk](https://github.com/ReFirmLabs/binwalk) | Analisis firmware |
| [Ghidra](https://ghidra-sre.org/) | Reverse engineering binary |
| [radare2](https://rada.re/n/) | Reverse engineering |

Gunakan alat ofensif hanya pada sistem yang Anda miliki atau punya izin tertulis.

---

## 5. Standar dan Spesifikasi

| Sumber | Isi |
|---|---|
| [NIST CSRC](https://csrc.nist.gov/) | FIPS, SP 800 series |
| [RFC Editor](https://www.rfc-editor.org/) | Protokol internet |
| [IETF Datatracker](https://datatracker.ietf.org/) | Draft dan diskusi |
| [SECG](https://www.secg.org/) | Standar kurva eliptik |
| [W3C WebCrypto](https://www.w3.org/TR/WebCryptoAPI/) | API kripto browser |
| [PKCS#11](https://docs.oasis-open.org/pkcs11/pkcs11-base/v2.40/) | API hardware security module |

### Standar yang wajib dikenal

| Nomor | Isi |
|---|---|
| FIPS 197 | AES |
| FIPS 180-4 | SHA-1 dan SHA-2 |
| FIPS 202 | SHA-3 dan SHAKE |
| FIPS 186-5 | DSA, ECDSA, EdDSA |
| SP 800-38A | Mode operasi block cipher |
| SP 800-38D | GCM |
| SP 800-56A | Key establishment |
| SP 800-63B | Autentikasi dan password |
| SP 800-90A | Random number generation |
| RFC 2104 | HMAC |
| RFC 5869 | HKDF |
| RFC 7748 | Curve25519 |
| RFC 8032 | EdDSA |
| RFC 8439 | ChaCha20-Poly1305 |
| RFC 9106 | Argon2 |

---

## 6. CTF dan Latihan

| Sumber | Fokus |
|---|---|
| [Cryptohack](https://cryptohack.org/) | Kriptografi modern, bertingkat |
| [CryptoPals](https://cryptopals.com/) | Implementasi dan serangan |
| [picoCTF](https://picoctf.org/) | Pemula |
| [OverTheWire](https://overthewire.org/) | Dasar keamanan |
| [Root Me](https://www.root-me.org/) | Tantangan luas |
| [Hack The Box](https://www.hackthebox.com/) | Lab dan mesin |
| [CTFtime](https://ctftime.org/) | Kalender CTF |

Rute yang disarankan: Cryptohack untuk konsep, CryptoPals untuk implementasi, lalu CTF untuk penerapan.

---

## 7. Alat Matematika

| Alat | Kegunaan |
|---|---|
| [SageMath](https://www.sagemath.org/) | Aljabar, kurva eliptik, lattice |
| [Pari/GP](https://pari.math.u-bordeaux.fr/) | Teori bilangan |
| [Magma](http://magma.maths.usyd.edu.au/) | Komputasi aljabar (berbayar) |
| [fpylll](https://github.com/fplll/fpylll) | Lattice reduction |
| [z3](https://github.com/Z3Prover/z3) | SMT solver, berguna untuk kriptanalisis |
| [sympy](https://www.sympy.org/) | Matematika simbolik |

Contoh penggunaan SageMath untuk kurva eliptik:

```python
E = EllipticCurve(GF(17), [2, 2])
G = E(5, 1)
print(G.order())
print(3 * G)
```

---

## 8. Alat Khusus

### Zero-Knowledge

| Alat | Kegunaan |
|---|---|
| [circom](https://docs.circom.io/) | Bahasa circuit |
| [snarkjs](https://github.com/iden3/snarkjs) | Pembuatan dan verifikasi SNARK |
| [Halo2](https://github.com/zcash/halo2) | Framework PLONK |
| [Noir](https://noir-lang.org/) | Bahasa untuk ZK |

### Homomorphic Encryption

| Alat | Kegunaan |
|---|---|
| [Microsoft SEAL](https://github.com/microsoft/SEAL) | BFV dan CKKS |
| [OpenFHE](https://www.openfhe.org/) | Banyak skema |
| [TFHE-rs](https://github.com/zama-ai/tfhe-rs) | TFHE di Rust |
| [Concrete](https://github.com/zama-ai/concrete) | Compiler TFHE |

### MPC

| Alat | Kegunaan |
|---|---|
| [MP-SPDZ](https://github.com/data61/MP-SPDZ) | Banyak protokol |
| [EMP-toolkit](https://github.com/emp-toolkit) | Garbled circuit |
| [ABY](https://github.com/encryptogroup/ABY) | Hybrid protocol |
| [Frigate](https://github.com/lsils/frigate) | Compiler circuit |

---

## 9. Utilitas Baris Perintah

### OpenSSL

```bash
# Hash file
openssl dgst -sha256 file.bin

# Enkripsi AES-256-GCM (contoh sederhana, bukan untuk produksi)
openssl enc -aes-256-gcm -pbkdf2 -iter 600000 -in plain.txt -out cipher.bin

# Buat kunci RSA
openssl genpkey -algorithm RSA -pkeyopt rsa_keygen_bits:3072 -out key.pem

# Inspeksi sertifikat
openssl s_client -connect example.com:443 -servername example.com

# Tanda tangan
openssl dgst -sha256 -sign key.pem -out sig.bin file.bin
```

### Python one-liner

```bash
python -c "import hashlib; print(hashlib.sha256(b'abc').hexdigest())"
```

---

## 10. Referensi Cepat

| Kebutuhan | Alat yang disarankan |
|---|---|
| Enkripsi data aplikasi | `cryptography` dengan AES-GCM atau ChaCha20 |
| Password | `argon2-cffi` |
| Tanda tangan | `cryptography` dengan Ed25519 |
| Pertukaran kunci | `cryptography` dengan X25519 |
| Hash file | `hashlib` atau `b3sum` |
| Analisis cepat | CyberChef |
| Belajar algoritma | Implementasi manual di repo ini |
| Audit TLS | `testssl.sh` |
| CTF | Cryptohack dan CryptoPals |

---

## 11. Catatan Keamanan

1. Jangan memakai library yang tidak dirawat.
2. Periksa riwayat CVE sebelum memilih library.
3. Jangan menulis kriptografi sendiri untuk produksi.
4. Jangan menyalin kode dari Stack Overflow tanpa memahami asal-usulnya.
5. Perhatikan lisensi.
6. Perbarui dependensi secara berkala.
7. Verifikasi checksum unduhan.

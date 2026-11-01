# 📁 Struktur Repo GitHub: Belajar & Riset Kriptografi

Struktur folder ini ditujukan untuk membangun portofolio dan repositori belajar yang terorganisir, lengkap dengan dokumentasi, eksperimen, dan catatan konsep.

```bash
kriptografi-research-roadmap/
├── README.md
├── 01-fondasi-matematika/
│   ├── teori-bilangan.md                  # Konsep bilangan prima, GCD, modulo
│   ├── operasi-modular.md                 # Modular arithmetic, inverse mod
│   ├── operasi-modular.py                 # Implementasi modular exponentiation
│   └── cipher-klasik/
│       ├── caesar.py                      # Implementasi Caesar Cipher
│       ├── vigenere.py                    # Implementasi Vigenère Cipher
│       ├── transposition.py               # Implementasi Transposition Cipher
│       └── cipher-klasik.md               # Catatan analisis cipher klasik
├── 02-symmetric-encryption/
│   ├── aes.md                             # Teori AES dan mode operasi
│   ├── aes.py                             # Implementasi AES dengan PyCryptodome
│   ├── mode-cbc-vs-ecb.md                 # Analisis perbandingan mode
│   ├── chacha20.md                        # Penjelasan ChaCha20
│   ├── chacha20.py                        # Implementasi ChaCha20
│   └── padding-iv.md                      # Konsep padding dan IV
├── 03-asymmetric-encryption/
│   ├── rsa.md                             # Teori RSA dan aplikasinya
│   ├── rsa-from-scratch.py                # Implementasi RSA dari nol
│   ├── diffie-hellman.md                  # Teori dan aplikasi DH Key Exchange
│   ├── diffie-hellman.py                  # Simulasi pertukaran kunci
│   ├── dsa.md                             # Teori DSA & Digital Signature
│   ├── dsa-digital-signature.py           # Implementasi DSA
│   ├── elgamal.md                         # Penjelasan ElGamal
│   └── elgamal.py                         # Implementasi ElGamal
├── 04-hashing-authentication/
│   ├── hash-function.md                   # SHA family, BLAKE, properti hash
│   ├── sha256-example.py                  # Simulasi SHA-256
│   ├── blake3-example.py                  # Contoh BLAKE3
│   ├── password-hashing.md                # Teknik hashing password
│   ├── password-hashing.py                # PBKDF2, bcrypt, scrypt
│   ├── hmac.md                            # Konsep HMAC
│   └── hmac.py                            # Implementasi HMAC
├── 05-advanced-crypto/
│   ├── ecc.md                             # Dasar ECC
│   ├── elliptic-curve.py                  # Contoh ECC
│   ├── zero-knowledge.md                  # Zero Knowledge Proofs
│   ├── zk-snark-summary.md               # Ringkasan konsep zk-SNARK
│   ├── homomorphic-overview.md            # Konsep dasar homomorphic encryption
│   └── mpc-overview.md                    # Secure MPC overview
├── 06-riset-mandiri/
│   ├── metodologi-riset.md                # Cara merancang penelitian kriptografi
│   ├── whitepaper-template.md             # Template laporan riset
│   ├── topik-riset.md                     # Ide-ide topik riset
│   ├── hasil-eksperimen/
│   │   └── perbandingan-sha256-vs-blake3.md
│   └── publikasi-blog.md                  # Panduan membuat artikel publikasi
├── resources/
│   ├── buku-referensi.md                  # Daftar buku & sumber belajar
│   ├── link-tools.md                      # Link tools, library, dan playground
│   └── artikel-favorit.md                 # Kumpulan artikel teknis penting
└── LICENSE
```

## 📘 README.md (Contoh Isi)
```markdown
# Belajar & Riset Kriptografi

Repositori ini berisi pembelajaran terstruktur, eksperimen, dan proyek riset di bidang kriptografi. Tujuan utama: menjadi peneliti mandiri yang memahami teori dan praktik keamanan digital.

## Struktur
- 📚 Bulan 1: Fondasi Matematika
- 🔐 Bulan 2: Kriptografi Simetris
- 🔓 Bulan 3: Kriptografi Asimetris
- #️⃣ Bulan 4: Fungsi Hash & Autentikasi
- 🚀 Bulan 5: Topik Lanjut
- 🧪 Bulan 6: Penelitian & Publikasi

## Kontribusi
Silakan fork, clone, dan tambahkan eksperimen Anda sendiri!
```

---

## ✅ Status Isi Repo

Seluruh materi pada struktur di atas sudah terisi lengkap.

| Folder | Isi | Status |
|---|---|---|
| `01-fondasi-matematika/` | Teori bilangan, aritmatika modular, implementasi, cipher klasik | Lengkap |
| `02-symmetric-encryption/` | AES dari nol, mode operasi, ChaCha20, padding dan IV | Lengkap |
| `03-asymmetric-encryption/` | RSA, Diffie-Hellman, DSA, ElGamal, semuanya dari nol | Lengkap |
| `04-hashing-authentication/` | SHA-256, BLAKE3, HMAC, password hashing | Lengkap |
| `05-advanced-crypto/` | ECC, zero-knowledge, zk-SNARK, homomorphic, MPC | Lengkap |
| `06-riset-mandiri/` | Metodologi, template, topik riset, laporan eksperimen | Lengkap |
| `resources/` | Buku, tools, artikel rujukan | Lengkap |

Seluruh skrip Python sudah diuji dan berjalan tanpa dependensi eksternal, kecuali bagian opsional yang disebutkan di bawah.

---

## ▶️ Cara Menjalankan

```bash
python --version          # butuh Python 3.10 atau lebih baru

# Fondasi matematika dan cipher klasik
python 01-fondasi-matematika/operasi-modular.py
python 01-fondasi-matematika/cipher-klasik/caesar.py
python 01-fondasi-matematika/cipher-klasik/vigenere.py
python 01-fondasi-matematika/cipher-klasik/transposition.py

# Kriptografi simetris
python 02-symmetric-encryption/aes.py
python 02-symmetric-encryption/chacha20.py

# Kriptografi asimetris
python 03-asymmetric-encryption/rsa-from-scratch.py
python 03-asymmetric-encryption/diffie-hellman.py
python 03-asymmetric-encryption/dsa-digital-signature.py
python 03-asymmetric-encryption/elgamal.py

# Hash dan autentikasi
python 04-hashing-authentication/sha256-example.py
python 04-hashing-authentication/blake3-example.py
python 04-hashing-authentication/hmac.py
python 04-hashing-authentication/password-hashing.py

# Topik lanjut
python 05-advanced-crypto/elliptic-curve.py
```

### Dependensi opsional

Tidak ada dependensi wajib. Beberapa bagian bersifat opsional dan akan dilewati jika library tidak tersedia.

```bash
pip install pycryptodome   # perbandingan AES manual dengan library di 02-symmetric-encryption/aes.py
pip install blake3         # perbandingan BLAKE3 dengan library C di 04-hashing-authentication/blake3-example.py
pip install argon2-cffi    # contoh Argon2 di 04-hashing-authentication/password-hashing.md
```

Catatan: file `04-hashing-authentication/hmac.py` bernama sama dengan modul standar Python. Jalankan dari folder lain atau muat modul standar lewat `importlib` seperti yang dilakukan skrip tersebut.

---

## 🧭 Urutan Belajar yang Disarankan

1. **Bulan 1, fondasi matematika.** Baca `teori-bilangan.md` dan `operasi-modular.md`, lalu jalankan `operasi-modular.py`.
2. **Bulan 1, cipher klasik.** Baca `cipher-klasik/cipher-klasik.md`, jalankan tiga skrip cipher, lalu coba kriptanalisisnya.
3. **Bulan 2, simetris.** Baca `aes.md` dan `chacha20.md`, jalankan implementasi, lalu baca `mode-cbc-vs-ecb.md` dan `padding-iv.md`.
4. **Bulan 3, asimetris.** Mulai dari `rsa.md`, lanjut ke Diffie-Hellman, DSA, dan ElGamal.
5. **Bulan 4, hash dan autentikasi.** Baca `hash-function.md` dan `hmac.md`, lalu `password-hashing.md`.
6. **Bulan 5, topik lanjut.** ECC, zero-knowledge, homomorphic encryption, dan MPC.
7. **Bulan 6, riset.** Ikuti `06-riset-mandiri/metodologi-riset.md`, pilih topik, tulis laporan dengan template, lalu publikasikan.

---

## ⚠️ Catatan Keamanan

Kode di repositori ini ditulis untuk pembelajaran. Beberapa implementasi sengaja tidak constant time, memakai parameter kecil, atau memakai padding sederhana agar mudah dipahami. Jangan memakai kode ini untuk melindungi data nyata. Untuk produksi gunakan library teruji seperti `cryptography`, `libsodium`, atau `OpenSSL`.

---

## 📜 Lisensi

MIT. Lihat file `LICENSE`.

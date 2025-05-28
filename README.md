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
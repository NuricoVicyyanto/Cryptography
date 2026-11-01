# 📁 Struktur Repo GitHub: Belajar & Riset Kriptografi

Struktur folder ini ditujukan untuk membangun portofolio dan repositori belajar yang terorganisir, lengkap dengan dokumentasi, eksperimen, dan catatan konsep.

Repositori dipisah menjadi dua pohon agar mudah dibaca:

- `materi/` berisi seluruh teori, analisis, catatan, template, dan laporan dalam format Markdown.
- `kode/` berisi seluruh implementasi dalam format Python.
- Nama subfolder modul sama di kedua pohon, sehingga teori dan kodenya mudah dipasangkan.

```bash
kriptografi-research-roadmap/
├── README.md
├── LICENSE
│
├── materi/                                   # SEMUA TEORI DAN CATATAN (Markdown)
│   ├── README.md                             # Indeks materi dan urutan baca
│   ├── 01-fondasi-matematika/
│   │   ├── 01-teori-bilangan.md              # Bilangan prima, GCD, modulo
│   │   ├── 02-operasi-modular.md             # Aritmatika modular, EEA, CRT
│   │   └── 03-cipher-klasik/
│   │       └── cipher-klasik.md              # Analisis cipher klasik
│   ├── 02-symmetric-encryption/
│   │   ├── 01-aes.md                         # Teori AES dan mode operasi
│   │   ├── 02-mode-cbc-vs-ecb.md             # Perbandingan ECB dan CBC
│   │   ├── 03-chacha20.md                    # Penjelasan ChaCha20
│   │   └── 04-padding-iv.md                  # Padding dan IV
│   ├── 03-asymmetric-encryption/
│   │   ├── 01-rsa.md                         # Teori RSA dan aplikasinya
│   │   ├── 02-diffie-hellman.md              # Teori DH Key Exchange
│   │   ├── 03-dsa.md                         # Teori DSA dan tanda tangan
│   │   └── 04-elgamal.md                     # Penjelasan ElGamal
│   ├── 04-hashing-authentication/
│   │   ├── 01-hash-function.md               # SHA family, BLAKE, properti hash
│   │   ├── 02-hmac.md                        # Konsep HMAC
│   │   └── 03-password-hashing.md            # Teknik hashing password
│   ├── 05-advanced-crypto/
│   │   ├── 01-ecc.md                         # Dasar ECC
│   │   ├── 02-zero-knowledge.md              # Zero Knowledge Proofs
│   │   ├── 03-zk-snark-summary.md            # Ringkasan zk-SNARK
│   │   ├── 04-homomorphic-overview.md        # Homomorphic encryption
│   │   └── 05-mpc-overview.md                # Secure MPC overview
│   ├── 06-riset-mandiri/
│   │   ├── 01-metodologi-riset.md            # Cara merancang penelitian
│   │   ├── 02-whitepaper-template.md         # Template laporan riset
│   │   ├── 03-topik-riset.md                 # Ide topik riset
│   │   ├── 04-publikasi-blog.md              # Panduan artikel publikasi
│   │   └── 05-hasil-eksperimen/
│   │       └── perbandingan-sha256-vs-blake3.md
│   └── resources/
│       ├── 01-buku-referensi.md              # Daftar buku dan sumber belajar
│       ├── 02-link-tools.md                  # Tools, library, playground
│       └── 03-artikel-favorit.md             # Artikel teknis penting
│
└── kode/                                     # SEMUA IMPLEMENTASI (Python)
    ├── README.md                             # Indeks dan cara menjalankan
    ├── 01-fondasi-matematika/
    │   ├── operasi-modular.py                # Modular exponentiation, EEA, CRT
    │   └── cipher-klasik/
    │       ├── caesar.py                     # Caesar Cipher dan kriptanalisis
    │       ├── vigenere.py                   # Vigenere, Kasiski, IC
    │       └── transposition.py              # Rail fence, columnar, route
    ├── 02-symmetric-encryption/
    │   ├── aes.py                            # AES-128/192/256, CBC, CTR
    │   └── chacha20.py                       # ChaCha20 dan Poly1305
    ├── 03-asymmetric-encryption/
    │   ├── rsa-from-scratch.py               # RSA, PKCS#1 v1.5, CRT
    │   ├── diffie-hellman.py                 # DH, MITM, forward secrecy
    │   ├── dsa-digital-signature.py          # DSA dan serangan nonce reuse
    │   └── elgamal.py                        # Enkripsi dan tanda tangan ElGamal
    ├── 04-hashing-authentication/
    │   ├── sha256-example.py                 # SHA-256 dan length extension
    │   ├── blake3-example.py                 # BLAKE3, tree hashing, XOF
    │   ├── password-hashing.py               # PBKDF2 dan scrypt
    │   └── hmac.py                           # HMAC dan constant time compare
    └── 05-advanced-crypto/
        └── elliptic-curve.py                 # ECC, ECDH, ECDSA
```

### Aturan penamaan

| Folder | Isi | Ekstensi |
|---|---|---|
| `materi/` | Teori, analisis, catatan, template, laporan | `.md` |
| `kode/` | Implementasi, eksperimen, benchmark | `.py` |

Nama subfolder modul (`01-fondasi-matematika`, `02-symmetric-encryption`, dan seterusnya) sama persis di kedua pohon. Untuk membaca teori modul 2, buka `materi/02-symmetric-encryption/`. Untuk menjalankan kodenya, buka `kode/02-symmetric-encryption/`.

### Aturan penomoran materi

| Posisi angka | Arti | Contoh |
|---|---|---|
| Depan nama folder modul | Urutan modul | `01-fondasi-matematika`, `02-symmetric-encryption` |
| Depan nama file materi | Urutan baca di dalam modul | `01-aes.md`, `02-mode-cbc-vs-ecb.md`, `03-chacha20.md` |
| Depan nama subfolder materi | Urutan topik di dalam modul | `03-cipher-klasik/`, `05-hasil-eksperimen/` |

Nomor selalu dibaca berurutan, sehingga urutan materi tetap sama meskipun folder diurutkan berdasarkan abjad. Indeks lengkap dengan urutan baca ada di [`materi/README.md`](materi/README.md).

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

| Modul | Materi (`materi/`) | Kode (`kode/`) | Status |
|---|---|---|---|
| 01 Fondasi Matematika | Teori bilangan, operasi modular, cipher klasik | Operasi modular, Caesar, Vigenere, transposition | Lengkap |
| 02 Simetris | AES, mode operasi, ChaCha20, padding dan IV | AES dari nol, ChaCha20 dan Poly1305 | Lengkap |
| 03 Asimetris | RSA, Diffie-Hellman, DSA, ElGamal | Semua algoritma diimplementasikan dari nol | Lengkap |
| 04 Hash dan Autentikasi | Fungsi hash, HMAC, password hashing | SHA-256, BLAKE3, HMAC, PBKDF2, scrypt | Lengkap |
| 05 Topik Lanjut | ECC, ZKP, zk-SNARK, homomorphic, MPC | ECC, ECDH, ECDSA | Lengkap |
| 06 Riset Mandiri | Metodologi, template, topik, laporan eksperimen | Tidak ada, modul ini bersifat dokumentasi | Lengkap |
| resources | Buku, tools, artikel rujukan | Tidak ada | Lengkap |

Seluruh skrip Python sudah diuji dan berjalan tanpa dependensi eksternal, kecuali bagian opsional yang disebutkan di bawah.

---

## ▶️ Cara Menjalankan

```bash
python --version          # butuh Python 3.10 atau lebih baru

# Fondasi matematika dan cipher klasik
python kode/01-fondasi-matematika/operasi-modular.py
python kode/01-fondasi-matematika/cipher-klasik/caesar.py
python kode/01-fondasi-matematika/cipher-klasik/vigenere.py
python kode/01-fondasi-matematika/cipher-klasik/transposition.py

# Kriptografi simetris
python kode/02-symmetric-encryption/aes.py
python kode/02-symmetric-encryption/chacha20.py

# Kriptografi asimetris
python kode/03-asymmetric-encryption/rsa-from-scratch.py
python kode/03-asymmetric-encryption/diffie-hellman.py
python kode/03-asymmetric-encryption/dsa-digital-signature.py
python kode/03-asymmetric-encryption/elgamal.py

# Hash dan autentikasi
python kode/04-hashing-authentication/sha256-example.py
python kode/04-hashing-authentication/blake3-example.py
python kode/04-hashing-authentication/hmac.py
python kode/04-hashing-authentication/password-hashing.py

# Topik lanjut
python kode/05-advanced-crypto/elliptic-curve.py
```

### Dependensi opsional

Tidak ada dependensi wajib. Beberapa bagian bersifat opsional dan akan dilewati jika library tidak tersedia.

```bash
pip install pycryptodome   # perbandingan AES manual dengan library di kode/02-symmetric-encryption/aes.py
pip install blake3         # perbandingan BLAKE3 dengan library C di kode/04-hashing-authentication/blake3-example.py
pip install argon2-cffi    # contoh Argon2 di materi/04-hashing-authentication/03-password-hashing.md
```

Catatan: file `kode/04-hashing-authentication/hmac.py` bernama sama dengan modul standar Python. Jalankan dari folder lain atau muat modul standar lewat `importlib` seperti yang dilakukan skrip tersebut.

---

## 🧭 Urutan Belajar yang Disarankan

1. **Bulan 1, fondasi matematika.** Baca `materi/01-fondasi-matematika/01-teori-bilangan.md` dan `02-operasi-modular.md`, lalu jalankan `kode/01-fondasi-matematika/operasi-modular.py`.
2. **Bulan 1, cipher klasik.** Baca `materi/01-fondasi-matematika/03-cipher-klasik/cipher-klasik.md`, jalankan tiga skrip di `kode/01-fondasi-matematika/cipher-klasik/`, lalu coba kriptanalisisnya.
3. **Bulan 2, simetris.** Baca `materi/02-symmetric-encryption/01-aes.md` dan `03-chacha20.md`, jalankan kode di `kode/02-symmetric-encryption/`, lalu baca `02-mode-cbc-vs-ecb.md` dan `04-padding-iv.md`.
4. **Bulan 3, asimetris.** Mulai dari `materi/03-asymmetric-encryption/01-rsa.md`, lanjut ke Diffie-Hellman, DSA, dan ElGamal, dengan kode di `kode/03-asymmetric-encryption/`.
5. **Bulan 4, hash dan autentikasi.** Baca `materi/04-hashing-authentication/01-hash-function.md` dan `02-hmac.md`, lalu `03-password-hashing.md`, dan jalankan kode di `kode/04-hashing-authentication/`.
6. **Bulan 5, topik lanjut.** Baca materi di `materi/05-advanced-crypto/`, lalu jalankan `kode/05-advanced-crypto/elliptic-curve.py`.
7. **Bulan 6, riset.** Ikuti `materi/06-riset-mandiri/01-metodologi-riset.md`, pilih topik, tulis laporan dengan template, lalu publikasikan.

---

## ⚠️ Catatan Keamanan

Kode di repositori ini ditulis untuk pembelajaran. Beberapa implementasi sengaja tidak constant time, memakai parameter kecil, atau memakai padding sederhana agar mudah dipahami. Jangan memakai kode ini untuk melindungi data nyata. Untuk produksi gunakan library teruji seperti `cryptography`, `libsodium`, atau `OpenSSL`.

---

## 📜 Lisensi

MIT. Lihat file `LICENSE`.

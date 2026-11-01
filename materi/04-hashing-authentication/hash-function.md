# #️⃣ Fungsi Hash: SHA, BLAKE, dan Propertinya

Fungsi hash kriptografis mengubah data sepanjang apa pun menjadi sidik jari berukuran tetap. Ia adalah pondasi integritas data, tanda tangan digital, password, blockchain, dan struktur data terautentikasi.

---

## 1. Definisi dan Sifat Wajib

Fungsi hash kriptografis `H` harus memenuhi:

| Sifat | Arti | Konsekuensi jika gagal |
|---|---|---|
| Deterministik | Input sama selalu menghasilkan output sama | Tidak bisa dipakai verifikasi |
| Cepat | Murah untuk dihitung | Tidak praktis |
| Preimage resistant | Diberi `h`, sulit menemukan `m` dengan `H(m) = h` | Rahasia bisa dibuka dari hash |
| Second preimage resistant | Diberi `m1`, sulit menemukan `m2 != m1` dengan `H(m1) = H(m2)` | Dokumen bisa diganti |
| Collision resistant | Sulit menemukan pasangan `m1 != m2` dengan hash sama | Tanda tangan bisa dipalsukan |
| Avalanche | Perubahan 1 bit input mengubah sekitar 50 persen bit output | Pola bisa dilacak |

Collision resistance lebih lemah dari preimage resistance secara alami, karena serangan birthday hanya butuh `2^(n/2)` percobaan.

---

## 2. Serangan Birthday

Jika hash memiliki `n` bit output, mencari collision butuh sekitar `2^(n/2)` percobaan, bukan `2^n`.

```
Peluang collision kira-kira 1 - exp(-k^2 / (2 * 2^n))
Untuk peluang 50 persen: k sekitar 1.177 * 2^(n/2)
```

Artinya:

| Output | Preimage | Collision |
|---|---|---|
| 128 bit | 2^128 | 2^64 |
| 160 bit | 2^160 | 2^80 |
| 256 bit | 2^256 | 2^128 |
| 512 bit | 2^512 | 2^256 |

Inilah alasan SHA-1 (160 bit) sudah tidak aman untuk collision: 2^80 bisa dicapai dengan GPU dan teknik diferensial. Pada 2017, Google dan CWI memproduksi collision SHA-1 nyata (SHAttered) dengan biaya sekitar 110 ribu dolar GPU.

---

## 3. Merkle-Damgard dan Length Extension

SHA-1 dan SHA-2 memakai konstruksi Merkle-Damgard:

1. Pesan di-padding ke kelipatan blok.
2. Setiap blok dikompresi bersama state sebelumnya.
3. State akhir menjadi digest.

```
h0 = IV
h1 = f(h0, block1)
h2 = f(h1, block2)
...
digest = h_last
```

### Konsekuensi: length extension

Jika `H(secret || message)` diketahui, penyerang bisa menghitung `H(secret || message || padding || extra)` tanpa mengetahui `secret`, karena ia bisa melanjutkan kompresi dari state yang bocor.

Mitigasi:

1. Gunakan HMAC, bukan `H(key || message)`.
2. Gunakan konstruksi sponge seperti SHA-3.
3. Gunakan hash berbasis tree seperti BLAKE3 dengan mode keyed.

Contoh serangan ini ada di `kode/04-hashing-authentication/sha256-example.py`.

---

## 4. Keluarga SHA-2

| Algoritma | Output | Blok | Round | Konstanta |
|---|---|---|---|---|
| SHA-224 | 224 bit | 512 bit | 64 | SHA-256 |
| SHA-256 | 256 bit | 512 bit | 64 | SHA-256 |
| SHA-384 | 384 bit | 1024 bit | 80 | SHA-512 |
| SHA-512 | 512 bit | 1024 bit | 80 | SHA-512 |
| SHA-512/256 | 256 bit | 1024 bit | 80 | SHA-512 |

SHA-256 memakai 32 bit word, SHA-512 memakai 64 bit word. Pada CPU 64 bit, SHA-512 sering lebih cepat dari SHA-256 meskipun outputnya lebih panjang.

Konstanta SHA-256 berasal dari akar kuadrat dan akar pangkat tiga bilangan prima pertama:

```
H[i] = 32 bit pertama frac(sqrt(prime_i))
K[i] = 32 bit pertama frac(cbrt(prime_i))
```

### Struktur satu round SHA-256

```
T1 = h + Sigma1(e) + Ch(e,f,g) + K[i] + W[i]
T2 = Sigma0(a) + Maj(a,b,c)
h=g, g=f, f=e, e=d+T1, d=c, c=b, b=a, a=T1+T2
```

Fungsi `Ch`, `Maj`, `Sigma` adalah kombinasi boolean dan rotasi yang menciptakan non-linearitas dan diffusion.

---

## 5. SHA-3 dan Sponge

SHA-3 (Keccak) memenangkan kompetisi NIST pada 2012. Ia memakai konstruksi **sponge**, bukan Merkle-Damgard.

```
State besar (1600 bit)
Phase absorb : XOR pesan ke state, lalu permutasi
Phase squeeze: keluarkan bagian state, permutasi lagi jika perlu
```

Keuntungan:

1. Tidak rentan length extension.
2. Bisa menjadi XOF (SHAKE128, SHAKE256).
3. Paralel dan sederhana di hardware.
4. Margin keamanan besar.

Kelemahan: lebih lambat dari SHA-256 di banyak CPU karena belum ada akselerasi luas.

---

## 6. BLAKE2 dan BLAKE3

### BLAKE2

Dirilis 2012, lebih cepat dari MD5 tetapi sekuat SHA-3. Dua varian:

- BLAKE2b: 64 bit word, output sampai 64 byte, optimal untuk CPU 64 bit.
- BLAKE2s: 32 bit word, output sampai 32 byte, optimal untuk perangkat kecil.

BLAKE2 mendukung keyed hashing, salt, personalization, dan tree hashing.

### BLAKE3

Dirilis 2020, menggabungkan BLAKE2s dengan struktur pohon dan XOF.

| Aspek | BLAKE2b | BLAKE3 |
|---|---|---|
| Round | 12 | 7 |
| Struktur | Iteratif atau tree opsional | Tree wajib |
| Paralelisme | Opsional | Bawaan |
| XOF | Tidak | Ya |
| Kecepatan | Cepat | Sangat cepat, bisa beberapa GB/detik |
| Kriptanalisis | Matang | Relatif baru |

BLAKE3 membagi input menjadi chunk 1024 byte, membangun pohon biner, dan menggabungkan chaining value. Karena itu ia bisa memanfaatkan SIMD dan multi-core secara alami.

Contoh implementasi ada di `kode/04-hashing-authentication/blake3-example.py`, termasuk uji vektor resmi.

---

## 7. Perbandingan Algoritma

| Algoritma | Output | Status | Catatan |
|---|---|---|---|
| MD5 | 128 bit | Rusak total | Collision dalam hitungan detik |
| SHA-1 | 160 bit | Rusak untuk collision | SHAttered 2017 |
| SHA-256 | 256 bit | Aman | Standar industri |
| SHA-512 | 512 bit | Aman | Cepat di CPU 64 bit |
| SHA-3-256 | 256 bit | Aman | Sponge, tahan length extension |
| BLAKE2b | sampai 512 bit | Aman | Sangat cepat |
| BLAKE3 | variabel | Aman | Tercepat, XOF, paralel |
| RIPEMD-160 | 160 bit | Cukup | Dipakai Bitcoin |

Untuk sistem baru: SHA-256, SHA-512, SHA-3, atau BLAKE3. Jangan memakai MD5 atau SHA-1 untuk tujuan keamanan apa pun.

---

## 8. Hash Bukan Enkripsi

| Aspek | Hash | Enkripsi |
|---|---|---|
| Arah | Satu arah | Dua arah |
| Kunci | Tidak perlu | Perlu |
| Output | Tetap | Seukuran input |
| Tujuan | Integritas | Kerahasiaan |
| Reversibel | Tidak | Ya dengan kunci |

Meng-hash password bukan berarti menyimpannya dengan aman. Untuk password, hash cepat pun tidak cukup, perlu KDF lambat seperti Argon2. Lihat `password-hashing.md`.

---

## 9. Aplikasi

1. **Integritas file.** Unduhan menyertakan checksum SHA-256.
2. **Tanda tangan digital.** Hash pesan lebih dulu, lalu tanda tangani hash.
3. **HMAC.** MAC berbasis hash untuk autentikasi pesan.
4. **Password.** Dengan KDF lambat dan salt.
5. **Struktur data terautentikasi.** Merkle tree, hash chain.
6. **Blockchain.** Hash blok sebelumnya mengikat riwayat.
7. **Content addressing.** Git memakai SHA-1 atau SHA-256 dari isi objek.
8. **Deduplikasi.** Menyimpan satu salinan data identik.
9. **Derivasi kunci.** HKDF menurunkan kunci dari shared secret.
10. **Proof of work.** Mencari nonce dengan hash di bawah target.

---

## 10. Merkle Tree

Untuk memverifikasi satu bagian dari data besar tanpa mengunduh semuanya:

```
          root
        /      \
     H(AB)     H(CD)
     /  \      /  \
   H(A) H(B) H(C) H(D)
```

Membuktikan `A` hanya butuh `H(B)`, `H(CD)`, dan root. Ukuran bukti `O(log n)`.

Dipakai di Git, IPFS, Certificate Transparency, dan blockchain.

---

## 11. Kesalahan Umum

1. Memakai MD5 atau SHA-1 untuk keamanan.
2. Memakai `H(key || message)` sebagai MAC. Rentan length extension.
3. Membandingkan hash dengan `==` yang tidak constant time saat dipakai untuk verifikasi rahasia.
4. Memakai hash cepat untuk password.
5. Lupa salt pada penyimpanan password.
6. Memotong hash terlalu pendek, misalnya 64 bit, sehingga birthday attack menjadi mudah.
7. Menganggap hash memberi autentikasi. Hash saja tidak.
8. Memakai hash yang sama untuk dua tujuan berbeda tanpa key separation.

---

## 12. Latihan

1. Implementasikan SHA-256 dan bandingkan dengan hashlib untuk 100 ukuran acak.
2. Tunjukkan length extension pada `H(key || message)` dan jelaskan mengapa HMAC kebal.
3. Hitung berapa percobaan yang dibutuhkan untuk collision pada hash 64 bit.
4. Bandingkan kecepatan SHA-256, BLAKE2b, dan BLAKE3 pada file 100 MB.
5. Bangun Merkle tree sederhana dan buat proof untuk satu elemen.
6. Jelaskan mengapa SHA-3 tidak rentan length extension.
7. Rancang skema checksum untuk rilis perangkat lunak yang tahan manipulasi.

---

## 13. Referensi

- [FIPS 180-4: Secure Hash Standard](https://csrc.nist.gov/publications/detail/fips/180/4/final)
- [FIPS 202: SHA-3 Standard](https://csrc.nist.gov/publications/detail/fips/202/final)
- [RFC 7693: BLAKE2](https://www.rfc-editor.org/rfc/rfc7693)
- [BLAKE3 specification](https://github.com/BLAKE3-team/BLAKE3-specs/blob/master/blake3.pdf)
- [SHAttered: SHA-1 collision](https://shattered.io/)
- Christof Paar dan Jan Pelzl, *Understanding Cryptography*, bab 11.

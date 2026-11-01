# 🧪 Perbandingan SHA-256 vs BLAKE3

Laporan eksperimen mandiri: mengukur throughput lima fungsi hash pada tiga ukuran data, membandingkan implementasi library dengan implementasi Python murni, dan menganalisis kapan masing-masing sebaiknya dipakai.

Tanggal pengukuran: November 2026.

---

## 1. Tujuan

1. Mengukur throughput SHA-256, SHA3-256, BLAKE2b, BLAKE2s, dan BLAKE3 pada data 1 KB, 1 MB, dan 10 MB.
2. Membandingkan BLAKE3 dengan BLAKE2b sebagai generasi sebelumnya.
3. Membandingkan implementasi library (C) dengan implementasi Python murni dari folder `04-hashing-authentication`.
4. Menjelaskan penyebab perbedaan performa dari sisi desain algoritma.

---

## 2. Lingkungan Pengujian

| Komponen | Nilai |
|---|---|
| Sistem operasi | Windows |
| Python | 3.13.15 |
| Library | hashlib bawaan, paket `blake3` |
| Implementasi manual | `kode/04-hashing-authentication/sha256-example.py`, `kode/04-hashing-authentication/blake3-example.py` |
| Metode waktu | `time.perf_counter`, nilai minimum dari 7 pengulangan |
| Sumber data | `os.urandom` |

Nilai minimum dipakai untuk mengurangi noise dari proses lain. Setiap algoritma menerima data yang sama dan output yang sudah dihitung sehingga kompilasi atau alokasi tidak mendominasi.

---

## 3. Hasil

### Data 1 MB

| Algoritma | Waktu | Throughput |
|---|---|---|
| SHA-256 | 2.242 ms | 446.1 MB/detik |
| SHA3-256 | 3.055 ms | 327.4 MB/detik |
| BLAKE2b | 1.973 ms | 506.8 MB/detik |
| BLAKE2s | 3.687 ms | 271.2 MB/detik |
| BLAKE3 | 0.371 ms | 2694.7 MB/detik |

### Data 10 MB

| Algoritma | Waktu | Throughput |
|---|---|---|
| SHA-256 | 28.087 ms | 356.0 MB/detik |
| SHA3-256 | 32.641 ms | 306.4 MB/detik |
| BLAKE2b | 22.637 ms | 441.7 MB/detik |
| BLAKE2s | 32.808 ms | 304.8 MB/detik |
| BLAKE3 | 3.592 ms | 2783.8 MB/detik |

### Data 1 KB

| Algoritma | Waktu | Throughput |
|---|---|---|
| SHA-256 | 3 mikrodetik | 295.9 MB/detik |
| SHA3-256 | 4 mikrodetik | 232.5 MB/detik |
| BLAKE2b | 2 mikrodetik | 424.6 MB/detik |
| BLAKE2s | 3 mikrodetik | 295.9 MB/detik |
| BLAKE3 | 2 mikrodetik | 514.0 MB/detik |

Pada data kecil, biaya overhead pemanggilan fungsi mendominasi, sehingga perbedaan antar algoritma menyempit.

### Implementasi Python murni, 64 KB

| Implementasi | Waktu | Throughput |
|---|---|---|
| SHA-256 manual | 343.7 ms | 0.186 MB/detik |
| BLAKE3 manual | 142.7 ms | 0.448 MB/detik |

Implementasi Python murni sekitar 1000 kali lebih lambat dari implementasi C. Ini bukan kelemahan algoritma, melainkan biaya interpreter dan operasi per byte di level Python.

---

## 4. Rasio

Perbandingan terhadap SHA-256 pada 10 MB:

| Algoritma | Relatif terhadap SHA-256 |
|---|---|
| SHA-256 | 1.00 |
| SHA3-256 | 0.86 |
| BLAKE2b | 1.24 |
| BLAKE2s | 0.86 |
| BLAKE3 | 7.82 |

BLAKE3 sekitar 7.8 kali lebih cepat dari SHA-256 pada mesin ini, dan sekitar 6.3 kali lebih cepat dari BLAKE2b.

---

## 5. Analisis

### Kenapa BLAKE3 cepat

1. **Struktur pohon.** Input dibagi menjadi chunk 1024 byte yang bisa diproses paralel. Implementasi C memanfaatkan SIMD dan multi-core.
2. **Hanya 7 round.** BLAKE2s memakai 10 round, SHA-256 memakai 64 round dengan operasi 32 bit yang lebih banyak per byte.
3. **Operasi word 32 bit sederhana.** Penjumlahan, XOR, dan rotasi, tanpa tabel besar.
4. **Sedikit ketergantungan antar blok.** Setiap chunk independen, sehingga CPU bisa melakukan out-of-order execution lebih agresif.

### Kenapa SHA-256 lebih lambat

1. 64 round per blok 512 bit.
2. Message schedule 64 word per blok.
3. Ketergantungan serial pada state.
4. Tanpa struktur paralel di dalam hash tunggal.

Namun SHA-256 punya akselerasi hardware di banyak CPU (SHA-NI), sehingga pada prosesor yang mendukung, throughput bisa jauh lebih tinggi dari angka di sini.

### Kenapa SHA3-256 paling lambat di pengujian ini

Keccak memakai permutasi 24 round pada state 1600 bit. Beban per byte lebih besar, dan akselerasi hardware belum seluas SHA-256.

### Kenapa BLAKE2b lebih cepat dari BLAKE2s

BLAKE2b memakai word 64 bit, cocok untuk CPU 64 bit modern. BLAKE2s memakai word 32 bit dan lebih cocok untuk perangkat kecil. Pada mesin 64 bit, BLAKE2b unggul.

---

## 6. Diskusi

### Apakah BLAKE3 selalu pilihan terbaik

Tidak. Pertimbangan:

1. **Kematangan kriptanalisis.** SHA-256 sudah dianalisis lebih dari dua dekade. BLAKE3 relatif baru, meskipun berbasis BLAKE2 yang lebih matang.
2. **Dukungan platform.** SHA-256 tersedia di mana-mana, termasuk hardware dan FIPS. BLAKE3 belum tersedia di semua library standar.
3. **Kebutuhan XOF.** Jika butuh output variabel, BLAKE3 sangat cocok. Jika hanya butuh 32 byte, keunggulannya berkurang.
4. **Kepatuhan.** Lingkungan yang mewajibkan FIPS harus memakai SHA-2 atau SHA-3.

### Kapan memilih apa

| Kebutuhan | Pilihan |
|---|---|
| Kompatibilitas maksimal | SHA-256 |
| Kepatuhan FIPS | SHA-256 atau SHA-3 |
| Kecepatan di software | BLAKE3 |
| Hash dengan key dan salt | BLAKE2b |
| XOF | SHAKE atau BLAKE3 |
| Password | Argon2id, bukan hash cepat |

---

## 7. Keterbatasan

1. Pengukuran hanya pada satu mesin dan satu sistem operasi.
2. Tidak mengukur penggunaan memori atau konsumsi daya.
3. Implementasi manual Python tidak constant time dan bukan pembanding performa yang adil.
4. Paket `blake3` memakai implementasi C dengan SIMD, sehingga perbandingan mencerminkan kualitas implementasi juga, bukan hanya algoritma.
5. Ukuran 10 MB belum cukup untuk menguji perilaku cache pada data sangat besar.
6. Tidak mengukur latensi untuk input sangat kecil yang umum di protokol jaringan.

---

## 8. Kesimpulan

1. BLAKE3 paling cepat pada semua ukuran yang diuji, dengan keunggulan terbesar pada data besar.
2. BLAKE2b mengungguli SHA-256 sekitar 24 persen pada 10 MB.
3. SHA3-256 lebih lambat di lingkungan tanpa akselerasi khusus.
4. Implementasi Python murni tidak layak untuk produksi, tetapi sangat berharga untuk memahami detail algoritma.
5. Pemilihan algoritma harus mempertimbangkan keamanan, kompatibilitas, dan kepatuhan, bukan hanya kecepatan.

---

## 9. Cara Mengulang Eksperimen

```python
import hashlib, os, time

def bench(fn, data, repeats=7):
    best = float("inf")
    for _ in range(repeats):
        start = time.perf_counter()
        fn(data)
        best = min(best, time.perf_counter() - start)
    return best

data = os.urandom(10 * 1024 * 1024)
for name, fn in [
    ("SHA-256", lambda d: hashlib.sha256(d).digest()),
    ("SHA3-256", lambda d: hashlib.sha3_256(d).digest()),
    ("BLAKE2b", lambda d: hashlib.blake2b(d).digest()),
    ("BLAKE2s", lambda d: hashlib.blake2s(d).digest()),
]:
    t = bench(fn, data)
    print(f"{name}: {10 / t:.1f} MB/detik")
```

Untuk BLAKE3:

```bash
pip install blake3
```

```python
import blake3
t = bench(lambda d: blake3.blake3(d).digest(), data)
print(f"BLAKE3: {10 / t:.1f} MB/detik")
```

---

## 10. Referensi

- [BLAKE3 specification](https://github.com/BLAKE3-team/BLAKE3-specs/blob/master/blake3.pdf)
- [FIPS 180-4](https://csrc.nist.gov/publications/detail/fips/180/4/final)
- [FIPS 202](https://csrc.nist.gov/publications/detail/fips/202/final)
- [RFC 7693: BLAKE2](https://www.rfc-editor.org/rfc/rfc7693)
- [eBACS: Benchmarking hash functions](https://bench.cr.yp.to/)

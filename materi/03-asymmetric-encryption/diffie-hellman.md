# 🤝 Diffie-Hellman Key Exchange

Diffie-Hellman (DH) memungkinkan dua pihak menyepakati kunci rahasia bersama melalui kanal yang sepenuhnya publik, tanpa pernah mengirim kunci itu. Ditemukan Whitfield Diffie dan Martin Hellman pada 1976, ini adalah salah satu tonggak lahirnya kriptografi kunci publik.

DH **tidak** dipakai untuk mengenkripsi data. Ia dipakai untuk **menyepakati kunci** yang kemudian dipakai cipher simetris seperti AES.

---

## 1. Intuisi: Analogi Cat

Bayangkan cat:

1. Alice dan Bob sepakat memakai warna kuning publik.
2. Alice memilih warna rahasia merah, mencampurnya, mengirim hasil campuran.
3. Bob memilih warna rahasia biru, mencampurnya, mengirim hasil campuran.
4. Alice mencampur campuran Bob dengan merah miliknya.
5. Bob mencampur campuran Alice dengan biru miliknya.
6. Keduanya mendapat warna akhir yang sama.

Penyerang melihat kuning, campuran merah-kuning, dan campuran biru-kuning, tetapi tidak bisa memisahkan warna rahasia dari campuran. Analogi ini tidak sempurna karena pencampuran cat tidak reversibel, sedangkan matematika modulo reversibel jika kuncinya diketahui.

---

## 2. Matematika

Parameter publik:

```
p : bilangan prima besar
g : generator dari grup multiplikatif modulo p
```

Langkah:

```
Alice                      Bob
pilih a rahasia            pilih b rahasia
A = g^a mod p              B = g^b mod p
kirim A  ---------------->  terima A
terima B  <--------------- kirim B
S = B^a mod p              S = A^b mod p
```

Keduanya mendapat `S = g^(a*b) mod p`.

Penyerang yang melihat `A` dan `B` harus menyelesaikan:

```
a = log_g(A) mod p
```

Ini adalah **Discrete Logarithm Problem**, yang dipercaya sulit untuk `p` besar dengan subgrup berorder prima besar.

---

## 3. Contoh Angka

```
p = 23, g = 5
Alice: a = 6,  A = 5^6 mod 23 = 8
Bob  : b = 15, B = 5^15 mod 23 = 19

Alice: S = 19^6 mod 23 = 2
Bob  : S = 8^15 mod 23 = 2
```

`S = 2` adalah rahasia bersama. Angka ini tentu tidak aman, hanya untuk ilustrasi.

---

## 4. Memilih Grup yang Aman

### Bahaya subgrup kecil

Jika `p - 1` memiliki faktor kecil, penyerang bisa memakai **Pohlig-Hellman** untuk memulihkan sebagian eksponen, lalu menggabungkannya dengan CRT.

### Solusi: safe prime dan subgrup prima

1. Pilih `p` prima dan `q = (p - 1) / 2` juga prima. `p` disebut **safe prime**.
2. Pakai generator `g` yang berorder `q`, bukan order `p - 1`.
3. Periksa `g^q mod p == 1` dan `g != 1`.

Dengan cara ini, `g` hanya menghasilkan subgrup berukuran `q`, dan small subgroup attack tidak berlaku.

### Grup standar

Jangan membuat parameter sendiri untuk produksi. Gunakan grup yang sudah diaudit:

| Grup | Ukuran | Standar |
|---|---|---|
| MODP Group 14 | 2048 bit | RFC 3526 |
| MODP Group 16 | 4096 bit | RFC 3526 |
| ffdhe2048 | 2048 bit | RFC 7919 |
| X25519 | 255 bit | RFC 7748 |
| P-256 | 256 bit | NIST SP 800-56A |

**Logjam attack** (2015) menunjukkan bahwa banyak server memakai grup 512 bit atau 1024 bit yang bisa dipatahkan negara dengan sumber daya besar, dan bahwa parameter yang sama dipakai ulang di banyak tempat sehingga serangan precomputation menjadi efisien.

---

## 5. Man in the Middle

DH murni tidak punya autentikasi. Mallory bisa mendarat di tengah:

```
Alice ---- A ---- Mallory ---- A' ---- Bob
Alice ---- B' --- Mallory ---- B  ---- Bob
```

Mallory berbagi kunci berbeda dengan Alice dan dengan Bob. Ia bisa mendekripsi semua pesan, membacanya, lalu meneruskannya kembali dengan enkripsi baru. Alice dan Bob tidak menyadari apa pun.

### Mitigasi

1. **Tanda tangan kunci publik.** Setiap pihak menandatangani nilai publik `A` atau `B` dengan kunci jangka panjang. Ini pola dalam TLS 1.2 dengan sertifikat.
2. **Authenticated DH dengan password.** Memakai SRP atau PAKE.
3. **Pre-shared key.** Dalam SSH, kunci host dan fingerprint mencegah MITM.
4. **Key confirmation.** Setelah sepakat, kirim MAC atas identifier dan kunci untuk memastikan pihak lawan benar.

---

## 6. Forward Secrecy

Keuntungan besar DH sementara (ephemeral DH):

- Setiap sesi memakai `a` dan `b` baru.
- Jika kunci jangka panjang bocor besok, sesi yang sudah selesai kemarin tetap aman.
- Ini disebut **forward secrecy** atau **perfect forward secrecy**.

TLS 1.3 mewajibkan hal ini: semua handshake memakai ephemeral DH, baik ECDHE maupun DHE.

Tanpa ephemeral, misalnya pada TLS RSA key exchange, kunci privat server bisa membuka semua rekaman lama yang pernah direkam penyerang.

---

## 7. ECDH (Elliptic Curve Diffie-Hellman)

Alih-alih grup modulo prima, ECDH memakai grup titik pada kurva eliptik.

```
Alice: A = a * G
Bob  : B = b * G
Alice: S = a * B
Bob  : S = b * A
```

Keuntungan:

- Kunci jauh lebih pendek: 256 bit ECC setara 3072 bit DH.
- Operasi lebih cepat.
- Cocok untuk perangkat terbatas.

`X25519` adalah varian Montgomery curve yang sangat populer karena implementasinya sederhana dan tahan terhadap banyak jebakan implementasi.

Perbandingan ukuran:

| Keamanan setara | DH klasik | ECDH |
|---|---|---|
| 112 bit | 2048 bit | 224 bit |
| 128 bit | 3072 bit | 256 bit |
| 192 bit | 7680 bit | 384 bit |
| 256 bit | 15360 bit | 521 bit |

---

## 8. Derivation: Jangan Pakai Shared Secret Langsung

Shared secret `S` adalah bilangan bulat, bukan byte acak berkualitas. Jangan langsung dipakai sebagai kunci AES.

Praktik yang benar:

1. Serialisasi `S` secara tetap, misalnya big endian dengan panjang tetap.
2. Jalankan **HKDF** untuk menurunkan kunci.
3. Ikat hasilnya dengan konteks, misalnya transkrip handshake.

```python
import hashlib, hmac

def hkdf_extract(salt: bytes, ikm: bytes) -> bytes:
    return hmac.new(salt, ikm, hashlib.sha256).digest()

def hkdf_expand(prk: bytes, info: bytes, length: int) -> bytes:
    out, t, counter = b"", b"", 1
    while len(out) < length:
        t = hmac.new(prk, t + info + bytes([counter]), hashlib.sha256).digest()
        out += t
        counter += 1
    return out[:length]
```

---

## 9. Implementasi Manual

File `kode/03-asymmetric-encryption/diffie-hellman.py` berisi:

- Parameter grup 256 bit dengan `p` safe prime dan `g` berorder `q`.
- `Party` dengan kunci privat acak dan kunci publik.
- Derivasi kunci dengan hash, bukan memakai shared secret langsung.
- Demonstrasi angka kecil, pertukaran nyata, dan MITM.
- Pemeriksaan subgrup.
- Demonstrasi forward secrecy.

Catatan: 256 bit hanya untuk pembelajaran. Untuk keamanan nyata gunakan 2048 bit atau lebih, atau ECDH.

---

## 10. Kesalahan Umum

1. Memakai DH tanpa autentikasi, sehingga rentan MITM.
2. Memakai modulus yang terlalu kecil atau grup yang tidak standar.
3. Tidak memeriksa bahwa kunci publik peer berada dalam subgrup yang benar.
4. Memakai ulang eksponen `a` untuk banyak sesi tanpa alasan.
5. Memakai shared secret langsung sebagai kunci tanpa KDF.
6. Tidak menghapus nilai rahasia dari memori setelah dipakai.
7. Menegosiasikan parameter yang bisa diturunkan penyerang, misalnya mengizinkan grup 512 bit.
8. Memakai `random` biasa, bukan CSPRNG.

---

## 11. Latihan

1. Hitung DH manual dengan `p = 23`, `g = 5`, `a = 4`, `b = 3`.
2. Tunjukkan bahwa `g = 5` adalah generator penuh untuk `p = 23`, lalu cari `g` yang berorder `q = 11`.
3. Implementasikan Pohlig-Hellman untuk `p` dengan faktor kecil.
4. Simulasikan MITM lengkap dengan enkripsi AES menggunakan dua kunci berbeda.
5. Tambahkan autentikasi dengan tanda tangan RSA atas kunci publik DH.
6. Bandingkan waktu `pow(g, a, p)` untuk 256, 1024, dan 2048 bit.
7. Jelaskan mengapa TLS 1.3 membuang DHE dengan parameter yang bisa dipilih server.
8. Implementasikan X25519 dengan library dan bandingkan hasilnya dengan implementasi referensi.

---

## 12. Referensi

- [RFC 3526: MODP Diffie-Hellman groups](https://www.rfc-editor.org/rfc/rfc3526)
- [RFC 7748: Elliptic Curves for Security](https://www.rfc-editor.org/rfc/rfc7748)
- [RFC 7919: Negotiated FFDHE Parameters](https://www.rfc-editor.org/rfc/rfc7919)
- [Logjam attack](https://weakdh.org/)
- Christof Paar dan Jan Pelzl, *Understanding Cryptography*, bab 8.

# 🔑 HMAC (Hash-based Message Authentication Code)

HMAC adalah cara mengubah fungsi hash menjadi **MAC**: kode yang membuktikan bahwa pesan berasal dari pemegang kunci dan tidak berubah. HMAC distandarkan di RFC 2104 dan FIPS 198-1, dipakai di TLS, IPsec, JWT (HS256), webhook, dan API signature.

---

## 1. Masalah: Hash Saja Tidak Cukup

Hash memberi integritas terhadap perubahan tidak sengaja, bukan terhadap penyerang aktif. Jika checksum dikirim bersama file, penyerang bisa mengganti keduanya.

Yang dibutuhkan adalah checksum yang **tidak bisa dihitung tanpa kunci rahasia**. Itulah MAC.

| Mekanisme | Kunci | Menahan penyerang aktif |
|---|---|---|
| Checksum CRC | Tidak | Tidak |
| Hash biasa | Tidak | Tidak |
| MAC | Ya | Ya |
| Tanda tangan digital | Ya, asimetris | Ya, plus non-repudiation |

---

## 2. Konstruksi HMAC

```
HMAC(K, m) = H((K' xor opad) || H((K' xor ipad) || m))
```

Dengan:

```
K' = K jika len(K) <= block_size
K' = H(K) jika len(K) > block_size
K' = K' dipad dengan nol sampai block_size

ipad = 0x36 berulang
opad = 0x5C berulang
```

### Kenapa dua lapis

Hash bagian dalam mengikat pesan dan kunci. Hash bagian luar mengikat hasil dalam dengan kunci lagi. Karena state bagian luar tidak bisa disentuh penyerang, length extension menjadi tidak mungkin.

Bahkan jika hash dasarnya punya kelemahan tertentu, HMAC tetap relatif aman. HMAC-SHA1 masih dianggap aman meskipun SHA-1 rusak untuk collision.

---

## 3. Kenapa Bukan H(key || message)

Konstruksi naif `H(key || message)` rentan **length extension**. Dari `H(key || message)` penyerang bisa menghitung `H(key || message || padding || extra)` tanpa mengetahui key.

`H(message || key)` juga bermasalah:

- Rentan collision jika hash-nya lemah, karena collision pada `message` langsung menjadi collision pada MAC.
- Untuk hash dengan Merkle-Damgard, ada serangan yang lebih halus.

Contoh serangan ada di `sha256-example.py`, fungsi `length_extension_attack`.

---

## 4. Sifat Keamanan

HMAC dianggap **PRF** (pseudo-random function) jika hash dasarnya punya properti tertentu. Artinya, tanpa kunci, output HMAC tidak bisa dibedakan dari acak.

Jaminan praktis:

1. Tidak bisa memalsukan MAC tanpa kunci.
2. Tidak bisa memulihkan kunci dari pasangan pesan dan MAC.
3. Tidak bisa memakai ulang MAC untuk pesan lain.
4. Aman meskipun hash dasarnya hanya collision resistant secara lemah, dengan catatan tertentu.

---

## 5. Pemakaian yang Benar

### Verifikasi pesan

```python
import hmac, hashlib

def sign(key: bytes, message: bytes) -> bytes:
    return hmac.new(key, message, hashlib.sha256).digest()

def verify(key: bytes, message: bytes, tag: bytes) -> bool:
    expected = sign(key, message)
    return hmac.compare_digest(expected, tag)
```

Aturan:

1. Bandingkan dengan **constant time**, jangan `==`.
2. Verifikasi sebelum memproses data.
3. Tolak pesan jika tag tidak cocok, tanpa menjelaskan detail.
4. Sertakan semua field penting dalam perhitungan MAC, termasuk timestamp dan user id.

### Encrypt-then-MAC

Pola yang benar untuk enkripsi dan autentikasi terpisah:

```
ciphertext = Encrypt(k_enc, plaintext)
tag = HMAC(k_mac, iv || ciphertext)
kirim (iv, ciphertext, tag)
```

Saat menerima:

1. Hitung ulang MAC atas `iv || ciphertext`.
2. Bandingkan constant time.
3. Jika gagal, tolak sebelum dekripsi.
4. Jika berhasil, dekripsi.

Jangan memakai MAC-then-Encrypt, dan jangan Encrypt-and-MAC.

---

## 6. Key Separation

Jangan memakai satu kunci untuk dua tujuan. Turunkan kunci terpisah:

```
k_enc = HKDF(master, info="encryption")
k_mac = HKDF(master, info="authentication")
```

Alasan: jika kunci yang sama dipakai di dua algoritma, interaksi antar keduanya bisa menciptakan serangan yang tidak terduga.

---

## 7. HKDF: Dari Shared Secret ke Kunci

HKDF (RFC 5869) memiliki dua tahap:

```
PRK = HMAC(salt, IKM)                          extract
OKM = HMAC(PRK, T(i-1) || info || i) ...       expand
```

Contoh:

```python
def hkdf(ikm: bytes, salt: bytes, info: bytes, length: int) -> bytes:
    prk = hmac.new(salt or b"\x00" * 32, ikm, hashlib.sha256).digest()
    okm, t, counter = b"", b"", 1
    while len(okm) < length:
        t = hmac.new(prk, t + info + bytes([counter]), hashlib.sha256).digest()
        okm += t
        counter += 1
    return okm[:length]
```

HKDF bukan untuk password. Untuk password gunakan Argon2, scrypt, atau PBKDF2.

---

## 8. HMAC vs AEAD

| Aspek | HMAC | AEAD (GCM, ChaCha20-Poly1305) |
|---|---|---|
| Kerahasiaan | Tidak | Ya |
| Integritas | Ya | Ya |
| Kunci | Satu | Satu |
| Pemakaian | MAC pesan, API signature | Enkripsi plus autentikasi |
| Kesalahan umum | Perbandingan tidak constant time | Nonce reuse |
| Kompleksitas | Rendah | Sedang |

Jika hanya butuh autentikasi, HMAC tepat. Jika butuh kerahasiaan dan autentikasi, gunakan AEAD langsung, jangan menggabungkan sendiri.

---

## 9. Contoh Nyata

### JWT HS256

```
header.payload.signature
signature = HMAC-SHA256(secret, header + "." + payload)
```

Kesalahan umum:

1. Secret lemah sehingga bisa di-brute force.
2. Menerima algoritma `none`.
3. Mencampur HS256 dan RS256 tanpa validasi algoritma, sehingga penyerang bisa memakai kunci publik sebagai HMAC key.

### Webhook signature

Banyak layanan mengirim header seperti `X-Signature: sha256=...`. Verifikasi harus:

1. Ambil raw body, bukan hasil parsing JSON.
2. Hitung HMAC atas timestamp dan body.
3. Tolak timestamp terlalu lama untuk mencegah replay.
4. Bandingkan constant time.

---

## 10. Implementasi di Folder Ini

`hmac.py` berisi:

- `hmac_new`, implementasi HMAC untuk SHA-256, SHA-1, dan SHA-512.
- `constant_time_compare` dan `unsafe_compare` untuk demonstrasi timing.
- Uji vektor RFC 4231.
- Perbandingan dengan modul standar.
- Demo verifikasi pesan.
- Demo key separation.
- Pengukuran waktu perbandingan naif.

Catatan penting: karena file ini bernama `hmac.py`, ia membayangi modul standar `hmac` di Python jika dijalankan dari folder yang sama. Skrip ini mengatasi hal itu dengan memuat modul standar lewat `importlib`. Untuk proyek nyata, gunakan nama file lain atau letakkan di package terpisah.

---

## 11. Kesalahan Umum

1. Memakai `H(key || message)` sebagai MAC.
2. Membandingkan tag dengan `==`.
3. Memakai kunci yang sama untuk enkripsi dan MAC.
4. Lupa mengautentikasi metadata seperti IV, timestamp, atau user id.
5. Menerima pesan sebelum verifikasi selesai.
6. Memakai secret pendek yang bisa di-brute force.
7. Mencampur algoritma JWT tanpa whitelist.
8. Menyimpan tag di tempat yang bisa diubah penyerang tanpa ikut dihitung ulang.

---

## 12. Latihan

1. Implementasikan HMAC-SHA256 dan uji dengan RFC 4231 test case 1 sampai 6.
2. Tunjukkan length extension pada `H(key || message)` dan buktikan HMAC kebal.
3. Ukur waktu perbandingan naif untuk prefix cocok 0, 8, 16, dan 31 byte.
4. Implementasikan Encrypt-then-MAC dengan AES-CBC dan HMAC-SHA256.
5. Bangun verifikasi webhook dengan timestamp dan tolak replay lebih dari 5 menit.
6. Turunkan kunci enkripsi dan MAC dari satu master key dengan HKDF.
7. Jelaskan mengapa HMAC-SHA1 masih dianggap aman untuk MAC.

---

## 13. Referensi

- [RFC 2104: HMAC](https://www.rfc-editor.org/rfc/rfc2104)
- [FIPS 198-1: The Keyed-Hash Message Authentication Code](https://csrc.nist.gov/publications/detail/fips/198/1/final)
- [RFC 5869: HKDF](https://www.rfc-editor.org/rfc/rfc5869)
- [RFC 4231: Test Cases for HMAC](https://www.rfc-editor.org/rfc/rfc4231)
- [Python hmac documentation](https://docs.python.org/3/library/hmac.html)

# 🌊 ChaCha20

ChaCha20 adalah stream cipher yang dirancang Daniel J. Bernstein pada 2008 sebagai penyempurnaan Salsa20. Ia menjadi standar IETF pada RFC 8439, dipakai di TLS 1.3, WireGuard, SSH, Android, dan Chrome. Bersama Poly1305, ia membentuk AEAD `ChaCha20-Poly1305` yang menjadi alternatif utama AES-GCM.

---

## 1. Kenapa ChaCha20 Penting

AES sangat cepat jika CPU punya AES-NI. Namun tidak semua perangkat punya:

- Mikrokontroler murah.
- Perangkat lama tanpa instruksi khusus.
- Lingkungan virtual yang tidak mengekspos AES-NI.
- Implementasi JavaScript atau bahasa dinamis.

Pada perangkat seperti itu, AES dengan tabel lookup rawan **cache timing attack**. ChaCha20 hanya memakai operasi aritmetika register, sehingga waktu eksekusinya tidak bergantung pada data rahasia.

Keunggulan lain:

1. Konstan time secara alami pada implementasi software.
2. Tidak butuh tabel besar, ramah cache.
3. Paralel dan vektorisasi mudah.
4. Nonce 96 bit, jauh lebih aman dari pengulangan dibanding nonce 64 bit pada AES-CTR klasik.

---

## 2. Perbandingan Dengan AES

| Aspek | AES-GCM | ChaCha20-Poly1305 |
|---|---|---|
| Jenis | Block cipher dalam mode AEAD | Stream cipher plus MAC |
| Ukuran blok | 128 bit | 512 bit internal |
| Kunci | 128 atau 256 bit | 256 bit |
| Nonce | 96 bit | 96 bit |
| Kecepatan dengan AES-NI | Sangat tinggi, 5+ GB/detik | Tinggi, 1 sampai 3 GB/detik |
| Kecepatan tanpa AES-NI | Sedang, rawan timing | Tinggi, konstan time |
| Standar | NIST SP 800-38D | RFC 8439 |
| Penggunaan | Default di banyak server | Default di mobile dan TLS 1.3 |

Keduanya aman. Pilih berdasarkan platform dan ada tidaknya akselerasi hardware.

---

## 3. Struktur State

State ChaCha20 terdiri dari 16 word 32 bit (512 bit):

```
cccccccc  cccccccc  cccccccc  cccccccc     konstanta "expand 32-byte k"
kkkkkkkk  kkkkkkkk  kkkkkkkk  kkkkkkkk     kunci, 8 word
kkkkkkkk  kkkkkkkk  kkkkkkkk  kkkkkkkk
bbbbbbbb  nnnnnnnn  nnnnnnnn  nnnnnnnn     counter 32 bit, nonce 96 bit
```

Posisi 0 sampai 3 adalah konstanta ASCII:

```
"expa" "nd 3" "2-by" "te k"
```

Dalam little endian, keempatnya menjadi `0x61707865`, `0x3320646e`, `0x79622d32`, `0x6b206574`.

---

## 4. Quarter Round

Fungsi inti, dijalankan pada empat word `(a, b, c, d)`:

```
a += b; d ^= a; d <<<= 16;
c += d; b ^= c; b <<<= 12;
a += b; d ^= a; d <<<= 8;
c += d; b ^= c; b <<<= 7;
```

Operasi `<<<=` adalah rotasi kiri 32 bit. Perhatikan pola: penjumlahan menciptakan carry antar bit (diffusion), rotasi memindahkan bit antar posisi, XOR mencampur.

Setiap round terdiri dari 4 column round dan 4 diagonal round:

```
Column round:      Diagonal round:
QR(0, 4,  8, 12)   QR(0, 5, 10, 15)
QR(1, 5,  9, 13)   QR(1, 6, 11, 12)
QR(2, 6, 10, 14)   QR(2, 7,  8, 13)
QR(3, 7, 11, 15)   QR(3, 4,  9, 14)
```

Total 20 round, yaitu 10 iterasi pasangan column dan diagonal.

---

## 5. Proses Blok

```
working = state
for 10 kali:
    column rounds
    diagonal rounds
output[i] = working[i] + state[i]
```

Penambahan akhir dengan state awal disebut **feed-forward**. Tanpa langkah ini, round ChaCha bisa dibalik dan cipher menjadi lemah. Feed-forward membuat hubungan input dan output menjadi non-invertibel tanpa kunci.

Output 16 word kemudian di-serialisasi little endian menjadi 64 byte keystream.

---

## 6. Enkripsi

ChaCha20 adalah stream cipher:

```
ciphertext = plaintext XOR keystream
plaintext  = ciphertext XOR keystream
```

Karena itu enkripsi dan dekripsi memakai fungsi yang sama persis.

Counter dinaikkan setiap blok 64 byte. Untuk pesan panjang, counter tidak boleh meluap atau berulang. Batas praktisnya adalah `2^32 * 64` byte, sekitar 256 GB per pasangan kunci dan nonce.

---

## 7. Nonce dan Counter

RFC 8439 menetapkan pembagian state terakhir:

```
word 12      : counter 32 bit
word 13-15   : nonce 96 bit
```

Aturan:

1. Nonce harus unik untuk setiap pesan dengan kunci yang sama.
2. Nonce boleh acak atau berupa penghitung, asal tidak berulang.
3. Jangan memakai nonce yang sama dua kali. Jika terjadi, XOR kedua ciphertext sama dengan XOR kedua plaintext, dan kerahasiaan hilang total.

Varian lama memakai nonce 64 bit dan counter 64 bit. Itu masih didukung banyak library sebagai `ChaCha20` klasik, tetapi untuk protokol baru gunakan varian 96 bit.

---

## 8. Poly1305

Poly1305 adalah message authentication code satu kali pakai (one-time MAC) yang dirancang untuk berpasangan dengan ChaCha20.

Rumusnya:

```
r = key[0..16] dengan bit clamp
s = key[16..32]
acc = 0
for setiap 16 byte pesan:
    n = potongan + 0x01
    acc = ((acc + n) * r) mod (2^130 - 5)
tag = (acc + s) mod 2^128
```

Properti penting:

- `r` harus unik per pesan. Jika `r` dipakai dua kali, kunci MAC bisa dipulihkan.
- Karena itu ChaCha20-Poly1305 menurunkan kunci Poly1305 dari blok keystream pertama (counter 0), sehingga selalu berbeda.

---

## 9. ChaCha20-Poly1305 (AEAD)

Konstruksi lengkap:

```
otk = ChaCha20(key, nonce, counter=0)[0..32]     kunci Poly1305
ciphertext = ChaCha20(key, nonce, counter=1, plaintext)
mac_data = aad || pad(aad) || ciphertext || pad(ciphertext) || len(aad) || len(ciphertext)
tag = Poly1305(mac_data, otk)
```

Verifikasi tag wajib constant time. Jika gagal, tolak seluruh pesan, jangan mengembalikan plaintext parsial.

Contoh pemakaian dengan PyCryptodome:

```python
from Crypto.Cipher import ChaCha20_Poly1305
from Crypto.Random import get_random_bytes

key = get_random_bytes(32)
nonce = get_random_bytes(12)

cipher = ChaCha20_Poly1305.new(key=key, nonce=nonce)
cipher.update(b"header publik")
ct, tag = cipher.encrypt_and_digest(b"pesan rahasia")

cipher = ChaCha20_Poly1305.new(key=key, nonce=nonce)
cipher.update(b"header publik")
pt = cipher.decrypt_and_verify(ct, tag)
```

---

## 10. Keamanan

| Aspek | Status |
|---|---|
| Serangan praktis pada cipher inti | Tidak ada |
| Kriptanalisis terbaik | 7 dari 20 round dengan kompleksitas besar |
| Nonce reuse | Fatal, membocorkan XOR plaintext |
| Related-key | Tidak praktis |
| Timing attack software | Sulit, karena tidak ada tabel data-dependent |
| Fault attack | Mungkin pada hardware, sama seperti cipher lain |

Catatan penting: ChaCha20 **tidak** memberi autentikasi. Jika hanya memakai ChaCha20 tanpa Poly1305, penyerang bisa memodifikasi ciphertext dan perubahan itu tidak terdeteksi, meskipun hasil dekripsi menjadi acak. Selalu pakai bentuk AEAD untuk data yang perlu integritas.

---

## 11. Implementasi Manual

File `chacha20.py` berisi:

- `quarter_round`, fungsi inti.
- `block`, pembangkit satu blok 64 byte.
- `keystream` dan `chacha20_encrypt`, API enkripsi.
- `poly1305_mac`, implementasi MAC.
- Uji vektor RFC 8439 untuk keystream dan Poly1305.
- Uji avalanche dan benchmark.

Vektor uji keystream:

```
key    = 000102...1f
nonce  = 000000090000004a00000000
counter= 1
output = 10f1e7e4d13b5915500fdd1fa32071c4...
```

Vektor uji Poly1305:

```
key     = 85d6be7857556d337f4452fe42d506a8 0103808afb0db2fd4abff6af4149f51b
message = "Cryptographic Forum Research Group"
tag     = a8061dc1305136c6c22b8baf0c0127a9
```

---

## 12. Kesalahan Umum

1. Memakai nonce statis atau nonce yang diambil dari waktu.
2. Memakai counter mulai dari 0 untuk enkripsi padahal Poly1305 memakai counter 0.
3. Lupa memverifikasi tag, sehingga AEAD berubah menjadi cipher tanpa integritas.
4. Memakai Poly1305 dua kali dengan kunci yang sama.
5. Menganggap ChaCha20 sudah autentikasi. Tanpa Poly1305, ia hanya menjaga kerahasiaan.
6. Menyimpan hanya ciphertext tanpa nonce, sehingga data tidak bisa didekripsi.

---

## 13. Latihan

1. Implementasikan Salsa20 lalu bandingkan struktur quarter round-nya dengan ChaCha20.
2. Buktikan bahwa mengganti counter dari 1 ke 2 mengubah sekitar setengah bit keystream.
3. Hitung berapa maksimum byte yang boleh dienkripsi dengan satu pasangan kunci dan nonce.
4. Modifikasi kode untuk memakai nonce 64 bit dan counter 64 bit, lalu uji dengan vektor lama.
5. Jelaskan mengapa feed-forward membuat ChaCha20 tidak bisa dibalik tanpa kunci.
6. Rancang protokol sederhana yang memakai ChaCha20-Poly1305 untuk enkripsi file, tentukan apa saja yang disimpan.

---

## 14. Referensi

- [RFC 8439: ChaCha20 and Poly1305 for IETF Protocols](https://www.rfc-editor.org/rfc/rfc8439)
- Daniel J. Bernstein, [The ChaCha family of stream ciphers](https://cr.yp.to/chacha.html)
- [libsodium documentation](https://doc.libsodium.org/advanced/stream_ciphers/chacha20)
- Christof Paar dan Jan Pelzl, *Understanding Cryptography*, bab stream cipher.

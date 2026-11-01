# 🧱 Analisis Mode ECB vs CBC

Memilih mode operasi sama pentingnya dengan memilih cipher. AES yang kuat bisa menjadi tidak berguna jika dipasang pada mode yang salah. Dokumen ini membandingkan ECB dan CBC secara detail, menunjukkan serangan nyata, lalu menjelaskan kapan mode lain lebih tepat.

---

## 1. Masalah Dasar: Block Cipher Hanya Bekerja Pada Satu Blok

AES hanya bisa mengenkripsi 16 byte sekaligus. Untuk pesan yang lebih panjang, kita perlu **mode operasi**, yaitu aturan bagaimana blok-blok disusun, diikat, dan diproses.

Tanpa mode yang benar, dua blok plaintext yang identik akan menghasilkan dua blok ciphertext yang identik. Itu adalah kebocoran informasi.

---

## 2. ECB (Electronic Codebook)

### Cara kerja

```
C_i = E_k(P_i)
P_i = D_k(C_i)
```

Setiap blok dienkripsi secara independen. Tidak ada IV, tidak ada chaining.

### Kelebihan

1. Paling sederhana.
2. Bisa diparalelkan penuh, enkripsi dan dekripsi.
3. Bisa akses acak per blok.
4. Tidak butuh IV, sehingga tidak ada risiko IV salah.

### Kelemahan fatal: deterministik

Plaintext yang sama selalu menghasilkan ciphertext yang sama. Artinya:

- Penyerang bisa mengenali blok yang berulang.
- Penyerang bisa menyusun ulang blok.
- Penyerang bisa menghapus atau menduplikasi blok tanpa terdeteksi.
- Pola data tetap terlihat, seperti pada gambar Tux yang terkenal (ECB Penguin).

### Demonstrasi pola

Plaintext berupa gambar bitmap 16 warna. Setiap warna menempati blok 16 byte yang identik secara internal. Dengan ECB, semua area berwarna sama menjadi blok ciphertext yang sama, sehingga bentuk gambar tetap tampak.

```
Plaintext pattern:        ECB:                CBC:
AAAA BBBB CCCC            x1x1 y1y1 z1z1      a1b2 c3d4 e5f6
AAAA BBBB CCCC            x1x1 y1y1 z1z1      f6e5 d4c3 b2a1
DDDD EEEE FFFF            w1w1 v1v1 u1u1      ...acak...
```

Dengan CBC, setiap blok terlihat acak dan pola hilang.

### Kapan ECB masih dipakai

Hampir tidak pernah untuk data yang bisa diprediksi. Satu-satunya penggunaan yang masih dianggap wajar adalah enkripsi **satu blok acak** (misalnya membungkus kunci) atau dalam konstruksi khusus seperti deterministik nonce untuk SIV, dan itu pun bukan ECB langsung.

Standar NIST SP 800-38A tidak melarang ECB secara teknis, tetapi praktik modern menganggapnya salah untuk data umum.

---

## 3. CBC (Cipher Block Chaining)

### Cara kerja

```
C_0 = IV
C_i = E_k(P_i XOR C_(i-1))
P_i = D_k(C_i) XOR C_(i-1)
```

Setiap blok plaintext di-XOR dengan ciphertext blok sebelumnya sebelum dienkripsi. Karena itu blok yang identik menghasilkan ciphertext berbeda.

### Kelebihan

1. Menyembunyikan pola berulang.
2. Sudah lama teruji, banyak implementasi.
3. Dekripsi bisa diparalelkan.

### Kelemahan

1. **Enkripsi serial.** Setiap blok butuh hasil blok sebelumnya, sehingga tidak bisa diparalelkan.
2. **Butuh padding.** Karena bekerja per blok, panjang pesan harus kelipatan 16. Ini membuka celah padding oracle.
3. **Tidak ada autentikasi.** Penyerang bisa mengubah ciphertext dan menghasilkan perubahan terkontrol pada plaintext.
4. **IV harus acak dan unik.** IV yang diulang membocorkan kesamaan prefix.
5. **Rawan padding oracle** jika aplikasi membedakan jenis error.

### Bit flipping attack

Karena `P_i = D_k(C_i) XOR C_(i-1)`, mengubah satu bit pada `C_(i-1)` akan mengubah bit yang sama pada `P_i` secara terkontrol.

```
C_(i-1) diubah:  C' = C XOR delta
P_i menjadi:     P_i XOR delta
```

Blok `P_(i-1)` akan menjadi sampah, tetapi blok `P_i` bisa diubah sesuka hati. Jika penyerang tahu struktur data, misalnya `role=user`, ia bisa mengubahnya menjadi `role=admn` hanya dengan mengubah ciphertext. Tidak perlu kunci.

Contoh skenario:

```
Plaintext : "user=alice;admin=false;..."
Target    : "user=alice;admin=true ;..."
Penyerang mengubah 1 byte di blok sebelumnya.
```

Inilah alasan CBC tanpa MAC tidak boleh dipakai untuk data yang butuh integritas.

### Padding oracle

Jika server mengembalikan pesan error berbeda untuk "padding salah" dan "MAC salah", penyerang bisa mendekripsi seluruh ciphertext byte demi byte tanpa kunci. Ini adalah serangan yang dipakai pada ASP.NET, POODLE, dan banyak library lain.

Mitigasi:

1. Gunakan Encrypt-then-MAC.
2. Jangan pernah membedakan error padding dan error autentikasi.
3. Verifikasi MAC constant time sebelum dekripsi.
4. Lebih baik lagi, pindah ke AEAD.

---

## 4. Perbandingan Detail

| Aspek | ECB | CBC |
|---|---|---|
| IV | Tidak ada | Wajib, acak, unik |
| Paralel enkripsi | Ya | Tidak |
| Paralel dekripsi | Ya | Ya |
| Padding | Wajib | Wajib |
| Menyembunyikan pola | Tidak | Ya |
| Deterministik | Ya | Tidak |
| Bit flipping | Tidak terkontrol | Terkontrol |
| Padding oracle | Tidak ada | Ada |
| Autentikasi | Tidak | Tidak |
| Rekomendasi | Jangan | Hanya dengan MAC |
| Mode pengganti | GCM | GCM atau CTR plus HMAC |

---

## 5. Contoh Kode: Membuktikan Kebocoran ECB

```python
def ecb_encrypt_blocks(cipher, data: bytes) -> bytes:
    assert len(data) % 16 == 0
    return b"".join(cipher.encrypt_block(data[i:i+16])
                    for i in range(0, len(data), 16))

# Dua blok identik
block = b"RAHASIA-16-BYTE!"
plaintext = block * 4

ct = ecb_encrypt_blocks(cipher, plaintext)
print(len(set(ct[i:i+16] for i in range(0, len(ct), 16))))  # hasil: 1
```

Dari ciphertext saja, terlihat bahwa keempat blok berasal dari plaintext yang sama. Dengan CBC, keempatnya berbeda total.

```python
ct = cbc_encrypt(key, os.urandom(16), plaintext)
print(len(set(ct[i:i+16] for i in range(0, len(ct), 16))))  # hasil: 4
```

---

## 6. Demonstrasi Bit Flipping pada CBC

```python
iv = os.urandom(16)
plaintext = b"role=user&admin=0" + b"x" * 16
ct = bytearray(cbc_encrypt(key, iv, plaintext))

# Ubah byte pada blok ciphertext pertama agar blok plaintext kedua berubah.
target_byte = 9          # posisi '0' pada "admin=0" di blok kedua
position = target_byte   # karena blok kedua di-XOR dengan C_1, bukan IV
ct[position] ^= ord("0") ^ ord("1")

tampered = cbc_decrypt(key, iv, bytes(ct))
print(tampered[:16])     # blok pertama rusak
print(tampered[16:32])   # blok kedua berubah sesuai keinginan
```

Hasil: penyerang mengubah `admin=0` menjadi `admin=1` tanpa mengetahui kunci.

---

## 7. Rekomendasi Praktis

### Untuk aplikasi baru

Gunakan **AEAD**:

- AES-GCM jika CPU punya AES-NI.
- ChaCha20-Poly1305 jika tidak, atau untuk mobile.
- AES-GCM-SIV jika butuh nonce misuse resistance.

### Jika Harus Memakai CBC

1. IV acak 16 byte dari CSPRNG, dibuat baru setiap enkripsi.
2. Padding PKCS#7.
3. Encrypt-then-MAC dengan HMAC-SHA256 memakai kunci terpisah.
4. Verifikasi MAC constant time sebelum dekripsi.
5. Satu pesan error generik untuk semua kegagalan.

### Yang Harus Dihindari

1. ECB untuk data apa pun yang punya struktur.
2. IV statis, IV nol, atau IV yang diambil dari penghitung yang bisa ditebak.
3. CBC tanpa MAC.
4. Membocorkan perbedaan error padding.
5. Menggunakan kunci yang sama untuk enkripsi dan MAC tanpa KDF.

---

## 8. Mode Lain Sekilas

| Mode | Sifat | Catatan |
|---|---|---|
| CTR | Stream, paralel | Nonce unik, tanpa padding, tanpa autentikasi |
| CFB | Stream berbasis cipher | Butuh IV unik |
| OFB | Stream | Keystream tidak bergantung plaintext |
| GCM | AEAD | Standar industri, nonce 96 bit wajib unik |
| CCM | AEAD | Lebih sederhana, cocok untuk IoT |
| SIV | AEAD, nonce misuse resistant | Lebih lambat, aman jika nonce diulang |
| XTS | Disk encryption | Bukan AEAD, khusus penyimpanan |

---

## 9. Latihan

1. Enkripsi gambar BMP dengan ECB dan CBC, lalu bandingkan secara visual.
2. Tulis program yang mendeteksi apakah sebuah ciphertext memakai ECB, dengan mencari blok berulang.
3. Lakukan bit flipping pada CBC dan tunjukkan blok mana yang rusak.
4. Bangun simulasi padding oracle sederhana dan jelaskan langkah pemulihan satu byte terakhir.
5. Implementasikan Encrypt-then-MAC dengan AES-CBC dan HMAC-SHA256.
6. Bandingkan ukuran ciphertext AES-GCM dan AES-CBC untuk pesan 1000 byte.

---

## 10. Referensi

- [NIST SP 800-38A](https://csrc.nist.gov/publications/detail/sp/800-38a/final)
- [ECB Penguin](https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation#Electronic_codebook_(ECB))
- [Serangan padding oracle](https://robertheaton.com/2013/07/29/padding-oracle-attack/)
- [Cryptopals Set 2](https://cryptopals.com/sets/2), latihan ECB dan CBC.

# 🧩 Padding dan IV

Dua konsep kecil yang paling sering menyebabkan bug keamanan nyata. Padding berkaitan dengan ukuran blok, IV berkaitan dengan keunikan awal. Salah memahami keduanya bisa membuat enkripsi yang secara matematis kuat menjadi bisa dibongkar.

---

## 1. Kenapa Padding Diperlukan

AES adalah block cipher dengan blok tetap 16 byte. Jika plaintext 20 byte, ia harus dipecah menjadi blok 16 dan 4. Blok terakhir tidak penuh.

Ada dua pendekatan:

1. **Padding**: tambahkan byte agar menjadi kelipatan 16.
2. **Stream mode**: ubah block cipher menjadi stream cipher (CTR, CFB, OFB) sehingga padding tidak perlu.

Mode CBC, ECB, dan XTS membutuhkan padding. Mode CTR, GCM, ChaCha20 tidak.

---

## 2. PKCS#7 Padding

Aturan: jika kurang `n` byte, tambahkan `n` byte yang masing-masing bernilai `n`.

```
"HELLO" (5 byte)   -> 5 byte 0x0B
"HELLO WORLD" (11) -> 5 byte 0x05
16 byte tepat      -> 16 byte 0x10
```

Contoh konkret:

```
Plain : 48 45 4C 4C 4F
Pad   : 0B 0B 0B 0B 0B 0B 0B 0B 0B 0B 0B
Hasil : 48 45 4C 4C 4F 0B 0B 0B 0B 0B 0B 0B 0B 0B 0B 0B
```

### Kenapa selalu menambah blok penuh jika sudah kelipatan

Jika plaintext tepat 16 byte dan tidak ditambah apa pun, hasil dekripsi tidak bisa membedakan "tidak ada padding" dari "padding palsu". Dengan selalu menambah satu blok penuh berisi `0x10`, aturan menjadi unambigu: setiap pesan selalu punya padding.

### Validasi yang benar

Saat unpadding, periksa:

1. Panjang data minimal 1 dan kelipatan block size.
2. Nilai byte terakhir `n` berada di antara 1 dan block size.
3. `n` byte terakhir semuanya bernilai `n`.

```python
def pkcs7_unpad(data: bytes, block_size: int = 16) -> bytes:
    if not data or len(data) % block_size != 0:
        raise ValueError("panjang tidak valid")
    n = data[-1]
    if n == 0 or n > block_size:
        raise ValueError("nilai padding tidak valid")
    if data[-n:] != bytes([n]) * n:
        raise ValueError("padding tidak konsisten")
    return data[:-n]
```

Kesalahan umum: hanya memeriksa byte terakhir tanpa memverifikasi seluruh byte padding. Ini menciptakan oracle yang bisa dieksploitasi.

---

## 3. Padding Oracle Attack

### Skenario

Server mendekripsi ciphertext CBC, lalu:

- Jika padding salah, mengembalikan "padding error".
- Jika padding benar tetapi data tidak valid, mengembalikan "data error".

Perbedaan respons ini adalah oracle.

### Mekanisme

Untuk memulihkan byte terakhir blok `P_i`:

```
P_i = D_k(C_i) XOR C_(i-1)
```

Penyerang memodifikasi `C_(i-1)` dan mengamati apakah padding valid.

1. Tebak `P_i[15] = 0x01`. Ubah `C_(i-1)[15]` sehingga `D_k(C_i)[15]` menjadi `0x01`. Jika server bilang padding valid, tebakan benar.
2. Ulangi untuk `0x02 0x02`, `0x03 0x03 0x03`, dan seterusnya untuk setiap byte.
3. Dengan rata-rata 128 request per byte, seluruh blok bisa dipulihkan.

256 kali 16 byte sama dengan sekitar 4096 request untuk satu blok. Sangat murah.

### Dampak nyata

- ASP.NET padding oracle (2010).
- POODLE pada SSL 3.0 (2014).
- Serangan pada banyak library JWT dan session cookie.

### Mitigasi

1. Gunakan AEAD seperti AES-GCM atau ChaCha20-Poly1305.
2. Jika tetap CBC, pakai Encrypt-then-MAC dan verifikasi MAC sebelum dekripsi.
3. Semua kegagalan mengembalikan pesan yang sama dan waktu yang sama.
4. Jangan pernah membocorkan status padding ke luar sistem.

---

## 4. IV (Initialization Vector)

IV adalah nilai awal yang membuat dua enkripsi plaintext sama menghasilkan ciphertext berbeda.

### IV pada CBC

```
C_0 = IV
C_i = E_k(P_i XOR C_(i-1))
```

Syarat:

1. **Acak** dan diambil dari CSPRNG kriptografis.
2. **Unik** untuk setiap enkripsi dengan kunci yang sama.
3. **Tidak rahasia**, boleh dikirim bersama ciphertext.
4. **Tidak boleh bisa diprediksi** sebelum enkripsi.

IV yang diulang pada CBC membuat dua pesan dengan prefix sama memiliki prefix ciphertext sama, sehingga kebocoran pola muncul kembali.

### IV pada CTR dan GCM

Pada mode stream, istilahnya biasanya **nonce** atau **counter**.

```
keystream_i = E_k(nonce || counter_i)
```

Syarat mutlak: pasangan kunci dan nonce tidak boleh berulang. Jika berulang:

```
C1 = P1 XOR KS
C2 = P2 XOR KS
C1 XOR C2 = P1 XOR P2
```

Dua ciphertext yang di-XOR menghasilkan XOR dua plaintext. Dengan pengetahuan bahasa atau struktur data, plaintext bisa dipulihkan. Pada GCM, pengulangan nonce juga merusak kunci autentikasi, sehingga penyerang bisa memalsukan pesan.

### Perbandingan Istilah

| Mode | Nama | Ukuran umum | Sifat |
|---|---|---|---|
| CBC | IV | 16 byte | Acak, unik |
| CFB | IV | 16 byte | Acak, unik |
| OFB | IV | 16 byte | Acak, unik |
| CTR | Nonce dan counter | 8 sampai 16 byte | Unik, boleh sekuensial |
| GCM | Nonce | 12 byte | Unik, sangat kritis |
| ChaCha20 | Nonce | 12 byte | Unik, sangat kritis |

---

## 5. IV Statis: Contoh Kegagalan

```python
# SALAH
IV = b"\x00" * 16

c1 = cbc_encrypt(key, IV, b"password=rahasia")
c2 = cbc_encrypt(key, IV, b"password=rahasia")
assert c1 == c2   # dua enkripsi identik
```

Penyerang yang melihat `c1 == c2` tahu kedua pesan sama, tanpa perlu mendekripsi.

Kasus yang lebih halus: dua pesan berbagi prefix 16 byte. Dengan IV sama, blok pertama ciphertext juga sama. Penyerang bisa menebak isi prefix.

Perbaikan:

```python
# BENAR
iv = os.urandom(16)
ciphertext = cbc_encrypt(key, iv, plaintext)
hasil = iv + ciphertext   # simpan IV bersama ciphertext
```

---

## 6. IV yang Bisa Diprediksi

Menggunakan timestamp atau penghitung sederhana sebagai IV terlihat aman, tetapi bisa diprediksi. Pada CBC, penyerang yang bisa menebak IV dapat melakukan **chosen plaintext** dan memverifikasi tebakan blok pertama:

```
C_1 = E_k(P_1 XOR IV)
```

Jika penyerang bisa memilih plaintext dan menebak IV, ia bisa membuat `P_1 XOR IV` bernilai yang diinginkan, lalu membandingkan dengan ciphertext yang pernah dilihat. Ini disebut serangan BEAST pada TLS 1.0.

Aturan: IV harus acak dari CSPRNG, bukan dari waktu, bukan dari penghitung yang bisa ditebak publik, dan bukan hasil hash dari sesuatu yang tidak rahasia.

---

## 7. Nonce Reuse pada GCM

GCM memakai nonce untuk menurunkan dua hal:

1. Keystream enkripsi.
2. Kunci autentikasi GHASH.

Jika nonce diulang:

- XOR dua ciphertext sama dengan XOR dua plaintext.
- Kunci autentikasi bisa dihitung, sehingga penyerang bisa membuat tag palsu untuk pesan apa pun.

Ini bukan sekadar kebocoran data, melainkan kehilangan total integritas.

Praktik aman:

1. Nonce acak 96 bit dari CSPRNG. Peluang tabrakan sangat kecil untuk jumlah pesan yang wajar.
2. Atau nonce berupa penghitung yang dijamin unik per kunci.
3. Batasi jumlah pesan per kunci, misalnya 2^32 pesan, lalu rotasi kunci.
4. Untuk sistem yang sulit menjamin keunikan, gunakan AES-GCM-SIV.

---

## 8. Padding pada Data Biner

PKCS#7 bekerja untuk data biner apa pun, tetapi ada beberapa catatan:

1. Data yang sudah terkompresi atau terenkripsi tetap perlu padding jika memakai mode block.
2. Jangan memakai padding sebagai satu-satunya mekanisme integritas. Padding yang valid bukan bukti data asli.
3. Untuk protokol dengan panjang tetap, padding bisa dihilangkan dengan mode stream.

Alternatif padding lain:

| Skema | Keterangan | Status |
|---|---|---|
| PKCS#7 | Standar de facto | Dipakai luas |
| ISO 10126 | Byte acak lalu panjang | Usang |
| ANSI X9.23 | Nol lalu panjang | Usang |
| ISO/IEC 7816-4 | 0x80 lalu nol | Dipakai di smart card |
| Zero padding | Nol, ambigu | Hindari |

---

## 9. Checklist Implementasi

### Padding

- [ ] Gunakan PKCS#7 dengan block size sesuai cipher.
- [ ] Selalu tambahkan blok penuh jika data kelipatan block size.
- [ ] Validasi semua byte padding, bukan hanya yang terakhir.
- [ ] Jangan membedakan error padding dari error lain ke pengguna.
- [ ] Pertimbangkan AEAD agar padding tidak diperlukan.

### IV dan Nonce

- [ ] IV acak dari CSPRNG untuk CBC, CFB, OFB.
- [ ] IV baru untuk setiap enkripsi, tidak pernah dipakai ulang.
- [ ] Simpan IV atau nonce bersama ciphertext.
- [ ] Nonce GCM dan ChaCha20 96 bit, unik per kunci.
- [ ] Rotasi kunci sebelum batas jumlah pesan tercapai.
- [ ] Jangan menurunkan IV dari timestamp, user id, atau penghitung publik.

---

## 10. Latihan

1. Implementasikan PKCS#7 unpad yang benar dan uji dengan padding tidak valid.
2. Buat simulasi padding oracle pada CBC dan pulihkan satu blok penuh.
3. Enkripsi pesan sama dua kali dengan IV berbeda, tunjukkan ciphertext berbeda.
4. Enkripsi pesan sama dua kali dengan IV sama, tunjukkan ciphertext identik.
5. Jelaskan mengapa nonce reuse pada CTR lebih berbahaya daripada IV reuse pada CBC.
6. Rancang format file terenkripsi yang menyimpan versi, nonce, ciphertext, dan tag.
7. Cari tahu bagaimana TLS 1.3 menghindari masalah IV yang bisa diprediksi.

---

## 11. Referensi

- [NIST SP 800-38A](https://csrc.nist.gov/publications/detail/sp/800-38a/final), mode operasi dan IV.
- [NIST SP 800-38D](https://csrc.nist.gov/publications/detail/sp/800-38d/final), GCM dan nonce.
- [RFC 8018: PKCS#5](https://www.rfc-editor.org/rfc/rfc8018), padding dan KDF.
- [Serangan padding oracle](https://robertheaton.com/2013/07/29/padding-oracle-attack/)
- [Nonce reuse pada GCM](https://csrc.nist.gov/csrc/media/projects/block-cipher-techniques/documents/bcm/proposed-modes/gcm/gcm-spec.pdf)

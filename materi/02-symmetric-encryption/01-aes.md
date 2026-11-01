# 🔐 AES (Advanced Encryption Standard)

AES adalah standar enkripsi simetris yang dipakai hampir di seluruh internet: TLS, Wi-Fi (WPA2/WPA3), penyimpanan disk, VPN, dan pesan terenkripsi. Sejak 2001 menggantikan DES, AES belum pernah mengalami serangan praktis yang memecahkan cipher intinya. Yang sering diserang bukan AES, melainkan **cara memakainya**: mode operasi, padding, IV, dan manajemen kunci.

---

## 1. Latar Belakang

| Tahun | Peristiwa |
|---|---|
| 1977 | DES diadopsi, kunci efektif 56 bit |
| 1997 | NIST membuka kompetisi AES |
| 1998 | DES dipecah oleh EFF Deep Crack dalam 56 jam |
| 2000 | Rijndael (Daemen dan Rijmen) terpilih |
| 2001 | FIPS-197 diterbitkan |
| 2009 | Serangan related-key pada AES-256 versi lemah, tidak praktis untuk AES standar |
| 2019 | Serangan oracle pada mode CBC di implementasi nyata, bukan pada AES |

AES adalah **block cipher**, bukan cipher aliran. Ia memproses blok tetap 128 bit (16 byte) dengan kunci 128, 192, atau 256 bit.

---

## 2. Parameter

| Varian | Panjang kunci | Nk (word) | Nr (round) | Ukuran blok |
|---|---|---|---|---|
| AES-128 | 16 byte | 4 | 10 | 16 byte |
| AES-192 | 24 byte | 6 | 12 | 16 byte |
| AES-256 | 32 byte | 8 | 14 | 16 byte |

`Nk` adalah jumlah word 32 bit pada kunci, `Nr` adalah jumlah round.

Catatan keamanan: AES-128 secara teori cukup kuat, tetapi AES-256 lebih disukai untuk perlindungan jangka panjang karena margin terhadap serangan kuantum (Grover) lebih besar, meskipun Grover hanya memberi percepatan kuadratik.

---

## 3. Struktur State

AES memandang blok 16 byte sebagai matriks 4x4 **kolom demi kolom** (column major).

```
Input byte: b0 b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 b13 b14 b15

State:
    col0 col1 col2 col3
row0  b0   b4   b8   b12
row1  b1   b5   b9   b13
row2  b2   b6   b10  b14
row3  b3   b7   b11  b15
```

Konvensi ini penting saat mengimplementasikan ShiftRows dan MixColumns, karena keduanya bekerja per kolom.

---

## 4. Empat Transformasi

### SubBytes

Setiap byte diganti melalui S-box, sebuah pemetaan non-linear 8 bit ke 8 bit. S-box dibangun dari invers multiplikatif di `GF(2^8)` lalu transformasi affine:

```
s = inv(x) XOR rotl(inv(x),1) XOR rotl(inv(x),2) XOR rotl(inv(x),3) XOR rotl(inv(x),4) XOR 0x63
```

Properti penting: tidak ada titik tetap, tidak ada pasangan berlawanan, dan jarak minimum antar output tinggi. Inilah sumber **confusion**.

Nilai terkenal: `SBOX[0x00] = 0x63`, `SBOX[0x53] = 0xED`.

### ShiftRows

Baris `r` digeser ke kiri sebanyak `r` posisi.

```
sebelum        sesudah
b0 b4 b8 b12   b0 b4 b8 b12
b1 b5 b9 b13   b5 b9 b13 b1
b2 b6 b10 b14  b10 b14 b2 b6
b3 b7 b11 b15  b15 b3 b7 b11
```

Tujuan: menyebarkan byte antar kolom sehingga satu byte memengaruhi empat kolom pada round berikutnya.

### MixColumns

Setiap kolom dikalikan dengan matriks tetap di `GF(2^8)`:

```
[02 03 01 01]
[01 02 03 01]
[01 01 02 03]
[03 01 01 02]
```

Efeknya: satu byte berubah, seluruh kolom berubah. Inilah sumber **diffusion**.

### AddRoundKey

State di-XOR dengan round key. Satu-satunya langkah yang memasukkan kunci.

---

## 5. Alur Enkripsi

```
AddRoundKey(state, rk[0])
for round in 1..Nr-1:
    SubBytes
    ShiftRows
    MixColumns
    AddRoundKey(rk[round])
SubBytes
ShiftRows
AddRoundKey(rk[Nr])
```

Perhatikan: round terakhir **tidak** memakai MixColumns. Ini disengaja agar struktur enkripsi dan dekripsi simetris dan implementasi inverse lebih sederhana.

Dekripsi memakai urutan terbalik dengan transformasi inverse: InvShiftRows, InvSubBytes, AddRoundKey, InvMixColumns.

---

## 6. Key Expansion

Kunci diperluas menjadi `4 * (Nr + 1)` word 32 bit.

Untuk AES-128 (Nk = 4):

```
w[i] = w[i-4] XOR temp
temp = w[i-1]
jika i mod 4 == 0:
    temp = SubWord(RotWord(temp)) XOR Rcon[i/4]
```

`Rcon` adalah konstanta round:

```
Rcon = 01, 02, 04, 08, 10, 20, 40, 80, 1B, 36
```

Untuk AES-256, ada langkah tambahan `SubWord` setiap `i mod 8 == 4`.

Sifat penting: perbedaan satu bit pada kunci menyebar ke hampir semua round key setelah beberapa round.

---

## 7. Kenapa AES Cepat

1. **Operasi byte dan XOR.** Tidak ada perkalian bilangan besar, hanya tabel dan XOR.
2. **Paralelisme.** Setiap blok independen, dan dalam satu blok keempat kolom bisa diproses paralel.
3. **Instruksi hardware.** CPU modern punya AES-NI yang mengeksekusi satu round dalam satu instruksi. Throughput bisa melebihi 5 GB per detik per core.
4. **Tabel T (T-tables).** Implementasi software menggabungkan SubBytes, ShiftRows, dan MixColumns menjadi empat tabel lookup 32 bit.

---

## 8. Keamanan AES

### Serangan yang diketahui

| Serangan | Kompleksitas | Relevansi |
|---|---|---|
| Brute force AES-128 | 2^128 | Tidak praktis |
| Brute force AES-256 | 2^256 | Tidak praktis |
| Biclique (2011) | 2^126.1 untuk AES-128 | Akademis, tidak praktis |
| Related-key AES-256 | 2^99 | Hanya jika penyerang bisa memilih kunci terkait |
| Side channel (cache timing) | Bervariasi | Nyata pada implementasi tanpa AES-NI |
| Fault injection | Bervariasi | Nyata pada hardware fisik |

### Yang tidak diserang

Belum ada serangan yang memecahkan AES penuh dengan asumsi standar: penyerang hanya tahu ciphertext dan tidak punya akses ke kunci atau implementasi internal.

### Yang justru diserang

1. **Mode ECB** yang membocorkan pola.
2. **IV yang diulang** pada CBC atau CTR.
3. **Padding oracle** pada CBC.
4. **Nonce reuse** pada GCM, yang langsung membocorkan XOR plaintext dan merusak autentikasi.
5. **Kunci yang diturunkan dari password** tanpa KDF yang kuat.

Pelajaran: AES aman, tetapi sistem di sekitarnya yang rapuh.

---

## 9. Mode Operasi

| Mode | Paralel enkripsi | Butuh padding | Autentikasi | Catatan |
|---|---|---|---|---|
| ECB | Ya | Ya | Tidak | Jangan dipakai, membocorkan pola |
| CBC | Tidak (dekripsi ya) | Ya | Tidak | Butuh IV acak, rawan padding oracle |
| CFB | Ya | Tidak | Tidak | Mirip stream cipher |
| OFB | Ya | Tidak | Tidak | Keystream independen dari plaintext |
| CTR | Ya | Tidak | Tidak | Nonce tidak boleh diulang |
| GCM | Ya | Tidak | Ya (AEAD) | Pilihan default modern |
| CCM | Ya | Tidak | Ya | Cocok untuk perangkat terbatas |
| XTS | Ya | Ya | Tidak | Khusus enkripsi disk |

Untuk aplikasi baru, pilihan yang aman adalah **AES-GCM** atau **ChaCha20-Poly1305**. Detail perbandingan ada di `02-mode-cbc-vs-ecb.md`.

---

## 10. Contoh Kode

```python
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

key = get_random_bytes(32)          # AES-256
nonce = get_random_bytes(12)        # 96 bit untuk GCM

cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
ciphertext, tag = cipher.encrypt_and_digest(b"pesan rahasia")

# Dekripsi
cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
plaintext = cipher.decrypt_and_verify(ciphertext, tag)
```

Aturan penting:

1. Nonce GCM **wajib unik** untuk setiap enkripsi dengan kunci yang sama.
2. Simpan nonce dan tag bersama ciphertext.
3. Jangan pernah memakai ulang kunci tanpa rotasi.

---

## 11. Implementasi Manual

File `kode/02-symmetric-encryption/aes.py` mengimplementasikan AES-128, AES-192, dan AES-256 dari nol:

- S-box dibangkitkan secara matematis, bukan diketik manual.
- Key expansion lengkap untuk ketiga ukuran kunci.
- Enkripsi dan dekripsi blok tunggal.
- Mode CBC dengan PKCS#7 dan mode CTR dengan penghitung 64 bit.
- Uji vektor resmi FIPS-197 untuk ketiga varian.
- Perbandingan opsional dengan PyCryptodome.

Vektor uji yang dipakai:

```
plaintext  : 00112233445566778899aabbccddeeff
AES-128 key: 000102030405060708090a0b0c0d0e0f
AES-128 ct : 69c4e0d86a7b0430d8cdb78070b4c55a

AES-192 ct : dda97ca4864cdfe06eaf70a0ec0d7191
AES-256 ct : 8ea2b7ca516745bfeafc49904b496089
```

Peringatan: implementasi manual tidak constant time dan tidak boleh dipakai untuk melindungi data nyata.

---

## 12. Kesalahan Umum

1. Memakai ECB karena "lebih sederhana". Pola gambar tetap terlihat.
2. IV statis atau IV yang bisa diprediksi pada CBC.
3. Memakai nonce yang sama dua kali pada GCM. Ini bencana total.
4. Menyimpan kunci di source code atau environment tanpa KMS.
5. Menurunkan kunci langsung dari password dengan SHA-256. Gunakan Argon2, scrypt, atau PBKDF2.
6. Membandingkan tag autentikasi dengan `==` biasa yang tidak constant time.
7. Mengabaikan error saat verifikasi tag, sehingga menciptakan padding oracle.

---

## 13. Latihan

1. Bangkitkan S-box dengan kode sendiri dan cocokkan dengan tabel FIPS-197.
2. Ubah satu bit pada plaintext, hitung persentase bit ciphertext yang berubah setelah 1, 2, dan 4 round.
3. Implementasikan mode CFB dan OFB di atas `AES.encrypt_block`.
4. Bandingkan waktu enkripsi 1 MB data dengan implementasi manual dan PyCryptodome.
5. Jelaskan mengapa AES tidak memakai MixColumns pada round terakhir.
6. Rancang skema penyimpanan file dengan AES-GCM: apa saja yang harus disimpan bersama ciphertext.
7. Cari tahu mengapa AES-256 lebih lambat dari AES-128 di CPU tanpa AES-NI.

---

## 14. Referensi

- [FIPS-197: Advanced Encryption Standard](https://csrc.nist.gov/publications/detail/fips/197/final)
- [NIST SP 800-38A: Mode of Operation](https://csrc.nist.gov/publications/detail/sp/800-38a/final)
- [NIST SP 800-38D: GCM](https://csrc.nist.gov/publications/detail/sp/800-38d/final)
- Christof Paar dan Jan Pelzl, *Understanding Cryptography*, bab 4.
- [AES Step by Step](https://formaestudio.com/rijndaelinspector/archivos/Rijndael_Animation_v4_eng-html5.html)

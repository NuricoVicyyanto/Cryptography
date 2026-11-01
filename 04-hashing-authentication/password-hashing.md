# 🛡️ Password Hashing

Menyimpan password pengguna adalah salah satu tugas keamanan yang paling sering dilakukan dan paling sering salah. Hash cepat seperti SHA-256 tidak dirancang untuk ini. Yang dibutuhkan adalah fungsi yang **sengaja lambat** dan **memory-hard**, sehingga satu tebakan mahal bagi penyerang.

---

## 1. Ancaman yang Dihadapi

1. **Kebocoran database.** Penyerang mendapat tabel `users` berisi hash.
2. **Brute force offline.** Tanpa batas request, GPU bisa menguji miliaran kandidat per detik.
3. **Rainbow table.** Tabel hash yang sudah dihitung sebelumnya.
4. **Credential stuffing.** Password yang bocor dipakai ulang di layanan lain.
5. **Serangan online.** Tebakan langsung ke endpoint login, dibatasi dengan rate limit.

Password hashing yang baik hanya bisa mengatasi ancaman 1 sampai 3. Untuk 4 dan 5 dibutuhkan MFA, rate limiting, dan pemantauan kebocoran.

---

## 2. Kenapa Hash Cepat Gagal

SHA-256 dirancang cepat. GPU modern bisa menghitung lebih dari 10 miliar SHA-256 per detik. Dengan daftar 10 juta password umum, seluruh daftar bisa diuji dalam waktu kurang dari satu detik.

Solusinya adalah **key derivation function** yang mahal secara komputasi dan memori:

| Fungsi | Tahun | Memory-hard | Paralel | Catatan |
|---|---|---|---|---|
| PBKDF2 | 2000 | Tidak | Ya | FIPS, paling kompatibel |
| bcrypt | 1999 | Sedikit | Terbatas | Maksimal 72 byte password |
| scrypt | 2009 | Ya | Ya | Butuh memori besar |
| Argon2 | 2015 | Ya | Ya | Pemenang PHC, pilihan utama |

---

## 3. Salt

Salt adalah nilai acak yang ditambahkan ke password sebelum di-hash.

```
hash = KDF(password, salt)
```

Fungsi salt:

1. **Mencegah rainbow table.** Tabel harus dibuat ulang untuk setiap salt.
2. **Membuat hash unik.** Dua pengguna dengan password sama menghasilkan hash berbeda.
3. **Mencegah identifikasi pengguna dengan password sama.**

Aturan:

- Salt minimal 16 byte, dari CSPRNG.
- Salt tidak perlu rahasia.
- Salt harus unik per pengguna, bukan per aplikasi.
- Simpan salt bersama hash.

Salt **tidak** memperlambat serangan terhadap satu password tertentu. Ia hanya membuat serangan massal menjadi mahal.

---

## 4. Pepper

Pepper adalah nilai rahasia tambahan yang disimpan terpisah dari database, misalnya di environment variable atau KMS.

```
hash = KDF(password, salt)
stored = Encrypt(pepper, hash)
```

Atau:

```
hash = HMAC(pepper, password)
```

Manfaat: jika hanya database yang bocor, penyerang tetap butuh pepper.

Keterbatasan: jika kode aplikasi juga bocor, pepper ikut bocor. Jangan menganggapnya pengganti salt atau KDF yang kuat.

---

## 5. Faktor Biaya

Setiap KDF punya parameter biaya:

| Fungsi | Parameter | Arti |
|---|---|---|
| PBKDF2 | iterations | Jumlah pengulangan HMAC |
| bcrypt | cost | 2^cost iterasi |
| scrypt | N, r, p | Memori, blok, paralelisme |
| Argon2 | memory, iterations, parallelism | Memori, waktu, thread |

Target praktis: satu verifikasi memakan 100 sampai 500 milidetik pada server produksi, dan parameter harus dinaikkan seiring waktu.

---

## 6. PBKDF2

Standar: RFC 8018, NIST SP 800-132.

```
DK = T1 || T2 || ... || Tn
Ti = F(P, S, c, i)
F  = U1 xor U2 xor ... xor Uc
U1 = HMAC(P, S || INT(i))
Uj = HMAC(P, U(j-1))
```

Kelebihan:

- Didukung di mana-mana, termasuk FIPS.
- Sederhana dan mudah diimplementasikan.
- Parameter mudah dipahami.

Kekurangan:

- Tidak memory-hard, sehingga GPU dan ASIC sangat efisien.
- Butuh iterasi sangat tinggi untuk setara Argon2.

Rekomendasi OWASP: 600.000 iterasi untuk PBKDF2-HMAC-SHA256, atau 210.000 untuk SHA-512.

Contoh:

```python
import hashlib

salt = os.urandom(16)
dk = hashlib.pbkdf2_hmac("sha256", password, salt, 600_000, 32)
```

---

## 7. bcrypt

Dibuat oleh Niels Provos dan David Mazieres pada 1999, berbasis cipher Blowfish.

```
bcrypt(cost, salt, password)
```

Kelebihan:

- Sudah teruji lama.
- Cost factor mudah dinaikkan.
- Tahan terhadap GPU karena memakai memori dan operasi non-linear.

Kekurangan:

- Memotong password pada 72 byte. Password lebih panjang diamankan dengan pre-hash, tetapi itu menimbulkan jebakan.
- Tidak memory-hard seperti scrypt atau Argon2.
- Tidak cocok untuk password dengan byte nol.

Format hash:

```
$2b$12$R9h/cIPz0gi.URNNX3kh2OPST9/PgBkqquzi.Ss7KIUgO2t0jWMUW
 |  |  |                    |
 |  |  salt (22 karakter)   hash
 |  cost
 versi
```

Contoh:

```python
import bcrypt

salt = bcrypt.gensalt(rounds=12)
hashed = bcrypt.hashpw(password, salt)
ok = bcrypt.checkpw(password, hashed)
```

---

## 8. scrypt

Standar: RFC 7914. Dirancang untuk mahal secara memori.

```
scrypt(P, S, N, r, p, dkLen)
```

Parameter:

- `N`: cost, harus pangkat dua. Memori sekitar `128 * r * N` byte.
- `r`: ukuran blok, biasanya 8.
- `p`: paralelisme, biasanya 1.

Contoh:

```python
import hashlib

dk = hashlib.scrypt(password, salt=salt, n=2**15, r=8, p=1,
                    dklen=32, maxmem=64 * 1024 * 1024)
```

Kelebihan:

- Memory-hard, sehingga ASIC mahal.
- Parameter jelas.

Kekurangan:

- Butuh memori besar per verifikasi, sehingga bisa menjadi serangan DoS jika parameter terlalu tinggi.
- Kurang fleksibel dibanding Argon2.

Implementasi dari nol ada di `password-hashing.py`, termasuk Salsa20/8 dan BlockMix.

---

## 9. Argon2

Pemenang Password Hashing Competition 2015, distandarkan di RFC 9106.

Tiga varian:

| Varian | Sifat | Penggunaan |
|---|---|---|
| Argon2d | Data-dependent memory access | Tahan GPU, rentan side channel |
| Argon2i | Data-independent | Tahan side channel, kurang tahan GPU |
| Argon2id | Hibrida | Pilihan default |

Parameter:

```
memory  : KiB, misalnya 65536 untuk 64 MB
time    : jumlah iterasi, misalnya 3
parallelism : jumlah lane, misalnya 4
```

Contoh:

```python
from argon2 import PasswordHasher

ph = PasswordHasher(time_cost=3, memory_cost=65536, parallelism=4)
hash_value = ph.hash(password)
ok = ph.verify(hash_value, password)
```

Kelebihan:

- Memori dan waktu bisa diatur terpisah.
- Argon2id tahan side channel dan GPU.
- Format hash menyimpan parameter, sehingga mudah dimigrasi.

Rekomendasi OWASP: Argon2id dengan 19 MiB, 2 iterasi, 1 paralelisme sebagai minimum; 46 MiB atau lebih untuk keamanan lebih tinggi.

---

## 10. Perbandingan

| Aspek | PBKDF2 | bcrypt | scrypt | Argon2id |
|---|---|---|---|---|
| Memory-hard | Tidak | Sedikit | Ya | Ya |
| Tahan GPU | Rendah | Sedang | Tinggi | Tinggi |
| Tahan side channel | Ya | Ya | Ya | Ya dengan id |
| Dukungan library | Sangat luas | Luas | Luas | Baik |
| FIPS | Ya | Tidak | Tidak | Tidak |
| Batas password | Tidak ada | 72 byte | Tidak ada | Tidak ada |
| Rekomendasi 2026 | Warisan | Masih layak | Layak | Utama |

Jika membangun sistem baru, gunakan Argon2id. Jika tidak tersedia, gunakan scrypt. Jika keduanya tidak tersedia, bcrypt dengan cost 12 atau lebih. PBKDF2 hanya jika ada kebutuhan kepatuhan.

---

## 11. Verifikasi dan Timing

Verifikasi harus constant time dan tidak membocorkan apakah username ada.

```python
def login(username: str, password: str) -> bool:
    record = db.find(username)
    if record is None:
        # Lakukan dummy hash agar waktu respons serupa
        dummy_verify(password)
        return False
    return verify_hash(record.hash, password)
```

Kesalahan:

- Mengembalikan "user tidak ditemukan" berbeda dari "password salah".
- Waktu respons berbeda antara user ada dan tidak ada.
- Membandingkan hash dengan `==`.

---

## 12. Migrasi dan Rotasi

Format penyimpanan harus menyertakan algoritma dan parameter:

```
$argon2id$v=19$m=65536,t=3,p=4$c2FsdA$aGFzaA
```

Saat pengguna login:

1. Baca parameter dari hash.
2. Verifikasi.
3. Jika parameter di bawah kebijakan saat ini, hitung ulang dengan parameter baru dan simpan.
4. Ini disebut **rehash on login**.

Jangan memaksa reset password hanya karena parameter berubah.

---

## 13. Kebijakan Password

Praktik modern (NIST SP 800-63B):

1. Minimal 8 karakter, disarankan 12.
2. Izinkan panjang sampai minimal 64 karakter.
3. Jangan memaksa kombinasi karakter yang rumit.
4. Periksa terhadap daftar password bocor (misalnya Have I Been Pwned).
5. Jangan memaksa rotasi berkala tanpa alasan.
6. Jangan memakai pertanyaan keamanan.
7. Dukung password manager, jangan blokir paste.
8. Terapkan rate limiting dan MFA.

---

## 14. Kesalahan Umum

1. Memakai SHA-256 atau MD5 untuk password.
2. Memakai salt yang sama untuk semua pengguna.
3. Tidak memakai salt sama sekali.
4. Memakai salt pendek, misalnya 4 byte.
5. Parameter biaya terlalu rendah.
6. Membandingkan hash dengan `==`.
7. Menyimpan password di log.
8. Mengirim password lewat email.
9. Memakai enkripsi reversibel untuk password.
10. Membatasi panjang password pada 8 atau 12 karakter.
11. Menerapkan aturan komposisi yang rumit dan rotasi wajib.
12. Lupa menaikkan parameter seiring waktu.

---

## 15. Implementasi di Folder Ini

`password-hashing.py` berisi:

- PBKDF2-HMAC-SHA256 dari nol, diuji terhadap `hashlib`.
- scrypt dari nol, termasuk `salsa20_8`, `blockmix`, dan `romix`, diuji terhadap `hashlib.scrypt`.
- Demonstrasi serangan kamus pada SHA-256.
- Demonstrasi salt menghasilkan hash berbeda.
- Perbandingan biaya waktu SHA-256, PBKDF2, dan scrypt.
- Format penyimpanan yang menyertakan algoritma, parameter, salt, dan hash.

Contoh keluaran:

```
PBKDF2 310000 iterasi : 355 ms
scrypt N=16384 r=8    : 83 ms
```

---

## 16. Latihan

1. Implementasikan PBKDF2 dan cocokkan dengan `hashlib.pbkdf2_hmac`.
2. Implementasikan scrypt dan cocokkan dengan `hashlib.scrypt`.
3. Ukur waktu verifikasi Argon2id dengan parameter berbeda.
4. Rancang skema rehash on login.
5. Simulasikan serangan kamus pada hash SHA-256 tanpa salt dan dengan salt.
6. Jelaskan mengapa bcrypt membatasi password 72 byte.
7. Bandingkan penggunaan memori scrypt N=2^14, 2^15, dan 2^16.
8. Buat endpoint login yang tidak membocorkan keberadaan username.

---

## 17. Referensi

- [OWASP Password Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)
- [RFC 9106: Argon2](https://www.rfc-editor.org/rfc/rfc9106)
- [RFC 7914: scrypt](https://www.rfc-editor.org/rfc/rfc7914)
- [RFC 8018: PKCS#5](https://www.rfc-editor.org/rfc/rfc8018)
- [NIST SP 800-63B: Digital Identity Guidelines](https://pages.nist.gov/800-63-3/sp800-63b.html)
- [Password Hashing Competition](https://www.password-hashing.net/)

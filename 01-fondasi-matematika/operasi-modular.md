# 🔁 Operasi Modular untuk Kriptografi

Aritmatika modular adalah "matematika jam". Semua operasi dilakukan dalam rentang terbatas `0` sampai `n-1`, lalu diputar kembali ke awal. Hampir semua algoritma kriptografi modern berdiri di atas operasi ini: RSA memakai eksponensial modular, Diffie-Hellman memakai perkalian modular, AES memakai aritmatika di `GF(2^8)`, dan ECC memakai aritmatika modulo bilangan prima besar.

---

## 1. Definisi Dasar

Notasi `a mod n` menyatakan sisa pembagian `a` oleh `n`.

```
a = q * n + r,  dengan 0 <= r < n
maka a mod n = r
```

Contoh:

```
17 mod 5 = 2      karena 17 = 3 * 5 + 2
-3 mod 7 = 4      karena -3 = (-1) * 7 + 4
25 mod 5 = 0
```

Catatan penting: dalam Python, `%` selalu mengembalikan hasil non-negatif untuk `n > 0`, sehingga `-3 % 7 == 4`. Ini berbeda dengan C atau Java yang mengembalikan `-3`. Untuk kriptografi, konvensi non-negatif yang benar.

### Kongruensi

Dua bilangan `a` dan `b` disebut kongruen modulo `n` jika selisihnya habis dibagi `n`:

```
a ≡ b (mod n)  ⇔  n | (a - b)
```

Contoh: `22 ≡ 4 (mod 6)` karena `22 - 4 = 18` habis dibagi 6.

---

## 2. Properti Aritmatika Modular

Semua properti berikut menjadi dasar optimasi implementasi, karena kita boleh mereduksi modulo di setiap langkah tanpa mengubah hasil akhir.

| Operasi | Sifat | Contoh |
|---|---|---|
| Penjumlahan | `(a + b) mod n = ((a mod n) + (b mod n)) mod n` | `(17 + 25) mod 7 = 42 mod 7 = 0` |
| Pengurangan | `(a - b) mod n = ((a mod n) - (b mod n)) mod n` | `(3 - 10) mod 7 = 0` |
| Perkalian | `(a * b) mod n = ((a mod n) * (b mod n)) mod n` | `(17 * 25) mod 7 = (3 * 4) mod 7 = 5` |
| Perpangkatan | `a^b mod n = (a mod n)^b mod n` | `(12^5) mod 7 = (5^5) mod 7` |
| Distributif | `a * (b + c) ≡ a*b + a*c (mod n)` | berlaku umum |

**Kenapa penting?** Angka di kriptografi bisa ribuan bit. Dengan mereduksi modulo di setiap langkah, ukuran angka tetap kecil sehingga perkalian tetap murah.

Yang **tidak** boleh dilakukan: pembagian biasa. `(a / b) mod n` tidak sama dengan `(a mod n) / (b mod n)`. Pembagian modulo harus memakai invers modular.

---

## 3. Penjumlahan dan Pengurangan Modular

```python
def mod_add(a, b, n):
    return (a + b) % n

def mod_sub(a, b, n):
    return (a - b) % n
```

Aplikasi nyata: Caesar cipher adalah penjumlahan modular dengan `n = 26`.

```
'E' = 4, geser 3  ->  (4 + 3) mod 26 = 7  ->  'H'
```

---

## 4. Perkalian Modular

```python
def mod_mul(a, b, n):
    return (a * b) % n
```

Untuk angka besar (lebih dari 64 bit), `a * b` bisa meluap di bahasa seperti C. Solusinya adalah **perkalian Rusia** (double and add), yang hanya memakai penjumlahan dan penggandaan:

```python
def mod_mul_safe(a, b, n):
    """Hitung (a * b) % n tanpa pernah melampaui 2n."""
    result = 0
    a %= n
    while b > 0:
        if b & 1:
            result = (result + a) % n
        a = (a * 2) % n
        b >>= 1
    return result
```

Di Python tidak diperlukan karena `int` bersifat arbitrary precision, tetapi konsep ini penting saat membaca implementasi C atau hardware.

---

## 5. Invers Modular

Invers dari `a` modulo `n` adalah bilangan `x` sehingga:

```
a * x ≡ 1 (mod n)
```

Ditulis `x = a^(-1) mod n`.

**Syarat keberadaan:** `gcd(a, n) = 1`. Jika tidak koprima, invers tidak ada.

Contoh: invers dari `3` modulo `11` adalah `4`, karena `3 * 4 = 12 ≡ 1 (mod 11)`.

### Metode 1: Extended Euclidean Algorithm

Algoritma ini mencari `x, y` sehingga `a*x + n*y = gcd(a, n)`. Jika gcd = 1, maka `x` adalah invers.

```python
def egcd(a, b):
    if b == 0:
        return a, 1, 0
    g, x1, y1 = egcd(b, a % b)
    return g, y1, x1 - (a // b) * y1

def mod_inverse(a, n):
    g, x, _ = egcd(a, n)
    if g != 1:
        raise ValueError(f"{a} tidak punya invers modulo {n}")
    return x % n
```

Verifikasi: `egcd(3, 11)` menghasilkan `1, 4, -1`, sehingga `3*4 + 11*(-1) = 1`. Benar.

### Metode 2: Fermat's Little Theorem

Jika `n` adalah bilangan prima dan `a` tidak habis dibagi `n`:

```
a^(n-1) ≡ 1 (mod n)   ⇒   a^(-1) ≡ a^(n-2) (mod n)
```

Metode ini lebih mahal karena butuh eksponensial modular, tetapi berguna ketika `n` sudah diketahui prima. Di kriptografi kurva eliptik, invers modulo prima sering dihitung dengan cara ini.

### Metode 3: Euler's Theorem

Untuk modulus komposit `n` dengan `gcd(a, n) = 1`:

```
a^φ(n) ≡ 1 (mod n)   ⇒   a^(-1) ≡ a^(φ(n)-1) (mod n)
```

`φ` adalah totient Euler. Untuk RSA, `φ(n) = (p-1)(q-1)`.

---

## 6. Eksponensial Modular

Menghitung `a^b mod n` secara naif butuh `b` perkalian. Untuk `b` berukuran 2048 bit, itu mustahil. Solusinya adalah **square and multiply** (binary exponentiation) dengan kompleksitas `O(log b)`.

```python
def mod_exp(a, b, n):
    result = 1
    a %= n
    while b > 0:
        if b & 1:              # bit terakhir b adalah 1
            result = (result * a) % n
        a = (a * a) % n        # kuadratkan basis
        b >>= 1                # geser b satu bit
    return result
```

Contoh langkah untuk `3^13 mod 7`:

```
b = 13 = 1101b
bit 1: result = 1*3 = 3,      a = 9 mod 7 = 2,  b = 6
bit 0: result = 3,            a = 4,            b = 3
bit 1: result = 3*4 = 12 = 5, a = 16 mod 7 = 2, b = 1
bit 1: result = 5*2 = 10 = 3, a = 4,            b = 0
hasil = 3
```

Cek: `3^13 = 1594323`, dan `1594323 mod 7 = 3`. Benar.

Di Python 3, `pow(a, b, n)` sudah mengimplementasikan versi yang jauh lebih cepat (memakai algoritma Montgomery dan sliding window). Gunakan `pow` di produksi, gunakan versi manual untuk belajar.

---

## 7. Teorema Pendukung

### Fermat's Little Theorem

Jika `p` prima dan `gcd(a, p) = 1`:

```
a^(p-1) ≡ 1 (mod p)
```

Ini dasar dari uji primalitas Fermat dan invers cepat modulo prima.

### Euler's Theorem

Jika `gcd(a, n) = 1`:

```
a^φ(n) ≡ 1 (mod n)
```

### Chinese Remainder Theorem (CRT)

Jika `n = n1 * n2` dengan `gcd(n1, n2) = 1`, sistem

```
x ≡ a1 (mod n1)
x ≡ a2 (mod n2)
```

punya solusi unik modulo `n`. RSA memakai CRT untuk mempercepat dekripsi sekitar 4 kali lipat, karena eksponensial dilakukan modulo `p` dan `q` yang jauh lebih kecil.

```python
def crt(a1, n1, a2, n2):
    inv = mod_inverse(n1, n2)
    t = ((a2 - a1) * inv) % n2
    return a1 + t * n1, n1 * n2
```

### Order dan Generator

Order dari `a` modulo `n` adalah bilangan positif terkecil `k` sehingga `a^k ≡ 1 (mod n)`. Jika order `a` sama dengan `φ(n)`, maka `a` disebut **primitive root** atau generator. Diffie-Hellman dan ElGamal membutuhkan generator dari grup prima.

---

## 8. Aritmatika di GF(2^8) untuk AES

AES tidak memakai modulo bilangan bulat, tetapi modulo polinomial biner. Setiap byte dianggap polinomial derajat 7 dengan koefisien 0 atau 1.

Contoh di `GF(2^8)` dengan polinomial irreducible `x^8 + x^4 + x^3 + x + 1` (`0x11B`):

```
0x57 * 0x83 = 0xC1
```

Perkalian dilakukan dengan shift dan XOR, bukan `*`. Inilah sebabnya AES sangat cepat di hardware.

---

## 9. Ringkasan Kompleksitas

| Operasi | Naif | Efisien |
|---|---|---|
| `a + b mod n` | O(1) | O(1) |
| `a * b mod n` | O(1) | O(1) |
| `a^(-1) mod n` | O(n) | O(log n) dengan EEA |
| `a^b mod n` | O(b) | O(log b) dengan square-multiply |
| Uji prima | O(√n) | O(k log^3 n) dengan Miller-Rabin |

---

## 10. Kesalahan Umum

1. **Membagi tanpa invers.** `(a / b) % n` di Python menghasilkan float dan kehilangan presisi. Selalu pakai `a * mod_inverse(b, n) % n`.
2. **Lupa syarat koprima.** Memanggil invers pada `gcd != 1` akan gagal atau menghasilkan sampah.
3. **Salah menangani bilangan negatif.** Di C, `-3 % 7 == -3`. Selalu normalisasi dengan `((x % n) + n) % n`.
4. **Memakai `**` untuk eksponen besar.** `a ** b` akan menghabiskan memori. Gunakan `pow(a, b, n)`.
5. **Menganggap modulo prima selalu aman.** Modulus komposit mengubah struktur grup dan bisa membocorkan informasi.

---

## 11. Kaitan ke Materi Berikutnya

| Konsep di sini | Dipakai di |
|---|---|
| Invers modular | RSA (kunci privat `d`), ECC (pembagian titik) |
| Eksponensial modular | RSA, Diffie-Hellman, ElGamal, DSA |
| Generator grup | Diffie-Hellman, ElGamal, DSA |
| CRT | Optimasi dekripsi RSA |
| GF(2^8) | AES, MixColumns |

---

## 12. Latihan

1. Hitung `(1234 * 5678) mod 97` tanpa menghitung hasil perkalian penuh terlebih dahulu.
2. Tentukan invers dari `17` modulo `43` dengan EEA, lalu verifikasi.
3. Hitung `5^117 mod 19` dengan square and multiply, tuliskan langkah bitanya.
4. Buktikan bahwa `a^2 mod 4` hanya bisa bernilai `0` atau `1`.
5. Selesaikan sistem `x ≡ 2 (mod 5)` dan `x ≡ 3 (mod 7)` dengan CRT.
6. Implementasikan `mod_exp` lalu bandingkan waktunya dengan `pow(a, b, n)` untuk eksponen 2048 bit.

---

## 13. Referensi

- David Burton, *Elementary Number Theory*, bab kongruensi.
- Christof Paar dan Jan Pelzl, *Understanding Cryptography*, bab 1 dan 6.
- [Python docs: pow()](https://docs.python.org/3/library/functions.html#pow)
- [Khan Academy: Modular arithmetic](https://www.khanacademy.org/computing/computer-science/cryptography/modarithmetic/a/what-is-modular-arithmetic)

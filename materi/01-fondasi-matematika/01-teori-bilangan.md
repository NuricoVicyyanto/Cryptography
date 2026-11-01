
# 📘 Teori Bilangan untuk Kriptografi

Teori bilangan adalah cabang matematika yang menjadi fondasi utama dalam kriptografi modern, khususnya kriptografi asimetris seperti RSA, Diffie-Hellman, dan ElGamal. Berikut adalah konsep-konsep penting yang perlu dipahami:

---

## 🧮 1. Bilangan Prima

**Definisi:**  
Bilangan prima adalah bilangan bulat positif lebih besar dari 1 yang hanya memiliki dua pembagi positif: 1 dan dirinya sendiri.

**Contoh:**  
2, 3, 5, 7, 11, 13, 17, ...

**Kenapa penting di kriptografi?**  
- RSA menggunakan dua bilangan prima besar untuk menghasilkan pasangan kunci.
- Keamanan banyak algoritma bergantung pada kesulitan faktorisasi bilangan besar.

---

## 🔄 2. Faktor Persekutuan Terbesar (GCD)

**Definisi:**  
GCD (Greatest Common Divisor) dari dua bilangan a dan b adalah bilangan bulat terbesar yang membagi keduanya tanpa sisa.

**Algoritma:**  
- Gunakan algoritma Euclidean:
  ```
  gcd(a, b) = gcd(b, a % b)
  ```
- Contoh:
  ```
  gcd(48, 18) = gcd(18, 12) = gcd(12, 6) = gcd(6, 0) = 6
  ```

**Implementasi Python:**
```python
def gcd(a, b):
    while b:
        a, b = b, a % b
    return a
```

---

## 🔁 3. Aritmatika Modular

**Definisi:**  
`a ≡ b (mod n)` artinya `(a - b)` habis dibagi oleh `n`. Dengan kata lain, `a` dan `b` memiliki sisa yang sama jika dibagi `n`.

**Contoh:**
- `17 mod 5 = 2`
- `22 ≡ 4 (mod 6)`

**Properti Penting:**
- Penjumlahan: `(a + b) mod n ≡ (a mod n + b mod n) mod n`
- Perkalian: `(a × b) mod n ≡ (a mod n × b mod n) mod n`

---

## 🧠 4. Invers Modulo

**Definisi:**  
Invers dari `a` modulo `m` adalah bilangan `x` sedemikian hingga:
```
(a * x) % m == 1
```
Invers hanya ada jika `gcd(a, m) = 1`.

**Contoh:**  
Invers dari `3 mod 11` adalah `4`, karena:
```
(3 × 4) % 11 = 12 % 11 = 1
```

**Algoritma:**  
Gunakan **Extended Euclidean Algorithm**.

**Python Code:**
```python
def mod_inverse(a, m):
    # Menggunakan Extended Euclidean Algorithm
    m0, x0, x1 = m, 0, 1
    while a > 1:
        q = a // m
        a, m = m, a % m
        x0, x1 = x1 - q * x0, x0
    return x1 % m0
```

---

## 🧩 5. Eksponensial Modular Cepat (Fast Mod Exponentiation)

**Definisi:**  
Digunakan untuk menghitung `(a^b) mod m` dengan efisien.

**Kenapa penting?**
- RSA menggunakan operasi ini untuk enkripsi dan dekripsi:
  ```
  c = (m^e) mod n
  m = (c^d) mod n
  ```

**Python Code:**
```python
def mod_exp(a, b, m):
    result = 1
    a = a % m
    while b > 0:
        if b % 2 == 1:
            result = (result * a) % m
        b = b >> 1
        a = (a * a) % m
    return result
```

---

## 🏁 Penutup

Teori bilangan memberikan landasan matematis penting bagi hampir seluruh algoritma kriptografi. Memahami konsep GCD, invers mod, dan aritmatika modular adalah syarat wajib sebelum masuk ke RSA, ECC, dan sistem kriptografi lainnya.

---

## 📚 Latihan

1. Tentukan apakah 101 adalah bilangan prima.
2. Hitung `gcd(4864, 3458)`.
3. Temukan invers modulo dari `17 mod 43`.
4. Hitung `7^128 mod 13` menggunakan fast modular exponentiation.

---

## 🔗 Referensi

- *Elementary Number Theory* by David Burton  
- [CryptoPals Challenges](https://cryptopals.com/)
- Khan Academy: Number Theory Basics

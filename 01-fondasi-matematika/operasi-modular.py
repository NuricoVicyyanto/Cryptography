"""
operasi-modular.py
Implementasi operasi aritmatika modular dari nol untuk pembelajaran kriptografi.

Isi:
    1. gcd dan extended gcd (EEA)
    2. invers modular (EEA, Fermat, Euler)
    3. eksponensial modular (square and multiply)
    4. perkalian modular aman untuk angka besar
    5. Chinese Remainder Theorem
    6. order elemen dan pencarian generator
    7. demo dan pengujian mandiri

Jalankan:
    python operasi-modular.py
"""

from __future__ import annotations

import random
import time


# ---------------------------------------------------------------------------
# 1. GCD dan Extended Euclidean Algorithm
# ---------------------------------------------------------------------------

def gcd(a: int, b: int) -> int:
    """GCD dengan algoritma Euclidean iteratif."""
    a, b = abs(a), abs(b)
    while b:
        a, b = b, a % b
    return a


def egcd(a: int, b: int) -> tuple[int, int, int]:
    """
    Extended Euclidean Algorithm.
    Mengembalikan (g, x, y) sehingga a*x + b*y == g == gcd(a, b).
    """
    old_r, r = a, b
    old_s, s = 1, 0
    old_t, t = 0, 1
    while r != 0:
        q = old_r // r
        old_r, r = r, old_r - q * r
        old_s, s = s, old_s - q * s
        old_t, t = t, old_t - q * t
    return old_r, old_s, old_t


# ---------------------------------------------------------------------------
# 2. Invers Modular
# ---------------------------------------------------------------------------

def mod_inverse(a: int, n: int) -> int:
    """Invers modular memakai EEA. Melempar ValueError jika tidak ada."""
    g, x, _ = egcd(a % n, n)
    if g != 1:
        raise ValueError(f"{a} tidak punya invers modulo {n} (gcd={g})")
    return x % n


def mod_inverse_fermat(a: int, p: int) -> int:
    """
    Invers modulo p prima memakai Fermat: a^(p-2) mod p.
    Hanya valid jika p prima dan a bukan kelipatan p.
    """
    if a % p == 0:
        raise ValueError("a habis dibagi p, tidak ada invers")
    return pow(a, p - 2, p)


def euler_phi(n: int) -> int:
    """Totient Euler dengan faktorisasi trial division sederhana."""
    if n <= 0:
        raise ValueError("n harus positif")
    result = n
    p = 2
    m = n
    while p * p <= m:
        if m % p == 0:
            while m % p == 0:
                m //= p
            result -= result // p
        p += 1
    if m > 1:
        result -= result // m
    return result


def mod_inverse_euler(a: int, n: int) -> int:
    """Invers modular memakai Euler: a^(phi(n)-1) mod n."""
    if gcd(a, n) != 1:
        raise ValueError("a dan n harus koprima")
    return pow(a, euler_phi(n) - 1, n)


# ---------------------------------------------------------------------------
# 3. Eksponensial Modular
# ---------------------------------------------------------------------------

def mod_exp(a: int, b: int, n: int) -> int:
    """Hitung a^b mod n dengan square and multiply, O(log b)."""
    if n <= 0:
        raise ValueError("modulus harus positif")
    if b < 0:
        a = mod_inverse(a, n)
        b = -b
    result = 1
    a %= n
    while b > 0:
        if b & 1:
            result = (result * a) % n
        a = (a * a) % n
        b >>= 1
    return result


def mod_exp_trace(a: int, b: int, n: int) -> list[tuple[int, int, int, int]]:
    """
    Versi mod_exp yang mencatat setiap langkah.
    Setiap baris: (bit, b_sebelum, result, a)
    """
    steps = []
    result = 1
    a %= n
    while b > 0:
        steps.append((b & 1, b, result, a))
        if b & 1:
            result = (result * a) % n
        a = (a * a) % n
        b >>= 1
    return steps


# ---------------------------------------------------------------------------
# 4. Perkalian Modular Aman
# ---------------------------------------------------------------------------

def mod_mul_safe(a: int, b: int, n: int) -> int:
    """
    Hitung (a*b) % n hanya dengan penjumlahan dan penggandaan.
    Berguna di bahasa yang rawan overflow 64 bit.
    """
    result = 0
    a %= n
    while b > 0:
        if b & 1:
            result = (result + a) % n
        a = (a << 1) % n
        b >>= 1
    return result


# ---------------------------------------------------------------------------
# 5. Chinese Remainder Theorem
# ---------------------------------------------------------------------------

def crt_2(a1: int, n1: int, a2: int, n2: int) -> tuple[int, int]:
    """Selesaikan x = a1 (mod n1), x = a2 (mod n2). Kembalikan (x, n1*n2)."""
    inv = mod_inverse(n1 % n2, n2)
    t = ((a2 - a1) * inv) % n2
    x = a1 + t * n1
    return x % (n1 * n2), n1 * n2


def crt(items: list[tuple[int, int]]) -> tuple[int, int]:
    """CRT untuk banyak kongruensi (a, n) dengan modulus saling koprima."""
    x, mod = 0, 1
    for a, n in items:
        x, mod = crt_2(x, mod, a % n, n)
    return x, mod


# ---------------------------------------------------------------------------
# 6. Order dan Generator
# ---------------------------------------------------------------------------

def multiplicative_order(a: int, n: int) -> int:
    """Order terkecil k > 0 sehingga a^k = 1 (mod n)."""
    if gcd(a, n) != 1:
        raise ValueError("a dan n harus koprima")
    k = 1
    value = a % n
    while value != 1:
        value = (value * a) % n
        k += 1
        if k > n:
            raise RuntimeError("order tidak ditemukan, periksa modulus")
    return k


def find_generator(p: int) -> int:
    """Cari generator grup multiplikatif modulo p prima."""
    phi = p - 1
    for g in range(2, p):
        if gcd(g, p) != 1:
            continue
        if multiplicative_order(g, p) == phi:
            return g
    raise ValueError("generator tidak ditemukan")


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

def demo_gcd() -> None:
    print("== GCD dan EEA ==")
    a, b = 4864, 3458
    print(f"gcd({a}, {b}) = {gcd(a, b)}")
    g, x, y = egcd(a, b)
    print(f"egcd({a}, {b}) = ({g}, {x}, {y})")
    print(f"cek: {a}*{x} + {b}*{y} = {a*x + b*y}")
    print()


def demo_inverse() -> None:
    print("== Invers Modular ==")
    a, n = 17, 43
    inv = mod_inverse(a, n)
    print(f"invers {a} mod {n} = {inv}, cek {(a*inv) % n}")
    print(f"versi Fermat  = {mod_inverse_fermat(a, n)}")
    print(f"versi Euler   = {mod_inverse_euler(a, n)}")
    print()


def demo_exp() -> None:
    print("== Eksponensial Modular ==")
    a, b, n = 3, 13, 7
    print(f"{a}^{b} mod {n} = {mod_exp(a, b, n)}")
    for bit, bb, res, base in mod_exp_trace(a, b, n):
        print(f"  b={bb:>4}  bit={bit}  result={res}  a={base}")
    print()


def demo_crt() -> None:
    print("== Chinese Remainder Theorem ==")
    x, m = crt([(2, 5), (3, 7)])
    print(f"x = {x} mod {m}")
    print(f"cek: {x % 5} == 2, {x % 7} == 3")
    print()


def demo_generator() -> None:
    print("== Order dan Generator ==")
    p = 23
    for g in range(2, 6):
        print(f"order({g}, {p}) = {multiplicative_order(g, p)}")
    print(f"generator untuk p={p}: {find_generator(p)}")
    print()


def benchmark() -> None:
    print("== Benchmark mod_exp vs pow ==")
    random.seed(42)
    a = random.getrandbits(2048)
    b = random.getrandbits(2048)
    n = random.getrandbits(2048) | 1

    t0 = time.perf_counter()
    manual = mod_exp(a, b, n)
    t1 = time.perf_counter()
    builtin = pow(a, b, n)
    t2 = time.perf_counter()

    assert manual == builtin, "hasil berbeda"
    print(f"mod_exp manual : {t1 - t0:.6f} detik")
    print(f"pow() bawaan   : {t2 - t1:.6f} detik")
    print(f"hasil sama     : {manual == builtin}")
    print()


def self_test() -> None:
    assert gcd(48, 18) == 6
    assert mod_inverse(3, 11) == 4
    assert mod_exp(3, 13, 7) == 3
    assert mod_exp(2, 10, 1000) == 24
    assert mod_mul_safe(123456789, 987654321, 10**9 + 7) == (123456789 * 987654321) % (10**9 + 7)
    assert crt([(2, 5), (3, 7)])[0] == 17
    assert euler_phi(9) == 6
    assert multiplicative_order(2, 7) == 3
    print("Semua self test lulus.\n")


if __name__ == "__main__":
    self_test()
    demo_gcd()
    demo_inverse()
    demo_exp()
    demo_crt()
    demo_generator()
    benchmark()

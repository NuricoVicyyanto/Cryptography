"""
password-hashing.py
Implementasi PBKDF2 dan scrypt dari nol, perbandingan dengan hashlib,
serta demonstrasi mengapa hash cepat tidak cocok untuk password.

Jalankan:
    python password-hashing.py

Catatan: scrypt murni Python lambat. Demo memakai parameter kecil.
"""

from __future__ import annotations

import hashlib
import os
import struct
import time

MASK32 = 0xFFFFFFFF


# ---------------------------------------------------------------------------
# HMAC internal
# ---------------------------------------------------------------------------
# Modul ini tidak mengimpor file hmac.py di folder yang sama agar tidak
# bertabrakan dengan modul standar. Implementasi kecil berikut sudah cukup.

def hmac_sha256(key: bytes, message: bytes) -> bytes:
    if len(key) > 64:
        key = hashlib.sha256(key).digest()
    key = key.ljust(64, b"\x00")
    inner = hashlib.sha256(bytes(b ^ 0x36 for b in key) + message).digest()
    return hashlib.sha256(bytes(b ^ 0x5C for b in key) + inner).digest()


# ---------------------------------------------------------------------------
# PBKDF2
# ---------------------------------------------------------------------------

def pbkdf2_hmac_sha256(password: bytes, salt: bytes, iterations: int,
                       dklen: int = 32) -> bytes:
    """
    PBKDF2 sesuai RFC 8018.

    DK = T1 || T2 || ... || Tn
    Ti = F(P, S, c, i)
    F  = U1 xor U2 xor ... xor Uc
    U1 = HMAC(P, S || INT(i))
    Uj = HMAC(P, U(j-1))
    """
    if iterations < 1:
        raise ValueError("iterations minimal 1")
    if dklen < 1:
        raise ValueError("dklen minimal 1")

    h_len = 32
    blocks = (dklen + h_len - 1) // h_len
    out = b""
    for i in range(1, blocks + 1):
        u = hmac_sha256(password, salt + struct.pack(">I", i))
        t = bytearray(u)
        for _ in range(iterations - 1):
            u = hmac_sha256(password, u)
            for j in range(h_len):
                t[j] ^= u[j]
        out += bytes(t)
    return out[:dklen]


# ---------------------------------------------------------------------------
# scrypt
# ---------------------------------------------------------------------------

def rotl32(x: int, n: int) -> int:
    return ((x << n) | (x >> (32 - n))) & MASK32


def salsa20_8(block: bytes) -> bytes:
    """Salsa20/8 core, dipakai sebagai fungsi round di scrypt."""
    x = list(struct.unpack("<16I", block))
    original = x[:]

    for _ in range(4):
        x[4] ^= rotl32((x[0] + x[12]) & MASK32, 7)
        x[8] ^= rotl32((x[4] + x[0]) & MASK32, 9)
        x[12] ^= rotl32((x[8] + x[4]) & MASK32, 13)
        x[0] ^= rotl32((x[12] + x[8]) & MASK32, 18)

        x[9] ^= rotl32((x[5] + x[1]) & MASK32, 7)
        x[13] ^= rotl32((x[9] + x[5]) & MASK32, 9)
        x[1] ^= rotl32((x[13] + x[9]) & MASK32, 13)
        x[5] ^= rotl32((x[1] + x[13]) & MASK32, 18)

        x[14] ^= rotl32((x[10] + x[6]) & MASK32, 7)
        x[2] ^= rotl32((x[14] + x[10]) & MASK32, 9)
        x[6] ^= rotl32((x[2] + x[14]) & MASK32, 13)
        x[10] ^= rotl32((x[6] + x[2]) & MASK32, 18)

        x[3] ^= rotl32((x[15] + x[11]) & MASK32, 7)
        x[7] ^= rotl32((x[3] + x[15]) & MASK32, 9)
        x[11] ^= rotl32((x[7] + x[3]) & MASK32, 13)
        x[15] ^= rotl32((x[11] + x[7]) & MASK32, 18)

        x[1] ^= rotl32((x[0] + x[3]) & MASK32, 7)
        x[2] ^= rotl32((x[1] + x[0]) & MASK32, 9)
        x[3] ^= rotl32((x[2] + x[1]) & MASK32, 13)
        x[0] ^= rotl32((x[3] + x[2]) & MASK32, 18)

        x[6] ^= rotl32((x[5] + x[4]) & MASK32, 7)
        x[7] ^= rotl32((x[6] + x[5]) & MASK32, 9)
        x[4] ^= rotl32((x[7] + x[6]) & MASK32, 13)
        x[5] ^= rotl32((x[4] + x[7]) & MASK32, 18)

        x[11] ^= rotl32((x[10] + x[9]) & MASK32, 7)
        x[8] ^= rotl32((x[11] + x[10]) & MASK32, 9)
        x[9] ^= rotl32((x[8] + x[11]) & MASK32, 13)
        x[10] ^= rotl32((x[9] + x[8]) & MASK32, 18)

        x[12] ^= rotl32((x[15] + x[14]) & MASK32, 7)
        x[13] ^= rotl32((x[12] + x[15]) & MASK32, 9)
        x[14] ^= rotl32((x[13] + x[12]) & MASK32, 13)
        x[15] ^= rotl32((x[14] + x[13]) & MASK32, 18)

    out = [(x[i] + original[i]) & MASK32 for i in range(16)]
    return struct.pack("<16I", *out)


def xor_bytes(a: bytes, b: bytes) -> bytes:
    return bytes(x ^ y for x, y in zip(a, b))


def blockmix(b: bytes, r: int) -> bytes:
    """BlockMix sesuai RFC 7914."""
    x = b[(2 * r - 1) * 64:(2 * r) * 64]
    y = []
    for i in range(2 * r):
        x = salsa20_8(xor_bytes(x, b[i * 64:(i + 1) * 64]))
        y.append(x)
    even = b"".join(y[0::2])
    odd = b"".join(y[1::2])
    return even + odd


def romix(b: bytes, n: int, r: int) -> bytes:
    """ROMix, inti memory-hard dari scrypt."""
    x = b
    v = []
    for _ in range(n):
        v.append(x)
        x = blockmix(x, r)
    for _ in range(n):
        j = int.from_bytes(x[(2 * r - 1) * 64:], "little") % n
        x = blockmix(xor_bytes(x, v[j]), r)
    return x


def scrypt(password: bytes, salt: bytes, n: int = 1024, r: int = 8,
           p: int = 1, dklen: int = 32) -> bytes:
    """
    scrypt sesuai RFC 7914.
    Parameter: N (cost, harus pangkat dua), r (block size), p (paralelisme).
    Penggunaan memori sekitar 128 * r * N byte.
    """
    if n < 2 or (n & (n - 1)) != 0:
        raise ValueError("N harus pangkat dua dan minimal 2")
    if r < 1 or p < 1:
        raise ValueError("r dan p minimal 1")

    b = pbkdf2_hmac_sha256(password, salt, 1, p * 128 * r)
    blocks = [b[i * 128 * r:(i + 1) * 128 * r] for i in range(p)]
    mixed = b"".join(romix(block, n, r) for block in blocks)
    return pbkdf2_hmac_sha256(password, mixed, 1, dklen)


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

def demo_pbkdf2() -> None:
    print("== PBKDF2-HMAC-SHA256 ==")
    password = b"kata-sandi-rahasia"
    salt = b"salt-tetap-untuk-demo"
    dk = pbkdf2_hmac_sha256(password, salt, 100000, 32)
    print(f"100000 iterasi: {dk.hex()}")

    reference = hashlib.pbkdf2_hmac("sha256", password, salt, 100000, 32)
    print(f"cocok dengan hashlib: {dk == reference}")
    assert dk == reference

    # Vektor uji RFC 6070 versi SHA-1 tidak berlaku di sini,
    # jadi gunakan perbandingan hashlib sebagai acuan.
    print()


def demo_scrypt() -> None:
    print("== scrypt ==")
    password = b"kata-sandi-rahasia"
    salt = b"salt-tetap-untuk-demo"
    dk = scrypt(password, salt, n=1024, r=8, p=1, dklen=32)
    print(f"N=1024 r=8 p=1: {dk.hex()}")

    reference = hashlib.scrypt(password, salt=salt, n=1024, r=8, p=1,
                               dklen=32, maxmem=64 * 1024 * 1024)
    print(f"cocok dengan hashlib: {dk == reference}")
    assert dk == reference
    print()


def demo_dictionary_attack() -> None:
    print("== Kenapa hash cepat berbahaya ==")
    target_hash = hashlib.sha256(b"password123").hexdigest()
    candidates = [b"123456", b"password", b"qwerty", b"password123", b"admin"]

    start = time.perf_counter()
    found = None
    for candidate in candidates:
        if hashlib.sha256(candidate).hexdigest() == target_hash:
            found = candidate
            break
    elapsed = time.perf_counter() - start

    print(f"target: {target_hash[:32]}...")
    print(f"ditemukan: {found} dalam {elapsed * 1000:.3f} ms")
    print("Dengan GPU, miliaran kandidat per detik bisa diuji.")
    print()


def demo_salt() -> None:
    print("== Salt mencegah rainbow table ==")
    password = b"password123"
    for salt in (b"user-a", b"user-b"):
        digest = pbkdf2_hmac_sha256(password, salt, 1000, 16)
        print(f"salt {salt!r}: {digest.hex()}")
    print("password sama menghasilkan hash berbeda untuk user berbeda.")
    print()


def demo_timing() -> None:
    print("== Biaya komputasi ==")
    password = b"password"
    salt = os.urandom(16)

    t0 = time.perf_counter()
    hashlib.sha256(password + salt).digest()
    t1 = time.perf_counter()
    print(f"SHA-256 sekali        : {(t1 - t0) * 1e6:.2f} mikrodetik")

    t0 = time.perf_counter()
    hashlib.pbkdf2_hmac("sha256", password, salt, 310000, 32)
    t1 = time.perf_counter()
    print(f"PBKDF2 310000 iterasi : {(t1 - t0) * 1000:.2f} ms")

    t0 = time.perf_counter()
    hashlib.scrypt(password, salt=salt, n=16384, r=8, p=1, dklen=32,
                   maxmem=64 * 1024 * 1024)
    t1 = time.perf_counter()
    print(f"scrypt N=16384 r=8    : {(t1 - t0) * 1000:.2f} ms")
    print("Semakin lambat, semakin mahal serangan brute force.")
    print()


def demo_store_format() -> None:
    print("== Format penyimpanan password ==")
    algorithm = "scrypt"
    n, r, p = 16384, 8, 1
    salt = os.urandom(16)
    dk = scrypt(b"password-baru", salt, n=n, r=r, p=p, dklen=32)
    encoded = f"{algorithm}${n}${r}${p}${salt.hex()}${dk.hex()}"
    print(encoded)
    print("Simpan parameter dan salt bersama hash agar bisa diverifikasi nanti.")
    print("Naikkan parameter seiring waktu tanpa merusak hash lama.")
    print()


if __name__ == "__main__":
    demo_pbkdf2()
    demo_scrypt()
    demo_dictionary_attack()
    demo_salt()
    demo_timing()
    demo_store_format()

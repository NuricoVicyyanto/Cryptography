"""
rsa-from-scratch.py
Implementasi RSA dari nol: pembangkitan prima, key generation, enkripsi,
dekripsi dengan CRT, tanda tangan digital PKCS#1 v1.5, dan demonstrasi
kerentanan RSA tanpa padding.

Peringatan: kode ini untuk belajar. Jangan dipakai untuk melindungi data nyata.
Implementasi produksi harus constant time, memakai OAEP atau PSS, dan sudah
melewati audit keamanan.

Jalankan:
    python rsa-from-scratch.py
"""

from __future__ import annotations

import hashlib
import secrets
import time

# ---------------------------------------------------------------------------
# 1. Utilitas bilangan
# ---------------------------------------------------------------------------

SMALL_PRIMES = [
    2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53,
    59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113,
]


def is_probable_prime(n: int, rounds: int = 40) -> bool:
    """
    Uji Miller-Rabin.
    Untuk bilangan di bawah 2^64, himpunan basis deterministik dipakai
    sehingga hasilnya pasti, bukan probabilistik.
    """
    if n < 2:
        return False
    for p in SMALL_PRIMES:
        if n % p == 0:
            return n == p

    d = n - 1
    r = 0
    while d % 2 == 0:
        d //= 2
        r += 1

    if n < 2**64:
        bases = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
    else:
        bases = [secrets.randbelow(n - 3) + 2 for _ in range(rounds)]

    for a in bases:
        a %= n
        if a < 2:
            continue
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def generate_prime(bits: int, e: int = 65537) -> int:
    """
    Bangkitkan prima acak sepanjang bits bit.
    Pastikan gcd(p - 1, e) = 1 agar e punya invers modulo phi.
    """
    while True:
        candidate = secrets.randbits(bits) | (1 << (bits - 1)) | 1
        if candidate % e == 1:
            continue
        if is_probable_prime(candidate):
            return candidate


def gcd(a: int, b: int) -> int:
    while b:
        a, b = b, a % b
    return a


def egcd(a: int, b: int) -> tuple[int, int, int]:
    old_r, r = a, b
    old_s, s = 1, 0
    old_t, t = 0, 1
    while r:
        q = old_r // r
        old_r, r = r, old_r - q * r
        old_s, s = s, old_s - q * s
        old_t, t = t, old_t - q * t
    return old_r, old_s, old_t


def mod_inverse(a: int, m: int) -> int:
    g, x, _ = egcd(a % m, m)
    if g != 1:
        raise ValueError("invers tidak ada")
    return x % m


# ---------------------------------------------------------------------------
# 2. Key generation
# ---------------------------------------------------------------------------

class RSAPublicKey:
    def __init__(self, n: int, e: int):
        self.n = n
        self.e = e

    def __repr__(self) -> str:
        return f"RSAPublicKey(n_bits={self.n.bit_length()}, e={self.e})"


class RSAPrivateKey:
    def __init__(self, n: int, e: int, d: int, p: int, q: int):
        self.n = n
        self.e = e
        self.d = d
        self.p = p
        self.q = q
        # Parameter CRT untuk mempercepat dekripsi
        self.dp = d % (p - 1)
        self.dq = d % (q - 1)
        self.qinv = mod_inverse(q, p)

    def __repr__(self) -> str:
        return f"RSAPrivateKey(n_bits={self.n.bit_length()}, d_bits={self.d.bit_length()})"


def generate_keypair(bits: int = 1024, e: int = 65537) -> tuple[RSAPublicKey, RSAPrivateKey]:
    """
    Bangkitkan pasangan kunci RSA.
    bits adalah ukuran modulus n, sehingga setiap prima berukuran bits/2.
    """
    if bits < 512:
        raise ValueError("gunakan minimal 512 bit, idealnya 2048 atau lebih")
    half = bits // 2
    while True:
        p = generate_prime(half, e)
        q = generate_prime(half, e)
        if p == q:
            continue
        n = p * q
        if n.bit_length() != bits:
            continue
        phi = (p - 1) * (q - 1)
        if gcd(e, phi) != 1:
            continue
        d = mod_inverse(e, phi)
        return RSAPublicKey(n, e), RSAPrivateKey(n, e, d, p, q)


# ---------------------------------------------------------------------------
# 3. Enkripsi dan dekripsi
# ---------------------------------------------------------------------------

def rsa_encrypt_int(pub: RSAPublicKey, m: int) -> int:
    if not 0 <= m < pub.n:
        raise ValueError("pesan harus lebih kecil dari modulus")
    return pow(m, pub.e, pub.n)


def rsa_decrypt_int(priv: RSAPrivateKey, c: int) -> int:
    return pow(c, priv.d, priv.n)


def rsa_decrypt_crt(priv: RSAPrivateKey, c: int) -> int:
    """
    Dekripsi dengan Chinese Remainder Theorem.
    Dua eksponensial kecil menggantikan satu eksponensial besar,
    sehingga sekitar 4 kali lebih cepat.
    """
    m1 = pow(c, priv.dp, priv.p)
    m2 = pow(c, priv.dq, priv.q)
    h = (priv.qinv * (m1 - m2)) % priv.p
    return m2 + h * priv.q


# ---------------------------------------------------------------------------
# 4. Padding PKCS#1 v1.5 untuk enkripsi
# ---------------------------------------------------------------------------

def pkcs1v15_encrypt(pub: RSAPublicKey, message: bytes) -> bytes:
    """
    Format blok: 00 02 PS 00 M
    PS adalah byte acak bukan nol sepanjang k - len(M) - 3.
    """
    k = (pub.n.bit_length() + 7) // 8
    if len(message) > k - 11:
        raise ValueError("pesan terlalu panjang untuk modulus ini")

    ps_len = k - len(message) - 3
    ps = bytearray()
    while len(ps) < ps_len:
        b = secrets.token_bytes(1)[0]
        if b != 0:
            ps.append(b)
    block = b"\x00\x02" + bytes(ps) + b"\x00" + message
    m = int.from_bytes(block, "big")
    c = rsa_encrypt_int(pub, m)
    return c.to_bytes(k, "big")


def pkcs1v15_decrypt(priv: RSAPrivateKey, ciphertext: bytes, use_crt: bool = True) -> bytes:
    k = (priv.n.bit_length() + 7) // 8
    if len(ciphertext) != k:
        raise ValueError("panjang ciphertext tidak sesuai modulus")
    c = int.from_bytes(ciphertext, "big")
    m = rsa_decrypt_crt(priv, c) if use_crt else rsa_decrypt_int(priv, c)
    block = m.to_bytes(k, "big")
    if block[0] != 0 or block[1] != 2:
        raise ValueError("format blok tidak valid")
    sep = block.find(b"\x00", 2)
    if sep < 10:
        raise ValueError("separator tidak ditemukan atau PS terlalu pendek")
    return block[sep + 1:]


# ---------------------------------------------------------------------------
# 5. Tanda tangan PKCS#1 v1.5
# ---------------------------------------------------------------------------

# DigestInfo untuk SHA-256 menurut RFC 8017, tanpa byte pesan hash.
SHA256_DIGEST_INFO_PREFIX = bytes.fromhex("3031300d060960864801650304020105000420")


def rsa_sign(priv: RSAPrivateKey, message: bytes) -> bytes:
    """
    Tanda tangan PKCS#1 v1.5 dengan SHA-256.
    Format: 00 01 FF..FF 00 DigestInfo(hash)
    """
    k = (priv.n.bit_length() + 7) // 8
    digest = hashlib.sha256(message).digest()
    t = SHA256_DIGEST_INFO_PREFIX + digest
    if len(t) > k - 11:
        raise ValueError("modulus terlalu kecil")
    padding = b"\xff" * (k - len(t) - 3)
    block = b"\x00\x01" + padding + b"\x00" + t
    m = int.from_bytes(block, "big")
    s = pow(m, priv.d, priv.n)
    return s.to_bytes(k, "big")


def rsa_verify(pub: RSAPublicKey, message: bytes, signature: bytes) -> bool:
    k = (pub.n.bit_length() + 7) // 8
    if len(signature) != k:
        return False
    s = int.from_bytes(signature, "big")
    if s >= pub.n:
        return False
    m = pow(s, pub.e, pub.n)
    block = m.to_bytes(k, "big")
    digest = hashlib.sha256(message).digest()
    expected = b"\x00\x01" + b"\xff" * (k - len(digest) - len(SHA256_DIGEST_INFO_PREFIX) - 3) \
        + b"\x00" + SHA256_DIGEST_INFO_PREFIX + digest
    # Perbandingan constant time sederhana
    return secrets.compare_digest(block, expected)


# ---------------------------------------------------------------------------
# 6. Demonstrasi kelemahan textbook RSA
# ---------------------------------------------------------------------------

def demo_deterministic(priv: RSAPrivateKey, pub: RSAPublicKey) -> None:
    print("== Textbook RSA bersifat deterministik ==")
    m = int.from_bytes(b"RAHASIA", "big")
    c1 = rsa_encrypt_int(pub, m)
    c2 = rsa_encrypt_int(pub, m)
    print(f"dua enkripsi pesan sama identik: {c1 == c2}")
    print(f"dekripsi: {rsa_decrypt_crt(priv, c1).to_bytes(7, 'big')}")
    print()


def demo_homomorphic(priv: RSAPrivateKey, pub: RSAPublicKey) -> None:
    print("== Textbook RSA bersifat multiplikatif ==")
    m1, m2 = 7, 11
    c1 = rsa_encrypt_int(pub, m1)
    c2 = rsa_encrypt_int(pub, m2)
    c_prod = (c1 * c2) % pub.n
    m_prod = rsa_decrypt_crt(priv, c_prod)
    print(f"E(7) * E(11) didekripsi menjadi {m_prod}, seharusnya 77")
    print("Penyerang bisa mengubah ciphertext tanpa tahu kunci.")
    print()


def demo_small_exponent() -> None:
    print("== Serangan eksponen kecil tanpa padding ==")
    e = 3
    pub = RSAPublicKey(n=10**30 + 57, e=e)
    m = 12345
    c = rsa_encrypt_int(pub, m)
    # Jika m^e < n, akar pangkat e atas ciphertext memberi pesan langsung.
    lo, hi = 0, c
    while lo < hi:
        mid = (lo + hi) // 2
        if mid ** e < c:
            lo = mid + 1
        else:
            hi = mid
    print(f"m = {m}, c = {c}, akar kubik = {lo}, cocok: {lo == m}")
    print("Padding acak mencegah serangan ini karena m^e selalu lebih besar dari n.")
    print()


# ---------------------------------------------------------------------------
# Demo utama
# ---------------------------------------------------------------------------

def main() -> None:
    print("== Pembangkitan kunci ==")
    t0 = time.perf_counter()
    pub, priv = generate_keypair(1024)
    t1 = time.perf_counter()
    print(pub)
    print(priv)
    print(f"waktu pembangkitan: {t1 - t0:.2f} detik")
    print()

    print("== Enkripsi dengan PKCS#1 v1.5 ==")
    message = b"Rahasia negara: serang fajar."
    ct = pkcs1v15_encrypt(pub, message)
    print("ciphertext:", ct.hex()[:64], "...")
    print("dekripsi  :", pkcs1v15_decrypt(priv, ct).decode())
    assert pkcs1v15_decrypt(priv, ct) == message
    print()

    print("== Dekripsi CRT vs dekripsi langsung ==")
    c = int.from_bytes(ct, "big")
    t0 = time.perf_counter()
    for _ in range(20):
        rsa_decrypt_int(priv, c)
    t1 = time.perf_counter()
    for _ in range(20):
        rsa_decrypt_crt(priv, c)
    t2 = time.perf_counter()
    print(f"langsung: {(t1 - t0) / 20 * 1000:.2f} ms")
    print(f"CRT     : {(t2 - t1) / 20 * 1000:.2f} ms")
    print(f"rasio percepatan: {(t1 - t0) / (t2 - t1):.2f}x")
    print()

    print("== Tanda tangan digital ==")
    sig = rsa_sign(priv, message)
    print("signature:", sig.hex()[:64], "...")
    print("verifikasi pesan asli :", rsa_verify(pub, message, sig))
    print("verifikasi pesan salah:", rsa_verify(pub, b"pesan lain", sig))
    print()

    # Uncomment bila ingin menjalankan demonstrasi kelemahan.
    # demo_deterministic(priv, pub)
    # demo_homomorphic(priv, pub)
    demo_small_exponent()


if __name__ == "__main__":
    main()

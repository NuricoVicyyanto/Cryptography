"""
dsa-digital-signature.py
Implementasi DSA (Digital Signature Algorithm) dari nol, plus demonstrasi
serangan nonce reuse yang pernah menghancurkan kunci privat Sony PlayStation 3.

Parameter di bawah dibangkitkan khusus untuk pembelajaran: p 1024 bit,
q 160 bit. Untuk produksi gunakan minimal p 2048 bit dan library teruji.

Jalankan:
    python dsa-digital-signature.py
"""

from __future__ import annotations

import hashlib
import secrets

# ---------------------------------------------------------------------------
# Parameter domain (p, q, g)
# ---------------------------------------------------------------------------
# q adalah prima 160 bit, p = k*q + 1 adalah prima 1024 bit,
# dan g = h^((p-1)/q) mod p memiliki order q.

P = int(
    "891c4ebcd8cd8ea62583403990751554d6abdd32dab40402a4eab3e3e05c395b"
    "f13831075625f6fef40fe65572045bbd33eb9bb8a8c38013e58b51ebd27489fa"
    "eecddcb07dc5a56111d03e41b6c1e48d1c72d5f227edf7191d7e965aca29b4e1"
    "83b02ccd98e7a2d7767013f22c3a762d39b2c50d3eeefdf6faede14a140bf9eb",
    16,
)
Q = int("c96891240a2b1616c78185fda9f9ea84bfb5667b", 16)


def _find_generator() -> int:
    """Cari generator subgrup berorder q dari p dan q yang sudah ada."""
    for h in range(2, 1000):
        candidate = pow(h, (P - 1) // Q, P)
        if candidate != 1:
            return candidate
    raise RuntimeError("generator tidak ditemukan")


G = _find_generator()


def hash_to_int(message: bytes) -> int:
    """Hash pesan dengan SHA-256 lalu potong menjadi q bit sesuai DSA."""
    digest = hashlib.sha256(message).digest()
    value = int.from_bytes(digest, "big")
    # DSA memakai z, yaitu n bit kiri dari hash, dengan n = bit_length(q).
    excess = len(digest) * 8 - Q.bit_length()
    if excess > 0:
        value >>= excess
    return value


def mod_inverse(a: int, m: int) -> int:
    return pow(a, -1, m)


# ---------------------------------------------------------------------------
# Key generation, tanda tangan, verifikasi
# ---------------------------------------------------------------------------

def generate_keypair() -> tuple[int, int]:
    """Kembalikan (private x, public y)."""
    x = secrets.randbelow(Q - 2) + 1
    y = pow(G, x, P)
    return x, y


def sign(message: bytes, private: int, k: int | None = None) -> tuple[int, int]:
    """
    Tanda tangan DSA. k adalah nonce rahasia per pesan.
    Jika k tidak diberikan, dibangkitkan acak dengan CSPRNG.
    """
    z = hash_to_int(message)
    for _ in range(100):
        nonce = k if k is not None else secrets.randbelow(Q - 2) + 1
        r = pow(G, nonce, P) % Q
        if r == 0:
            if k is not None:
                raise ValueError("k menghasilkan r = 0, pilih k lain")
            continue
        s = (mod_inverse(nonce, Q) * (z + private * r)) % Q
        if s == 0:
            if k is not None:
                raise ValueError("k menghasilkan s = 0, pilih k lain")
            continue
        return r, s
    raise RuntimeError("gagal menghasilkan tanda tangan")


def verify(message: bytes, signature: tuple[int, int], public: int) -> bool:
    r, s = signature
    if not (0 < r < Q and 0 < s < Q):
        return False
    z = hash_to_int(message)
    w = mod_inverse(s, Q)
    u1 = (z * w) % Q
    u2 = (r * w) % Q
    v = ((pow(G, u1, P) * pow(public, u2, P)) % P) % Q
    return v == r


# ---------------------------------------------------------------------------
# Demonstrasi serangan
# ---------------------------------------------------------------------------

def recover_private_key(m1: bytes, sig1: tuple[int, int],
                        m2: bytes, sig2: tuple[int, int]) -> int:
    """
    Jika dua pesan ditandatangani dengan k yang sama, k bisa dihitung:
        k = (z1 - z2) * (s1 - s2)^(-1) mod q
    lalu kunci privat:
        x = (s1 * k - z1) * r1^(-1) mod q
    """
    z1 = hash_to_int(m1)
    z2 = hash_to_int(m2)
    r1, s1 = sig1
    _, s2 = sig2

    k = ((z1 - z2) * mod_inverse(s1 - s2, Q)) % Q
    x = ((s1 * k - z1) * mod_inverse(r1, Q)) % Q
    return x


def demo_attack() -> None:
    print("== Serangan nonce reuse ==")
    private, public = generate_keypair()
    reused_k = secrets.randbelow(Q - 2) + 1

    m1 = b"kirim 100 ke alice"
    m2 = b"kirim 900 ke mallory"
    sig1 = sign(m1, private, k=reused_k)
    sig2 = sign(m2, private, k=reused_k)

    print(f"kunci publik y = {hex(public)[:40]}...")
    print("dua tanda tangan memakai k yang sama (simulasi bug RNG)")
    recovered = recover_private_key(m1, sig1, m2, sig2)
    print(f"kunci privat asli      = {hex(private)}")
    print(f"kunci privat dipulihkan= {hex(recovered)}")
    print(f"pemulihan berhasil: {recovered == private}")
    print()


def demo_small_subgroup() -> None:
    """
    Nonce k yang kecil bisa ditemukan dengan kangaroo atau brute force.
    Di sini kita hanya mengilustrasikan bahwa k = 1 membuat r = g mod p.
    """
    print("== Bahaya nonce kecil ==")
    private, _ = generate_keypair()
    sig = sign(b"pesan", private, k=1)
    print(f"jika k = 1, maka r = (g mod p) mod q = {sig[0] == G % Q}")
    print("penyerang langsung tahu k tanpa perlu memecahkan apa pun")
    print()


# ---------------------------------------------------------------------------
# Demo utama
# ---------------------------------------------------------------------------

def main() -> None:
    print("== Parameter domain ==")
    print(f"p bits = {P.bit_length()}")
    print(f"q bits = {Q.bit_length()}")
    print(f"g berorder q: {pow(G, Q, P) == 1}")
    print()

    print("== Key generation ==")
    private, public = generate_keypair()
    print(f"private x = {hex(private)}")
    print(f"public  y = {hex(public)[:40]}...")
    print()

    print("== Tanda tangan dan verifikasi ==")
    message = b"Saya menyetujui transfer ini."
    signature = sign(message, private)
    print(f"r = {signature[0]}")
    print(f"s = {signature[1]}")
    print(f"verifikasi pesan asli : {verify(message, signature, public)}")
    print(f"verifikasi pesan ubah : {verify(b'Saya menolak transfer ini.', signature, public)}")
    print(f"verifikasi tanda tangan palsu: {verify(message, (signature[0], signature[1] + 1), public)}")
    print()

    demo_attack()
    demo_small_subgroup()


def self_test() -> None:
    x, y = generate_keypair()
    m = b"uji"
    sig = sign(m, x)
    assert verify(m, sig, y)
    assert not verify(b"lain", sig, y)
    assert pow(G, Q, P) == 1
    print("Self test lulus.\n")


if __name__ == "__main__":
    self_test()
    main()

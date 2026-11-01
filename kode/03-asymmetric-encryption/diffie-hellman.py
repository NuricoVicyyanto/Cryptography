"""
diffie-hellman.py
Simulasi Diffie-Hellman key exchange plus demonstrasi man in the middle.

Dua pihak menyepakati kunci rahasia bersama tanpa pernah mengirim kunci itu.
Keamanannya bergantung pada kesulitan Discrete Logarithm Problem.

Jalankan:
    python diffie-hellman.py
"""

from __future__ import annotations

import hashlib
import secrets

# ---------------------------------------------------------------------------
# Parameter grup
# ---------------------------------------------------------------------------
# p adalah safe prime 256 bit, q = (p - 1) / 2 juga prima.
# g = 2 memiliki order q, jadi grup yang dipakai adalah subgrup berorder q.
# Ini praktik yang benar: memakai generator subgrup prima, bukan seluruh Zp*,
# agar terhindar dari serangan small subgroup.

P = 0xfc9182b76f58343cc016ff26caeb6bc61868818cb1560dd2b0f31808af8538ff
Q = 0x7e48c15bb7ac1a1e600b7f936575b5e30c3440c658ab06e958798c0457c29c7f
G = 2

# Untuk demonstrasi angka kecil di kelas.
SMALL_P = 23
SMALL_G = 5


# ---------------------------------------------------------------------------
# API dasar
# ---------------------------------------------------------------------------

def generate_private_key(q: int = Q) -> int:
    """Kunci privat acak di rentang 2 sampai q-1."""
    return secrets.randbelow(q - 3) + 2


def public_key(private: int, p: int = P, g: int = G) -> int:
    """A = g^a mod p."""
    return pow(g, private, p)


def shared_secret(private: int, peer_public: int, p: int = P) -> int:
    """S = B^a mod p, nilainya sama dengan A^b mod p."""
    if not 1 < peer_public < p - 1:
        raise ValueError("kunci publik peer tidak valid")
    return pow(peer_public, private, p)


def derive_key(secret: int, length: int = 32, context: bytes = b"dh-demo") -> bytes:
    """
    Ubah shared secret menjadi kunci simetris dengan HKDF sederhana.
    Jangan memakai shared secret langsung sebagai kunci AES.
    """
    material = secret.to_bytes((secret.bit_length() + 7) // 8 or 1, "big")
    prk = hashlib.sha256(context + b"\x00" + material).digest()
    out = hashlib.sha256(prk + b"\x01" + context).digest()
    return out[:length]


class Party:
    """Satu pihak dalam pertukaran kunci."""

    def __init__(self, name: str, p: int = P, g: int = G):
        self.name = name
        self.p = p
        self.g = g
        self.private = generate_private_key()
        self.public = public_key(self.private, p, g)
        self.session_key: bytes | None = None

    def compute(self, peer_public: int) -> bytes:
        secret = shared_secret(self.private, peer_public, self.p)
        self.session_key = derive_key(secret)
        return self.session_key


# ---------------------------------------------------------------------------
# Demonstrasi
# ---------------------------------------------------------------------------

def demo_small() -> None:
    print("== Contoh angka kecil ==")
    a, b = 6, 15
    A = pow(SMALL_G, a, SMALL_P)
    B = pow(SMALL_G, b, SMALL_P)
    s1 = pow(B, a, SMALL_P)
    s2 = pow(A, b, SMALL_P)
    print(f"p={SMALL_P}, g={SMALL_G}")
    print(f"Alice private a={a}, public A={A}")
    print(f"Bob   private b={b}, public B={B}")
    print(f"Alice hitung B^a = {s1}")
    print(f"Bob   hitung A^b = {s2}")
    print(f"sepakat: {s1 == s2}")
    print()


def demo_real() -> None:
    print("== Pertukaran kunci 256 bit ==")
    alice = Party("Alice")
    bob = Party("Bob")

    print(f"p bits = {P.bit_length()}, q bits = {Q.bit_length()}")
    print(f"Alice publik = {hex(alice.public)[:34]}...")
    print(f"Bob   publik = {hex(bob.public)[:34]}...")

    ka = alice.compute(bob.public)
    kb = bob.compute(alice.public)
    print(f"session key Alice = {ka.hex()}")
    print(f"session key Bob   = {kb.hex()}")
    print(f"kunci sama: {ka == kb}")
    print()


def demo_mitm() -> None:
    print("== Man in the Middle ==")
    alice = Party("Alice")
    bob = Party("Bob")
    mallory_a = Party("Mallory untuk Alice")
    mallory_b = Party("Mallory untuk Bob")

    # Mallory bertukar kunci terpisah dengan masing-masing pihak.
    key_alice = alice.compute(mallory_a.public)
    key_mallory_a = mallory_a.compute(alice.public)
    key_bob = bob.compute(mallory_b.public)
    key_mallory_b = mallory_b.compute(bob.public)

    print(f"Alice dan Mallory berbagi kunci yang sama: {key_alice == key_mallory_a}")
    print(f"Bob   dan Mallory berbagi kunci yang sama: {key_bob == key_mallory_b}")
    print(f"Alice dan Bob mengira berbagi kunci, padahal: {key_alice != key_bob}")
    print("Kesimpulan: DH tanpa autentikasi rentan MITM.")
    print()


def demo_subgroup_check() -> None:
    print("== Pemeriksaan subgrup ==")
    print(f"g^q mod p = {pow(G, Q, P)} (harus 1)")
    print(f"g^2 mod p = {pow(G, 2, P)} (tidak boleh 1)")
    print("Pemeriksaan ini mencegah small subgroup attack.")
    print()


def demo_forward_secrecy() -> None:
    print("== Forward secrecy ==")
    alice = Party("Alice")
    bob = Party("Bob")
    k1 = alice.compute(bob.public)
    _ = bob.compute(alice.public)

    alice2 = Party("Alice baru")
    bob2 = Party("Bob baru")
    k2 = alice2.compute(bob2.public)
    _ = bob2.compute(alice2.public)

    print(f"sesi pertama berbeda dari sesi kedua: {k1 != k2}")
    print("Jika kunci jangka panjang bocor, kunci sesi lama tetap aman.")
    print()


def self_test() -> None:
    a = Party("a")
    b = Party("b")
    assert a.compute(b.public) == b.compute(a.public)
    assert pow(G, Q, P) == 1
    assert pow(G, 2, P) != 1
    print("Self test lulus.\n")


if __name__ == "__main__":
    self_test()
    demo_small()
    demo_real()
    demo_mitm()
    demo_subgroup_check()
    demo_forward_secrecy()

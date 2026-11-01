"""
elgamal.py
Implementasi ElGamal dari nol: enkripsi, dekripsi, tanda tangan, verifikasi,
serta demonstrasi sifat multiplikatif yang membuatnya malleable.

ElGamal adalah skema kunci publik berbasis Discrete Logarithm yang menjadi
dasar banyak sistem lain, termasuk DSA dan varian ECC.

Jalankan:
    python elgamal.py
"""

from __future__ import annotations

import hashlib
import secrets

# Parameter grup yang sama dengan diffie-hellman.py:
# p safe prime 256 bit, q = (p-1)/2 prima, g berorder q.
P = 0xfc9182b76f58343cc016ff26caeb6bc61868818cb1560dd2b0f31808af8538ff
Q = 0x7e48c15bb7ac1a1e600b7f936575b5e30c3440c658ab06e958798c0457c29c7f
G = 2


# ---------------------------------------------------------------------------
# Utilitas
# ---------------------------------------------------------------------------

def mod_inverse(a: int, m: int) -> int:
    return pow(a, -1, m)


def gcd(a: int, b: int) -> int:
    while b:
        a, b = b, a % b
    return a


def generate_keypair() -> tuple[int, int]:
    """Kembalikan (private x, public y = g^x mod p)."""
    x = secrets.randbelow(Q - 2) + 1
    y = pow(G, x, P)
    return x, y


# ---------------------------------------------------------------------------
# Enkripsi dan dekripsi
# ---------------------------------------------------------------------------

def encrypt(public: int, message: int, k: int | None = None) -> tuple[int, int]:
    """
    Enkripsi ElGamal. Setiap pesan membutuhkan k acak baru.
        c1 = g^k mod p
        c2 = m * y^k mod p
    """
    if not 0 < message < P:
        raise ValueError("pesan harus berada di rentang 1 sampai p-1")
    nonce = k if k is not None else secrets.randbelow(Q - 2) + 1
    c1 = pow(G, nonce, P)
    shared = pow(public, nonce, P)
    c2 = (message * shared) % P
    return c1, c2


def decrypt(private: int, ciphertext: tuple[int, int]) -> int:
    c1, c2 = ciphertext
    shared = pow(c1, private, P)
    return (c2 * mod_inverse(shared, P)) % P


def encrypt_bytes(public: int, data: bytes) -> tuple[int, int, bytes]:
    """
    Enkripsi hybrid: kunci sesi acak dienkripsi dengan ElGamal,
    data di-XOR dengan keystream turunan kunci sesi.
    Ini pola yang dipakai di dunia nyata karena ElGamal hanya bisa
    mengenkripsi satu bilangan lebih kecil dari p.
    """
    session = secrets.randbelow(Q - 2) + 1
    c1, c2 = encrypt(public, session)
    material = hashlib.sha256(session.to_bytes(32, "big")).digest()
    keystream = _expand(material, len(data))
    return c1, c2, bytes(a ^ b for a, b in zip(data, keystream))


def decrypt_bytes(private: int, c1: int, c2: int, ciphertext: bytes) -> bytes:
    session = (c2 * mod_inverse(pow(c1, private, P), P)) % P
    material = hashlib.sha256(session.to_bytes(32, "big")).digest()
    keystream = _expand(material, len(ciphertext))
    return bytes(a ^ b for a, b in zip(ciphertext, keystream))


def _expand(seed: bytes, length: int) -> bytes:
    out = bytearray()
    counter = 0
    while len(out) < length:
        out.extend(hashlib.sha256(seed + counter.to_bytes(4, "big")).digest())
        counter += 1
    return bytes(out[:length])


# ---------------------------------------------------------------------------
# Tanda tangan ElGamal
# ---------------------------------------------------------------------------

def hash_message(message: bytes) -> int:
    return int.from_bytes(hashlib.sha256(message).digest(), "big")


def sign(message: bytes, private: int, k: int | None = None) -> tuple[int, int]:
    """
    Tanda tangan ElGamal.
        r = g^k mod p
        s = (H(m) - x*r) * k^(-1) mod (p-1)
    k harus koprima dengan p-1.
    """
    h = hash_message(message)
    for _ in range(100):
        nonce = k if k is not None else secrets.randbelow(P - 3) + 2
        if gcd(nonce, P - 1) != 1:
            if k is not None:
                raise ValueError("k harus koprima dengan p-1")
            continue
        r = pow(G, nonce, P)
        s = ((h - private * r) * mod_inverse(nonce, P - 1)) % (P - 1)
        if s == 0:
            if k is not None:
                raise ValueError("k menghasilkan s = 0")
            continue
        return r, s
    raise RuntimeError("gagal menandatangani")


def verify(message: bytes, signature: tuple[int, int], public: int) -> bool:
    """
    Verifikasi: y^r * r^s mod p == g^H(m) mod p.
    """
    r, s = signature
    if not (0 < r < P):
        return False
    h = hash_message(message)
    left = (pow(public, r, P) * pow(r, s, P)) % P
    right = pow(G, h, P)
    return left == right


# ---------------------------------------------------------------------------
# Demonstrasi
# ---------------------------------------------------------------------------

def demo_encrypt() -> None:
    print("== Enkripsi dan dekripsi ==")
    private, public = generate_keypair()
    message = int.from_bytes(b"RAHASIA", "big")
    ct = encrypt(public, message)
    print(f"private x = {hex(private)[:32]}...")
    print(f"public  y = {hex(public)[:32]}...")
    print(f"c1 = {hex(ct[0])[:32]}...")
    print(f"c2 = {hex(ct[1])[:32]}...")
    print(f"dekripsi = {decrypt(private, ct).to_bytes(7, 'big')}")
    print()


def demo_probabilistic() -> None:
    print("== Enkripsi probabilistik ==")
    _, public = generate_keypair()
    m = 123456789
    c_a = encrypt(public, m)
    c_b = encrypt(public, m)
    print(f"dua enkripsi pesan sama berbeda: {c_a != c_b}")
    print("karena setiap enkripsi memakai k acak baru")
    print()


def demo_malleability() -> None:
    print("== Sifat multiplikatif (malleability) ==")
    private, public = generate_keypair()
    m = 7
    c1, c2 = encrypt(public, m)
    factor = 5
    tampered = (c1, (c2 * factor) % P)
    result = decrypt(private, tampered)
    print(f"dekripsi ciphertext yang diubah = {result}")
    print(f"hasilnya m * {factor} = {m * factor}")
    print("Penyerang mengubah plaintext tanpa tahu kunci.")
    print()


def demo_same_nonce() -> None:
    print("== Bahaya memakai k yang sama dua kali ==")
    _, public = generate_keypair()
    k = secrets.randbelow(Q - 2) + 1
    c1a, c2a = encrypt(public, 11, k=k)
    c1b, c2b = encrypt(public, 22, k=k)
    ratio = (c2b * mod_inverse(c2a, P)) % P
    print(f"c1 sama: {c1a == c1b}")
    print(f"rasio c2 = {ratio}, seharusnya 2 (22/11)")
    print("jika plaintext salah satunya diketahui, yang lain langsung terbuka")
    print()


def demo_hybrid() -> None:
    print("== Enkripsi hybrid untuk data panjang ==")
    private, public = generate_keypair()
    data = b"Pesan ini jauh lebih panjang dari modulus dan tetap aman."
    c1, c2, ct = encrypt_bytes(public, data)
    back = decrypt_bytes(private, c1, c2, ct)
    print(f"panjang data = {len(data)} byte")
    print(f"kembali      = {back.decode()}")
    print(f"utuh         = {back == data}")
    print()


def demo_signature() -> None:
    print("== Tanda tangan ElGamal ==")
    private, public = generate_keypair()
    message = b"Dokumen ini sah."
    sig = sign(message, private)
    print(f"verifikasi pesan asli : {verify(message, sig, public)}")
    print(f"verifikasi pesan ubah : {verify(b'Dokumen ini palsu.', sig, public)}")
    print()


if __name__ == "__main__":
    demo_encrypt()
    demo_probabilistic()
    demo_malleability()
    demo_same_nonce()
    demo_hybrid()
    demo_signature()

"""
elliptic-curve.py
Implementasi kurva eliptik dari nol: penjumlahan titik, perkalian skalar,
ECDH, dan ECDSA pada secp256k1.

Kurva yang dipakai dalam bentuk short Weierstrass:
    y^2 = x^3 + a*x + b  (mod p)

Jalankan:
    python elliptic-curve.py
"""

from __future__ import annotations

import hashlib
import secrets

# ---------------------------------------------------------------------------
# Tipe dasar
# ---------------------------------------------------------------------------
# Titik direpresentasikan sebagai tuple (x, y), dan None berarti titik infinity.

Point = tuple[int, int] | None


class Curve:
    """Kurva eliptik y^2 = x^3 + a*x + b mod p."""

    def __init__(self, p: int, a: int, b: int):
        self.p = p
        self.a = a % p
        self.b = b % p
        # Diskriminan tidak boleh nol, jika nol kurva menjadi singular.
        if (4 * pow(self.a, 3, p) + 27 * pow(self.b, 2, p)) % p == 0:
            raise ValueError("kurva singular")

    # -- operasi dasar ------------------------------------------------------

    def is_on_curve(self, point: Point) -> bool:
        if point is None:
            return True
        x, y = point
        return (y * y - (x * x * x + self.a * x + self.b)) % self.p == 0

    def add(self, P: Point, Q: Point) -> Point:
        """Penjumlahan dua titik sesuai aturan grup."""
        if P is None:
            return Q
        if Q is None:
            return P

        x1, y1 = P
        x2, y2 = Q
        p = self.p

        if x1 == x2 and (y1 + y2) % p == 0:
            # P dan Q saling invers, hasilnya titik infinity.
            return None

        if P == Q:
            # Tangen: lambda = (3x^2 + a) / (2y)
            numerator = (3 * x1 * x1 + self.a) % p
            denominator = (2 * y1) % p
        else:
            numerator = (y2 - y1) % p
            denominator = (x2 - x1) % p

        lam = numerator * pow(denominator, -1, p) % p
        x3 = (lam * lam - x1 - x2) % p
        y3 = (lam * (x1 - x3) - y1) % p
        return (x3, y3)

    def double(self, P: Point) -> Point:
        return self.add(P, P)

    def negate(self, P: Point) -> Point:
        if P is None:
            return None
        return (P[0], (-P[1]) % self.p)

    def sub(self, P: Point, Q: Point) -> Point:
        return self.add(P, self.negate(Q))

    def mul(self, k: int, P: Point) -> Point:
        """Perkalian skalar dengan metode double and add."""
        if k < 0:
            return self.mul(-k, self.negate(P))
        result: Point = None
        addend = P
        while k:
            if k & 1:
                result = self.add(result, addend)
            addend = self.add(addend, addend)
            k >>= 1
        return result

    def order_of(self, P: Point, limit: int = 10**6) -> int:
        """Cari order titik dengan brute force, hanya untuk kurva kecil."""
        if P is None:
            return 1
        current: Point = P
        k = 1
        while current is not None:
            current = self.add(current, P)
            k += 1
            if k > limit:
                raise RuntimeError("order melebihi limit")
        return k

    def all_points(self) -> list[Point]:
        """Enumerasi semua titik, hanya untuk p kecil."""
        points: list[Point] = []
        for x in range(self.p):
            rhs = (x * x * x + self.a * x + self.b) % self.p
            for y in range(self.p):
                if y * y % self.p == rhs:
                    points.append((x, y))
        return points


# ---------------------------------------------------------------------------
# Kurva kecil untuk pembelajaran
# ---------------------------------------------------------------------------

SMALL = Curve(p=17, a=2, b=2)
SMALL_G = (5, 1)


# ---------------------------------------------------------------------------
# secp256k1
# ---------------------------------------------------------------------------

SECP256K1 = Curve(
    p=0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F,
    a=0,
    b=7,
)

SECP256K1_G = (
    0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,
    0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8,
)

SECP256K1_N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141


# ---------------------------------------------------------------------------
# ECDH
# ---------------------------------------------------------------------------

def ecdh_keypair(curve: Curve = SECP256K1, g: Point = SECP256K1_G,
                 n: int = SECP256K1_N) -> tuple[int, Point]:
    private = secrets.randbelow(n - 1) + 1
    return private, curve.mul(private, g)


def ecdh_shared(curve: Curve, private: int, peer_public: Point) -> Point:
    if peer_public is None or not curve.is_on_curve(peer_public):
        raise ValueError("kunci publik peer tidak valid")
    return curve.mul(private, peer_public)


# ---------------------------------------------------------------------------
# ECDSA
# ---------------------------------------------------------------------------

def hash_to_int(message: bytes, n: int) -> int:
    digest = hashlib.sha256(message).digest()
    value = int.from_bytes(digest, "big")
    excess = len(digest) * 8 - n.bit_length()
    if excess > 0:
        value >>= excess
    return value


def ecdsa_sign(curve: Curve, g: Point, n: int, private: int,
               message: bytes) -> tuple[int, int]:
    z = hash_to_int(message, n)
    while True:
        k = secrets.randbelow(n - 1) + 1
        point = curve.mul(k, g)
        if point is None:
            continue
        r = point[0] % n
        if r == 0:
            continue
        s = (pow(k, -1, n) * (z + r * private)) % n
        if s != 0:
            return r, s


def ecdsa_verify(curve: Curve, g: Point, n: int, public: Point,
                 message: bytes, signature: tuple[int, int]) -> bool:
    r, s = signature
    if not (0 < r < n and 0 < s < n):
        return False
    if public is None:
        return False
    z = hash_to_int(message, n)
    w = pow(s, -1, n)
    u1 = (z * w) % n
    u2 = (r * w) % n
    point = curve.add(curve.mul(u1, g), curve.mul(u2, public))
    if point is None:
        return False
    return point[0] % n == r


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

def demo_small_curve() -> None:
    print("== Kurva kecil: y^2 = x^3 + 2x + 2 mod 17 ==")
    points = SMALL.all_points()
    print(f"jumlah titik afinitas: {len(points)} (termasuk titik infinity: {len(points) + 1})")
    print("contoh titik:", points[:6])
    print(f"G = {SMALL_G} pada kurva: {SMALL.is_on_curve(SMALL_G)}")
    print(f"order G = {SMALL.order_of(SMALL_G)}")
    print(f"2G = {SMALL.double(SMALL_G)}")
    print(f"3G = {SMALL.mul(3, SMALL_G)}")
    print(f"19G = {SMALL.mul(19, SMALL_G)} (titik infinity)")
    print()


def demo_group_law() -> None:
    print("== Hukum grup ==")
    P = SMALL_G
    Q = SMALL.mul(7, P)
    print(f"P = {P}")
    print(f"Q = 7P = {Q}")
    print(f"P + Q = {SMALL.add(P, Q)}")
    print(f"Q + P = {SMALL.add(Q, P)}")
    print(f"komutatif: {SMALL.add(P, Q) == SMALL.add(Q, P)}")
    print(f"P + (-P) = {SMALL.add(P, SMALL.negate(P))}")
    print()


def demo_ecdh() -> None:
    print("== ECDH pada secp256k1 ==")
    a, A = ecdh_keypair()
    b, B = ecdh_keypair()
    s1 = ecdh_shared(SECP256K1, a, B)
    s2 = ecdh_shared(SECP256K1, b, A)
    print(f"kurva valid: {SECP256K1.is_on_curve(SECP256K1_G)}")
    print(f"n * G = infinity: {SECP256K1.mul(SECP256K1_N, SECP256K1_G) is None}")
    print(f"public A = ({hex(A[0])[:24]}..., ...)")
    print(f"shared x sama: {s1[0] == s2[0]}")
    key = hashlib.sha256(str(s1[0]).encode()).hexdigest()
    print(f"kunci turunan: {key[:32]}...")
    print()


def demo_ecdsa() -> None:
    print("== ECDSA pada secp256k1 ==")
    private, public = ecdh_keypair()
    message = b"Saya setuju dengan perjanjian ini."
    sig = ecdsa_sign(SECP256K1, SECP256K1_G, SECP256K1_N, private, message)
    print(f"r = {hex(sig[0])[:32]}...")
    print(f"s = {hex(sig[1])[:32]}...")
    print(f"verifikasi asli : {ecdsa_verify(SECP256K1, SECP256K1_G, SECP256K1_N, public, message, sig)}")
    print(f"verifikasi ubah : {ecdsa_verify(SECP256K1, SECP256K1_G, SECP256K1_N, public, b'pesan lain', sig)}")
    print()


def demo_non_ce_curve() -> None:
    print("== Mengapa kurva harus non-singular ==")
    try:
        Curve(p=17, a=0, b=0)
    except ValueError as error:
        print("ditolak:", error)
    print("Diskriminan 4a^3 + 27b^2 harus tidak nol modulo p.")
    print()


if __name__ == "__main__":
    assert SECP256K1.is_on_curve(SECP256K1_G)
    assert SECP256K1.mul(SECP256K1_N, SECP256K1_G) is None
    assert SMALL.order_of(SMALL_G) == 19

    demo_small_curve()
    demo_group_law()
    demo_ecdh()
    demo_ecdsa()
    demo_non_ce_curve()

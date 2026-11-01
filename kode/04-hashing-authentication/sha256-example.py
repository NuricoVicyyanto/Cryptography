"""
sha256-example.py
Implementasi SHA-256 dari nol, lengkap dengan demonstrasi avalanche effect
dan serangan length extension terhadap MAC naif.

Konstanta K dan H dibangkitkan secara matematis dari akar bilangan prima,
bukan diketik manual, sehingga terhindar dari kesalahan transkripsi.

Jalankan:
    python sha256-example.py
"""

from __future__ import annotations

import hashlib
import struct

# ---------------------------------------------------------------------------
# Pembangkitan konstanta
# ---------------------------------------------------------------------------
# H[0..7] = 32 bit pertama bagian pecahan akar kuadrat 8 prima pertama.
# K[0..63] = 32 bit pertama bagian pecahan akar pangkat tiga 64 prima pertama.


def _is_prime(n: int) -> bool:
    if n < 2:
        return False
    i = 2
    while i * i <= n:
        if n % i == 0:
            return False
        i += 1
    return True


def _first_primes(count: int) -> list[int]:
    primes, candidate = [], 2
    while len(primes) < count:
        if _is_prime(candidate):
            primes.append(candidate)
        candidate += 1
    return primes


def _integer_cuberoot(n: int) -> int:
    """Akar pangkat tiga bilangan bulat terbesar yang pangkat tiganya <= n."""
    lo, hi = 0, 1 << ((n.bit_length() // 3) + 2)
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if mid ** 3 <= n:
            lo = mid
        else:
            hi = mid - 1
    return lo


def _build_constants() -> tuple[list[int], list[int]]:
    import math

    primes = _first_primes(64)
    h = [math.isqrt(p << 64) & 0xFFFFFFFF for p in primes[:8]]
    k = [_integer_cuberoot(p << 96) & 0xFFFFFFFF for p in primes]
    return h, k


H0, K = _build_constants()


# ---------------------------------------------------------------------------
# Operasi 32 bit
# ---------------------------------------------------------------------------

MASK = 0xFFFFFFFF


def rotr(x: int, n: int) -> int:
    return ((x >> n) | (x << (32 - n))) & MASK


def ch(x: int, y: int, z: int) -> int:
    return (x & y) ^ (~x & z) & MASK


def maj(x: int, y: int, z: int) -> int:
    return (x & y) ^ (x & z) ^ (y & z)


def big_sigma0(x: int) -> int:
    return rotr(x, 2) ^ rotr(x, 13) ^ rotr(x, 22)


def big_sigma1(x: int) -> int:
    return rotr(x, 6) ^ rotr(x, 11) ^ rotr(x, 25)


def small_sigma0(x: int) -> int:
    return rotr(x, 7) ^ rotr(x, 18) ^ (x >> 3)


def small_sigma1(x: int) -> int:
    return rotr(x, 17) ^ rotr(x, 19) ^ (x >> 10)


# ---------------------------------------------------------------------------
# Kompresi dan padding
# ---------------------------------------------------------------------------

def compress(state: list[int], block: bytes) -> list[int]:
    w = list(struct.unpack(">16I", block))
    for i in range(16, 64):
        w.append((small_sigma1(w[i - 2]) + w[i - 7] + small_sigma0(w[i - 15]) + w[i - 16]) & MASK)

    a, b, c, d, e, f, g, h = state
    for i in range(64):
        t1 = (h + big_sigma1(e) + ch(e, f, g) + K[i] + w[i]) & MASK
        t2 = (big_sigma0(a) + maj(a, b, c)) & MASK
        h, g, f, e = g, f, e, (d + t1) & MASK
        d, c, b, a = c, b, a, (t1 + t2) & MASK

    return [(x + y) & MASK for x, y in zip(state, [a, b, c, d, e, f, g, h])]


def pad(message: bytes, total_len: int | None = None) -> bytes:
    """
    Padding SHA-256: 0x80, lalu nol, lalu panjang pesan 64 bit big endian.
    total_len adalah panjang seluruh pesan, bukan hanya sisa buffer.
    """
    if total_len is None:
        total_len = len(message)
    bit_len = total_len * 8
    message += b"\x80"
    message += b"\x00" * ((56 - len(message) % 64) % 64)
    message += struct.pack(">Q", bit_len)
    return message


# ---------------------------------------------------------------------------
# API hash
# ---------------------------------------------------------------------------

class SHA256:
    """Objek hash yang bisa di-update bertahap."""

    def __init__(self):
        self.state = H0[:]
        self.buffer = b""
        self.length = 0

    def update(self, data: bytes) -> "SHA256":
        self.length += len(data)
        self.buffer += data
        while len(self.buffer) >= 64:
            self.state = compress(self.state, self.buffer[:64])
            self.buffer = self.buffer[64:]
        return self

    def digest(self) -> bytes:
        clone = SHA256()
        clone.state = self.state[:]
        clone.buffer = self.buffer
        clone.length = self.length
        padded = pad(clone.buffer, clone.length)
        for i in range(0, len(padded), 64):
            clone.state = compress(clone.state, padded[i:i + 64])
        return struct.pack(">8I", *clone.state)

    def hexdigest(self) -> str:
        return self.digest().hex()


def sha256(data: bytes) -> bytes:
    return SHA256().update(data).digest()


# ---------------------------------------------------------------------------
# Serangan length extension
# ---------------------------------------------------------------------------

def naive_mac(key: bytes, message: bytes) -> bytes:
    """MAC naif: H(key || message). Rentan length extension."""
    return sha256(key + message)


def length_extension_attack(digest: bytes, original_len: int, extra: bytes) -> tuple[bytes, bytes]:
    """
    Diberikan H(key || message) dan panjang key || message, hitung
    H(key || message || padding || extra) tanpa mengetahui key.

    Kembalikan (digest palsu, glue padding) agar pemanggil bisa
    menghitung pesan lengkap yang dipalsukan.
    """
    glue = b"\x80" + b"\x00" * ((56 - (original_len + 1) % 64) % 64) + struct.pack(">Q", original_len * 8)

    forged = SHA256()
    forged.state = list(struct.unpack(">8I", digest))
    forged.length = original_len + len(glue)
    forged.buffer = b""
    # Proses tambahan sebagai blok penuh, padding akhir ditangani digest().
    forged.update(extra)
    return forged.digest(), glue


def hmac_sha256(key: bytes, message: bytes) -> bytes:
    """HMAC standar, lihat hmac.py untuk implementasi lengkap."""
    if len(key) > 64:
        key = sha256(key)
    key = key.ljust(64, b"\x00")
    inner = sha256(bytes(b ^ 0x36 for b in key) + message)
    outer = sha256(bytes(b ^ 0x5C for b in key) + inner)
    return outer


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

def demo_basic() -> None:
    print("== Uji vektor SHA-256 ==")
    vectors = {
        b"": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        b"abc": "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad",
        b"abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq":
            "248d6a61d20638b8e5c026930c3e6039a33ce45964ff2167f6ecedd419db06c1",
    }
    for msg, expected in vectors.items():
        got = sha256(msg).hex()
        label = msg.decode() if len(msg) < 60 else f"{len(msg)} byte"
        print(f"{label!r}: {got}")
        assert got == expected, "hash tidak cocok"
    print("semua vektor cocok")
    print()


def demo_matches_hashlib() -> None:
    print("== Perbandingan dengan hashlib ==")
    for size in (0, 1, 55, 56, 63, 64, 65, 1000, 100000):
        data = bytes((i * 31) & 0xFF for i in range(size))
        assert sha256(data) == hashlib.sha256(data).digest()
    print("cocok untuk semua ukuran termasuk batas padding 55, 56, 63, 64")
    print()


def demo_incremental() -> None:
    print("== Hash bertahap ==")
    h = SHA256()
    for part in (b"Hello, ", b"world", b"!"):
        h.update(part)
    print("bertahap:", h.hexdigest())
    print("sekaligus:", sha256(b"Hello, world!").hex())
    print()


def demo_avalanche() -> None:
    print("== Efek avalanche ==")
    a = sha256(b"kriptografi")
    b = sha256(b"Kriptografi")
    diff = sum(bin(x ^ y).count("1") for x, y in zip(a, b))
    print(f"beda 1 bit input, bit output berubah: {diff} dari 256 ({diff / 256 * 100:.1f}%)")
    print()


def demo_length_extension() -> None:
    print("== Serangan length extension pada H(key || message) ==")
    key = b"rahasia"
    message = b"jumlah=100"
    total_len = len(key) + len(message)
    mac = naive_mac(key, message)
    extra = b"&admin=true"

    forged, glue = length_extension_attack(mac, total_len, extra)
    target = naive_mac(key, message + glue + extra)

    print(f"MAC asli  : {mac.hex()[:32]}...")
    print(f"MAC palsu : {forged.hex()[:32]}...")
    print(f"cocok dengan perhitungan server: {forged == target}")
    print("MAC naif bisa dipalsukan tanpa mengetahui key.")
    print()


def demo_hmac_defense() -> None:
    print("== HMAC tidak rentan length extension ==")
    key = b"rahasia"
    message = b"jumlah=100"
    tag = hmac_sha256(key, message)
    forged, glue = length_extension_attack(tag, len(key) + len(message), b"&admin=true")
    print(f"HMAC asli    : {tag.hex()[:32]}...")
    print(f"hasil ekstensi: {forged.hex()[:32]}...")
    print(f"berhasil? {forged == hmac_sha256(key, message + glue + b'&admin=true')}")
    print("Nilai ekstensi tidak sama dengan HMAC yang sah.")
    print("HMAC memakai dua lapis hash sehingga state tidak bisa diperpanjang.")
    print()


if __name__ == "__main__":
    demo_basic()
    demo_matches_hashlib()
    demo_incremental()
    demo_avalanche()
    demo_length_extension()
    demo_hmac_defense()

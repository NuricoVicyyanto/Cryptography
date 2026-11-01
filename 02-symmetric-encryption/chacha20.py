"""
chacha20.py
Implementasi ChaCha20 dari nol sesuai RFC 8439, plus Poly1305 dan benchmark.

ChaCha20 adalah stream cipher rancangan Daniel J. Bernstein. Ia cepat di
software karena hanya memakai penjumlahan 32 bit, rotasi, dan XOR, tanpa
tabel lookup besar. Ini membuatnya tahan terhadap cache timing attack dan
sangat cocok untuk perangkat tanpa akselerasi AES.

Jalankan:
    python chacha20.py
"""

from __future__ import annotations

import os
import struct
import time

MASK32 = 0xFFFFFFFF


# ---------------------------------------------------------------------------
# Utilitas
# ---------------------------------------------------------------------------

def rotl32(x: int, n: int) -> int:
    """Rotasi kiri 32 bit."""
    return ((x << n) | (x >> (32 - n))) & MASK32


def quarter_round(state: list[int], a: int, b: int, c: int, d: int) -> None:
    """
    Quarter round ChaCha, empat penjumlahan, empat XOR, empat rotasi.
    Inilah satu-satunya operasi non-linear selain carry dari penjumlahan.
    """
    state[a] = (state[a] + state[b]) & MASK32
    state[d] ^= state[a]
    state[d] = rotl32(state[d], 16)

    state[c] = (state[c] + state[d]) & MASK32
    state[b] ^= state[c]
    state[b] = rotl32(state[b], 12)

    state[a] = (state[a] + state[b]) & MASK32
    state[d] ^= state[a]
    state[d] = rotl32(state[d], 8)

    state[c] = (state[c] + state[d]) & MASK32
    state[b] ^= state[c]
    state[b] = rotl32(state[b], 7)


def block(key: bytes, counter: int, nonce: bytes) -> bytes:
    """
    Hitung satu blok keystream 64 byte.

    State 16 word:
        konstanta "expand 32-byte k"  (4 word)
        kunci 32 byte                (8 word)
        counter 32 bit               (1 word)
        nonce 96 bit                 (3 word)
    """
    if len(key) != 32:
        raise ValueError("kunci harus 32 byte")
    if len(nonce) != 12:
        raise ValueError("nonce harus 12 byte")

    constants = struct.unpack("<4I", b"expand 32-byte k")
    key_words = struct.unpack("<8I", key)
    nonce_words = struct.unpack("<3I", nonce)

    state = list(constants) + list(key_words) + [counter & MASK32] + list(nonce_words)
    working = state[:]

    # 20 round = 10 iterasi, masing-masing satu column round dan satu diagonal round.
    for _ in range(10):
        quarter_round(working, 0, 4, 8, 12)
        quarter_round(working, 1, 5, 9, 13)
        quarter_round(working, 2, 6, 10, 14)
        quarter_round(working, 3, 7, 11, 15)

        quarter_round(working, 0, 5, 10, 15)
        quarter_round(working, 1, 6, 11, 12)
        quarter_round(working, 2, 7, 8, 13)
        quarter_round(working, 3, 4, 9, 14)

    out = [(working[i] + state[i]) & MASK32 for i in range(16)]
    return struct.pack("<16I", *out)


def keystream(key: bytes, nonce: bytes, length: int, initial_counter: int = 1) -> bytes:
    """Bangkitkan keystream sepanjang length byte."""
    out = bytearray()
    counter = initial_counter
    while len(out) < length:
        out.extend(block(key, counter, nonce))
        counter += 1
        if counter > MASK32:
            raise OverflowError("counter ChaCha20 habis, ganti kunci")
    return bytes(out[:length])


def chacha20_encrypt(key: bytes, nonce: bytes, plaintext: bytes,
                     initial_counter: int = 1) -> bytes:
    """Enkripsi = XOR plaintext dengan keystream."""
    ks = keystream(key, nonce, len(plaintext), initial_counter)
    return bytes(p ^ k for p, k in zip(plaintext, ks))


def chacha20_decrypt(key: bytes, nonce: bytes, ciphertext: bytes,
                     initial_counter: int = 1) -> bytes:
    """Dekripsi identik dengan enkripsi."""
    return chacha20_encrypt(key, nonce, ciphertext, initial_counter)


# ---------------------------------------------------------------------------
# Poly1305 (bonus, untuk memahami AEAD ChaCha20-Poly1305)
# ---------------------------------------------------------------------------

def poly1305_mac(message: bytes, key: bytes) -> bytes:
    """
    Poly1305 one-time authenticator sesuai RFC 8439.
    key harus 32 byte: 16 byte pertama r, 16 byte berikutnya s.
    """
    if len(key) != 32:
        raise ValueError("kunci Poly1305 harus 32 byte")

    r = int.from_bytes(key[:16], "little") & 0x0FFFFFFC0FFFFFFC0FFFFFFC0FFFFFFF
    s = int.from_bytes(key[16:], "little")
    p = (1 << 130) - 5

    acc = 0
    for i in range(0, len(message), 16):
        chunk = message[i:i + 16]
        n = int.from_bytes(chunk + b"\x01", "little")
        acc = ((acc + n) * r) % p

    tag = (acc + s) & ((1 << 128) - 1)
    return tag.to_bytes(16, "little")


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

def demo_rfc_vector() -> None:
    print("== Vektor uji RFC 8439 ==")
    key = bytes(range(32))
    nonce = bytes.fromhex("000000090000004a00000000")
    expected = (
        "10f1e7e4d13b5915500fdd1fa32071c4"
        "c7d1f4c733c068030422aa9ac3d46c4e"
        "d2826446079faa0914c2d705d98b02a2"
        "b5129cd1de164eb9cbd083e8a2503c4e"
    )
    ks = keystream(key, nonce, 64, initial_counter=1)
    print("keystream:", ks.hex())
    print("expected :", expected)
    assert ks.hex() == expected, "keystream tidak sesuai RFC 8439"
    print("cocok dengan RFC 8439")
    print()


def demo_encrypt() -> None:
    print("== Enkripsi dan dekripsi ==")
    key = bytes.fromhex("00" * 32)
    nonce = bytes.fromhex("000000000000004a00000000")
    plaintext = (
        b"Ladies and Gentlemen of the class of '99: If I could offer you "
        b"only one tip for the future, sunscreen would be it."
    )
    cipher = chacha20_encrypt(key, nonce, plaintext, initial_counter=1)
    print("ciphertext:", cipher.hex()[:96], "...")
    back = chacha20_decrypt(key, nonce, cipher, initial_counter=1)
    print("kembali   :", back.decode())
    assert back == plaintext
    print()


def demo_poly1305() -> None:
    print("== Poly1305 ==")
    key = bytes.fromhex(
        "85d6be7857556d337f4452fe42d506a8"
        "0103808afb0db2fd4abff6af4149f51b"
    )
    message = b"Cryptographic Forum Research Group"
    tag = poly1305_mac(message, key)
    print("tag     :", tag.hex())
    print("expected: a8061dc1305136c6c22b8baf0c0127a9")
    assert tag.hex() == "a8061dc1305136c6c22b8baf0c0127a9"
    print("cocok dengan RFC 8439")
    print()


def demo_avalanche() -> None:
    print("== Efek avalanche ==")
    key = bytes(32)
    nonce = bytes(12)
    a = keystream(key, nonce, 64, 1)
    b = keystream(key, nonce, 64, 2)
    diff = sum(bin(x ^ y).count("1") for x, y in zip(a, b))
    print(f"ganti counter 1 ke 2, bit berubah: {diff} dari 512")
    print()


def benchmark() -> None:
    print("== Kecepatan ==")
    key = os.urandom(32)
    nonce = os.urandom(12)
    data = os.urandom(1024 * 1024)
    t0 = time.perf_counter()
    out = chacha20_encrypt(key, nonce, data)
    t1 = time.perf_counter()
    print(f"ChaCha20 murni Python, 1 MB: {t1 - t0:.2f} detik")
    print(f"laju sekitar {1 / (t1 - t0):.2f} MB/detik")
    assert len(out) == len(data)
    print("Catatan: implementasi C atau hardware bisa mencapai ribuan MB/detik.")
    print()


if __name__ == "__main__":
    demo_rfc_vector()
    demo_encrypt()
    demo_poly1305()
    demo_avalanche()
    benchmark()

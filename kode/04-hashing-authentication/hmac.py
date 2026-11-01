"""
hmac.py
Implementasi HMAC (RFC 2104) di atas SHA-256 dan SHA-1, plus demonstrasi
perbandingan waktu yang constant time dan kesalahan umum.

HMAC dirancang untuk mengubah hash function menjadi MAC (Message
Authentication Code) yang aman, meskipun hash tersebut rentan terhadap
length extension.

Jalankan:
    python hmac.py
"""

from __future__ import annotations

import hashlib
import importlib.util
import os
import sysconfig
import time


def _load_stdlib_hmac():
    """
    Muat modul hmac dari standard library secara eksplisit.
    Ini diperlukan karena file ini sendiri bernama hmac.py sehingga
    'import hmac' akan memuat file ini, bukan modul standar.
    """
    path = os.path.join(sysconfig.get_paths()["stdlib"], "hmac.py")
    spec = importlib.util.spec_from_file_location("_stdlib_hmac", path)
    if spec is None or spec.loader is None:
        raise ImportError("tidak bisa memuat hmac standar")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


stdlib_hmac = _load_stdlib_hmac()

BLOCK_SIZE = {
    "sha256": 64,
    "sha1": 64,
    "sha512": 128,
}


# ---------------------------------------------------------------------------
# Implementasi HMAC
# ---------------------------------------------------------------------------

def hmac_new(key: bytes, message: bytes, algorithm: str = "sha256") -> bytes:
    """
    HMAC(K, m) = H((K' xor opad) || H((K' xor ipad) || m))

    K' adalah key yang dipotong atau di-pad menjadi ukuran blok hash.
    ipad = 0x36 berulang, opad = 0x5C berulang.
    """
    block = BLOCK_SIZE[algorithm]
    hash_fn = getattr(hashlib, algorithm)

    if len(key) > block:
        key = hash_fn(key).digest()
    key = key.ljust(block, b"\x00")

    inner = hash_fn(bytes(b ^ 0x36 for b in key) + message).digest()
    return hash_fn(bytes(b ^ 0x5C for b in key) + inner).digest()


def hmac_hex(key: bytes, message: bytes, algorithm: str = "sha256") -> str:
    return hmac_new(key, message, algorithm).hex()


# ---------------------------------------------------------------------------
# Perbandingan constant time
# ---------------------------------------------------------------------------

def unsafe_compare(a: bytes, b: bytes) -> bool:
    """
    Perbandingan naif. Berhenti di byte pertama yang berbeda,
    sehingga waktu eksekusi membocorkan panjang prefix yang cocok.
    """
    if len(a) != len(b):
        return False
    for x, y in zip(a, b):
        if x != y:
            return False
    return True


def constant_time_compare(a: bytes, b: bytes) -> bool:
    """
    Bandingkan seluruh byte tanpa early return.
    Waktu eksekusi hanya bergantung pada panjang, bukan isi.
    """
    if len(a) != len(b):
        return False
    result = 0
    for x, y in zip(a, b):
        result |= x ^ y
    return result == 0


def timing_demo() -> None:
    print("== Timing perbandingan naif ==")
    secret = b"A" * 32
    guesses = [
        b"B" * 32,
        b"A" * 16 + b"B" * 16,
        b"A" * 31 + b"B",
        secret,
    ]
    for guess in guesses:
        start = time.perf_counter()
        for _ in range(200000):
            unsafe_compare(secret, guess)
        elapsed = time.perf_counter() - start
        matched = sum(1 for x, y in zip(secret, guess) if x == y)
        print(f"prefix cocok {matched:>2} byte: {elapsed:.3f} detik")
    print("Pola waktu membocorkan seberapa banyak byte awal yang sudah benar.")
    print()


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

def demo_rfc4231() -> None:
    print("== Vektor uji RFC 4231 (HMAC-SHA256) ==")
    # Test case 1
    key = b"\x0b" * 20
    data = b"Hi There"
    expected = "b0344c61d8db38535ca8afceaf0bf12b881dc200c9833da726e9376c2e32cff7"
    got = hmac_hex(key, data)
    print("case 1:", got)
    assert got == expected
    print("cocok")

    # Test case 2
    key = b"Jefe"
    data = b"what do ya want for nothing?"
    expected = "5bdcc146bf60754e6a042426089575c75a003f089d2739839dec58b964ec3843"
    got = hmac_hex(key, data)
    print("case 2:", got)
    assert got == expected
    print("cocok")

    # Test case 6, key lebih panjang dari block size
    key = b"\xaa" * 131
    data = b"Test Using Larger Than Block-Size Key - Hash Key First"
    expected = "60e431591ee0b67f0d8a26aacbf5b77f8e0bc6213728c5140546040f0ee37f54"
    got = hmac_hex(key, data)
    print("case 6:", got)
    assert got == expected
    print("cocok")
    print()


def demo_stdlib_compare() -> None:
    print("== Perbandingan dengan library standar ==")
    for size in (0, 1, 32, 64, 65, 1000):
        key = os.urandom(size)
        msg = os.urandom(37)
        assert hmac_new(key, msg) == stdlib_hmac.new(key, msg, hashlib.sha256).digest()
    print("cocok untuk berbagai ukuran key, termasuk key lebih panjang dari blok")
    print()


def demo_hmac_sha1() -> None:
    print("== HMAC-SHA1 ==")
    key = b"key"
    data = b"The quick brown fox jumps over the lazy dog"
    print("HMAC-SHA1:", hmac_hex(key, data, "sha1"))
    assert hmac_new(key, data, "sha1") == stdlib_hmac.new(key, data, hashlib.sha1).digest()
    print("Catatan: HMAC-SHA1 masih dianggap aman untuk MAC, tetapi SHA-1 ")
    print("sudah tidak disarankan untuk collision resistance.")
    print()


def demo_usage() -> None:
    print("== Pemakaian: memverifikasi pesan ==")
    key = os.urandom(32)
    message = b"transfer|1000|rekening-123"
    tag = hmac_new(key, message)

    print(f"pesan : {message.decode()}")
    print(f"tag   : {tag.hex()}")

    tampered = b"transfer|9000|rekening-123"
    print(f"pesan asli valid   : {constant_time_compare(tag, hmac_new(key, message))}")
    print(f"pesan ubah valid   : {constant_time_compare(tag, hmac_new(key, tampered))}")
    print("Gunakan perbandingan constant time saat memeriksa tag.")
    print()


def demo_key_separation() -> None:
    print("== Panjang key dan keamanan ==")
    print("HMAC dengan key 16 byte keamanan efektif 128 bit.")
    print("HMAC dengan key 32 byte keamanan efektif 256 bit, sebatas kekuatan hash.")
    print("Jangan memakai key yang sama untuk enkripsi dan MAC.")
    print("Turunkan dua key terpisah dengan HKDF atau KDF lain.")
    print()


if __name__ == "__main__":
    demo_rfc4231()
    demo_stdlib_compare()
    demo_hmac_sha1()
    demo_usage()
    demo_key_separation()
    timing_demo()

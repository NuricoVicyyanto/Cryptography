"""
blake3-example.py
Implementasi BLAKE3 dari nol (hash pohon, XOF, 7 round) plus perbandingan
dengan BLAKE2b yang tersedia di hashlib.

BLAKE3 adalah fungsi hash modern yang sangat cepat karena:
    1. Berbasis struktur pohon (tree hashing), sehingga paralel.
    2. Hanya 7 round per kompresi.
    3. Bisa menghasilkan output sepanjang apa pun (XOF).

Jalankan:
    python blake3-example.py
"""

from __future__ import annotations

import hashlib
import os
import struct
import time

# ---------------------------------------------------------------------------
# Konstanta
# ---------------------------------------------------------------------------
# IV BLAKE3 sama dengan IV SHA-256, yaitu bagian pecahan akar kuadrat
# delapan bilangan prima pertama.

IV = [
    0x6A09E667, 0xBB67AE85, 0x3C6EF372, 0xA54FF53A,
    0x510E527F, 0x9B05688C, 0x1F83D9AB, 0x5BE0CD19,
]

# Permutasi pesan antar round. BLAKE3 hanya memakai 7 round,
# berbeda dari BLAKE2s yang memakai 10 round.
MSG_PERMUTATION = [2, 6, 3, 10, 7, 0, 4, 13, 1, 11, 12, 5, 9, 14, 15, 8]

CHUNK_START = 1
CHUNK_END = 2
PARENT = 4
ROOT = 8

MASK32 = 0xFFFFFFFF


def rotr(x: int, n: int) -> int:
    return ((x >> n) | (x << (32 - n))) & MASK32


# ---------------------------------------------------------------------------
# Kompresi
# ---------------------------------------------------------------------------

def g(state: list[int], a: int, b: int, c: int, d: int, mx: int, my: int) -> None:
    """
    Fungsi G BLAKE3. Sama seperti BLAKE2s, tetapi tidak ada penambahan
    konstanta karena konstanta sudah masuk melalui state awal.
    """
    state[a] = (state[a] + state[b] + mx) & MASK32
    state[d] = rotr(state[d] ^ state[a], 16)

    state[c] = (state[c] + state[d]) & MASK32
    state[b] = rotr(state[b] ^ state[c], 12)

    state[a] = (state[a] + state[b] + my) & MASK32
    state[d] = rotr(state[d] ^ state[a], 8)

    state[c] = (state[c] + state[d]) & MASK32
    state[b] = rotr(state[b] ^ state[c], 7)


def compress(cv: list[int], block_words: list[int], counter: int,
             block_len: int, flags: int) -> list[int]:
    """
    Kompresi 64 byte menjadi 8 word chaining value.
    Output penuh 16 word dipakai untuk mode XOF.
    """
    state = (
        list(cv)
        + list(IV[:4])
        + [counter & MASK32, (counter >> 32) & MASK32, block_len, flags]
    )
    m = list(block_words)

    for _ in range(7):
        g(state, 0, 4, 8, 12, m[0], m[1])
        g(state, 1, 5, 9, 13, m[2], m[3])
        g(state, 2, 6, 10, 14, m[4], m[5])
        g(state, 3, 7, 11, 15, m[6], m[7])

        g(state, 0, 5, 10, 15, m[8], m[9])
        g(state, 1, 6, 11, 12, m[10], m[11])
        g(state, 2, 7, 8, 13, m[12], m[13])
        g(state, 3, 4, 9, 14, m[14], m[15])

        m = [m[i] for i in MSG_PERMUTATION]

    out = [(state[i] ^ state[i + 8]) & MASK32 for i in range(8)]
    out += [(state[i + 8] ^ cv[i]) & MASK32 for i in range(8)]
    return out


# ---------------------------------------------------------------------------
# Output dan chunk
# ---------------------------------------------------------------------------

class Output:
    """Merepresentasikan hasil kompresi yang belum difinalisasi."""

    def __init__(self, cv, block_words, counter, block_len, flags):
        self.cv = cv
        self.block_words = block_words
        self.counter = counter
        self.block_len = block_len
        self.flags = flags

    def chaining_value(self) -> list[int]:
        return compress(self.cv, self.block_words, self.counter, self.block_len, self.flags)[:8]

    def root_bytes(self, length: int) -> bytes:
        """Hasilkan output XOF sepanjang length byte."""
        out = bytearray()
        output_block_counter = 0
        while len(out) < length:
            words = compress(self.cv, self.block_words, output_block_counter,
                             self.block_len, self.flags | ROOT)
            out.extend(struct.pack("<16I", *words))
            output_block_counter += 1
        return bytes(out[:length])


class ChunkState:
    """Satu chunk berukuran maksimal 1024 byte."""

    def __init__(self, counter: int):
        self.cv = list(IV)
        self.counter = counter
        self.buf = b""
        self.blocks = 0

    def length(self) -> int:
        return 64 * self.blocks + len(self.buf)

    def start_flag(self) -> int:
        return CHUNK_START if self.blocks == 0 else 0

    def update(self, data: bytes) -> None:
        while data:
            if len(self.buf) == 64:
                words = struct.unpack("<16I", self.buf)
                self.cv = compress(self.cv, list(words), self.counter, 64, self.start_flag())[:8]
                self.blocks += 1
                self.buf = b""
            take = min(64 - len(self.buf), len(data))
            self.buf += data[:take]
            data = data[take:]

    def output(self) -> Output:
        padded = self.buf + b"\x00" * (64 - len(self.buf))
        words = list(struct.unpack("<16I", padded))
        return Output(self.cv, words, self.counter, len(self.buf),
                      self.start_flag() | CHUNK_END)


def parent_output(left: list[int], right: list[int]) -> Output:
    return Output(list(IV), list(left) + list(right), 0, 64, PARENT)


def parent_cv(left: list[int], right: list[int]) -> list[int]:
    return parent_output(left, right).chaining_value()


# ---------------------------------------------------------------------------
# API hash
# ---------------------------------------------------------------------------

class BLAKE3:
    """Hash BLAKE3 dengan dukungan update bertahap dan output XOF."""

    def __init__(self):
        self.chunk = ChunkState(0)
        self.stack: list[list[int]] = []
        self.total_bytes = 0

    def update(self, data: bytes) -> "BLAKE3":
        while data:
            if self.chunk.length() == 1024:
                cv = self.chunk.output().chaining_value()
                total_chunks = self.chunk.counter + 1
                self.stack.append(cv)
                self._merge(total_chunks)
                self.chunk = ChunkState(total_chunks)
            take = min(1024 - self.chunk.length(), len(data))
            self.chunk.update(data[:take])
            self.total_bytes += take
            data = data[take:]
        return self

    def _merge(self, total_chunks: int) -> None:
        while total_chunks & 1 == 0 and len(self.stack) > 1:
            right = self.stack.pop()
            left = self.stack.pop()
            self.stack.append(parent_cv(left, right))
            total_chunks >>= 1

    def digest(self, length: int = 32) -> bytes:
        output = self.chunk.output()
        for cv in reversed(self.stack):
            output = parent_output(cv, output.chaining_value())
        return output.root_bytes(length)

    def hexdigest(self, length: int = 32) -> str:
        return self.digest(length).hex()


def blake3(data: bytes, length: int = 32) -> bytes:
    return BLAKE3().update(data).digest(length)


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

def demo_vectors() -> None:
    print("== Vektor uji BLAKE3 ==")
    expected_empty = "af1349b9f5f9a1a6a0404dea36dcc9499bcb25c9adc112b7cc9a93cae41f3262"
    expected_abc = "6437b3ac38465133ffb63b75273a8db548c558465d79db03fd359c6cd5bd9d85"

    got_empty = blake3(b"").hex()
    got_abc = blake3(b"abc").hex()
    print("kosong:", got_empty)
    print("abc   :", got_abc)
    assert got_empty == expected_empty
    assert got_abc == expected_abc
    print("cocok dengan vektor resmi")
    print()


def demo_tree() -> None:
    print("== Hash pohon lintas chunk ==")
    for size in (0, 1, 63, 64, 65, 1023, 1024, 1025, 2048, 5000, 10000):
        data = bytes((i * 7 + 3) & 0xFF for i in range(size))
        one_shot = blake3(data)
        incremental = BLAKE3()
        for i in range(0, size, 333):
            incremental.update(data[i:i + 333])
        assert incremental.digest() == one_shot, f"gagal pada ukuran {size}"
    print("update bertahap konsisten dengan sekali jalan untuk semua ukuran")
    print("termasuk batas chunk 1024 byte dan penggabungan pohon")
    print()


def demo_xof() -> None:
    print("== Output extensible (XOF) ==")
    full = blake3(b"kriptografi", length=96)
    print("32 byte pertama:", full[:32].hex())
    print("32 byte kedua  :", full[32:64].hex())
    print("32 byte ketiga :", full[64:96].hex())
    print("Output 32 byte adalah prefix dari output lebih panjang.")
    assert blake3(b"kriptografi", length=32) == full[:32]
    print()


def demo_compare_blake2() -> None:
    print("== Perbandingan dengan BLAKE2b ==")
    data = os.urandom(1024 * 1024)

    t0 = time.perf_counter()
    h2 = hashlib.blake2b(data).hexdigest()
    t1 = time.perf_counter()
    h3 = blake3(data).hex()
    t2 = time.perf_counter()

    print(f"BLAKE2b (C, 1 MB): {(t1 - t0) * 1000:.2f} ms")
    print(f"BLAKE3  (Python, 1 MB): {(t2 - t1) * 1000:.2f} ms")
    print(f"BLAKE2b: {h2[:32]}...")
    print(f"BLAKE3 : {h3[:32]}...")
    print("Implementasi Python wajar lebih lambat, tetapi BLAKE3 di C")
    print("memanfaatkan SIMD dan paralelisme pohon sehingga jauh lebih cepat.")
    print()


def demo_properties() -> None:
    print("== Properti avalanche ==")
    a = blake3(b"kriptografi")
    b = blake3(b"Kriptografi")
    diff = sum(bin(x ^ y).count("1") for x, y in zip(a, b))
    print(f"ubah 1 bit input, {diff} dari 256 bit output berubah")
    print()


if __name__ == "__main__":
    demo_vectors()
    demo_tree()
    demo_xof()
    demo_properties()
    demo_compare_blake2()

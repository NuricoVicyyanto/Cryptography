"""
transposition.py
Implementasi beberapa transposition cipher klasik.

Berbeda dari substitusi (Caesar, Vigenere) yang mengganti huruf, transposition
hanya memindahkan posisi huruf. Frekuensi huruf tidak berubah, sehingga
analisis frekuensi sederhana tidak bekerja, tetapi pola anagram masih terlihat.

Isi:
    1. Rail Fence Cipher
    2. Columnar Transposition Cipher
    3. Route Cipher (spiral sederhana)
    4. Kriptanalisis Columnar dengan anagram scoring

Jalankan:
    python transposition.py
"""

from __future__ import annotations

import itertools
import math
import string
from collections import Counter

ALPHABET = string.ascii_uppercase


# ---------------------------------------------------------------------------
# 1. Rail Fence Cipher
# ---------------------------------------------------------------------------

def rail_fence_encrypt(plaintext: str, rails: int) -> str:
    """
    Tulis plaintext dalam pola zigzag sebanyak rails baris,
    lalu baca baris demi baris.
    """
    if rails < 2:
        raise ValueError("rails minimal 2")
    clean = "".join(c for c in plaintext.upper() if c.isalpha())
    fence = [[] for _ in range(rails)]
    rail, direction = 0, 1
    for ch in clean:
        fence[rail].append(ch)
        if rail == 0:
            direction = 1
        elif rail == rails - 1:
            direction = -1
        rail += direction
    return "".join("".join(row) for row in fence)


def rail_fence_decrypt(ciphertext: str, rails: int) -> str:
    """
    Rekonstruksi pola zigzag, isi baris sesuai panjang aslinya,
    lalu baca ulang mengikuti pola yang sama.
    """
    if rails < 2:
        raise ValueError("rails minimal 2")
    clean = "".join(c for c in ciphertext.upper() if c.isalpha())
    pattern = _rail_pattern(len(clean), rails)
    lengths = Counter(pattern)

    rows = []
    idx = 0
    for r in range(rails):
        rows.append(list(clean[idx:idx + lengths[r]]))
        idx += lengths[r]

    positions = [0] * rails
    out = []
    for r in pattern:
        out.append(rows[r][positions[r]])
        positions[r] += 1
    return "".join(out)


def _rail_pattern(n: int, rails: int) -> list[int]:
    """Hasilkan urutan indeks rail untuk n karakter."""
    pattern = []
    rail, direction = 0, 1
    for _ in range(n):
        pattern.append(rail)
        if rail == 0:
            direction = 1
        elif rail == rails - 1:
            direction = -1
        rail += direction
    return pattern


# ---------------------------------------------------------------------------
# 2. Columnar Transposition Cipher
# ---------------------------------------------------------------------------

def _column_order(key: str) -> list[int]:
    """
    Urutkan kolom berdasarkan abjad kunci.
    Jika ada huruf kembar, posisi asli dipakai sebagai pemecah seri.
    """
    key = "".join(c for c in key.upper() if c.isalpha())
    return [i for i, _ in sorted(enumerate(key), key=lambda pair: (pair[1], pair[0]))]


def columnar_encrypt(plaintext: str, key: str, pad: str = "X") -> str:
    """
    Tulis plaintext baris demi baris ke grid selebar panjang kunci,
    lalu baca kolom sesuai urutan abjad kunci.
    """
    clean = "".join(c for c in plaintext.upper() if c.isalpha())
    width = len(key)
    if width < 2:
        raise ValueError("kunci minimal 2 huruf")

    remainder = len(clean) % width
    if remainder:
        clean += pad * (width - remainder)

    grid = [clean[i:i + width] for i in range(0, len(clean), width)]
    order = _column_order(key)
    return "".join("".join(row[col] for row in grid) for col in order)


def columnar_decrypt(ciphertext: str, key: str, pad: str = "X") -> str:
    """
    Kebalikan dari columnar_encrypt. Padding di akhir dibuang.
    """
    clean = "".join(c for c in ciphertext.upper() if c.isalpha())
    width = len(key)
    rows = math.ceil(len(clean) / width)
    order = _column_order(key)

    columns = {}
    idx = 0
    for col in order:
        columns[col] = clean[idx:idx + rows]
        idx += rows

    out = []
    for r in range(rows):
        for col in range(width):
            if r < len(columns[col]):
                out.append(columns[col][r])
    text = "".join(out)
    return text.rstrip(pad)


# ---------------------------------------------------------------------------
# 3. Route Cipher
# ---------------------------------------------------------------------------

def route_encrypt(plaintext: str, cols: int) -> str:
    """Tulis plaintext baris demi baris, baca kolom demi kolom (sama seperti columnar tanpa kunci)."""
    clean = "".join(c for c in plaintext.upper() if c.isalpha())
    rows = math.ceil(len(clean) / cols)
    clean = clean.ljust(rows * cols, "X")
    grid = [clean[i:i + cols] for i in range(0, len(clean), cols)]
    return "".join(grid[r][c] for c in range(cols) for r in range(rows))


def route_decrypt(ciphertext: str, cols: int) -> str:
    clean = "".join(c for c in ciphertext.upper() if c.isalpha())
    rows = math.ceil(len(clean) / cols)
    grid = [["" for _ in range(cols)] for _ in range(rows)]
    idx = 0
    for c in range(cols):
        for r in range(rows):
            grid[r][c] = clean[idx]
            idx += 1
    return "".join("".join(row) for row in grid).rstrip("X")


# ---------------------------------------------------------------------------
# 4. Kriptanalisis Columnar
# ---------------------------------------------------------------------------

# Bigram dan trigram umum bahasa Inggris, dipakai untuk menilai apakah teks "terlihat bahasa".
COMMON_BIGRAMS = {
    "TH", "HE", "IN", "ER", "AN", "RE", "ON", "AT", "EN", "ND",
    "TI", "ES", "OR", "TE", "OF", "ED", "IS", "IT", "AL", "AR",
    "ST", "TO", "NT", "NG", "SE", "HA", "AS", "OU", "IO", "LE",
    "VE", "CO", "ME", "DE", "HI", "RI", "RO", "IC", "NE", "EA",
}
COMMON_TRIGRAMS = {
    "THE", "AND", "ING", "HER", "ERE", "ENT", "THA", "NTH", "WAS",
    "ETH", "FOR", "DTH", "HAT", "HIS", "STH", "ION", "TIO", "VER",
    "ALL", "OUL", "ITY", "ARE", "ATE", "HIS", "CON", "RES", "PER",
    "PRO", "TIO", "ONS", "MEN", "ITH", "TED", "ERS", "ATI", "TER",
}


def bigram_score(text: str) -> int:
    """Hitung berapa banyak bigram dan trigram umum yang muncul."""
    clean = "".join(c for c in text.upper() if c.isalpha())
    bi = sum(1 for i in range(len(clean) - 1) if clean[i:i + 2] in COMMON_BIGRAMS)
    tri = sum(1 for i in range(len(clean) - 2) if clean[i:i + 3] in COMMON_TRIGRAMS)
    return bi + 4 * tri


def brute_force_columnar(ciphertext: str, key_length: int, top: int = 5) -> list[tuple[str, int]]:
    """
    Coba semua permutasi kolom untuk panjang kunci kecil (maksimal 8).
    Kembalikan top kandidat (teks, skor).
    """
    clean = "".join(c for c in ciphertext.upper() if c.isalpha())
    rows = math.ceil(len(clean) / key_length)
    results = []

    for perm in itertools.permutations(range(key_length)):
        columns = {}
        idx = 0
        for col in perm:
            columns[col] = clean[idx:idx + rows]
            idx += rows
        out = []
        for r in range(rows):
            for col in range(key_length):
                if r < len(columns[col]):
                    out.append(columns[col][r])
        text = "".join(out)
        results.append((text, bigram_score(text)))

    results.sort(key=lambda pair: pair[1], reverse=True)
    return results[:top]


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

def demo_rail_fence() -> None:
    print("== Rail Fence ==")
    plaintext = "WE ARE DISCOVERED FLEE AT ONCE"
    for rails in (2, 3, 4):
        cipher = rail_fence_encrypt(plaintext, rails)
        back = rail_fence_decrypt(cipher, rails)
        print(f"rails={rails}: {cipher}")
        print(f"  kembali: {back}")
    print()


def demo_columnar() -> None:
    print("== Columnar Transposition ==")
    plaintext = "KRIPTOGRAFI KLASIK SANGAT MENARIK UNTUK DIPELAJARI"
    key = "ZEBRA"
    cipher = columnar_encrypt(plaintext, key)
    print(f"key      : {key}")
    print(f"cipher   : {cipher}")
    print(f"kembali  : {columnar_decrypt(cipher, key)}")
    print()


def demo_route() -> None:
    print("== Route Cipher ==")
    plaintext = "PESAN RAHASIA UNTUK AGEN UTAMA DI JAKARTA"
    for cols in (4, 5, 6):
        cipher = route_encrypt(plaintext, cols)
        print(f"cols={cols}: {cipher}")
        print(f"  kembali: {route_decrypt(cipher, cols)}")
    print()


def demo_break() -> None:
    print("== Kriptanalisis Columnar ==")
    plaintext = (
        "THE GENERAL ORDERS ARE TO ADVANCE AT DAWN AND TO SECURE THE BRIDGE "
        "BEFORE THE ENEMY CAN REINFORCE THEIR POSITION ON THE OTHER SIDE. "
        "ALL UNITS MUST MAINTAIN RADIO SILENCE UNTIL THE ATTACK BEGINS AND "
        "THE ARTILLERY SUPPORT IS READY TO FIRE ON THE DESIGNATED TARGET. "
        "REMEMBER THAT THE MISSION DEPENDS ON SPEED AND SURPRISE SO THERE "
        "WILL BE NO SECOND CHANCE TO CROSS THE RIVER AND TAKE THE HILL."
    )
    key = "BATTLE"
    cipher = columnar_encrypt(plaintext, key, pad="X")
    print(f"cipher: {cipher[:70]}...")
    print("kandidat terbaik:")
    for text, score in brute_force_columnar(cipher, len(key), top=3):
        print(f"  skor {score:>3}: {text[:60]}...")
    print()


def demo_analysis() -> None:
    print("== Bukti frekuensi tidak berubah ==")
    plain = "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG"
    cipher = columnar_encrypt(plain, "KEY")
    plain_freq = Counter(c for c in plain if c.isalpha())
    cipher_freq = Counter(c for c in cipher if c.isalpha())
    # Padding X menambah satu kemunculan X pada ciphertext.
    diff = {k: (plain_freq.get(k, 0), cipher_freq.get(k, 0))
            for k in set(plain_freq) | set(cipher_freq)
            if plain_freq.get(k, 0) != cipher_freq.get(k, 0)}
    print(f"perbedaan frekuensi: {diff}")
    print("hanya huruf padding yang berbeda, distribusi lain identik.")
    print()


def self_test() -> None:
    assert rail_fence_encrypt("HELLO WORLD", 3) == "HOLELWRDLO"
    assert rail_fence_decrypt(rail_fence_encrypt("HELLO WORLD", 3), 3) == "HELLOWORLD"
    assert columnar_encrypt("HELLO", "KEY") == "EOHLLX"
    assert columnar_decrypt(columnar_encrypt("HELLO", "KEY"), "KEY") == "HELLO"
    assert route_decrypt(route_encrypt("ABCDEFGH", 3), 3) == "ABCDEFGH"
    print("Self test lulus.\n")


if __name__ == "__main__":
    self_test()
    demo_rail_fence()
    demo_columnar()
    demo_route()
    demo_break()
    demo_analysis()

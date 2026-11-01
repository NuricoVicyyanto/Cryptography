"""
vigenere.py
Implementasi Vigenere Cipher plus uji Kasiski untuk menebak panjang kunci.

Vigenere adalah Caesar dengan pergeseran yang berubah setiap huruf, mengikuti
huruf kunci. Secara matematis:

    C_i = (P_i + K_i) mod 26
    P_i = (C_i - K_i) mod 26

Kunci diulang sepanjang pesan.

Jalankan:
    python vigenere.py
"""

from __future__ import annotations

import string
from collections import Counter

ALPHABET = string.ascii_uppercase


# ---------------------------------------------------------------------------
# Enkripsi dan dekripsi
# ---------------------------------------------------------------------------

def _clean_key(key: str) -> list[int]:
    key = "".join(c for c in key.upper() if c.isalpha())
    if not key:
        raise ValueError("kunci tidak boleh kosong")
    return [ALPHABET.index(c) for c in key]


def vigenere_encrypt(plaintext: str, key: str) -> str:
    """
    Enkripsi Vigenere. Hanya huruf yang menggeser posisi kunci,
    sehingga spasi dan tanda baca tidak merusak sinkronisasi.
    """
    shifts = _clean_key(key)
    out = []
    idx = 0
    for ch in plaintext:
        if ch.isupper():
            out.append(ALPHABET[(ALPHABET.index(ch) + shifts[idx % len(shifts)]) % 26])
            idx += 1
        elif ch.islower():
            out.append(ALPHABET[(ALPHABET.index(ch.upper()) + shifts[idx % len(shifts)]) % 26].lower())
            idx += 1
        else:
            out.append(ch)
    return "".join(out)


def vigenere_decrypt(ciphertext: str, key: str) -> str:
    """
    Dekripsi Vigenere. Gunakan pergeseran negatif dari kunci.
    """
    shifts = _clean_key(key)
    out = []
    idx = 0
    for ch in ciphertext:
        if ch.isupper():
            out.append(ALPHABET[(ALPHABET.index(ch) - shifts[idx % len(shifts)]) % 26])
            idx += 1
        elif ch.islower():
            out.append(ALPHABET[(ALPHABET.index(ch.upper()) - shifts[idx % len(shifts)]) % 26].lower())
            idx += 1
        else:
            out.append(ch)
    return "".join(out)


# ---------------------------------------------------------------------------
# Kasiski Examination
# ---------------------------------------------------------------------------

def kasiski_repeats(ciphertext: str, min_len: int = 3) -> dict[str, list[int]]:
    """
    Temukan semua substring yang muncul lebih dari sekali.
    Jarak antar kemunculan adalah kelipatan panjang kunci, dengan asumsi
    potongan yang sama dienkripsi dengan posisi kunci yang sama.
    """
    text = "".join(c for c in ciphertext.upper() if c.isalpha())
    positions: dict[str, list[int]] = {}
    for i in range(len(text) - min_len + 1):
        sub = text[i:i + min_len]
        positions.setdefault(sub, []).append(i)
    return {sub: pos for sub, pos in positions.items() if len(pos) > 1}


def kasiski_distances(ciphertext: str, min_len: int = 3) -> list[int]:
    """Kumpulkan semua jarak antar kemunculan substring yang berulang."""
    distances = []
    for positions in kasiski_repeats(ciphertext, min_len).values():
        for i in range(len(positions) - 1):
            distances.append(positions[i + 1] - positions[i])
    return distances


def guess_key_length(ciphertext: str, max_len: int = 20) -> list[tuple[int, float]]:
    """
    Tebak panjang kunci dengan mencari nilai yang paling banyak membagi
    jarak-jarak Kasiski. Kembalikan daftar (panjang, rasio).
    """
    distances = kasiski_distances(ciphertext)
    if not distances:
        return []
    scores = []
    for length in range(2, max_len + 1):
        divisible = sum(1 for d in distances if d % length == 0)
        scores.append((length, divisible / len(distances)))
    return sorted(scores, key=lambda item: item[1], reverse=True)


# ---------------------------------------------------------------------------
# Index of Coincidence
# ---------------------------------------------------------------------------

def index_of_coincidence(text: str) -> float:
    """
    Ukur kemungkinan dua huruf acak dalam text identik.
    Bahasa Inggris sekitar 0.066, teks acak sekitar 0.038.
    """
    letters = [c for c in text.upper() if c.isalpha()]
    n = len(letters)
    if n < 2:
        return 0.0
    counts = Counter(letters)
    return sum(c * (c - 1) for c in counts.values()) / (n * (n - 1))


def split_by_key_length(ciphertext: str, length: int) -> list[str]:
    """Pecah ciphertext menjadi length kolom berdasarkan posisi modulo length."""
    text = "".join(c for c in ciphertext.upper() if c.isalpha())
    return ["".join(text[i::length]) for i in range(length)]


def average_ic_for_length(ciphertext: str, length: int) -> float:
    columns = split_by_key_length(ciphertext, length)
    return sum(index_of_coincidence(col) for col in columns) / len(columns)


# ---------------------------------------------------------------------------
# Kriptanalisis per kolom
# ---------------------------------------------------------------------------

ENGLISH_FREQ = {
    "A": 8.167, "B": 1.492, "C": 2.782, "D": 4.253, "E": 12.702,
    "F": 2.228, "G": 2.015, "H": 6.094, "I": 6.966, "J": 0.153,
    "K": 0.772, "L": 4.025, "M": 2.406, "N": 6.749, "O": 7.507,
    "P": 1.929, "Q": 0.095, "R": 5.987, "S": 6.327, "T": 9.056,
    "U": 2.758, "V": 0.978, "W": 2.360, "X": 0.150, "Y": 1.974,
    "Z": 0.074,
}


def best_shift_for_column(column: str) -> tuple[int, float]:
    """Cari pergeseran Caesar terbaik untuk satu kolom dengan chi-squared."""
    best_shift, best_score = 0, float("inf")
    n = len(column)
    for shift in range(26):
        shifted = "".join(ALPHABET[(ALPHABET.index(c) - shift) % 26] for c in column)
        counts = Counter(shifted)
        score = 0.0
        for letter in ALPHABET:
            expected = ENGLISH_FREQ[letter] / 100 * n
            observed = counts.get(letter, 0)
            if expected > 0:
                score += (observed - expected) ** 2 / expected
        if score < best_score:
            best_shift, best_score = shift, score
    return best_shift, best_score


def break_vigenere(ciphertext: str, key_length: int) -> tuple[str, str]:
    """
    Tebak kunci dan plaintext jika panjang kunci diketahui.
    Kembalikan (key, plaintext).
    """
    columns = split_by_key_length(ciphertext, key_length)
    key = "".join(ALPHABET[best_shift_for_column(col)[0]] for col in columns)
    return key, vigenere_decrypt(ciphertext, key)


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

def demo_basic() -> None:
    print("== Enkripsi dan dekripsi dasar ==")
    plaintext = "KRIPTOGRAFI ADALAH SENI MENJAGA RAHASIA"
    key = "KUNCI"
    cipher = vigenere_encrypt(plaintext, key)
    print(f"plaintext : {plaintext}")
    print(f"key       : {key}")
    print(f"ciphertext: {cipher}")
    print(f"kembali   : {vigenere_decrypt(cipher, key)}")
    print()


def demo_kasiski() -> None:
    print("== Kasiski Examination ==")
    plaintext = (
        "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG. "
        "THE QUICK BROWN FOX JUMPS AGAIN OVER THE LAZY DOG. "
        "A QUICK BROWN FOX IS STILL A BROWN FOX AND THE LAZY DOG SLEEPS."
    )
    cipher = vigenere_encrypt(plaintext, "LEMON")
    repeats = kasiski_repeats(cipher)
    print(f"substring berulang ditemukan: {len(repeats)}")
    for sub, pos in list(repeats.items())[:5]:
        print(f"  '{sub}' pada posisi {pos}")
    print(f"jarak: {kasiski_distances(cipher)[:12]}")
    print("tebakan panjang kunci:", guess_key_length(cipher)[:5])
    print()


def demo_ic() -> None:
    print("== Index of Coincidence ==")
    plaintext = (
        "CRYPTOGRAPHY IS THE PRACTICE AND STUDY OF TECHNIQUES FOR SECURE "
        "COMMUNICATION IN THE PRESENCE OF ADVERSARIAL BEHAVIOR. IT IS USED "
        "TO PROTECT INFORMATION AND TO PROVIDE CONFIDENTIALITY AND INTEGRITY."
    )
    cipher = vigenere_encrypt(plaintext, "SECRET")
    print(f"IC ciphertext           : {index_of_coincidence(cipher):.4f}")
    print(f"IC rata-rata panjang 6  : {average_ic_for_length(cipher, 6):.4f}")
    print(f"IC rata-rata panjang 7  : {average_ic_for_length(cipher, 7):.4f}")
    print(f"IC rata-rata panjang 5  : {average_ic_for_length(cipher, 5):.4f}")
    print()


def demo_break() -> None:
    print("== Kriptanalisis penuh ==")
    plaintext = (
        "SETIAP SISTEM KRIPTOGRAFI YANG BAIK HARUS MENGASUMSIKAN BAHWA "
        "PENYERANG MENGETAHUI ALGORITMA DAN HANYA KUNCI YANG RAHASIA. "
        "PRINSIP INI DIKENAL SEBAGAI KERCHOFFS PRINCIPLE DAN TETAP RELEVAN."
    )
    cipher = vigenere_encrypt(plaintext, "RAHASIA")
    print(f"panjang kunci sebenarnya: {len('RAHASIA')}")
    print("kandidat panjang kunci (Kasiski):", guess_key_length(cipher)[:5])
    for length in (6, 7, 8):
        key, plain = break_vigenere(cipher, length)
        print(f"  panjang {length} -> kunci '{key}'")
        print(f"    {plain[:70]}...")
    print()


def self_test() -> None:
    assert vigenere_encrypt("ATTACKATDAWN", "LEMON") == "LXFOPVEFRNHR"
    assert vigenere_decrypt("LXFOPVEFRNHR", "LEMON") == "ATTACKATDAWN"
    assert vigenere_encrypt("abc", "KEY") == "kfa"
    assert index_of_coincidence("AAAA") == 1.0
    print("Self test lulus.\n")


if __name__ == "__main__":
    self_test()
    demo_basic()
    demo_kasiski()
    demo_ic()
    demo_break()

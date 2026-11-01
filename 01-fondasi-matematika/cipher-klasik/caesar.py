"""
caesar.py
Implementasi Caesar Cipher plus analisis frekuensi dan brute force.

Caesar Cipher menggeser setiap huruf sejauh k posisi dalam alfabet.
Secara matematis: C = (P + k) mod 26, dan P = (C - k) mod 26.

Jalankan:
    python caesar.py
"""

from __future__ import annotations

import string

ALPHABET = string.ascii_uppercase


# ---------------------------------------------------------------------------
# Enkripsi dan dekripsi
# ---------------------------------------------------------------------------

def caesar_encrypt(plaintext: str, shift: int) -> str:
    """
    Enkripsi Caesar dengan mempertahankan huruf besar, kecil, dan non-huruf.
    shift boleh negatif atau lebih besar dari 26.
    """
    shift %= 26
    out = []
    for ch in plaintext:
        if ch.isupper():
            out.append(ALPHABET[(ALPHABET.index(ch) + shift) % 26])
        elif ch.islower():
            out.append(ALPHABET[(ALPHABET.index(ch.upper()) + shift) % 26].lower())
        else:
            out.append(ch)
    return "".join(out)


def caesar_decrypt(ciphertext: str, shift: int) -> str:
    """Dekripsi = enkripsi dengan pergeseran negatif."""
    return caesar_encrypt(ciphertext, -shift)


# ---------------------------------------------------------------------------
# Kriptanalisis
# ---------------------------------------------------------------------------

# Frekuensi huruf bahasa Inggris dalam persen (A sampai Z).
ENGLISH_FREQ = {
    "A": 8.167, "B": 1.492, "C": 2.782, "D": 4.253, "E": 12.702,
    "F": 2.228, "G": 2.015, "H": 6.094, "I": 6.966, "J": 0.153,
    "K": 0.772, "L": 4.025, "M": 2.406, "N": 6.749, "O": 7.507,
    "P": 1.929, "Q": 0.095, "R": 5.987, "S": 6.327, "T": 9.056,
    "U": 2.758, "V": 0.978, "W": 2.360, "X": 0.150, "Y": 1.974,
    "Z": 0.074,
}

# Frekuensi huruf bahasa Indonesia, untuk perbandingan.
INDONESIAN_FREQ = {
    "A": 19.8, "B": 2.5, "C": 0.8, "D": 3.3, "E": 8.1, "F": 0.4,
    "G": 2.4, "H": 1.8, "I": 6.5, "J": 0.5, "K": 4.3, "L": 3.2,
    "M": 2.4, "N": 8.5, "O": 1.6, "P": 2.6, "Q": 0.1, "R": 5.2,
    "S": 3.6, "T": 4.5, "U": 1.7, "V": 0.2, "W": 0.1, "X": 0.1,
    "Y": 1.1, "Z": 0.1,
}


def letter_frequency(text: str) -> dict[str, float]:
    """Hitung persentase kemunculan setiap huruf A-Z."""
    text = "".join(c for c in text.upper() if c.isalpha())
    total = len(text)
    if total == 0:
        return {letter: 0.0 for letter in ALPHABET}
    counts = {letter: 0 for letter in ALPHABET}
    for ch in text:
        counts[ch] += 1
    return {letter: counts[letter] / total * 100 for letter in ALPHABET}


def chi_squared(text: str, reference: dict[str, float]) -> float:
    """
    Ukur seberapa cocok distribusi huruf text dengan distribusi referensi.
    Semakin kecil nilainya, semakin cocok.
    """
    freq = letter_frequency(text)
    n = sum(1 for c in text if c.isalpha())
    if n == 0:
        return float("inf")
    score = 0.0
    for letter in ALPHABET:
        expected = reference[letter] / 100 * n
        observed = freq[letter] / 100 * n
        if expected > 0:
            score += (observed - expected) ** 2 / expected
    return score


def break_caesar(ciphertext: str, reference: dict[str, float] | None = None) -> list[tuple[int, float, str]]:
    """
    Coba semua 26 kemungkinan pergeseran dan urutkan berdasarkan chi-squared.
    Kembalikan daftar (shift, skor, plaintext), terbaik di depan.
    """
    reference = reference or ENGLISH_FREQ
    candidates = []
    for shift in range(26):
        plain = caesar_decrypt(ciphertext, shift)
        candidates.append((shift, chi_squared(plain, reference), plain))
    return sorted(candidates, key=lambda item: item[1])


def brute_force(ciphertext: str) -> None:
    """Cetak semua kemungkinan plaintext untuk inspeksi manual."""
    for shift in range(26):
        print(f"shift {shift:>2}: {caesar_decrypt(ciphertext, shift)}")


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

def demo_basic() -> None:
    print("== Enkripsi dan dekripsi dasar ==")
    plaintext = "Serang fajar, bawa bekal!"
    shift = 3
    cipher = caesar_encrypt(plaintext, shift)
    print(f"plaintext : {plaintext}")
    print(f"ciphertext: {cipher}")
    print(f"kembali   : {caesar_decrypt(cipher, shift)}")
    print()


def demo_frequency() -> None:
    print("== Analisis frekuensi ==")
    # Kutipan panjang berbahasa Inggris sebagai contoh.
    plaintext = (
        "The science of cryptography is the study of techniques for secure "
        "communication in the presence of adversaries. Modern cryptography "
        "relies on mathematics, computer science, and electrical engineering."
    )
    cipher = caesar_encrypt(plaintext, 7)
    freq = letter_frequency(cipher)
    top = sorted(freq.items(), key=lambda kv: kv[1], reverse=True)[:5]
    print("Ciphertext terenkripsi dengan shift 7")
    print("Lima huruf teratas:", ", ".join(f"{k}={v:.2f}%" for k, v in top))
    print()


def demo_break() -> None:
    print("== Kriptanalisis otomatis ==")
    plaintext = (
        "Cryptography is essential for protecting data in transit and at rest. "
        "Every secure connection you make today depends on it."
    )
    for true_shift in (3, 11, 25):
        cipher = caesar_encrypt(plaintext, true_shift)
        ranking = break_caesar(cipher)
        best_shift, score, best_plain = ranking[0]
        status = "BENAR" if best_shift == true_shift else "SALAH"
        print(f"shift asli {true_shift:>2}, tebakan {best_shift:>2} ({status}), chi2={score:.2f}")
        print(f"  hasil: {best_plain[:60]}...")
    print()


def self_test() -> None:
    assert caesar_encrypt("ABC", 3) == "DEF"
    assert caesar_encrypt("xyz", 3) == "abc"
    assert caesar_decrypt("DEF", 3) == "ABC"
    assert caesar_encrypt("Halo!", 0) == "Halo!"
    assert caesar_encrypt("Halo!", 26) == "Halo!"
    assert caesar_decrypt(caesar_encrypt("Kriptografi", 19), 19) == "Kriptografi"
    print("Self test lulus.\n")


if __name__ == "__main__":
    self_test()
    demo_basic()
    demo_frequency()
    demo_break()
    brute_force(caesar_encrypt("Halo dunia", 4))

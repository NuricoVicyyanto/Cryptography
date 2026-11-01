"""
aes.py
Implementasi AES dari nol (AES-128, AES-192, AES-256) plus mode CBC dan CTR,
lalu perbandingan dengan PyCryptodome jika library tersebut tersedia.

Tujuan file ini adalah pembelajaran. Untuk produksi gunakan library teruji
seperti PyCryptodome, cryptography, atau libsodium. Implementasi manual rawan
terhadap serangan side channel karena tidak constant time.

Referensi: FIPS-197 (Advanced Encryption Standard).

Jalankan:
    python aes.py
"""

from __future__ import annotations

import os
import struct

# ---------------------------------------------------------------------------
# Pembangkitan S-box dari definisi matematis
# ---------------------------------------------------------------------------
# S-box AES bukan tabel acak. Nilainya adalah invers multiplikatif di GF(2^8)
# yang dikenai transformasi affine. Membangkitkannya lebih aman daripada
# menulis 256 angka manual yang rawan salah ketik.

def gmul(a: int, b: int) -> int:
    """Perkalian di GF(2^8) dengan polinomial 0x11B."""
    p = 0
    for _ in range(8):
        if b & 1:
            p ^= a
        hi = a & 0x80
        a = (a << 1) & 0xFF
        if hi:
            a ^= 0x1B
        b >>= 1
    return p


def ginv(a: int) -> int:
    """Invers multiplikatif di GF(2^8), dengan 0 dipetakan ke 0."""
    if a == 0:
        return 0
    return gpow(a, 254)


def gpow(a: int, n: int) -> int:
    result = 1
    while n:
        if n & 1:
            result = gmul(result, a)
        a = gmul(a, a)
        n >>= 1
    return result


def _rotl8(x: int, shift: int) -> int:
    return ((x << shift) | (x >> (8 - shift))) & 0xFF


def _build_sbox() -> tuple[list[int], list[int]]:
    sbox = [0] * 256
    inv_sbox = [0] * 256
    for i in range(256):
        x = ginv(i)
        s = (x ^ _rotl8(x, 1) ^ _rotl8(x, 2) ^ _rotl8(x, 3) ^ _rotl8(x, 4) ^ 0x63) & 0xFF
        sbox[i] = s
        inv_sbox[s] = i
    return sbox, inv_sbox


SBOX, INV_SBOX = _build_sbox()

RCON = [0x00, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1B, 0x36,
        0x6C, 0xD8, 0xAB, 0x4D]


# ---------------------------------------------------------------------------
# Inti AES
# ---------------------------------------------------------------------------

class AES:
    """
    AES block cipher murni. Panjang blok selalu 128 bit (16 byte).
    Panjang kunci 16, 24, atau 32 byte.
    """

    def __init__(self, key: bytes):
        if len(key) not in (16, 24, 32):
            raise ValueError("panjang kunci harus 16, 24, atau 32 byte")
        self.key = key
        self.nk = len(key) // 4          # jumlah word 32 bit pada kunci
        self.nr = self.nk + 6            # jumlah round: 10, 12, 14
        self.round_keys = self._expand_key(key)

    # -- key expansion ------------------------------------------------------

    @staticmethod
    def _sub_word(word: list[int]) -> list[int]:
        return [SBOX[b] for b in word]

    @staticmethod
    def _rot_word(word: list[int]) -> list[int]:
        return word[1:] + word[:1]

    def _expand_key(self, key: bytes) -> list[list[int]]:
        words: list[list[int]] = [list(key[4 * i:4 * i + 4]) for i in range(self.nk)]
        total = 4 * (self.nr + 1)
        for i in range(self.nk, total):
            temp = words[i - 1][:]
            if i % self.nk == 0:
                temp = self._sub_word(self._rot_word(temp))
                temp[0] ^= RCON[i // self.nk]
            elif self.nk > 6 and i % self.nk == 4:
                temp = self._sub_word(temp)
            words.append([words[i - self.nk][j] ^ temp[j] for j in range(4)])

        round_keys = []
        for r in range(self.nr + 1):
            block = []
            for w in words[4 * r:4 * r + 4]:
                block.extend(w)
            round_keys.append(block)
        return round_keys

    # -- transformasi round -------------------------------------------------

    @staticmethod
    def _add_round_key(state: list[int], rk: list[int]) -> list[int]:
        return [s ^ k for s, k in zip(state, rk)]

    @staticmethod
    def _sub_bytes(state: list[int]) -> list[int]:
        return [SBOX[b] for b in state]

    @staticmethod
    def _inv_sub_bytes(state: list[int]) -> list[int]:
        return [INV_SBOX[b] for b in state]

    @staticmethod
    def _shift_rows(state: list[int]) -> list[int]:
        out = [0] * 16
        for c in range(4):
            for r in range(4):
                out[4 * c + r] = state[4 * ((c + r) % 4) + r]
        return out

    @staticmethod
    def _inv_shift_rows(state: list[int]) -> list[int]:
        out = [0] * 16
        for c in range(4):
            for r in range(4):
                out[4 * c + r] = state[4 * ((c - r) % 4) + r]
        return out

    @staticmethod
    def _mix_columns(state: list[int]) -> list[int]:
        out = [0] * 16
        for c in range(4):
            a0, a1, a2, a3 = state[4 * c:4 * c + 4]
            out[4 * c + 0] = gmul(a0, 2) ^ gmul(a1, 3) ^ a2 ^ a3
            out[4 * c + 1] = a0 ^ gmul(a1, 2) ^ gmul(a2, 3) ^ a3
            out[4 * c + 2] = a0 ^ a1 ^ gmul(a2, 2) ^ gmul(a3, 3)
            out[4 * c + 3] = gmul(a0, 3) ^ a1 ^ a2 ^ gmul(a3, 2)
        return out

    @staticmethod
    def _inv_mix_columns(state: list[int]) -> list[int]:
        out = [0] * 16
        for c in range(4):
            a0, a1, a2, a3 = state[4 * c:4 * c + 4]
            out[4 * c + 0] = gmul(a0, 14) ^ gmul(a1, 11) ^ gmul(a2, 13) ^ gmul(a3, 9)
            out[4 * c + 1] = gmul(a0, 9) ^ gmul(a1, 14) ^ gmul(a2, 11) ^ gmul(a3, 13)
            out[4 * c + 2] = gmul(a0, 13) ^ gmul(a1, 9) ^ gmul(a2, 14) ^ gmul(a3, 11)
            out[4 * c + 3] = gmul(a0, 11) ^ gmul(a1, 13) ^ gmul(a2, 9) ^ gmul(a3, 14)
        return out

    # -- API publik ---------------------------------------------------------

    def encrypt_block(self, block: bytes) -> bytes:
        if len(block) != 16:
            raise ValueError("blok harus 16 byte")
        state = list(block)
        state = self._add_round_key(state, self.round_keys[0])
        for rnd in range(1, self.nr):
            state = self._sub_bytes(state)
            state = self._shift_rows(state)
            state = self._mix_columns(state)
            state = self._add_round_key(state, self.round_keys[rnd])
        state = self._sub_bytes(state)
        state = self._shift_rows(state)
        state = self._add_round_key(state, self.round_keys[self.nr])
        return bytes(state)

    def decrypt_block(self, block: bytes) -> bytes:
        if len(block) != 16:
            raise ValueError("blok harus 16 byte")
        state = list(block)
        state = self._add_round_key(state, self.round_keys[self.nr])
        for rnd in range(self.nr - 1, 0, -1):
            state = self._inv_shift_rows(state)
            state = self._inv_sub_bytes(state)
            state = self._add_round_key(state, self.round_keys[rnd])
            state = self._inv_mix_columns(state)
        state = self._inv_shift_rows(state)
        state = self._inv_sub_bytes(state)
        state = self._add_round_key(state, self.round_keys[0])
        return bytes(state)


# ---------------------------------------------------------------------------
# Padding dan mode operasi
# ---------------------------------------------------------------------------

def pkcs7_pad(data: bytes, block_size: int = 16) -> bytes:
    if not 1 <= block_size <= 255:
        raise ValueError("block_size harus 1 sampai 255")
    pad_len = block_size - (len(data) % block_size)
    return data + bytes([pad_len]) * pad_len


def pkcs7_unpad(data: bytes) -> bytes:
    if not data:
        raise ValueError("data kosong")
    pad_len = data[-1]
    if pad_len == 0 or pad_len > len(data):
        raise ValueError("padding tidak valid")
    if data[-pad_len:] != bytes([pad_len]) * pad_len:
        raise ValueError("padding tidak konsisten")
    return data[:-pad_len]


def cbc_encrypt(key: bytes, iv: bytes, plaintext: bytes) -> bytes:
    if len(iv) != 16:
        raise ValueError("IV harus 16 byte")
    cipher = AES(key)
    data = pkcs7_pad(plaintext)
    prev = iv
    out = []
    for i in range(0, len(data), 16):
        block = bytes(a ^ b for a, b in zip(data[i:i + 16], prev))
        prev = cipher.encrypt_block(block)
        out.append(prev)
    return b"".join(out)


def cbc_decrypt(key: bytes, iv: bytes, ciphertext: bytes) -> bytes:
    if len(ciphertext) % 16 != 0:
        raise ValueError("ciphertext harus kelipatan 16")
    cipher = AES(key)
    prev = iv
    out = []
    for i in range(0, len(ciphertext), 16):
        block = ciphertext[i:i + 16]
        plain = bytes(a ^ b for a, b in zip(cipher.decrypt_block(block), prev))
        out.append(plain)
        prev = block
    return pkcs7_unpad(b"".join(out))


def ctr_keystream(key: bytes, nonce: bytes, length: int) -> bytes:
    """Bangkitkan keystream AES-CTR dengan penghitung 64 bit big endian."""
    if len(nonce) != 8:
        raise ValueError("nonce harus 8 byte untuk mode demo ini")
    cipher = AES(key)
    out = bytearray()
    counter = 0
    while len(out) < length:
        block = nonce + struct.pack(">Q", counter)
        out.extend(cipher.encrypt_block(block))
        counter += 1
        if counter >= 2**64:
            raise OverflowError("counter habis, ganti kunci")
    return bytes(out[:length])


def ctr_xor(key: bytes, nonce: bytes, data: bytes) -> bytes:
    ks = ctr_keystream(key, nonce, len(data))
    return bytes(a ^ b for a, b in zip(data, ks))


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

def demo_sbox() -> None:
    print("== S-box hasil pembangkitan ==")
    print("SBOX[0x00] =", hex(SBOX[0x00]), "(seharusnya 0x63)")
    print("SBOX[0x53] =", hex(SBOX[0x53]), "(seharusnya 0xed)")
    print("INV_SBOX[0xed] =", hex(INV_SBOX[0xed]), "(seharusnya 0x53)")
    assert SBOX[0x00] == 0x63 and SBOX[0x53] == 0xED
    print()


def demo_vectors() -> None:
    print("== Uji vektor FIPS-197 ==")
    pt = bytes.fromhex("00112233445566778899aabbccddeeff")

    key128 = bytes.fromhex("000102030405060708090a0b0c0d0e0f")
    ct128 = AES(key128).encrypt_block(pt)
    print("AES-128:", ct128.hex())
    print("  expected: 69c4e0d86a7b0430d8cdb78070b4c55a")
    assert ct128.hex() == "69c4e0d86a7b0430d8cdb78070b4c55a"

    key192 = bytes.fromhex("000102030405060708090a0b0c0d0e0f1011121314151617")
    ct192 = AES(key192).encrypt_block(pt)
    print("AES-192:", ct192.hex())
    print("  expected: dda97ca4864cdfe06eaf70a0ec0d7191")
    assert ct192.hex() == "dda97ca4864cdfe06eaf70a0ec0d7191"

    key256 = bytes.fromhex("000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f")
    ct256 = AES(key256).encrypt_block(pt)
    print("AES-256:", ct256.hex())
    print("  expected: 8ea2b7ca516745bfeafc49904b496089")
    assert ct256.hex() == "8ea2b7ca516745bfeafc49904b496089"

    assert AES(key128).decrypt_block(ct128) == pt
    assert AES(key192).decrypt_block(ct192) == pt
    assert AES(key256).decrypt_block(ct256) == pt
    print("dekripsi mengembalikan plaintext: OK")
    print()


def demo_modes() -> None:
    print("== Mode CBC dan CTR ==")
    key = bytes.fromhex("2b7e151628aed2a6abf7158809cf4f3c")
    iv = bytes.fromhex("000102030405060708090a0b0c0d0e0f")
    plaintext = b"Serang fajar saat bugle berbunyi. Ini pesan rahasia."

    ct = cbc_encrypt(key, iv, plaintext)
    print("CBC ciphertext:", ct.hex())
    print("CBC kembali   :", cbc_decrypt(key, iv, ct))

    nonce = bytes(8)
    ct_ctr = ctr_xor(key, nonce, plaintext)
    print("CTR ciphertext:", ct_ctr.hex())
    print("CTR kembali   :", ctr_xor(key, nonce, ct_ctr))

    # Sifat CTR: enkripsi dan dekripsi adalah operasi yang sama.
    assert ctr_xor(key, nonce, ct_ctr) == plaintext
    print()


def demo_avalanche() -> None:
    print("== Efek avalanche ==")
    key = bytes(16)
    a = AES(key).encrypt_block(bytes(16))
    b = AES(key).encrypt_block(bytes([1]) + bytes(15))
    diff = sum(bin(x ^ y).count("1") for x, y in zip(a, b))
    print(f"bit berubah dari 1 bit input: {diff} dari 128 ({diff / 128 * 100:.1f}%)")
    print("ideal sekitar 50%, menunjukkan diffusion yang baik")
    print()


def demo_pycryptodome() -> None:
    print("== Perbandingan dengan PyCryptodome ==")
    try:
        from Crypto.Cipher import AES as RefAES
    except ImportError:
        print("PyCryptodome tidak terpasang. Jalankan: pip install pycryptodome")
        print("Bagian ini dilewati.")
        print()
        return

    key = os.urandom(16)
    pt = bytes.fromhex("00112233445566778899aabbccddeeff")
    ours = AES(key).encrypt_block(pt)
    theirs = RefAES.new(key, RefAES.MODE_ECB).encrypt(pt)
    print("hasil manual :", ours.hex())
    print("pycryptodome :", theirs.hex())
    print("cocok        :", ours == theirs)
    print()


if __name__ == "__main__":
    demo_sbox()
    demo_vectors()
    demo_modes()
    demo_avalanche()
    demo_pycryptodome()

"""Relocate the shipped arm64 engine's fixed batch arrays without changing its algorithms.

All Constants modes contain at most 81 cells. The original 16 matrix/light slots
overlap adjacent fields or the next heap allocation when a 20-cell page is drawn.
Only array writers and uniform readers change. The small companion allocator
expands the three batch owners; ordinary nodes retain their original allocation.
"""
import argparse
import hashlib
from pathlib import Path
import struct

ORIGINAL_SHA256 = '6474e74f9bfcc01fc651185052e15df5d6d17b79f83d9a8c7879b5c4f09846e7'
CAPACITY = 81
NODE_SIZE = 0x2040
MATRIX_OFFSET = 0xc00
LIGHT_OFFSET = 0x818


def add_immediate(word, value):
    assert value < 0x1000
    return (word & ~0x003ffc00) | value << 10


def mov_immediate(word, value):
    assert value < 0x10000
    return (word & ~0x001fffe0) | value << 5


# Verified virtual addresses equal file offsets in this exact ELF's executable segment.
PATCHES = {
    0x13490: (0x91042013, add_immediate(0x91042013, MATRIX_OFFSET)),
    0x135d0: (0x91042083, add_immediate(0x91042083, MATRIX_OFFSET)),
    # The writer adds an offset measured in floats, then writes at +8/+12/+16.
    0x134f8: (0x91075042, add_immediate(0x91075042, (LIGHT_OFFSET - 8) // 4)),
    0x13570: (0x911d6062, add_immediate(0x911d6062, LIGHT_OFFSET)),
}


def patch(data):
    original = bytearray(data)
    for offset, (before, after) in PATCHES.items():
        word, = struct.unpack_from('<I', original, offset)
        if word not in (before, after):
            raise ValueError('Unexpected instruction at 0x%x' % offset)
        struct.pack_into('<I', original, offset, before)
    if hashlib.sha256(original).hexdigest() != ORIGINAL_SHA256:
        raise ValueError('Unsupported library: untouched bytes differ from the verified original')
    result = bytearray(original)
    for offset, (_, after) in PATCHES.items():
        struct.pack_into('<I', result, offset, after)
    assert LIGHT_OFFSET + CAPACITY * 12 <= MATRIX_OFFSET
    assert MATRIX_OFFSET + CAPACITY * 64 <= NODE_SIZE
    return bytes(result)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument('--path', type=Path, default=Path(__file__).resolve().parents[1]
                        / 'launcher/lib/arm64-v8a/liblauncher_opt.so')
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    current = args.path.read_bytes()
    result = patch(current)
    if args.check:
        assert current == result, 'Library has not been patched'
    elif current != result:
        args.path.write_bytes(result)
    print('PASS NATIVE_BATCH_CAPACITY=%d sha256=%s' %
          (CAPACITY, hashlib.sha256(result).hexdigest()))

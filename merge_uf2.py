#!/usr/bin/env python3
"""
merge_uf2.py — properly combine two UF2 files into one.
Blocks from the second file override blocks from the first at the same address.
All block numbers and total counts are renumbered correctly.

Usage:
    python merge_uf2.py firmware.uf2 filesystem.uf2 combined.uf2
"""

import struct
import sys

MAGIC0 = 0x0A324655  # "UF2\n"
MAGIC1 = 0x9E5D5157
MAGIC_END = 0x0AB16F30

# UF2 block layout (512 bytes total):
#   0   magic0
#   4   magic1
#   8   flags
#  12   target_addr   ← flash address this block writes to
#  16   payload_size  ← bytes used in data (typically 256)
#  20   block_no      ← sequential index (we rewrite this)
#  24   num_blocks    ← total blocks in file (we rewrite this)
#  28   family_id
#  32   data[476]
# 508   magic_end

def read_blocks(path):
    """Read all valid UF2 blocks, keyed by target address."""
    blocks = {}
    with open(path, "rb") as f:
        while chunk := f.read(512):
            if len(chunk) < 512:
                break
            m0, m1 = struct.unpack_from("<II", chunk, 0)
            if m0 != MAGIC0 or m1 != MAGIC1:
                continue
            addr = struct.unpack_from("<I", chunk, 12)[0]
            blocks[addr] = bytearray(chunk)
    print(f"  {path}: {len(blocks)} blocks")
    return blocks

def write_uf2(blocks_dict, out_path):
    """Sort by address, renumber, and write."""
    blocks = sorted(blocks_dict.values(),
                    key=lambda b: struct.unpack_from("<I", b, 12)[0])
    total = len(blocks)
    with open(out_path, "wb") as f:
        for i, block in enumerate(blocks):
            struct.pack_into("<I", block, 20, i)      # block_no
            struct.pack_into("<I", block, 24, total)  # num_blocks
            f.write(bytes(block))
    print(f"  → {out_path}: {total} blocks written")

def main():
    if len(sys.argv) != 4:
        print("Usage: merge_uf2.py <firmware.uf2> <filesystem.uf2> <combined.uf2>")
        sys.exit(1)

    fw_path, fs_path, out_path = sys.argv[1], sys.argv[2], sys.argv[3]

    print("Reading:")
    fw_blocks = read_blocks(fw_path)
    fs_blocks = read_blocks(fs_path)

    # Filesystem blocks override firmware blocks at the same address
    combined = {**fw_blocks, **fs_blocks}
    overlap = len(fw_blocks) + len(fs_blocks) - len(combined)
    print(f"  Overlapping blocks replaced: {overlap}")

    print("Writing:")
    write_uf2(combined, out_path)

if __name__ == "__main__":
    main()

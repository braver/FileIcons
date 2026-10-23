#!/usr/bin/env python3
"""Compare two FileIcons output trees pixel by pixel.

Each argument is a directory that contains the theme icon folders, i.e.
`mono/icons/` and `color/icons/` (a repository checkout works as-is; a
`git archive` extraction of the committed icons works as the reference).

Slight per-pixel anti-aliasing differences are expected when the resvg
engine version changes; they are reported, not failed on. The comparison
fails (exit 1) when:

- a file is missing on either side, or
- the image dimensions differ, or
- more than --max-big-px pixels of a file differ by more than --max-delta.

Usage:
    python build/compare_icons.py OLD_DIR NEW_DIR [--max-delta 32] [--max-big-px 10]
"""

import argparse
import pathlib
import struct
import sys
import zlib

THEMES = ("mono", "color")


def png_rgba(data: bytes):
    """Decode an 8-bit RGBA, non-interlaced PNG to (width, height, bytes)."""
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("not a PNG")
    width, height = struct.unpack(">II", data[16:24])
    bit_depth, color_type = data[24], data[25]
    if bit_depth != 8 or color_type != 6:
        raise ValueError(f"expected 8-bit RGBA PNG, got depth={bit_depth} type={color_type}")
    if data[28] != 0:
        raise ValueError("interlaced PNG not supported")
    raw = b""
    pos = 8
    while pos < len(data):
        length = struct.unpack(">I", data[pos:pos + 4])[0]
        chunk_type = data[pos + 4:pos + 8]
        if chunk_type == b"IDAT":
            raw += data[pos + 8:pos + 8 + length]
        pos += 12 + length
    raw = zlib.decompress(raw)
    stride = 1 + width * 4
    if len(raw) != stride * height:
        raise ValueError("unexpected raw scanline data size")
    out = bytearray()
    prev = bytearray(width * 4)
    for y in range(height):
        pos = y * stride
        filt = raw[pos]
        line = bytearray(raw[pos + 1:pos + 1 + width * 4])
        if filt == 1:
            for x in range(4, width * 4):
                line[x] = (line[x] + line[x - 4]) & 0xFF
        elif filt == 2:
            for x in range(width * 4):
                line[x] = (line[x] + prev[x]) & 0xFF
        elif filt == 3:
            for x in range(width * 4):
                a = line[x - 4] if x >= 4 else 0
                line[x] = (line[x] + ((a + prev[x]) >> 1)) & 0xFF
        elif filt == 4:
            for x in range(width * 4):
                a = line[x - 4] if x >= 4 else 0
                b = prev[x]
                c = prev[x - 4] if x >= 4 else 0
                p = a + b - c
                pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
                pr = a if (pa <= pb and pa <= pc) else (b if pb <= pc else c)
                line[x] = (line[x] + pr) & 0xFF
        elif filt != 0:
            raise ValueError(f"unsupported PNG filter {filt}")
        out += line
        prev = line
    return width, height, bytes(out)


def compare_pair(old_path: pathlib.Path, new_path: pathlib.Path, max_delta: int, max_big_px: int):
    """Return (ok, pixel_identical, dim_mismatch, diff_px, big_px, max_seen)."""
    old_w, old_h, old_px = png_rgba(old_path.read_bytes())
    new_w, new_h, new_px = png_rgba(new_path.read_bytes())
    if (old_w, old_h) != (new_w, new_h):
        return False, False, True, 0, 0, 0
    if old_px == new_px:
        return True, True, False, 0, 0, 0
    diff_px = 0
    big_px = 0
    max_seen = 0
    for i in range(0, len(old_px), 4):
        d = 0
        for c in range(4):
            diff = abs(old_px[i + c] - new_px[i + c])
            if diff > d:
                d = diff
        if d:
            diff_px += 1
            if d > max_seen:
                max_seen = d
            if d > max_delta:
                big_px += 1
    return big_px <= max_big_px, False, False, diff_px, big_px, max_seen


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("old", type=pathlib.Path, help="reference tree (e.g. a git snapshot)")
    parser.add_argument("new", type=pathlib.Path, help="tree to check")
    parser.add_argument("--max-delta", type=int, default=32,
                        help="per-pixel max channel difference considered 'big' (default 32)")
    parser.add_argument("--max-big-px", type=int, default=10,
                        help="max allowed big-difference pixels per file (default 10)")
    args = parser.parse_args()

    compared = 0
    identical = 0
    dim_mismatches = 0
    big_px_total = 0
    failed = []
    worst = []

    for theme in THEMES:
        old_dir = args.old / theme / "icons"
        new_dir = args.new / theme / "icons"
        if not old_dir.is_dir() or not new_dir.is_dir():
            sys.exit(f"missing {theme}/icons in {args.old} or {args.new}")
        old_names = {p.name for p in old_dir.glob("*.png")}
        new_names = {p.name for p in new_dir.glob("*.png")}
        for missing in sorted(old_names - new_names):
            failed.append(f"{theme}: missing in new: {missing}")
        for missing in sorted(new_names - old_names):
            failed.append(f"{theme}: extra in new: {missing}")
        for name in sorted(old_names & new_names):
            compared += 1
            ok, pix_eq, dim_bad, diff_px, big_px, max_seen = compare_pair(
                old_dir / name, new_dir / name, args.max_delta, args.max_big_px)
            if pix_eq:
                identical += 1
                continue
            if dim_bad:
                dim_mismatches += 1
                failed.append(f"{theme}/{name}: dimensions changed")
                continue
            big_px_total += big_px
            worst.append((max_seen, big_px, diff_px, f"{theme}/{name}"))
            if not ok:
                failed.append(
                    f"{theme}/{name}: {big_px} pixels differ by more than {args.max_delta} "
                    f"(max allowed: {args.max_big_px})")

    worst.sort(reverse=True)
    print(f"files compared:   {compared}")
    print(f"pixel-identical:  {identical}")
    print(f"differing:        {compared - identical}")
    print(f"big px total:     {big_px_total} (delta > {args.max_delta}; "
          f">{args.max_big_px} px per file fails)")
    print(f"dim mismatches:   {dim_mismatches}")
    if worst:
        print("worst files (max-delta, big-px, diff-px, file):")
        for item in worst[:10]:
            print(f"  {item[0]:>4}  {item[1]:>5}  {item[2]:>7}  {item[3]}")
    if failed:
        print("FAILURES:")
        for item in failed:
            print(f"  {item}")
        sys.exit(1)
    print("OK: dimensions match and per-pixel differences are within tolerance")


if __name__ == "__main__":
    main()

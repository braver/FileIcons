#!/usr/bin/env python3

"""
Usage:
    .venv/bin/python build/generate_icons.py
"""

import json
import struct
import sys
import time
from pathlib import Path

import resvg_py

BUILD_DIR = Path(__file__).resolve().parent
ROOT_DIR = BUILD_DIR.parent
ASSETS_DIR = BUILD_DIR / "assets"

# Output sizes as (zoom, filename suffix). The assets carry an 18x16 viewport
# on disk; 18x16 is Sublime's default icon size.
SIZES = [(1, ""), (2, "@2x"), (3, "@3x")]


def build_theme(out_dir: Path, icons: dict, palette: dict | None) -> int:
    out_dir.mkdir(parents=True, exist_ok=True)

    built = 0
    for name, color_name in icons.items():
        full_icon_path = ASSETS_DIR / f"{name}.svg"
        if not full_icon_path.is_file():
            sys.exit(f"Failed to read icon file {full_icon_path} (missing)")
        svg = full_icon_path.read_text(encoding="utf-8")

        if palette:
            svg = svg.replace("#FFFFFF", palette[color_name])
        if 'preserveAspectRatio="xMinYMin meet"' not in svg:
            sys.exit(f"{full_icon_path.name} must have an 18x16 viewport with "
                     'preserveAspectRatio="xMinYMin meet" (see README)')

        for zoom, suffix in SIZES:
            full_output_path = out_dir / f"{name}{suffix}.png"

            print(f"Building {full_icon_path} to {full_output_path}")
            # Icons are just paths, so system fonts are never needed.
            png = resvg_py.svg_to_bytes(svg, zoom=zoom, skip_system_fonts=True)
            if struct.unpack('>II', png[16:24]) != (18 * zoom, 16 * zoom):
                sys.exit(f"{full_icon_path.name} does not render to an "
                         f"{18 * zoom}x{16 * zoom} canvas (check its viewport)")
            full_output_path.write_bytes(png)
            built += 1

    return built


def main() -> None:
    colors = json.loads((BUILD_DIR / "colors.json").read_text(encoding="utf-8"))
    icons = json.loads((BUILD_DIR / "icons.json").read_text(encoding="utf-8"))

    themes = [
        (ROOT_DIR / "mono" / "icons", None),
        (ROOT_DIR / "color" / "icons", colors),
    ]

    # if the Solarized package is present, also generate icons for it
    solarized = json.loads((BUILD_DIR / "solarized.json").read_text(encoding="utf-8"))
    solarized_pkg = ROOT_DIR.parent / "Solarized Color Scheme"
    if solarized_pkg.is_dir():
        themes.append((solarized_pkg / "icons", solarized))

    started = time.time()
    built = 0
    for out_dir, palette in themes:
        built += build_theme(out_dir, icons, palette)

    print(f"Built {built} icons in {time.time() - started:.1f}s")


if __name__ == "__main__":
    main()

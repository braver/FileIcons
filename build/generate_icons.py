#!/usr/bin/env python3

"""
Usage:
    .venv/bin/python build/generate_icons.py
"""

import json
import sys
import time
import xml.etree.ElementTree as ET
from pathlib import Path

import resvg_py

if sys.version_info < (3, 10):
    sys.exit("generate_icons.py requires Python 3.10 or newer (resvg_py wheels).")

BUILD_DIR = Path(__file__).resolve().parent
ROOT_DIR = BUILD_DIR.parent
ASSETS_DIR = BUILD_DIR / "assets"

# Namespace prefixes used by the svg assets; keep them stable when reserializing.
ET.register_namespace('', 'http://www.w3.org/2000/svg')
ET.register_namespace('xlink', 'http://www.w3.org/1999/xlink')
ET.register_namespace('serif', 'http://www.serif.com/')


def normalize_svg(svg: str, canvas_width: int, canvas_height: int) -> str:
    """Return the svg with an explicit canvas_width x canvas_height viewport.
    """
    try:
        root = ET.fromstring(svg)
    except ET.ParseError as e:
        sys.exit(f"invalid svg: {e}")
    root.set('width', str(canvas_width))
    root.set('height', str(canvas_height))
    root.set('preserveAspectRatio', 'xMinYMin meet')
    return ET.tostring(root, encoding='unicode')


def suffix_of(size_desc: dict) -> str:
    suffix = size_desc.get("suffix")
    return suffix if isinstance(suffix, str) else ""


def build_theme(colors: dict, icons: dict, sizes: list, theme: str, colorize: bool) -> int:
    theme_dir = ROOT_DIR / theme / "icons"
    theme_dir.mkdir(parents=True, exist_ok=True)

    built = 0
    for name, color_name in icons.items():
        full_icon_path = ASSETS_DIR / f"{name}.svg"
        if not full_icon_path.is_file():
            sys.exit(f"Failed to read icon file {full_icon_path} (missing)")
        svg = full_icon_path.read_text(encoding="utf-8")

        if colorize:
            svg = svg.replace("#FFFFFF", colors[color_name])

        for size_desc in sizes:
            canvas_w, canvas_h = size_desc["height"], size_desc["width"]
            full_output_path = theme_dir / f"{name}{suffix_of(size_desc)}.png"

            print(f"Building {full_icon_path} to {full_output_path}")
            full_output_path.write_bytes(
                # Icons are just paths, so system fonts are never needed.
                resvg_py.svg_to_bytes(normalize_svg(svg, canvas_w, canvas_h), skip_system_fonts=True))
            built += 1

    return built


def main() -> None:
    colors = json.loads((BUILD_DIR / "colors.json").read_text(encoding="utf-8"))
    icons = json.loads((BUILD_DIR / "icons.json").read_text(encoding="utf-8"))
    sizes = json.loads((BUILD_DIR / "sizes.json").read_text(encoding="utf-8"))

    started = time.time()
    built = build_theme(colors, icons, sizes, "mono", colorize=False)
    built += build_theme(colors, icons, sizes, "color", colorize=True)

    print(f"Built {built} icons in {time.time() - started:.1f}s")


if __name__ == "__main__":
    main()

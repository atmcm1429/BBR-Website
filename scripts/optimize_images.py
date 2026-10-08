#!/usr/bin/env python3
"""Build display images from the original files listed in image_sources.json.

Requires Pillow: python3 -m pip install Pillow
Run from any directory: python3 scripts/optimize_images.py
Original photographs, logos, and report screenshots are kept untouched.
"""

import json
import re
from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "assets" / "images"
PROFILES = {
    "portraits": ((640, 640), 84),
    "backgrounds": ((1600, 1000), 82),
    "reports": ((1100, 1440), 90),
    "logos": ((352, 96), 90),
}


def output_path(group, source):
    slug = re.sub(r"[^a-z0-9]+", "-", Path(source).stem.lower()).strip("-")
    return OUTPUT / group / f"{slug}.webp"


def main():
    sources = json.loads(Path(__file__).with_name("image_sources.json").read_text())
    original_bytes = 0
    optimized_bytes = 0
    outputs = set()

    for group, files in sources.items():
        max_size, quality = PROFILES[group]
        for source in files:
            destination = output_path(group, source)
            if destination in outputs:
                raise ValueError(f"Duplicate output name: {destination}")
            outputs.add(destination)
            destination.parent.mkdir(parents=True, exist_ok=True)
            source_path = ROOT / source

            with Image.open(source_path) as original:
                image = ImageOps.exif_transpose(original)
                has_alpha = "A" in image.getbands() or "transparency" in image.info
                image = image.convert("RGBA" if has_alpha else "RGB")
                if group == "portraits":
                    # Match the existing square, centered object-fit: cover cards.
                    edge = min(max_size[0], *image.size)
                    image = ImageOps.fit(image, (edge, edge), Image.Resampling.LANCZOS)
                else:
                    image.thumbnail(max_size, Image.Resampling.LANCZOS)
                image.save(destination, "WEBP", quality=quality, method=6)

            original_bytes += source_path.stat().st_size
            optimized_bytes += destination.stat().st_size

    # The browser only needs a small favicon, not the original full-size artwork.
    with Image.open(ROOT / "favicon.png") as original:
        icon = ImageOps.exif_transpose(original).convert("RGBA")
        icon.thumbnail((64, 64), Image.Resampling.LANCZOS)
        icon.save(OUTPUT / "favicon.png", optimize=True)

    print(
        f"Built {len(outputs)} WebP images: "
        f"{original_bytes / 1_000_000:.2f} MB -> {optimized_bytes / 1_000_000:.2f} MB "
        f"({100 * (1 - optimized_bytes / original_bytes):.1f}% smaller)."
    )


if __name__ == "__main__":
    main()

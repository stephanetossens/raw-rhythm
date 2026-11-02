"""Generate Raw Rhythm PWA icons (Raw Adventure palette: cream / leaf / clay).

Usage: python3 tools/make_icons.py
Writes icons/*.png. Requires Pillow.
"""
from PIL import Image, ImageDraw
import os

CREAM = (244, 240, 232, 255)   # --bg
LEAF = (74, 103, 65, 255)      # --leaf
LEAF_DEEP = (45, 69, 39, 255)  # --leaf-deep
CLAY = (184, 89, 58, 255)      # --clay
SS = 4  # supersampling factor

OUT = os.path.join(os.path.dirname(__file__), '..', 'icons')


def diamond(cx, cy, r):
    return [(cx, cy - r), (cx + r, cy), (cx, cy + r), (cx - r, cy)]


def render(size, *, bg, rounded, scale=1.0):
    """Draw mark on a size×size canvas. scale shrinks the mark (maskable safe zone)."""
    s = size * SS
    img = Image.new('RGBA', (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    if rounded:
        d.rounded_rectangle([0, 0, s - 1, s - 1], radius=int(s * 0.22), fill=bg)
    else:
        d.rectangle([0, 0, s - 1, s - 1], fill=bg)
    c = s / 2
    ring = s * 0.36 * scale
    d.ellipse([c - ring, c - ring, c + ring, c + ring], fill=LEAF)
    d.polygon(diamond(c, c, s * 0.21 * scale), fill=CLAY)
    d.polygon(diamond(c, c, s * 0.075 * scale), fill=CREAM)
    return img.resize((size, size), Image.LANCZOS)


def save(img, name):
    path = os.path.join(OUT, name)
    img.save(path, 'PNG', optimize=True)
    print('wrote', os.path.relpath(path), img.size)


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    save(render(192, bg=CREAM, rounded=True), 'icon-192.png')
    save(render(512, bg=CREAM, rounded=True), 'icon-512.png')
    # Maskable: full-bleed background, mark inside the 80% safe zone.
    save(render(512, bg=LEAF_DEEP, rounded=False, scale=0.78), 'icon-maskable-512.png')
    # iOS applies its own mask: opaque square, no rounding.
    save(render(180, bg=CREAM, rounded=False), 'apple-touch-icon.png')

"""
Удаляет непрозрачный чёрный фон у PNG: flood-fill от краёв по тёмным пикселям.
Требует: pip install pillow
"""
from __future__ import annotations

import sys
from collections import deque
from pathlib import Path

from PIL import Image


def remove_edge_connected_dark(
    path_in: Path,
    path_out: Path,
    *,
    threshold: int = 38,
) -> None:
    im = Image.open(path_in).convert("RGBA")
    pixels = im.load()
    w, h = im.size

    def is_dark(x: int, y: int) -> bool:
        r, g, b, _ = pixels[x, y]
        return r <= threshold and g <= threshold and b <= threshold

    visited: set[tuple[int, int]] = set()
    q: deque[tuple[int, int]] = deque()

    def try_add(x: int, y: int) -> None:
        if not (0 <= x < w and 0 <= y < h):
            return
        if (x, y) in visited:
            return
        if not is_dark(x, y):
            return
        visited.add((x, y))
        q.append((x, y))

    for x in range(w):
        try_add(x, 0)
        try_add(x, h - 1)
    for y in range(h):
        try_add(0, y)
        try_add(w - 1, y)

    while q:
        x, y = q.popleft()
        for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            try_add(nx, ny)

    for x, y in visited:
        r, g, b, _ = pixels[x, y]
        pixels[x, y] = (r, g, b, 0)

    path_out.parent.mkdir(parents=True, exist_ok=True)
    im.save(path_out, "PNG", optimize=True)


def main() -> None:
    args = sys.argv[1:]
    if len(args) < 2:
        print("Usage: remove_edge_black.py <input.png> <output.png> [threshold]", file=sys.stderr)
        sys.exit(1)
    path_in = Path(args[0])
    path_out = Path(args[1])
    threshold = int(args[2]) if len(args) > 2 else 38
    remove_edge_connected_dark(path_in, path_out, threshold=threshold)
    print(f"Wrote {path_out} (threshold={threshold})")


if __name__ == "__main__":
    main()

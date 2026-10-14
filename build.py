"""Build the marimo WASM site and derive the dist/ favicons from favicon.svg."""

import logging
import re
import subprocess
import xml.etree.ElementTree as ET
from io import BytesIO
from pathlib import Path

import resvg_py
from PIL import Image

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

ROOT = Path(__file__).parent
DIST = ROOT / "dist"
LOGO_SVG = ROOT / "favicon.svg"

SVG_NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG_NS)

PNG_ICONS = {
    "favicon-16x16.png": 16,
    "favicon-32x32.png": 32,
    "apple-touch-icon.png": 180,
    "android-chrome-192x192.png": 192,
    "android-chrome-512x512.png": 512,
}
ICO_SIZES = [16, 32, 48]


def export_wasm() -> None:
    """Export logoneef.py to a WASM site in dist/."""
    logger.info("Exporting marimo WASM site to %s", DIST)
    subprocess.run(
        [
            "uvx",
            "marimo",
            "export",
            "html-wasm",
            "logoneef.py",
            "-o",
            "dist",
            "--mode",
            "edit",
            "--execute",
            "--force",
            "--sandbox",
        ],
        cwd=ROOT,
        check=True,
    )


def favicon_svg() -> str:
    """Build the favicon SVG from favicon.svg.

    Strips the fixed width/height (keeping the viewBox) so the icon scales,
    removes the empty defs element, and rounds all numbers to two decimals.
    """
    root = ET.fromstring(LOGO_SVG.read_text(encoding="utf-8"))
    root.attrib.pop("width", None)
    root.attrib.pop("height", None)
    for defs in root.findall(f"{{{SVG_NS}}}defs"):
        if len(defs) == 0:
            root.remove(defs)
    svg = ET.tostring(root, encoding="unicode")
    return re.sub(
        r"-?\d+\.\d+",
        lambda m: f"{float(m.group()):.2f}".rstrip("0").rstrip("."),
        svg,
    )


def render_png(svg: str, size: int) -> bytes:
    """Render the favicon SVG as a PNG of size x size pixels."""
    return resvg_py.svg_to_bytes(svg_string=svg, width=size, height=size)


def write_icons(svg: str) -> None:
    """Replace marimo's default favicon files in dist/ with our own."""
    for name, size in PNG_ICONS.items():
        path = DIST / name
        path.write_bytes(render_png(svg, size))
        logger.info("Wrote %s (%dx%d)", path, size, size)

    image = Image.open(BytesIO(render_png(svg, max(ICO_SIZES))))
    image.save(
        DIST / "favicon.ico",
        format="ICO",
        sizes=[(size, size) for size in ICO_SIZES],
    )
    logger.info("Wrote %s (sizes %s)", DIST / "favicon.ico", ICO_SIZES)


def main() -> None:
    """Export the WASM site, then overwrite its favicon files."""
    svg = favicon_svg()
    export_wasm()
    write_icons(svg)


if __name__ == "__main__":
    main()

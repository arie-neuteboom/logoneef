# /// script
# requires-python = ">=3.14"
# dependencies = [
#     "fpdf2>=2.8.9",
#     "marimo>=0.23.3",
#     "svgwrite>=1.4",
# ]
# ///

import marimo

__generated_with = "0.25.1"
app = marimo.App(app_title="logoneef", css_file="logoneef.css")

with app.setup(hide_code=True):
    from dataclasses import dataclass
    from itertools import accumulate
    from math import cos, radians, sin

    import marimo as mo
    import svgwrite
    from fpdf import FPDF
    from fpdf.svg import SVGObject

    def push_arc(
        path: svgwrite.path.Path,
        cx: float,
        cy: float,
        r: float,
        start_deg: float,
        end_deg: float,
        cw: bool = True,
    ) -> None:
        """Move to the arc start and draw a circular arc onto ``path``.

        Angles rotate from the x-axis towards the positive y-axis, matching the
        circular-arc convention previously provided by ``drawsvg``.

        Args:
            path: The svgwrite path to append the arc to.
            cx: Center x-coordinate of the arc.
            cy: Center y-coordinate of the arc.
            r: Radius of the arc.
            start_deg: Start angle in degrees.
            end_deg: End angle in degrees.
            cw: Draw the sweep in the positive-angle direction.
        """
        large_arc = ((end_deg - start_deg) % 360 <= 180) ^ cw
        start_rad, end_rad = radians(start_deg), radians(end_deg)
        path.push("M", cx + r * cos(start_rad), cy + r * sin(start_rad))
        path.push_arc(
            target=(cx + r * cos(end_rad), cy + r * sin(end_rad)),
            rotation=0,
            r=r,
            large_arc=large_arc,
            angle_dir="+" if cw else "-",
            absolute=True,
        )


@app.cell(hide_code=True)
def _(logo):
    title = "# Welkom bij Logoneef"
    text = (
        "Hieronder staat een logoneef met twee knoppen om het logo als svg of "
        "als pdf bestand te downloaden. Het logo is aan te passen met de code "
        "die daar weer onderstaat. Pas de code en daarmee het logo gerust aan "
        "naar jouw wensen."
    )
    footer = (
        "Licentie: [PolyForm Noncommercial 1.0.0](LICENSE) · "
        "Broncode: [GitHub](https://github.com/arie-neuteboom/logoneef)"
    )

    _svg_str = logo.tostring()
    _svg_bytes = _svg_str.encode("utf-8")
    _pdf_bytes = svg_to_pdf(_svg_str, float(logo["width"]), float(logo["height"]))

    download_svg = mo.download(
        data=lambda: _svg_bytes,
        filename="logoneef.svg",
        mimetype="image/svg+xml",
        label="Download het logo als .svg",
    )
    download_pdf = mo.download(
        data=lambda: _pdf_bytes,
        filename="logoneef.pdf",
        mimetype="application/pdf",
        label="Download het logo als .pdf",
    )
    mo.vstack(
        [
            mo.md(title).center(),
            mo.md(text).center(),
            mo.Html(_svg_str).center(),
            download_svg,
            download_pdf,
            mo.md(footer).center(),
        ]
    ).center()
    return


@app.cell
def _():
    def create_logo() -> svgwrite.Drawing:
        # Standard screen DPI (96) divided by cm per inch (2.54) = pixels per cm
        cm = 96 / 2.54  # centimeter pixel ratio
        d_width = 7.2 * cm
        d_heigth = 5.0 * cm
        d = svgwrite.Drawing(size=(d_width, d_heigth))
        d.viewbox(-d_width / 2, -d_heigth / 2, d_width, d_heigth)
        d.add(
            d.rect(
                insert=(-d_width / 2, -d_heigth / 2),
                size=(d_width, d_heigth),
                fill="none",
            )
        )
        b = 0.4 * cm  # radius head
        q_small = 1.5  # head-body ratio small neefje
        q_big = 2  # head-body ratio big neefje
        r = b / 2.5
        r_l = r  # fillet left
        r_r = r  # fillet right
        h_big_neef = (3 + q_big) * b
        n = 5  # number of small neefjes

        kwargs_format = {
            "fill": "none",
            "stroke": "black",
            "stroke_width": 2.5,
        }
        kwargs_default = {
            "y": h_big_neef / 2,  # vertical center at half the height of big neefje
            "d": d,
            "b": b,
            "r_l": 0,
            "r_r": 0,
            **kwargs_format,
        }
        kw_list = (
            [{**kwargs_default, "q": q_big, "r_l": r_l}]
            + [{**kwargs_default, "q": q_small}] * n
            + [{**kwargs_default, "q": q_big, "r_r": r_r}]
        )

        b_incr = [kw_list[i - 1]["b"] + kw_list[i]["b"] for i in range(1, len(kw_list))]

        x_pos = list(accumulate(b_incr, initial=-sum(b_incr) / 2))

        for i, kw in enumerate(kw_list):
            append_neefje(**kw, x=x_pos[i])  # type: ignore

        # Add rounded border
        w_logo = 2 * sum(kw["b"] for kw in kw_list)
        w_border = 2 * b + w_logo
        h_border = 2 * b + h_big_neef
        d.add(
            d.rect(
                insert=(-w_border / 2, -h_border / 2),
                size=(w_border, h_border),
                rx=r,
                ry=r,
                **kwargs_format,
            )
        )
        # # Uncomment to display center lines
        # d.add(
        #     d.line(
        #         start=(-d_width / 2, 0), end=(d_width / 2, 0),
        #         stroke="red", stroke_dasharray="8,8",
        #     )
        # )
        # d.add(
        #     d.line(
        #         start=(0, -d_heigth / 2), end=(0, d_heigth / 2),
        #         stroke="red", stroke_dasharray="8,8",
        #     )
        # )

        # # Uncomment to display bounding box
        # d.add(
        #     d.rect(
        #         insert=(-d_width / 2, -d_heigth / 2),
        #         size=(d_width, d_heigth),
        #         fill="none",
        #         stroke="red",
        #     )
        # )

        return d

    logo = create_logo()
    return (logo,)


@app.class_definition
@dataclass
class Point:
    x: float
    y: float

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)


@app.function
def append_neefje(
    d: svgwrite.Drawing,
    b: float,
    q: float,
    r_l: float,
    r_r: float,
    x: float = 0,
    y: float = 0,
    **kwargs,
) -> None:
    """Append the neefje figure (head, shoulder, body) to the given drawing.

    Args:
        d: The drawing to append shapes to.
        b: Base unit length in pixels.
        q: Vertical offset multiplier for p_base.
        q_small: Vertical scale factor for the body height.
        r_l: Corner radius for the left-bottom arc.
        r_r: Corner radius for the right-bottom arc.
        x: Horizontal offset for p_base.
        y: Vertical offset for p_base.
        **kwargs: SVG style keyword arguments (fill, stroke, stroke_width, etc.).
    """
    # Coordinates
    p_base = Point(x, y)
    p_shoulder = p_base + Point(0, -q * b)
    p_head = p_shoulder + Point(0, -2 * b)

    p10 = p_base + Point(-b, 0)
    p11 = p10 + Point(r_l, 0)
    p12 = p10 + Point(r_l, -r_l)
    p13 = p10 + Point(0, -r_l)
    p14 = p_shoulder + Point(-b, 0)

    p20 = p_base + Point(b, 0)
    p21 = p20 + Point(-r_r, 0)
    p22 = p20 + Point(-r_r, -r_r)
    p23 = p20 + Point(0, -r_r)
    p24 = p_shoulder + Point(b, 0)
    # head
    d.add(d.circle(center=(p_head.x, p_head.y), r=b, **kwargs))
    # shoulder
    shoulder = d.path(**kwargs)
    push_arc(shoulder, p_shoulder.x, p_shoulder.y, b, 0, 180, cw=False)
    d.add(shoulder)
    # body
    body = d.path(**kwargs)
    body.push("M", p14.x, p14.y, "L", p13.x, p13.y)  # left line
    push_arc(body, p12.x, p12.y, r_l, 90, -180)
    body.push("M", p11.x, p11.y, "L", p21.x, p21.y)  # bottom line
    push_arc(body, p22.x, p22.y, r_r, 0, 90)
    body.push("M", p23.x, p23.y, "L", p24.x, p24.y)  # right line
    d.add(body)


@app.function(hide_code=True)
def svg_to_pdf(svg_str: str, width: float, height: float) -> bytes:
    """Convert an SVG string to PDF bytes using fpdf2.

    The SVG is embedded as vector paths, so the same code path serves both
    CPython and the Pyodide/WASM deployment. Width and height are CSS
    pixels (96 dpi) and are converted to PDF points (72 dpi) so the page
    has the same physical size as the on-screen logo. fpdf2 reads unitless
    SVG sizes as points, so the top-level width/height are ignored and the
    viewBox is scaled to the full page instead. fpdf2 only supports a
    subset of SVG (no text, markers, patterns, filters, masks);
    unsupported features are logged as warnings by the ``fpdf.svg`` logger.
    """
    pdf = FPDF(unit="pt", format=(width * 72 / 96, height * 72 / 96))
    pdf.add_page()
    _, _, paths = SVGObject(svg_str).transform_to_rect_viewport(
        pdf.k, pdf.w, pdf.h, ignore_svg_top_attrs=True
    )
    pdf.draw_path(paths)
    return bytes(pdf.output())


if __name__ == "__main__":
    app.run()

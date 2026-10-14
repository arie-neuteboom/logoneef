import marimo

__generated_with = "0.23.9"
app = marimo.App(css_file="logoneef.css")

with app.setup(hide_code=True):
    from dataclasses import dataclass
    from html import escape as html_escape
    from itertools import accumulate
    from pathlib import Path

    import drawsvg as draw
    import marimo as mo


@app.cell(hide_code=True)
def _(iframe_button, logo):
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

    download_svg = iframe_button(
        logo=logo,
        label="Download logo as svg",
        action="Svg",
    )
    download_pdf = iframe_button(
        logo=logo,
        label="Download logo as pdf",
        action="Pdf",
        extra_data=f' data-width="{logo.width}" data-height="{logo.height}"',
        scripts=(
            '<script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>\n'
            '<script src="https://unpkg.com/svg2pdf.js@2.2.3/dist/svg2pdf.umd.min.js"></script>'
        ),
    )
    mo.vstack(
        [
            mo.md(title).center(),
            mo.md(text).center(),
            mo.Html(logo.as_svg()).center(),
            download_svg,
            download_pdf,
            mo.md(footer).center(),
        ]
    ).center()
    return


@app.cell
def _(append_neefje):
    # Standard screen DPI (96) divided by cm per inch (2.54) = pixels per cm
    cm = 96 / 2.54  # centimeter pixel ratio

    def create_logo() -> draw.Drawing:
        d_width = 7.2 * cm
        d_heigth = 5.0 * cm
        d = draw.Drawing(width=d_width, height=d_heigth, origin="center")
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
        print(len(x_pos))

        for i, kw in enumerate(kw_list):
            append_neefje(**kw, x=x_pos[i])  # type: ignore

        # Add rounded border
        w_logo = 2 * sum(kw["b"] for kw in kw_list)
        w_border = 2 * b + w_logo
        h_border = 2 * b + h_big_neef
        d.append(
            draw.Rectangle(
                x=-w_border / 2,
                y=-h_border / 2,
                width=w_border,
                height=h_border,
                rx=r,
                ry=r,
                **kwargs_format,
            )
        )
        # # Uncomment to display center lines
        # d.append(
        #     draw.Line(
        #         -d_width / 2, 0, d_width / 2, 0,
        #         stroke="red", stroke_dasharray="8,8",
        #     )
        # )
        # d.append(
        #     draw.Line(
        #         0, -d_heigth / 2, 0, d_heigth / 2,
        #         stroke="red", stroke_dasharray="8,8",
        #     )
        # )

        # # Uncomment to display bounding box
        # d.append(
        #     draw.Rectangle(
        #         x=-d_width / 2,
        #         y=-d_heigth / 2,
        #         width=d_width,
        #         height=d_heigth,
        #         fill="none",
        #         stroke="red",
        #     )
        # )

        return d

    logo = create_logo()
    return (logo,)


@app.cell
def _():
    @dataclass
    class Point:
        x: float
        y: float

        def __add__(self, other):
            return Point(self.x + other.x, self.y + other.y)

        def __sub__(self, other):
            return Point(self.x - other.x, self.y - other.y)

    def append_neefje(
        d: draw.Drawing,
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
        d.append(draw.Circle(cx=p_head.x, cy=p_head.y, r=b, **kwargs))
        # shoulder
        d.append(
            draw.Arc(
                cx=p_shoulder.x,
                cy=p_shoulder.y,
                r=b,
                start_deg=0,
                end_deg=180,
                **kwargs,
            )
        )
        # body
        p = draw.Path(**kwargs)
        p.M(x=p14.x, y=p14.y)
        p.L(x=p13.x, y=p13.y)  # left line
        p.arc(cx=p12.x, cy=p12.y, r=r_l, start_deg=90, end_deg=-180)
        p.M(x=p11.x, y=p11.y)
        p.L(x=p21.x, y=p21.y)  # bottom line
        p.arc(cx=p22.x, cy=p22.y, r=r_r, start_deg=0, end_deg=90)
        p.M(x=p23.x, y=p23.y)
        p.L(x=p24.x, y=p24.y)  # right line
        # p.M(x=p8.x, y=p8.y)
        d.append(p)

    return (append_neefje,)


@app.cell(hide_code=True)
def _():
    _this_dir = Path(__file__).parent
    _css = (_this_dir / "download.css").read_text(encoding="utf-8")
    _js = (_this_dir / "download.js").read_text(encoding="utf-8")
    _icon = (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" '
        'fill="none" stroke="currentColor" stroke-width="2" '
        'stroke-linecap="round" stroke-linejoin="round">'
        '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>'
        '<polyline points="7 10 12 15 17 10"/>'
        '<line x1="12" y1="15" x2="12" y2="3"/></svg>'
    )
    _body_style = (
        "margin: 0; display: flex; "
        "align-items: center; justify-content: center; height: 100vh;"
    )

    def iframe_button(
        logo: draw.Drawing,
        label: str,
        action: str,
        extra_data: str = "",
        scripts: str = "",
    ) -> object:
        """Return an iframe containing a single download button."""
        _svg = html_escape(logo.as_svg())
        return mo.iframe(
            f"""
    <body style="{_body_style}">
    <style>{_css}</style>
    <button class="download-btn" type="button" onclick="download{action}(this)"
      data-svg="{_svg}"
      data-ext="{action.lower()}"{extra_data}>
    {_icon}<span class="download-label">{label}</span>
    </button>
    {scripts}
    <script>{_js}</script>
    </body>
    """,
            height="48px",
        )

    return (iframe_button,)


if __name__ == "__main__":
    app.run()

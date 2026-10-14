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
    import marimo as mo
    import svgwrite

    from logoneef import append_neefje


@app.cell(hide_code=True)
def _(logo):
    title = "# Welkom bij favicon"
    text = (
        "Hieronder staat een favicon met een knop om het logo als svg "
        "bestand te downloaden. Het logo is aan te passen met de code "
        "die daar weer onderstaat. Pas de code en daarmee het logo gerust aan "
        "naar jouw wensen."
    )

    _svg_str = logo.tostring()
    _svg_bytes = _svg_str.encode("utf-8")

    download_svg = mo.download(
        data=lambda: _svg_bytes,
        filename="favicon.svg",
        mimetype="image/svg+xml",
        label="Download logo as svg",
    )
    mo.vstack(
        [
            mo.md(title).center(),
            mo.md(text).center(),
            mo.Html(_svg_str).center(),
            download_svg,
        ]
    ).center()
    return


@app.cell
def _():
    # Standard screen DPI (96) divided by cm per inch (2.54) = pixels per cm
    cm = 96 / 2.54  # centimeter pixel ratio

    def create_logo() -> svgwrite.Drawing:
        d_width = 10 * cm
        d_heigth = 10 * cm
        d = svgwrite.Drawing(size=(d_width, d_heigth))
        d.viewbox(-d_width / 2, -d_heigth / 2, d_width, d_heigth)
        b = 1.5 * cm  # radius head
        q_small = 1.5  # head-body ratio small neefje
        r = b / 2.5
        h_small_neef = (3 + q_small) * b

        kwargs_formats = [
            {
                "fill": "none",
                "stroke": "white",
                "stroke_width": 30,
            },
            {
                "fill": "none",
                "stroke": "black",
                "stroke_width": 15,
            },
        ]

        for kwargs_format in kwargs_formats:
            kwargs = {
                "y": h_small_neef / 2,
                "x": 0,
                "d": d,
                "b": b,
                "r_r": r,
                "r_l": r,
                "q": q_small,
                **kwargs_format,
            }
            append_neefje(**kwargs)

            # Circle with radius r at the center
            d.add(d.circle(center=(0, 0), r=h_small_neef / 2 + b / 2, **kwargs_format))

        # Uncomment to display center lines
        # d.add(
        #     d.line(
        #         start=(-d_width / 2, 0),
        #         end=(d_width / 2, 0),
        #         stroke="red",
        #         stroke_dasharray="8,8",
        #     )
        # )
        # d.add(
        #     d.line(
        #         start=(0, -d_heigth / 2),
        #         end=(0, d_heigth / 2),
        #         stroke="red",
        #         stroke_dasharray="8,8",
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


if __name__ == "__main__":
    app.run()

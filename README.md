# Logoneef — Parametric Logo GUI

A standalone marimo web app that renders a parametric logo with `svgwrite` from an editable marimo cell, previews it live, and exports as SVG or PDF.

## Quickstart

1. **Install dependencies:**
   ```bash
   uv sync
   ```

2. **Run the app:**
   ```bash
   uvx marimo edit --sandbox logoneef.py
   ```

3. **Build the WASM site:**
   `build.py` also generates the favicon files in `dist/` from `favicon.svg`.
   ```bash
   uv run build.py
   uv run python -m http.server 8000 --directory dist
   ```

4. **Access the app:**
   Open `http://localhost:8000` in your browser.

## Features

- **Live preview**: See changes instantly as you adjust parameters
- **Export formats**: SVG, PDF
- **Timestamp-based filenames**: `logoneef_{yyyymmdd}_{hhmmss}.{svg,pdf}`

## Development

- **Python**: 3.14+
- **Package manager**: `uv`
- **Linting**: `ruff`
- **Framework**: marimo + svgwrite

## Source

[GitHub](https://github.com/arie-neuteboom/logoneef)

## License

[PolyForm Noncommercial 1.0.0](https://polyformproject.org/licenses/noncommercial/1.0.0) — see [LICENSE](LICENSE).
# Logoneef — Parametric Logo GUI

A standalone marimo web app that renders a parametric logo with `drawsvg` from an editable marimo cell, previews it live, and exports as SVG or PDF.

## Quickstart

1. **Install dependencies:**
   ```bash
   uv sync
   ```

2. **Run the app:**
   ```bash
   uv run marimo run app.py --host 0.0.0.0 --port 2718 --headless
   ```

3. **Access the app:**
   Open `http://localhost:2718` in your browser.

## Features

- **Live preview**: See changes instantly as you adjust parameters
- **Export formats**: SVG, PDF
- **Timestamp-based filenames**: `logoneef_{yyyymmdd}_{hhmmss}.{svg,pdf}`

## Development

- **Python**: 3.14+
- **Package manager**: `uv`
- **Linting**: `ruff`
- **Framework**: marimo + drawsvg

## Source

[GitHub](https://github.com/arie-neuteboom/logoneef)

## License

[PolyForm Noncommercial 1.0.0](https://polyformproject.org/licenses/noncommercial/1.0.0) — see [LICENSE](LICENSE).

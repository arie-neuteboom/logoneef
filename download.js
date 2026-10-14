// An iframe document cannot be truly transparent: the browser paints its canvas
// with the base color of its own color-scheme. Marimo themes the page with a
// `.dark` class and never sets `color-scheme`, so the canvas stays white.
// Instead of fighting that, copy the surrounding page's resolved colors in.
(function styleIframe() {
    const frame = window.frameElement;
    const isOpaque = (color) =>
        color && color !== 'transparent' && !color.startsWith('rgba(0, 0, 0, 0');

    let background = '';
    let foreground = '';
    try {
        const outer = window.parent;
        foreground = outer.getComputedStyle(outer.document.body).color;
        for (let el = frame; el; el = el.parentElement) {
            const color = outer.getComputedStyle(el).backgroundColor;
            if (isOpaque(color)) {
                background = color;
                break;
            }
        }
    } catch (err) {
        // Cross-origin parent: keep the browser defaults.
    }

    if (background) {
        document.documentElement.style.setProperty(
            'background-color', background, 'important'
        );
        document.body.style.setProperty(
            'background-color', background, 'important'
        );
    }
    if (foreground) {
        document.body.style.setProperty('color', foreground, 'important');
    }
})();

function triggerDownload(blob, filename) {
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

function getTimestampedFilename(ext) {
    const now = new Date();
    const year = now.getFullYear();
    const month = String(now.getMonth() + 1).padStart(2, '0');
    const day = String(now.getDate()).padStart(2, '0');
    const hours = String(now.getHours()).padStart(2, '0');
    const minutes = String(now.getMinutes()).padStart(2, '0');
    const seconds = String(now.getSeconds()).padStart(2, '0');
    return `logoneef_${year}${month}${day}_${hours}${minutes}${seconds}.${ext}`;
}

function downloadSvg(btn) {
    try {
        const svg = btn.dataset.svg;
        const filename = getTimestampedFilename(btn.dataset.ext);
        const blob = new Blob([svg], { type: 'image/svg+xml;charset=utf-8' });
        triggerDownload(blob, filename);
    } catch (err) {
        alert('Error generating SVG: ' + err.message);
    }
}

function downloadPdf(btn) {
    var textElement = btn.querySelector('.download-label') || btn;
    var originalText = textElement.textContent;
    try {
        if (!window.jspdf) {
            alert('jsPDF library not loaded. Check your network connection.');
            return;
        }
        btn.disabled = true;
        textElement.textContent = 'Bezig met genereren...';

        const svg = btn.dataset.svg;
        const width = parseFloat(btn.dataset.width);
        const height = parseFloat(btn.dataset.height);
        const filename = getTimestampedFilename(btn.dataset.ext);
        const { jsPDF } = window.jspdf;
        const pdf = new jsPDF({
            orientation: width > height ? 'landscape' : 'portrait',
            unit: 'px',
            format: [width, height]
        });
        if (typeof pdf.svg !== 'function') {
            btn.disabled = false;
            textElement.textContent = originalText;
            alert('PDF SVG plugin not loaded.');
            return;
        }

        // Attach the SVG to the DOM so svg2pdf can resolve references correctly,
        // then remove it once rendering is done.
        const container = document.createElement('div');
        container.style.position = 'fixed';
        container.style.visibility = 'hidden';
        container.innerHTML = svg;
        document.body.appendChild(container);
        const svgEl = container.querySelector('svg');
        if (!svgEl) {
            document.body.removeChild(container);
            btn.disabled = false;
            textElement.textContent = originalText;
            alert('Could not parse SVG data.');
            return;
        }

        pdf.svg(svgEl, { x: 0, y: 0, width, height })
            .then(() => {
                document.body.removeChild(container);
                pdf.save(filename);
                btn.disabled = false;
                textElement.textContent = originalText;
            })
            .catch((err) => {
                document.body.removeChild(container);
                btn.disabled = false;
                textElement.textContent = originalText;
                alert('Error generating PDF: ' + err.message);
            });
    } catch (err) {
        btn.disabled = false;
        textElement.textContent = originalText || 'Download logo as pdf';
        alert('Error: ' + err.message);
    }
}

import os
from xml.sax.saxutils import escape
from PIL import Image
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

_UNICODE_FONT = None


def _get_unicode_font():
    global _UNICODE_FONT
    if _UNICODE_FONT is not None:
        return _UNICODE_FONT
    candidates = [
        ("C:/Windows/Fonts/Nirmala.ttc", 0, "NirmalaUI"),
        ("C:/Windows/Fonts/Arial.ttf", "Arial"),
    ]
    for entry in candidates:
        if len(entry) == 3:
            path, subfont, name = entry
        else:
            path, name = entry
            subfont = None
        if not os.path.exists(path):
            continue
        try:
            kwargs = {}
            if subfont is not None:
                kwargs["subfontIndex"] = subfont
            pdfmetrics.registerFont(TTFont(name, path, **kwargs))
            _UNICODE_FONT = name
            return name
        except Exception:
            continue
    _UNICODE_FONT = "Helvetica"
    return "Helvetica"


def pdf_to_images(pdf_path: str, output_dir: str, dpi: int = 300) -> list:
    import fitz
    doc = fitz.open(pdf_path)
    image_paths = []
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        pix = page.get_pixmap(matrix=fitz.Matrix(dpi / 72, dpi / 72))
        img_path = os.path.join(output_dir, f"page_{page_num + 1}.png")
        pix.save(img_path)
        image_paths.append(img_path)
    doc.close()
    return image_paths


def text_to_pdf(text_pages: list, output_path: str):
    doc = SimpleDocTemplate(output_path, pagesize=A4,
                            leftMargin=20 * mm, rightMargin=20 * mm,
                            topMargin=20 * mm, bottomMargin=20 * mm)
    styles = getSampleStyleSheet()
    style = styles["Normal"]
    style.fontName = _get_unicode_font()
    style.fontSize = 11
    style.leading = 16

    elements = []
    for page_text in text_pages:
        for line in page_text.split("\n"):
            if line.strip():
                elements.append(Paragraph(escape(line), style))
                elements.append(Spacer(1, 4))
        elements.append(Spacer(1, 12))

    doc.build(elements)


def read_image_bytes(image_path: str) -> bytes:
    with open(image_path, "rb") as f:
        return f.read()

import os
from xml.sax.saxutils import escape
from PIL import Image
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

_FONT_CACHE = {}

_SCRIPT_FONTS = {
    "Deva": [
        ("C:/Windows/Fonts/Nirmala.ttc", 0, "NirmalaUI"),
        ("C:/Windows/Fonts/Nirmala.ttc", 1, "Nirmala"),
        ("C:/Windows/Fonts/Nirmala.ttc", "Nirmala"),
    ],
    "Beng": [
        ("C:/Windows/Fonts/Nirmala.ttc", 0, "NirmalaUI_Beng"),
        ("C:/Windows/Fonts/Shonar.ttf", "Shonar"),
        ("C:/Windows/Fonts/Vrinda.ttf", "Vrinda"),
    ],
    "Arab": [
        ("C:/Windows/Fonts/ariblk.ttf", "ArialBlack"),
        ("C:/Windows/Fonts/tradojo.ttf", "TraditionalArabic"),
        ("C:/Windows/Fonts/arabtype.ttf", "ArabicTypesetting"),
    ],
    "Cyrl": [
        ("C:/Windows/Fonts/Calibri.ttf", "Calibri"),
        ("C:/Windows/Fonts/Arial.ttf", "Arial"),
    ],
    "Hans": [
        ("C:/Windows/Fonts/msyh.ttc", 0, "MicrosoftYaHei"),
        ("C:/Windows/Fonts/simsun.ttc", 0, "SimSun"),
    ],
    "Hant": [
        ("C:/Windows/Fonts/msjh.ttc", 0, "MicrosoftJhengHei"),
        ("C:/Windows/Fonts/mingliu.ttc", 0, "MingLiU"),
    ],
    "Jpan": [
        ("C:/Windows/Fonts/msgothic.ttc", 0, "MSGothic"),
        ("C:/Windows/Fonts/meiryo.ttc", 0, "Meiryo"),
    ],
    "Hang": [
        ("C:/Windows/Fonts/malgun.ttf", "MalgunGothic"),
        ("C:/Windows/Fonts/batang.ttc", 0, "Batang"),
    ],
    "Thai": [
        ("C:/Windows/Fonts/tahoma.ttf", "Tahoma"),
        ("C:/Windows/Fonts/angsana.ttc", 0, "AngsanaNew"),
    ],
    "Grek": [
        ("C:/Windows/Fonts/calibri.ttf", "Calibri"),
        ("C:/Windows/Fonts/arial.ttf", "Arial"),
    ],
    "Telu": [
        ("C:/Windows/Fonts/Nirmala.ttc", "Nirmala_Telu"),
        ("C:/Windows/Fonts/Gautami.ttf", "Gautami"),
    ],
    "Taml": [
        ("C:/Windows/Fonts/Nirmala.ttc", "Nirmala_Taml"),
        ("C:/Windows/Fonts/Latha.ttf", "Latha"),
    ],
}


def _get_unicode_font(script: str = "Latn"):
    if script in _FONT_CACHE:
        return _FONT_CACHE[script]
    _fonts_dir = os.path.join(os.path.dirname(__file__), "fonts")
    bundled = os.path.join(_fonts_dir, "NotoSans-Regular.ttf")
    candidates = []
    if os.path.exists(bundled):
        candidates.append((bundled, "NotoSans"))
    candidates.extend(_SCRIPT_FONTS.get(script, []))
    candidates.extend([
        ("C:/Windows/Fonts/Noto.ttf", "Noto"),
        ("C:/Windows/Fonts/Arial.ttf", "Arial"),
    ])
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
            _FONT_CACHE[script] = name
            return name
        except Exception:
            continue
    _FONT_CACHE[script] = "Helvetica"
    return "Helvetica"


def pdf_to_images(pdf_path: str, output_dir: str, dpi: int = 200) -> list:
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


def text_to_pdf(text_pages: list, output_path: str, target_script: str = "Latn"):
    doc = SimpleDocTemplate(output_path, pagesize=A4,
                            leftMargin=20 * mm, rightMargin=20 * mm,
                            topMargin=20 * mm, bottomMargin=20 * mm)
    styles = getSampleStyleSheet()
    style = styles["Normal"]
    style.fontName = _get_unicode_font(target_script)
    style.fontSize = 11
    style.leading = 16

    elements = []
    for page_text in text_pages:
        paragraphs = page_text.split("\n")
        for i, para in enumerate(paragraphs):
            stripped = para.strip()
            if not stripped:
                elements.append(Spacer(1, 8))
                continue
            elements.append(Paragraph(escape(stripped), style))
            elements.append(Spacer(1, 4))
        elements.append(Spacer(1, 12))

    doc.build(elements)


def read_image_bytes(image_path: str) -> bytes:
    with open(image_path, "rb") as f:
        return f.read()

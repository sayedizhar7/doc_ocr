import io
from PIL import Image
import pytesseract
import fitz  # PyMuPDF

def _ocr_image(img: Image.Image) -> str:
    img = img.convert("RGB")
    return pytesseract.image_to_string(img)

def ocr_from_upload(uploaded_file) -> str:
    """
    - Images: OCR directly
    - PDFs: render pages to images using PyMuPDF then OCR
    """
    filename = (uploaded_file.name or "").lower()
    data = uploaded_file.read()
    uploaded_file.seek(0)

    if filename.endswith(".pdf"):
        parts = []
        doc = fitz.open(stream=data, filetype="pdf")
        for page in doc:
            pix = page.get_pixmap(dpi=200)
            png = pix.tobytes("png")
            img = Image.open(io.BytesIO(png))
            parts.append(_ocr_image(img))
        return "\n".join(parts)

    img = Image.open(io.BytesIO(data))
    return _ocr_image(img)

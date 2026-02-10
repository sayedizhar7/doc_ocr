import re
from .models import DocumentType

PATTERNS = {
    DocumentType.PAN: re.compile(r"\b[A-Z]{5}[0-9]{4}[A-Z]\b"),
    DocumentType.AADHAAR: re.compile(r"\b[0-9]{4}\s?[0-9]{4}\s?[0-9]{4}\b"),
    DocumentType.GST: re.compile(r"\b[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}\b"),
    DocumentType.FSSAI: re.compile(r"\b[0-9]{14}\b"),
    DocumentType.MSME: re.compile(r"\b(UAM|UDYAM)[A-Z0-9\-\/]{6,}\b", re.IGNORECASE),
}

def extract_doc_number(doc_type: str, text: str) -> str | None:
    pattern = PATTERNS.get(doc_type)
    if not pattern:
        return None
    m = pattern.search((text or "").upper())
    if not m:
        return None
    return m.group(0).replace(" ", "")

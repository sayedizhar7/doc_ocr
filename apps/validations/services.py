import requests
from django.conf import settings

class AuthBridgeTruthScreenClient:
    """
    AuthBridge TruthScreen API client.

    NOTE:
    - The exact endpoint paths/payload keys can differ by tenant/check.
    - We read paths from settings/.env so you can adjust without code changes.
    """

    def __init__(self):
        self.base = settings.AUTHBRIDGE_BASE_URL.rstrip("/")
        self.key = settings.AUTHBRIDGE_API_KEY

        self.paths = {
            "PAN": settings.AUTHBRIDGE_PAN_PATH,
            "AADHAAR": settings.AUTHBRIDGE_AADHAAR_PATH,
            "GST": settings.AUTHBRIDGE_GST_PATH,
            "FSSAI": settings.AUTHBRIDGE_FSSAI_PATH,
            "MSME": settings.AUTHBRIDGE_MSME_PATH,
        }

    def _headers(self):
        return {
            "Authorization": f"Bearer {self.key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    def validate(self, doc_type: str, doc_number: str) -> dict:
        if not self.base or not self.key:
            # Dev fallback - keeps app usable until you add AuthBridge creds
            return {
                "success": True,
                "mode": "DEV_FALLBACK",
                "doc_type": doc_type,
                "doc_number": doc_number,
                "result": {"valid": True, "name": "Demo User"},
                "note": "Set AUTHBRIDGE_BASE_URL and AUTHBRIDGE_API_KEY to call real AuthBridge.",
            }

        doc_type = doc_type.upper()
        path = self.paths.get(doc_type)
        if not path:
            raise ValueError("Unsupported document type")

        url = f"{self.base}{path}"

        # Payload mapping (adjust keys if AuthBridge doc says otherwise)
        payload_map = {
            "PAN": {"pan": doc_number},
            "AADHAAR": {"aadhaar": doc_number},
            "GST": {"gstin": doc_number},
            "FSSAI": {"license_number": doc_number},
            "MSME": {"udyam_number": doc_number},
        }

        payload = payload_map[doc_type]

        r = requests.post(url, headers=self._headers(), json=payload, timeout=30)
        r.raise_for_status()
        return r.json()

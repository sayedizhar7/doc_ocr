from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.cache import never_cache
from django.contrib import messages

from .forms import ValidateForm
from .models import ValidationRequest
from .ocr import ocr_from_upload
from .utils import extract_doc_number
from .services import AuthBridgeTruthScreenClient

def _normalize_authbridge(doc_type: str, api_json: dict) -> tuple[bool, str]:
    """
    Tries to infer validity + name from common shapes.
    Since AuthBridge responses can vary by check, we use safe heuristics.
    """
    j = api_json or {}
    result = j.get("result") or j.get("data") or j

    # validity heuristics
    candidates = [
        result.get("valid"),
        result.get("is_valid"),
        (result.get("status") == "SUCCESS"),
        (result.get("verification_status") == "SUCCESS"),
        (result.get("success") is True),
    ]
    is_valid = any(v is True for v in candidates)

    # name heuristics
    name = (
        result.get("name")
        or result.get("full_name")
        or result.get("holder_name")
        or result.get("business_name")
        or result.get("legal_name")
        or ""
    )
    return is_valid, str(name)

@never_cache
@login_required
def dashboard(request):
    form = ValidateForm(request.POST or None, request.FILES or None)

    if request.method == "POST" and form.is_valid():
        doc_type = form.cleaned_data["doc_type"]
        doc_number = (form.cleaned_data.get("doc_number") or "").strip()
        file = form.cleaned_data.get("file")

        if file and not doc_number:
            try:
                text = ocr_from_upload(file)
                doc_number = extract_doc_number(doc_type, text) or ""
            except Exception as e:
                messages.error(request, f"OCR failed: {e}")
                return redirect("dashboard")

        if not doc_number:
            messages.error(request, "Could not detect a valid document number. Please enter it manually.")
            return redirect("dashboard")

        vr = ValidationRequest.objects.create(
            user=request.user,
            doc_type=doc_type,
            doc_number=doc_number,
            uploaded_file=file if file else None,
        )

        client = AuthBridgeTruthScreenClient()
        try:
            data = client.validate(doc_type, doc_number)
            is_valid, name = _normalize_authbridge(doc_type, data)

            vr.api_response = data
            vr.holder_name = name
            vr.status = ValidationRequest.Status.VALID if is_valid else ValidationRequest.Status.INVALID
            vr.save()

        except Exception as e:
            vr.status = ValidationRequest.Status.ERROR
            vr.api_response = {"success": False, "error": str(e)}
            vr.save()

        return redirect("result", pk=vr.pk)

    history = ValidationRequest.objects.filter(user=request.user)[:50]
    return render(request, "validations/dashboard.html", {"form": form, "history": history})

@never_cache
@login_required
def result(request, pk: int):
    vr = get_object_or_404(ValidationRequest, pk=pk, user=request.user)
    return render(request, "validations/result.html", {"vr": vr})

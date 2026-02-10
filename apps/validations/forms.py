from django import forms
from .models import DocumentType

class ValidateForm(forms.Form):
    doc_type = forms.ChoiceField(choices=DocumentType.choices)
    doc_number = forms.CharField(required=False, max_length=80)
    file = forms.FileField(required=False)

    def clean(self):
        cleaned = super().clean()
        if not cleaned.get("doc_number") and not cleaned.get("file"):
            raise forms.ValidationError("Provide either a document number or upload an image/PDF.")
        return cleaned

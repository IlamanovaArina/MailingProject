from django.forms import BooleanField
from django import forms
from mailing.models import Mail

class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs["class"] = "form-check-input"
            else:
                field.widget.attrs["class"] = "form-control"

class GoMail(forms.ModelForm):
    class Meta:
        model = Mail
        fields = ['theme', 'body_mail']
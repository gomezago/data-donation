from django import forms
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

class DonationForm(forms.Form):
    name = forms.CharField(
        required=False,
        label="Insert Your Name:",
        max_length=100,
        widget=forms.TextInput(attrs={  #HTML Text Input element
            "class": "form-control",
            "placeholder": "Your Name"
        })
    )
    email = forms.EmailField(max_length=255,
            required=True,
            label="Insert Your Email*",
            validators=[validate_email],
            widget=forms.TextInput(attrs={
                "class" : "form-control",
                "placeholder": "Your Email"
            })
    )
    data = forms.ImageField(
        required=True,
        label="Upload Your Data:",
        widget=forms.FileInput()
    )

    available = forms.BooleanField(
        required=False,
        label="Do you agree to...",
        widget=forms.CheckboxInput()
    )
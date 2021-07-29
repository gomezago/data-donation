from django import forms
from django.core.validators import validate_image_file_extension

class ProjectForm(forms.Form):
    title = forms.CharField(
        required=True,
        label="Project Title",
        max_length=200,
        widget=forms.TextInput(
            attrs={
                'class' : 'form-control',
                'placeholder' : 'The amazing title of your project',
            }
        )
    )
    description_tweet = forms.CharField(
        required=True,
        label="Project Title",
        max_length=280,
        widget=forms.TextInput(
            attrs={
                'class' : 'form-control',
                'placeholder' : 'Tweet-like description',
            }
        )
    )
    description_long = forms.CharField(
        required=True,
        label="Project Title",
        max_length=1000,
        widget=forms.TextInput(
            attrs={
                'class' : 'form-control',
                'placeholder' : 'Extended description',
            }
        )
    )

    hrec = forms.BooleanField(
        required=True,
        initial=False,
        widget=forms.CheckboxInput(
            attrs={
                'class': 'checkbox',
            }
        )
    )
    data = forms.CharField(
        required=True,
        label="Data",
        max_length=400,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'What data you aim to collect',
            }
        )
    )
    data_info = forms.CharField(
        required=True,
        label="Data",
        max_length=400,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'How you are using the data',
            }
        )
    )

    start = forms.DateField(
        required=True,
        widget=forms.SelectDateWidget()
    )

    end = forms.DateField(
        required=True,
        widget=forms.SelectDateWidget()
    )

    image = forms.ImageField(
        required=False,
        label="Upload Your Data:",
        widget=forms.FileInput(
        )
    )

class DonateForm(forms.Form):
    updates = forms.BooleanField(
        initial=False,
        widget=forms.CheckboxInput(
            attrs={
                'class': 'checkbox',
            }
        )
    )

    data = forms.FileField(
        required=False,
        label="Upload Your Data:",
        widget=forms.FileInput(
        )
    )










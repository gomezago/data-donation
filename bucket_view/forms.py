from django import forms
from utils.bucket_functions import list_property_types
from django.core.validators import FileExtensionValidator
class ProjectForm(forms.Form):

    def __init__(self, *args, **kwargs):
        data_choices = kwargs.pop("choices")
        super(ProjectForm, self).__init__(*args, **kwargs)

        self.fields['data'].choices = data_choices


    title = forms.CharField(
        required=True,
        label="Project Title",
        max_length=200,
        widget=forms.TextInput(
            attrs={
                'class' : 'form-control',
                'placeholder' : 'Amazing title of your project',
            }
        )
    )

    researcher_name = forms.CharField(
        required=True,
        label="Researcher(s) Name(s)",
        max_length=200,
        widget=forms.TextInput(
            attrs={
                'class' : 'form-control',
                'placeholder' : 'Name of the researcher(s)',
            }
        )
    )

    researcher_affiliation  = forms.CharField(
        required=True,
        label="Researcher(s) Affiliation(S)",
        max_length=200,
        widget=forms.TextInput(
            attrs={
                'class' : 'form-control',
                'placeholder' : 'Affiliation of the researcher(s)',
            }
        )
    )

    id = forms.CharField(
        required=True,
        label="Project ID",
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Short ID of your project',
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
                'placeholder' : 'Describe your project in a tweet',
            }
        )
    )
    description_long = forms.CharField(
        required=True,
        label="Project Title",
        max_length=1000,
        widget=forms.Textarea(
            attrs={
                'class' : 'form-control',
                'placeholder' : 'Extended description of your project',
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
    data = forms.MultipleChoiceField(
        choices=(),
        required=True,
        widget=forms.CheckboxSelectMultiple(
            attrs={
                'class': 'checkbox',
            }
        )
    )
    data_info = forms.CharField(
        required=True,
        label="Data",
        max_length=400,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': 'Describe how you are using the data',
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
        label="Upload Your Image:",
        widget=forms.FileInput(
            attrs={
                'class' : 'form-control-file',
                'type' : 'file',
                'multiple' : False,
                'accept': 'image/*',
            }
        )
    )



class DonateForm(forms.Form):
    consent = forms.BooleanField(
        initial=False,
        widget=forms.CheckboxInput(
            attrs={
                'class': 'checkbox',
            }
        )
    )

    adult = forms.BooleanField(
        initial=False,
        widget=forms.CheckboxInput(
            attrs={
                'class': 'checkbox',
            }
        )
    )

    updates = forms.BooleanField(
        initial=False,
        widget=forms.CheckboxInput(
            attrs={
                'class': 'checkbox',
            }
        )
    )

    data = forms.FileField(
        required=True,
        label="Upload Your Data:",
        widget=forms.FileInput(
            attrs={
                'class' : 'form-control-file',
                'multiple' : 'False', #TODO: At some point, allow for multiple uploads
                'accept' : '.cluedata, .json, application/JSON,',
                #'style': 'display: none',
            }
        )
    )










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

    instructions = forms.CharField(
        required=True,
        label="Instructions",
        max_length=1000,
        widget=forms.Textarea(
            attrs={
                'class' : 'form-control',
                'placeholder' : 'Describe the steps to follow in order to donate data to your project',
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
        widget=forms.SelectMultiple(
            attrs={
                'class': 'form-control',
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

    data_ext = forms.CharField(
        required=True,
        label="Extension",
        max_length=400,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': 'Input the extension of the Takeout file',
            }
        )
    )

    start = forms.DateField(
        required=True,
        widget=forms.SelectDateWidget(
            attrs={
                'data-date-format' : 'dd/mm/yyy',
                'class' : 'form-control snps-inline-select',
            }
        )
    )

    end = forms.DateField(
        required=True,
        widget=forms.SelectDateWidget(
            attrs={
                'data-date-format': 'dd/mm/yyy',
                'class': 'form-control snps-inline-select',
            }
        )
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

    def __init__(self, *args, **kwargs):
        data_choices = kwargs.pop("choices")
        super(DonateForm, self).__init__(*args, **kwargs)

        self.fields['data_selection'].choices = data_choices

    data_selection = forms.MultipleChoiceField(
        choices=(),
        required=True,
        widget=forms.SelectMultiple(
            attrs={
                'class': 'form-control', #form-select in Boostrap 5
            }
        )
    )


    consent = forms.BooleanField(
        initial=False,
        required=True,
        widget=forms.CheckboxInput(
            attrs={
                'class': 'checkbox',
            }
        )
    )

    participate = forms.BooleanField(
        initial=False,
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                'class': 'checkbox',
            }
        )
    )

    updates = forms.BooleanField(
        initial=False,
        required=False,
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
                'accept' : '.cluedata, .json, application/JSON, .zip, .7zip',
                #'style': 'display: none',
            }
        )
    )


class DemographicsForm(forms.Form):
    SEX_CHOICES = (
        (0, "---"),
        (1, "Female"),
        (2, "Male"),
        (3, "Prefer to Self-Describe"),
    )

    sex = forms.ChoiceField(
        required=False,
        label = "Your Sex: ",
        choices=SEX_CHOICES,
        widget=forms.Select(attrs={
            'class' : 'form-control',
        })
    )

    date_of_birth = forms.DateField(
        required = False,
        widget = forms.SelectDateWidget(
            years = range(1955, 2025),
            attrs={
            #'data-date-format': 'dd/mm/yyy',
            'class': 'form-control snps-inline-select menu-scroll',

        })
    )


class ReminderForm(forms.Form):
    REMINDER_CHOICES = (
        (0, "Choose a Reminder Date*"),
        (1, "1 second"),
        (2, "10 seconds"),
        (3, "30 seconds"),
    )

    reminder_time = forms.ChoiceField(
        required=True,
        label = "When Shall we remind you?: ",
        choices=REMINDER_CHOICES,
        widget=forms.Select(attrs={
            'class' : 'form-control',
        })
    )

    reminder_email = forms.EmailField(
        required=True,
        label = "Your Email: ",
        widget=forms.EmailInput(attrs={
            'class' : 'form-control',
            'placeholder' : "Email*",
        })
    )



class MotivationForm(forms.Form):
    significance = forms.BooleanField(
        initial=False,
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                'class': 'checkbox',
            }
        )
    )

    curiosity = forms.BooleanField(
        initial=False,
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                'class': 'checkbox',
            }
        )
    )
    researcher  = forms.BooleanField(
        initial=False,
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                'class': 'checkbox',
            }
        )
    )

    participate = forms.BooleanField(
        initial=False,
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                'class': 'checkbox',
            }
        )
    )
    other = forms.CharField(
        required=False,
        max_length=300,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Other...',
            }
        )
    )




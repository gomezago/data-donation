from django import forms
from utils.bucket_functions import list_property_types
from django.core.validators import FileExtensionValidator
from django.core.validators import validate_email

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
        required=False,
        widget=forms.SelectMultiple(
            attrs={
                'class': 'form-control', #form-select in Boostrap 5
            }
        )
    )

    consent = forms.BooleanField(
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

    stored = forms.BooleanField(
        initial=False,
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                'class' : 'checkbox',
            }
        )
    )

    takeout = forms.BooleanField(
        initial=False,
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                'class' : 'checkbox',
            }
        )
    )

    info = forms.CharField(
        required=True,
        label="Goal",
        max_length=200,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': 'My voice assistant logs contain...',
                'rows':2,
            }
        )
    )


    goal = forms.CharField(
        required=True,
        label="Goal",
        max_length=200,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': 'I would like to learn...',
                'rows': 2,
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
        (1, "2 Weeks"),
        (2, "3 Weeks"),
        (3, "4 Weeks"),
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
        validators= [validate_email],
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



class MetadataForm(forms.Form):

    # Speaker
    SEX_CHOICES = (
        (3, "---"),
        (0, "Female"),
        (1, "Male"),
        (2, "Prefer to Self-Describe"),
    )

    AGE_CHOICES = (
        (7, "---"),
        (0, "18-24 Years Old"),
        (1, "25-34 Years Old"),
        (2, "35-44 Years Old"),
        (3, "45-54 Years Old"),
        (4, "55-64 Years Old"),
        (5, "65-74 Years Old"),
        (6, "Above 75 Years Old"),
    )


    LAN_CHOICES = (
        (15, "---"),
        (0, 'Danish'),
        (1, 'Dutch'),
        (2, 'English'),
        (3, 'French'),
        (4, 'German'),
        (5, 'Hindi'),
        (6, 'Indonesian'),
        (7, 'Italian'),
        (8, 'Japanese'),
        (9, 'Korean'),
        (10, 'Norwegian'),
        (11, 'Portuguese'),
        (12, 'Spanish'),
        (13, 'Swedish'),
        (14, 'Mandarin'),
    )

    DEV_CHOICES = (
        (8, '---'),
        (0, 'Smartphone'),
        (1, 'Smart Speaker'),
        (2, 'Smart Display'),
        (3, 'Smart Car'),
        (4, 'Smart TV'),
        (5, 'Laptop or Tablet'),
        (6, 'Smart Watch'),
        (7, "Other"), # Eg., Thermostat, Smart clock
    )

    USE_CHOICES = (
        (4, "---"),
        (0, "None"),
        (1, "One"),
        (2, "Two"),
        (3, "Three or more"),
    )

    sex = forms.ChoiceField(
        required=True,
        label = "Your Sex: ",
        choices=SEX_CHOICES,
        widget=forms.Select(attrs={
            'class' : 'form-control',
        })
    )

    age = forms.ChoiceField(
        required = True,
        label="Your Age: ",
        choices=AGE_CHOICES,
        widget = forms.Select(attrs={
            'class' : 'form-control',
        })
    )

    lan = forms.ChoiceField(
        required = True,
        label="The Language you Speak with your Assistant: ",
        choices=LAN_CHOICES,
        widget = forms.Select(attrs={
            'class' : 'form-control',
        })
    )

    acc = forms.CharField(
        required=False,
        label="Your Accent:",
        max_length=40,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Yorkshire',
            }
        )
    )

    use = forms.ChoiceField(
        required = True,
        label="How many people share your Voice Assistant? ",
        choices=USE_CHOICES,
        widget = forms.Select(attrs={
            'class' : 'form-control',
        })
    )

    # Device
    dev = forms.ChoiceField(
        required=True,
        label='Your Device:',
        choices=DEV_CHOICES,
        widget=forms.Select(attrs={
            'class' : 'form-control',
        })
    )

    # Awareness
    awa = forms.BooleanField(
        initial=False,
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                'class': 'checkbox',
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

class AwarenessSurveyForm(forms.Form):

    amount = forms.IntegerField(
        initial=2,
        required=False,
        widget=forms.NumberInput(
            attrs={
                'class':'form-control-range',
                'type' : 'range',
                'min': 0,
                'max': 4,
                'step' : 1,
            }
        )
    )

    types = forms.IntegerField(
        initial=2,
        required=False,
        widget=forms.NumberInput(
            attrs={
                'class':'form-control-range',
                'type' : 'range',
                'min': 0,
                'max': 4,
                'step' : 1,
            }
        )
    )

    duration = forms.IntegerField(
        initial=2,
        required=False,
        widget=forms.NumberInput(
            attrs={
                'class':'form-control-range',
                'type' : 'range',
                'min': 0,
                'max': 4,
                'step' : 1,
            }
        )
    )

    decision = forms.IntegerField(
        initial=2,
        required=False,
        widget=forms.NumberInput(
            attrs={
                'class':'form-control-range',
                'type' : 'range',
                'min': 0,
                'max': 4,
                'step' : 1,
            }
        )
    )

    learn = forms.CharField(
        required=True,
        label="Goal",
        max_length=200,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': 'I learned...',
                'rows':2,
            }
        )
    )


class DeleteSurveyForm(forms.Form):

    amount = forms.IntegerField(
        initial=2,
        required=False,
        widget=forms.NumberInput(
            attrs={
                'class':'form-control-range',
                'type' : 'range',
                'min': 0,
                'max': 4,
                'step' : 1,
            }
        )
    )

    types = forms.IntegerField(
        initial=2,
        required=False,
        widget=forms.NumberInput(
            attrs={
                'class':'form-control-range',
                'type' : 'range',
                'min': 0,
                'max': 4,
                'step' : 1,
            }
        )
    )

    duration = forms.IntegerField(
        initial=2,
        required=False,
        widget=forms.NumberInput(
            attrs={
                'class':'form-control-range',
                'type' : 'range',
                'min': 0,
                'max': 4,
                'step' : 1,
            }
        )
    )

    decision = forms.IntegerField(
        initial=2,
        required=False,
        widget=forms.NumberInput(
            attrs={
                'class':'form-control-range',
                'type' : 'range',
                'min': 0,
                'max': 4,
                'step' : 1,
            }
        )
    )

    learn = forms.CharField(
        required=True,
        label="Goal",
        max_length=200,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': 'I learned...',
                'rows': 5,
                'cols': 5,
            }
        )
    )

    delete = forms.CharField(
        required=True,
        label="Goal",
        max_length=200,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': 'I delecided to delete my data because...',
                'rows': 5,
                'cols': 5,
            }
        )
    )
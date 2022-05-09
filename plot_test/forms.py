from django import forms


class DeleteMotivationForm(forms.Form):
    delete_motive = forms.CharField(
        required=True,
        label="Goal",
        max_length=200,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': 'I chose to exclude these points because...',
                'rows' : 5,
                'cols' : 5,
            }
        )
    )

class SelectDonationForm(forms.Form):

    def __init__(self, *args, **kwargs):
        donation_choices = kwargs.pop("choices")
        super(SelectDonationForm, self).__init__(*args, **kwargs)

        self.fields['donation'].choices = donation_choices

    donation = forms.ChoiceField(
        choices=(),
        required=True,
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }
        )
    )
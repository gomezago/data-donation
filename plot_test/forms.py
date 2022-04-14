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
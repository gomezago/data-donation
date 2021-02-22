from django import forms


class CommentForm(forms.Form):
    author = forms.CharField(
        max_length=60, #If CharField here corresponds to CharField on model lenght should be the same
        widget=forms.TextInput(attrs={  #HTML Text Input element
            "class": "form-control",
            "placeholder": "Your Name"
        })
    )
    body = forms.CharField(widget=forms.Textarea( #HTML Text Area
        attrs={
            "class": "form-control",
            "placeholder": "Leave a comment!"
        })
    )
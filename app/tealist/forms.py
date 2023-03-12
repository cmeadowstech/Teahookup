from django import forms
from .models import comment


class CommentForm(forms.ModelForm):
    content = forms.CharField(
        label="",
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "placeholder": "Please share your thoughts...",
                "rows": 4,
                "cols": 50,
            }
        ),
    )

    class Meta:
        model = comment
        fields = ["content"]

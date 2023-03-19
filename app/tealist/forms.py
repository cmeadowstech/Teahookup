from django import forms
from .models import comment, vendor, location


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
    value = forms.ChoiceField(label="Rating", choices=comment.value.field.choices)

    class Meta:
        model = comment
        fields = ["content", "value"]


class VendorForm(forms.ModelForm):
    name = forms.CharField(
        help_text="The business name of the vendor",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
            }
        ),
    )
    url = forms.CharField(
        help_text="The URL of the vendor",
        widget=forms.URLInput(
            attrs={
                "class": "form-control",
            }
        ),
    )
    url_alt = forms.CharField(
        help_text="An alternate URL, if one exists. Such as for a global site",
        label="Alternative URL",
        required=False,
        widget=forms.URLInput(
            attrs={
                "class": "form-control",
                "placeholder": "Optional",
            }
        ),
    )
    description = forms.CharField(
        help_text="Description of the vendor. Often pulled from about pages or Google summaries",
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": 4,
                "cols": 50,
            }
        ),
    )
    ship_to = forms.ModelMultipleChoiceField(
        label="Ships to",
        help_text="Where does this vendor ship to?",
        queryset=location.objects.all().exclude(ship_to__isnull=True),
        widget=forms.CheckboxSelectMultiple(),
    )
    store_location = forms.ModelMultipleChoiceField(
        queryset=location.objects.all().exclude(store_location__isnull=True),
        help_text="Where does this vendor ship from?",
        widget=forms.CheckboxSelectMultiple(),
    )
    tea_source = forms.ModelMultipleChoiceField(
        help_text="What sort of teas does this vendor sell?",
        queryset=location.objects.all().exclude(tea_source__isnull=True),
        widget=forms.CheckboxSelectMultiple(),
    )

    class Meta:
        model = vendor
        fields = [
            "name",
            "description",
            "store_location",
            "ship_to",
            "tea_source",
            "url",
            "url_alt",
            "variety",
        ]
        widgets = {
            "variety": forms.CheckboxSelectMultiple,
        }

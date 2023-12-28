from django import forms
from .models import *


class CommentForm(forms.ModelForm):
    content = forms.CharField(
        label="",
        widget=forms.Textarea(
            attrs={
                "class": "textarea",
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
                "class": "input",
            }
        ),
    )
    url = forms.CharField(
        help_text="The URL of the vendor",
        widget=forms.URLInput(
            attrs={
                "class": "input",
            }
        ),
    )
    url_alt = forms.CharField(
        help_text="An alternate URL, if one exists. Such as for a global site",
        label="Alternative URL",
        required=False,
        widget=forms.URLInput(
            attrs={
                "class": "input",
                "placeholder": "Optional",
            }
        ),
    )
    description = forms.CharField(
        help_text="Description of the vendor. Often pulled from about pages or Google summaries",
        widget=forms.Textarea(
            attrs={
                "class": "textarea",
                "rows": 4,
                "cols": 50,
            }
        ),
    )
    ship_to = forms.ModelMultipleChoiceField(
        label="Ships to",
        help_text="Where does this vendor ship to?",
        queryset=location.objects.all().exclude(ship_to__isnull=True),
        widget=forms.CheckboxSelectMultiple(attrs={"class": "peer hidden"}),
    )
    store_location = forms.ModelMultipleChoiceField(
        queryset=location.objects.all().exclude(store_location__isnull=True),
        help_text="Where does this vendor ship from?",
        widget=forms.CheckboxSelectMultiple(attrs={"class": "peer hidden"}),
    )
    tea_source = forms.ModelMultipleChoiceField(
        help_text="Where does this vendor source its tea from?",
        queryset=location.objects.all().exclude(tea_source__isnull=True),
        widget=forms.CheckboxSelectMultiple(attrs={"class": "peer hidden"}),
    )
    variety = forms.ModelMultipleChoiceField(
        help_text="What sort of teas does this vendor sell?",
        queryset=variety.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={"class": "peer hidden"}),
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


class CollectionForm(forms.ModelForm):
    name = forms.CharField(
        help_text="What do you want to call this collection?",
        widget=forms.TextInput(
            attrs={
                "class": "input",
            }
        ),
    )
    vendors = forms.ModelMultipleChoiceField(
        help_text="Choose the vendors to add to this collection - up to 10.",
        queryset=vendor.objects.all().exclude(active=False),
        widget=forms.SelectMultiple(
            attrs={
                "id": "input-vendors",
                "placeholder": "Please pick at least three vendors.",
                "autocomplete": "off",
            }
        ),
    )
    content = forms.CharField(
        label="",
        widget=forms.Textarea(
            attrs={
                "id": "SimpleMDE",
                "class": "textarea",
                "placeholder": "Some additional context for this collection, if necessary.",
                "rows": 4,
                "cols": 50,
            }
        ),
    )

    class Meta:
        model = collection
        fields = ["name", "vendors", "content"]

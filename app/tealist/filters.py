import django_filters
from .models import *
from django import forms


class VendorFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        lookup_expr="icontains",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search...",
                "class": "input w-full",
                "autocomplete": "off",
            }
        ),
    )
    store_location = django_filters.ModelMultipleChoiceFilter(
        queryset=location.objects.exclude(store_location__isnull=True),
        widget=forms.CheckboxSelectMultiple(attrs={"class": "peer hidden"}),
    )
    ship_to = django_filters.ModelMultipleChoiceFilter(
        queryset=location.objects.exclude(ship_to__isnull=True),
        widget=forms.CheckboxSelectMultiple(attrs={"class": "peer hidden"}),
    )
    tea_source = django_filters.ModelMultipleChoiceFilter(
        queryset=location.objects.exclude(tea_source__isnull=True),
        widget=forms.CheckboxSelectMultiple(attrs={"class": "peer hidden"}),
    )
    variety = django_filters.ModelMultipleChoiceFilter(
        queryset=variety.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={"class": "peer hidden"}),
    )

    o = django_filters.OrderingFilter(
        fields=(("name", "rating")),
        widget=forms.Select,
    )

    class Meta:
        model = vendor
        fields = ["name", "store_location", "ship_to", "tea_source", "variety"]

    # https://stackoverflow.com/questions/68381768/how-to-set-class-of-orderingfilters-widget-in-django

    def __init__(
        self, data=None, queryset=None, request=None, prefix=None, *args, **kwargs
    ):
        super().__init__(*args, request=request, data=data, **kwargs)

        o = self.form.fields["o"]
        o.widget.attrs = {"class": "select w-full"}


class CollectionFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        lookup_expr="icontains",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search...",
                "class": "input w-full",
                "autocomplete": "off",
            }
        ),
    )

    class Meta:
        model = collection
        fields = ["name"]

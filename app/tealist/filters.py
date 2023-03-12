import django_filters
from .models import vendor, location, variety
from django import forms


class VendorFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        lookup_expr="icontains",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search...",
                "class": "vendor-search w-100",
                "autocomplete": "off",
            }
        ),
    )
    store_location = django_filters.ModelMultipleChoiceFilter(
        queryset=location.objects.exclude(store_location__isnull=True),
        widget=forms.CheckboxSelectMultiple,
    )
    ship_to = django_filters.ModelMultipleChoiceFilter(
        queryset=location.objects.exclude(ship_to__isnull=True),
        widget=forms.CheckboxSelectMultiple,
    )
    tea_source = django_filters.ModelMultipleChoiceFilter(
        queryset=location.objects.exclude(tea_source__isnull=True),
        widget=forms.CheckboxSelectMultiple,
    )
    variety = django_filters.ModelMultipleChoiceFilter(
        queryset=variety.objects.all(), widget=forms.CheckboxSelectMultiple
    )

    o = django_filters.OrderingFilter(fields=(("name", "name")))

    class Meta:
        model = vendor
        fields = ["name", "store_location", "ship_to", "tea_source", "variety"]

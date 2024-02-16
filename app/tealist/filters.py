import django_filters
from .models import *
from django import forms


class VendorFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        lookup_expr="icontains",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search...",
                "class": "input",
                "autocomplete": "off",
            }
        ),
    )
    store_location = django_filters.ModelMultipleChoiceFilter(
        queryset=Location.objects.exclude(store_location__isnull=True),
        widget=forms.CheckboxSelectMultiple(attrs={"class": "peer hidden"}),
    )
    ship_to = django_filters.ModelMultipleChoiceFilter(
        queryset=Location.objects.exclude(ship_to__isnull=True),
        widget=forms.CheckboxSelectMultiple(attrs={"class": "peer hidden"}),
    )
    tea_source = django_filters.ModelMultipleChoiceFilter(
        queryset=Location.objects.exclude(tea_source__isnull=True),
        widget=forms.CheckboxSelectMultiple(attrs={"class": "peer hidden"}),
    )
    variety = django_filters.ModelMultipleChoiceFilter(
        queryset=Variety.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={"class": "peer hidden"}),
    )

    o = django_filters.OrderingFilter(
        fields=(("name", "rating")),
        widget=forms.Select,
    )

    class Meta:
        model = Vendor
        fields = ["name", "store_location", "ship_to", "tea_source", "variety"]

    # https://stackoverflow.com/questions/68381768/how-to-set-class-of-orderingfilters-widget-in-django

    def __init__(
        self, data=None, queryset=None, request=None, prefix=None, *args, **kwargs
    ):
        super().__init__(*args, request=request, data=data, **kwargs)

        o = self.form.fields["o"]
        o.widget.attrs = {"class": "select"}


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
        model = Collection
        fields = ["name"]

class TeaFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(
        lookup_expr="icontains",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search...",
                "class": "input",
                "autocomplete": "off",
            }
        ),
    )
    variety = django_filters.ModelMultipleChoiceFilter(
        queryset=Variety.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={"class": "peer hidden"}),
    )
    on_sale = django_filters.BooleanFilter(widget=forms.CheckboxInput())

    o = django_filters.OrderingFilter(
        fields=(("title")),
        widget=forms.Select,
    )

    class Meta:
        model = Tea
        fields = ["title", "variety"]

    # https://stackoverflow.com/questions/68381768/how-to-set-class-of-orderingfilters-widget-in-django

    def __init__(
        self, data=None, queryset=None, request=None, prefix=None, *args, **kwargs
    ):
        super().__init__(*args, request=request, data=data, **kwargs)

        o = self.form.fields["o"]
        o.widget.attrs = {"class": "select"}
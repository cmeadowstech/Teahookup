import django_filters
from .models import vendor

class VendorFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = vendor
        fields = ['name', 'store_location', 'ship_to', 'tea_source', 'variety']
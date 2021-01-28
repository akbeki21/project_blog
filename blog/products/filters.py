import django_filters

from .models import Product


class ProductFilter(django_filters.FilterSet):
    min_calories  = django_filters.NumberFilter(field_name='calories', lookup_expr='gte')
    max_calories    = django_filters.NumberFilter(field_name='calories', lookup_expr='lte')


    class Meta:
        model  = Product
        fields = ('min_calories', 'max_calories')
from django_filters.rest_framework import FilterSet
from django_filters import NumberFilter, CharFilter

from reviews.models import Title


class TitleFilter(FilterSet):
    """ Фильтр произведений. """
    name = CharFilter(field_name='name', lookup_expr='icontains')
    year = NumberFilter(field_name='year', lookup_expr='icontains')
    category = CharFilter(field_name='category__slug', lookup_expr='icontains')
    genre = CharFilter(field_name='genre__slug', lookup_expr='icontains')

    class Meta:
        model = Title
        fields = ('name', 'year', 'genre', 'category')

from django.db.models import Q
from django_filters import FilterSet, ModelChoiceFilter, CharFilter

from .models import *


class LinkFilter(FilterSet):
    search = CharFilter(method="search_filter", label="Content")
    category = ModelChoiceFilter(queryset=lambda request: Category.objects.all(), label="Category")

    class Meta:
        model = Link
        fields = []

    @staticmethod
    def search_filter(queryset, _, value):
        return queryset.filter(
            Q(title__icontains=value) |
            Q(description__icontains=value) |
            Q(url__icontains=value)
        )

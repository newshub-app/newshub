from rest_framework.serializers import (
    HyperlinkedModelSerializer,
    ModelSerializer
)

from news.models import *

__all__ = [
    "CategorySerializer",
    "LinkSerializer"
]


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]
        read_only_fields = ["id"]


class LinkSerializer(HyperlinkedModelSerializer):
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Link
        fields = ["id", "url", "title", "description", "category", "created", "updated"]
        read_only_fields = ["id", "created", "updated"]

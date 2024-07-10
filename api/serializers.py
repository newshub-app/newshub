from rest_framework.fields import HiddenField, CurrentUserDefault
from rest_framework.relations import SlugRelatedField
from rest_framework.serializers import ModelSerializer

from news.models import *

__all__ = ["CategorySerializer", "LinkSerializer"]


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]
        read_only_fields = ["id", "name"]


class LinkSerializer(ModelSerializer):
    category = SlugRelatedField(slug_field="name", queryset=Category.objects.all())
    created_by = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = Link
        fields = [
            "id",
            "url",
            "title",
            "description",
            "category",
            "date_created",
            "date_updated",
            "created_by",
        ]
        read_only_fields = ["id", "date_created", "date_updated"]

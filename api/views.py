from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from news.models import *
from .serializers import CategorySerializer, LinkSerializer


class CategoryViewSet(ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [SearchFilter]
    search_fields = ["name"]


class LinkViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Link.objects.all()
    serializer_class = LinkSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["category__name"]
    search_fields = ["title", "description", "category__name"]
    ordering_fields = ["date_created", "date_updated"]
    ordering = ["-date_created"]

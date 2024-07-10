from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import PermissionDenied
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
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

    def update(self, request, *args, **kwargs):
        link = self.get_object()
        if link.created_by != request.user:
            return Response(status=PermissionDenied.status_code)
        return super().update(request, *args, **kwargs)

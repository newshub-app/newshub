from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register("category", views.CategoryViewSet)
router.register("link", views.LinkViewSet)

urlpatterns = [
    path("", include(router.urls), name="api"),
]

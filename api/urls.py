from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register("categories", views.CategoryViewSet)
router.register("links", views.LinkViewSet)

app_name = "api"
urlpatterns = [
    path("", include(router.urls), name="api"),
]

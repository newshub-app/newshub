from django.urls import path

from .views import *

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("links/", LinkListView.as_view(), name="links"),
    path("links/<int:pk>/", LinkUpdateView.as_view(), name="link_update"),
    path("links/new/", LinkCreateView.as_view(), name="link_create"),
]

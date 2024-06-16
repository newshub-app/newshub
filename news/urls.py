from django.urls import path

from .views import *

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("links/", LinksListView.as_view(), name="links"),
    path("link/<int:pk>/", LinkDetailView.as_view(), name="link"),
    path("link/new/", LinkCreateView.as_view(), name="link_create"),
]

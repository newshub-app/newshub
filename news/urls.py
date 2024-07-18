from django.urls import path

from .views import *

app_name = "news"
urlpatterns = [
    path("", LinkListView.as_view(), name="links"),
    path("links/<int:pk>/", LinkUpdateView.as_view(), name="link_update"),
    path("links/new/", LinkCreateView.as_view(), name="link_create"),
    path("newsletters/", NewsletterListView.as_view(), name="newsletters"),
]

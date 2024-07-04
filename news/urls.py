from django.urls import path
from django.views.decorators.cache import cache_page

from .views import *

app_name = "news"
urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("links/", cache_page(60 * 15)(LinkListView.as_view()), name="links"),
    path("links/<int:pk>/", LinkUpdateView.as_view(), name="link_update"),
    path("links/new/", LinkCreateView.as_view(), name="link_create"),
    path(
        "newsletters/",
        cache_page(60 * 15)(NewsletterListView.as_view()),
        name="newsletters",
    ),
]

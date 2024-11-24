from django.urls import path

from .views import *

app_name = "news"
urlpatterns = [
    path("", LinkListView.as_view(), name="index"),
    path("<int:pk>/", LinkUpdateView.as_view(), name="link_update"),
    path("new/", LinkCreateView.as_view(), name="link_create"),
    path("newsletters/", NewsletterListView.as_view(), name="newsletters"),
    path("feeds/", FeedListView.as_view(), name="feeds"),
    path("feeds/new/", FeedCreateView.as_view(), name="feed_create"),
]

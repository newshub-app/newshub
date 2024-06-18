from django.urls import path

from .views import *

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("login/", LoginView.as_view(), name="login"),
    path("register/", RegisterView.as_view(), name="register"),
    path("links/", LinkListView.as_view(), name="links"),
    path("links/<int:pk>/", LinkUpdateView.as_view(), name="link_update"),
    path("links/new/", LinkCreateView.as_view(), name="link_create"),
]

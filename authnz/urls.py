from django.urls import path, include

from .views import *

app_name = "authnz"
urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("", include("django.contrib.auth.urls")),
]

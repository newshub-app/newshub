from django.urls import path, include

from .views import *

urlpatterns = [
    # path("login/", LoginView.as_view(), name="login"),
    path("register/", RegisterView.as_view(), name="register"),
    path("", include("django.contrib.auth.urls"))
]

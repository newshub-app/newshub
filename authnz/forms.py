from django.contrib.auth.forms import (
    UserCreationForm,
    ReadOnlyPasswordHashField,
    UsernameField,
)
from django.forms import ModelForm, EmailField, CharField
from django.urls import reverse_lazy

from .models import *


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email"]


class UserForm(ModelForm):
    api_token = CharField(label="API token", required=False, disabled=True)
    password = ReadOnlyPasswordHashField(
        label="Password",
        help_text="To change your password, use <a href={reset_pw_link}>this form</a>.",
    )

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "subscribe_new_categories",
            "api_token",
            "password",
        ]
        field_classes = {"username": UsernameField, "email": EmailField}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        password = self.fields.get("password")
        if password:
            password.help_text = password.help_text.format(
                reset_pw_link=reverse_lazy("authnz:password_change")
            )

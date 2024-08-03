from django.contrib.auth.forms import (
    UserCreationForm,
    ReadOnlyPasswordHashField,
    UsernameField,
)
from django.forms import (
    ModelForm,
    EmailField,
    CharField,
    ModelMultipleChoiceField,
    CheckboxSelectMultiple,
)
from django.urls import reverse_lazy

from news.models import Category
from .models import User


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email"]


class UserForm(ModelForm):
    subscribed_categories = ModelMultipleChoiceField(
        queryset=Category.objects.all(), required=False, widget=CheckboxSelectMultiple
    )
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
            "subscribed_categories",
            "api_token",
            "password",
        ]
        field_classes = {"username": UsernameField, "email": EmailField}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set initial values for subscribed_categories
        self.fields[
            "subscribed_categories"
        ].initial = self.instance.subscribed_categories.all().values_list(
            "id", flat=True
        )

        # Set password help text
        password = self.fields.get("password")
        if password:
            password.help_text = password.help_text.format(
                reset_pw_link=reverse_lazy("authnz:password_change")
            )

    def save(self, *args, **kwargs):
        instance = super().save(*args, **kwargs)
        instance.subscribed_categories.set(self.cleaned_data["subscribed_categories"])
        return instance

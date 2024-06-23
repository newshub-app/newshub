from django.forms import ModelForm, URLField

from .models import *


class LinkForm(ModelForm):
    url = URLField(label="URL")

    class Meta:
        model = Link
        fields = ["url", "title", "description", "category"]

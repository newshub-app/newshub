from django.forms import ModelForm

from .models import *


class LinkForm(ModelForm):
    class Meta:
        model = Link
        fields = ["url", "title", "description", "category"]

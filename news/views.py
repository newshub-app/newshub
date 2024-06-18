from django import urls
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.http import HttpResponseNotAllowed
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, CreateView, UpdateView, FormView

from .models import *


class LoginView(FormView):
    template_name = "login.html"
    form_class = AuthenticationForm
    success_url = reverse_lazy("index")


class RegisterView(FormView):
    template_name = "register.html"
    form_class = UserCreationForm
    success_url = reverse_lazy("index")


class IndexView(TemplateView):
    template_name = "index.html"


class LinkListView(ListView):
    model = Link
    context_object_name = "links"
    ordering = ["-created"]
    paginate_by = 10


class LinkCreateView(CreateView):
    model = Link
    fields = ["url", "title", "description", "category"]
    success_url = urls.reverse_lazy("links")

    def get(self, request, *args, **kwargs):
        return HttpResponseNotAllowed(["POST"])


class LinkUpdateView(UpdateView):
    model = Link
    fields = ["url", "title", "description", "category"]
    success_url = urls.reverse_lazy("links")

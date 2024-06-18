from django import urls
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseNotAllowed
from django.views.generic import ListView, TemplateView, CreateView, UpdateView, FormView

from .models import *


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = "index.html"


class LinkListView(LoginRequiredMixin, ListView):
    model = Link
    context_object_name = "links"
    ordering = ["-created"]
    paginate_by = 10


class LinkCreateView(LoginRequiredMixin, CreateView):
    model = Link
    fields = ["url", "title", "description", "category"]
    success_url = urls.reverse_lazy("links")

    def get(self, request, *args, **kwargs):
        return HttpResponseNotAllowed(["POST"])


class LinkUpdateView(LoginRequiredMixin, UpdateView):
    model = Link
    fields = ["url", "title", "description", "category"]
    success_url = urls.reverse_lazy("links")

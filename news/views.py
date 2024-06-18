from django import urls
from django.http import HttpResponseNotAllowed
from django.views.generic import ListView, TemplateView, CreateView, UpdateView

from .models import *


class IndexView(TemplateView):
    template_name = "news/index.html"


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

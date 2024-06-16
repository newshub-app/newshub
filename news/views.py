from django.views.generic import ListView, DetailView, TemplateView, CreateView
from django import urls

from .models import *


class IndexView(TemplateView):
    template_name = "news/index.html"


class LinksListView(ListView):
    model = Link
    template_name = "news/links.html"
    context_object_name = "links"
    ordering = ["-created"]
    paginate_by = 10


class LinkDetailView(DetailView):
    model = Link
    template_name = "news/link-details.html"
    context_object_name = "link"


class LinkCreateView(CreateView):
    model = Link
    fields = ["url", "title", "description", "category"]
    success_url = urls.reverse_lazy("links")

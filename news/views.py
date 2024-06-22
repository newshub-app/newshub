from django import urls
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseNotAllowed
from django.views.generic import TemplateView, CreateView, UpdateView
from django_filters.views import FilterView

from .filters import LinkFilter
from .models import *


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = "index.html"


class LinkListView(LoginRequiredMixin, FilterView):
    model = Link
    context_object_name = "links"
    template_name_suffix = "_list"
    ordering = ["-created"]
    paginate_by = 5
    filterset_class = LinkFilter


class LinkCreateView(LoginRequiredMixin, CreateView):
    model = Link
    fields = ["url", "title", "description", "category"]
    success_url = urls.reverse_lazy("news:links")

    def get(self, request, *args, **kwargs):
        return HttpResponseNotAllowed(["POST"])


class LinkUpdateView(LoginRequiredMixin, UpdateView):
    model = Link
    fields = ["url", "title", "description", "category"]
    success_url = urls.reverse_lazy("news:links")

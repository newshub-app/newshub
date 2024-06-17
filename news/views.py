from django.http import HttpResponseNotAllowed
from django.views.generic import ListView, DetailView, TemplateView, CreateView
from django import urls

from .models import *


class IndexView(TemplateView):
    template_name = "news/index.html"


class LinkListView(ListView):
    model = Link
    context_object_name = "links"
    ordering = ["-created"]
    paginate_by = 10


class LinkDetailView(DetailView):
    model = Link
    context_object_name = "link"


class LinkCreateView(CreateView):
    model = Link
    fields = ["url", "title", "description", "category"]
    success_url = urls.reverse_lazy("links")

    def get(self, request, *args, **kwargs):
        return HttpResponseNotAllowed(["POST"])

    def get_success_url(self):
        return urls.reverse("link_detail", kwargs={"pk": self.object.pk})

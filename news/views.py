from django import urls
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseNotAllowed
from django.views.generic import TemplateView, CreateView, UpdateView, ListView
from django_filters.views import FilterView

from .filters import LinkFilter
from .models import *


class OwnerRequiredUpdateView(LoginRequiredMixin, UpdateView):
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.created_by != request.user and not request.user.is_staff:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = "news/index.html"


class LinkListView(LoginRequiredMixin, FilterView):
    model = Link
    context_object_name = "links"
    template_name = "news/link_list.html"
    ordering = ["-created"]
    paginate_by = 5
    filterset_class = LinkFilter


class LinkCreateView(LoginRequiredMixin, CreateView):
    model = Link
    fields = ["url", "title", "description", "category"]
    success_url = urls.reverse_lazy("news:links")

    def get(self, request, *args, **kwargs):
        return HttpResponseNotAllowed(["POST"])

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class LinkUpdateView(OwnerRequiredUpdateView):
    model = Link
    fields = ["url", "title", "description", "category"]
    template_name = "news/link_update.html"
    success_url = urls.reverse_lazy("news:links")


class NewsletterListView(LoginRequiredMixin, ListView):
    model = Newsletter
    context_object_name = "newsletters"
    template_name = "news/newsletter_list.html"
    ordering = ["-date_sent"]
    paginate_by = 10

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView, UpdateView

from .forms import *


class RegisterView(FormView):
    template_name = "authnz/register.html"
    form_class = SignUpForm
    success_url = reverse_lazy("news:index")


class ProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserForm
    template_name = "authnz/profile.html"
    success_url = reverse_lazy("news:links")

    def get_object(self, queryset=None):
        return self.request.user

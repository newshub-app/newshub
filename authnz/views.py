from django.views.generic import FormView

from .forms import *


class RegisterView(FormView):
    template_name = "authnz/register.html"
    form_class = SignUpForm
    success_url = reverse_lazy("news:index")

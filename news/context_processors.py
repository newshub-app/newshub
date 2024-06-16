from .forms import LinkForm


def new_link_form(request):
    return {"new_link_form": LinkForm()}

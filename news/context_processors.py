from .forms import LinkForm, FeedForm


def modal_forms(_):
    return {
        "new_link_form": LinkForm(),
        "new_feed_form": FeedForm(),
    }

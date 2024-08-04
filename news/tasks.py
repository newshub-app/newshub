import re

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db.models import Q
from django.template.loader import render_to_string

from authnz.models import User
from newshub.celery import app
from .models import Newsletter, Link

RE_EMPTY_LINES = re.compile(r"(\n *){3,}", re.MULTILINE)


@app.task
def send_newsletter():
    print("Preparing newsletter")

    links = Link.objects.filter(newsletter__isnull=True)
    total_links = links.count()
    if total_links == 0:
        print("No new links to add to the newsletter")
        return True
    print(f"Adding {total_links} links to the newsletter")

    print("Gathering newsletter recipients")
    users = User.objects.filter(~Q(email=""))  # Exclude users without email
    recipients = users.values_list("email", flat=True)
    if len(recipients) == 0:
        print("No users to send newsletter to")
        return False

    newsletter = Newsletter.objects.create()
    newsletter.recipients.set(users)
    links.update(newsletter=newsletter)

    ctx = {"newsletter": newsletter}

    messages_sent = 0
    messages_total = 0
    for user in users:
        messages_total += 1
        ctx["user"] = user

        try:
            print(f"Generating newsletter content for {user.email}")
            html_content = render_to_string("news/newsletter.html.tpl", context=ctx)
            text_content = render_to_string("news/newsletter.txt.tpl", context=ctx)
            text_content = RE_EMPTY_LINES.sub(r"\n\n", text_content)

            # FIXME: build links list before rendering and only send email if there are links
            print(f"Sending newsletter to {user.email}")
            message = EmailMultiAlternatives(
                subject="NewsHub newsletter",
                body=text_content,
                from_email=settings.EMAIL_FROM,
                to=[user.email],
            )
            message.attach_alternative(html_content, "text/html")
            messages_sent += message.send(fail_silently=True)
        except Exception as e:
            print(f"Failed to send newsletter to {user.email}: {e}")
            continue

    if messages_sent > 0:
        print(f"Newsletter sent successfully ({messages_sent}/{messages_total} sent)")
    else:
        print(f"Newsletter sent successfully ({messages_sent}/{messages_total} sent)")
        newsletter.delete()
        return False
    return True

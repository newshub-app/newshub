from django.core.mail import EmailMultiAlternatives
from django.db.models import Q
from django.template.loader import render_to_string

from authnz.models import User
from newshub.celery import app
from .models import Newsletter, Link


@app.task
def send_newsletter():
    print("Preparing newsletter")
    users = User.objects.filter(~Q(email=""))
    newsletter = Newsletter.objects.create()
    links = Link.objects.filter(newsletter__isnull=True)
    if links.count() == 0:
        print("No new links to add to the newsletter")
        return True
    for link in links:
        print(f"Adding link to newsletter: {link.title}")
    print(f"Added {links.count()} links to the newsletter")

    print("Generating newsletter content")
    recipients = users.values_list("email", flat=True)
    if len(recipients) == 0:
        print("No users to send newsletter to")
        return False
    ctx = {
        "links": links,
        "archives_url": "#",
    }
    html_content = render_to_string("news/newsletter.html", context=ctx)
    text_content = render_to_string("news/newsletter.txt.html", context=ctx)

    print(f"Sending newsletter to {len(recipients)} users: {', '.join(recipients)}")
    message = EmailMultiAlternatives(
        subject="NewsHub newsletter",
        body=text_content,
        # from_email=settings.EMAIL_FROM,
        bcc=recipients,
    )
    message.attach_alternative(html_content, "text/html")
    messages_sent = message.send(fail_silently=True)

    if messages_sent > 0:
        print("Newsletter sent successfully")
        links.update(newsletter=newsletter)
        newsletter.recipients.set(users)
        newsletter.mailout_success = True
        newsletter.save()
    else:
        print("Failed to send newsletter")
        newsletter.delete()
        return False
    return True

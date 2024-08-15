import re
from itertools import groupby

from celery.utils.log import get_task_logger
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db.models import Q
from django.template.loader import render_to_string

from authnz.models import User
from news.models import Newsletter, Link
from newshub.celery import app

RE_EMPTY_LINES = re.compile(r"(\n *){3,}", re.MULTILINE)

logger = get_task_logger(__name__)

__all__ = ["send_newsletter"]


@app.task
def send_newsletter():
    logger.info("Preparing newsletter")

    links = Link.objects.filter(newsletter__isnull=True)
    total_links = links.count()
    if total_links == 0:
        logger.warn("No new links to add to the newsletter")
        return True
    logger.debug(f"Adding {total_links} links to the newsletter")

    logger.debug("Gathering newsletter recipients")
    users = User.objects.filter(~Q(email=""))  # Exclude users without email
    recipients = users.values_list("email", flat=True)
    if len(recipients) == 0:
        logger.warn("No users to send newsletter to")
        return False

    newsletter = Newsletter.objects.create()
    newsletter.recipients.set(users)
    links.update(newsletter=newsletter)

    ctx = {"newsletter": newsletter}

    messages_sent = 0
    messages_total = 0
    for user in users:
        ctx["user"] = user

        try:
            logger.info(f"Generating newsletter content for {user.email}")
            user_links = []
            links = newsletter.get_links_data()
            for category, links in groupby(links, key=lambda i: i["category__name"]):
                if user.subscribed_categories.filter(name=category).exists():
                    user_links.append({"category": category, "links": list(links)})
            if not user_links:
                logger.info(f"No new links for {user.email}")
                continue
            ctx["links"] = user_links

            html_content = render_to_string("news/newsletter.html.tpl", context=ctx)
            text_content = render_to_string("news/newsletter.txt.tpl", context=ctx)
            text_content = RE_EMPTY_LINES.sub(r"\n\n", text_content)

            logger.info(f"Sending newsletter to {user.email}")
            messages_total += 1
            message = EmailMultiAlternatives(
                subject="NewsHub newsletter",
                body=text_content,
                from_email=settings.EMAIL_FROM,
                to=[user.email],
            )
            message.attach_alternative(html_content, "text/html")
            messages_sent += message.send(fail_silently=True)
        except Exception as e:
            logger.error(f"Failed to send newsletter to {user.email}: {e}")
            continue

    if messages_sent > 0:
        partial_send = " partially" if messages_sent < messages_total else ""
        log_msg = f"Newsletter #{newsletter.id} sent{partial_send} successfully ({messages_sent}/{messages_total} sent)"
        if partial_send:
            logger.warn(log_msg)
            return False
        logger.info(log_msg)
        return True
    elif messages_total == 0:
        logger.warn(f"Newsletter #{newsletter.id} was not sent to any user")
        return True
    else:
        logger.error(f"Failed to send newsletter #{newsletter.id}")
        newsletter.delete()
        return False

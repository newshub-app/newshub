from celery.schedules import crontab

from .celery import app

__all__ = ["send_newsletter"]


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(
            minute="*/5"
        ),  # TODO: send newsletter evert monday morning by default (once implemented)
        send_newsletter.s(),
    )


@app.task(bind=True, ignore_result=True)
def send_newsletter(_):
    print("Preparing newsletter...")
    print("Sending newsletter to users...")
    print("Newsletter sent successfully")

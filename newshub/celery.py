import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "newshub.settings")
app = Celery("newshub")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


@app.on_after_finalize.connect
def setup_periodic_tasks(*_, **__):
    from django_celery_beat.models import PeriodicTask, IntervalSchedule

    # create schedules
    schedule = IntervalSchedule.objects.get_or_create(
        every=5, period=IntervalSchedule.MINUTES
    )

    # create periodic tasks
    PeriodicTask.objects.get_or_create(
        interval=schedule,
        name="Send newsletter",
        task="news.tasks.send_newsletter",
    )

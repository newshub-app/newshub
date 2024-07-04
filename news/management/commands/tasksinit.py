from django.conf import settings
from django.core.management.base import BaseCommand
from django_celery_beat.models import IntervalSchedule, PeriodicTask


class Command(BaseCommand):
    help = "Initialize periodic tasks"

    def add_arguments(self, parser):
        parser.add_argument(
            "--newsletter-every",
            default=settings.NEWSLETTER_EVERY,
            type=int,
            help="Number of interval periods between newsletters",
        )
        parser.add_argument(
            "--newsletter-period",
            default=settings.NEWSLETTER_PERIOD,
            choices=[
                IntervalSchedule.SECONDS,
                IntervalSchedule.MINUTES,
                IntervalSchedule.HOURS,
                IntervalSchedule.DAYS,
            ],
            help="Type of period for newsletter interval",
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Initializing periodic tasks"))

        # create newsletter schedule
        self.stdout.write(self.style.NOTICE("Creating schedules..."))
        newsletter_schedule, created = IntervalSchedule.objects.get_or_create(
            every=options["newsletter_every"],
            period=options["newsletter_period"],
        )
        if created:
            self.stdout.write(
                self.style.SUCCESS(f"Created schedule: {newsletter_schedule}")
            )
        else:
            self.stdout.write(
                self.style.WARNING(f"Schedule already exists: {newsletter_schedule}")
            )

        # create newsletter task
        self.stdout.write(self.style.NOTICE("Creating scheduled tasks..."))
        newsletter_task, created = PeriodicTask.objects.get_or_create(
            interval=newsletter_schedule,
            name="Send newsletter",
            task="news.tasks.send_newsletter",
        )
        if created:
            self.stdout.write(
                self.style.SUCCESS(f"Task created: {newsletter_task.name}")
            )
        else:
            self.stdout.write(
                self.style.WARNING(f"Task already exists: {newsletter_task.name}")
            )

        self.stdout.write(self.style.SUCCESS("Done initializing periodic tasks"))

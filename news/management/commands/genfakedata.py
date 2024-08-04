import random

from django.core.management.base import BaseCommand
from faker import Faker

from authnz.models import *
from news.models import *


class Command(BaseCommand):
    help = "Generate fake data for testing"

    def add_arguments(self, parser):
        parser.add_argument(
            "--users", type=int, default=0, help="Amount of users to generate"
        )
        parser.add_argument(
            "--categories", type=int, default=0, help="Amount of categories to generate"
        )
        parser.add_argument("--links", type=int, default=0, help="Generate links")

    def handle(self, *args, **options):
        fake = Faker()
        users = [u for u in User.objects.all()]
        categories = [c for c in Category.objects.all()]

        for _ in range(options["users"]):
            password = fake.password(length=20)
            user = User.objects.create_user(
                username=fake.user_name(),
                email=fake.email(),
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                password=password,
            )
            users.append(user)
            self.stdout.write(
                self.style.NOTICE(
                    f"New user: username={user.username} password={password}"
                )
            )
        self.stdout.write(self.style.SUCCESS(f"Generated {options['users']} users"))

        for _ in range(options["categories"]):
            known_cats = Category.objects.values_list("name", flat=True)
            cat_name = fake.word()
            while cat_name in known_cats:
                cat_name = fake.word()
            cat = Category.objects.create(
                name=cat_name,
            )
            self.stdout.write(self.style.NOTICE(f"New category: {cat.name}"))
            categories.append(cat)
        self.stdout.write(
            self.style.SUCCESS(f"Generated {options['categories']} categories")
        )

        for _ in range(options["links"]):
            known_urls = Link.objects.values_list("url", flat=True)
            url = fake.url()
            while url in known_urls:
                url = fake.url()
            title = fake.sentence(nb_words=10)
            while len(title) > 100:
                title = fake.sentence(nb_words=10)
            link = Link.objects.create(
                url=url,
                title=title,
                description=fake.paragraph(nb_sentences=15),
                category=random.choice(categories),
                created_by=random.choice(users),
            )
            self.stdout.write(self.style.NOTICE(f"New link: {link.url}"))
        self.stdout.write(self.style.SUCCESS(f"Generated {options['links']} links"))

        self.stdout.write(self.style.SUCCESS("Done generating fake data"))

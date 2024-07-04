import random

from django.core.management.base import BaseCommand
from faker import Faker

from authnz.models import *
from news.models import *


class Command(BaseCommand):
    help = "Generate fake data for testing"

    def add_arguments(self, parser):
        parser.add_argument("--users", action="store_true", help="Generate users")
        parser.add_argument(
            "--num-users", default=5, type=int, help="Number of users to generate"
        )

        parser.add_argument(
            "--categories", action="store_true", help="Generate categories"
        )
        parser.add_argument(
            "--num-categories",
            default=10,
            type=int,
            help="Number of categories to generate",
        )

        parser.add_argument("--links", action="store_true", help="Generate links")
        parser.add_argument(
            "--num-links", default=200, type=int, help="Number of links to generate"
        )

    def handle(self, *args, **options):
        fake = Faker()
        num_users = options["num_users"]
        num_categories = options["num_categories"]
        num_links = options["num_links"]
        users = [u for u in User.objects.all()]
        categories = [c for c in Category.objects.all()]
        links = []

        if options["users"]:
            for _ in range(num_users):
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
            self.stdout.write(self.style.SUCCESS(f"Generated {len(users)} users"))

        if options["categories"]:
            for _ in range(num_categories):
                known_cats = Category.objects.values_list("name", flat=True)
                cat_name = fake.word()
                while cat_name in known_cats:
                    cat_name = fake.word()
                cat = Category.objects.create(
                    name=fake.word(),
                )
                self.stdout.write(self.style.NOTICE(f"New category: {cat.name}"))
                categories.append(cat)
            self.stdout.write(
                self.style.SUCCESS(f"Generated {len(categories)} categories")
            )

        if options["links"]:
            for _ in range(num_links):
                known_urls = Link.objects.values_list("url", flat=True)
                url = fake.url()
                while url in known_urls:
                    url = fake.url()
                link = Link.objects.create(
                    url=url,
                    title=fake.text(max_nb_chars=100),
                    description=fake.paragraph(),
                    category=random.choice(categories),
                    created_by=random.choice(users),
                )
                self.stdout.write(self.style.NOTICE(f"New link: {link.url}"))
                links.append(link)
            self.stdout.write(self.style.SUCCESS(f"Generated {len(links)} links"))

        self.stdout.write(self.style.SUCCESS("Done generating fake data"))

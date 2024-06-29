from random import randrange

from django.core.management.base import BaseCommand
from faker import Faker

from authnz.models import *
from news.models import *


class Command(BaseCommand):
    help = "Generate fake data for testing"

    def add_arguments(self, parser):
        parser.add_argument(
            "--num-users", default=5, type=int, help="Number of users to generate"
        )
        parser.add_argument(
            "--num-categories",
            default=10,
            type=int,
            help="Number of categories to generate",
        )
        parser.add_argument(
            "--num-links", default=200, type=int, help="Number of links to generate"
        )

    def handle(self, *args, **options):
        fake = Faker()
        num_users = options["num_users"]
        num_categories = options["num_categories"]
        num_links = options["num_links"]
        users = []
        categories = []
        links = []

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
            self.stdout.write("New user: username={user.username} password={password}")
        self.stdout.write(self.style.SUCCESS(f"Generated {len(users)} users"))

        for _ in range(num_categories):
            cat = Category.objects.create(
                name=fake.word(),
            )
            categories.append(cat)
        self.stdout.write(self.style.SUCCESS(f"Generated {len(categories)} categories"))

        for _ in range(num_links):
            url = fake.url()
            while url in [link.url for link in links]:
                url = fake.url()
            link = Link.objects.create(
                url=url,
                title=fake.text(max_nb_chars=100),
                description=fake.paragraph(),
                category=categories[randrange(len(categories))],
                created_by=users[randrange(len(users))],
            )
            links.append(link)
        self.stdout.write(self.style.SUCCESS(f"Generated {len(links)} links"))

        self.stdout.write(self.style.SUCCESS("Done generating fake data"))

import hashlib
from random import SystemRandom

from django.contrib.auth.models import AbstractUser, Group as BaseGroup
from django.db import models

__all__ = ["User", "Group"]


def generate_api_token():
    rand = SystemRandom()
    rand_bytes = rand.randbytes(40)
    return hashlib.sha1(rand_bytes).hexdigest()


class User(AbstractUser):
    api_token = models.CharField(max_length=40, null=False, default=generate_api_token)
    subscribe_new_categories = models.BooleanField(default=True)

    def get_full_name(self):
        full_name = f"{self.first_name} {self.last_name}".strip()
        if full_name:
            return full_name
        return self.username


class Group(BaseGroup):
    class Meta:
        proxy = True

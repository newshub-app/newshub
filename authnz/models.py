import hashlib
from random import SystemRandom

from django.contrib.auth.models import AbstractUser, Group as BaseGroup
from django.db.models import CharField

__all__ = ["User", "Group"]


def generate_api_key():
    rand = SystemRandom()
    rand_bytes = rand.randbytes(40)
    return hashlib.sha1(rand_bytes).hexdigest()


class User(AbstractUser):
    api_key = CharField(max_length=40, null=False, default=generate_api_key)


class Group(BaseGroup):
    class Meta:
        proxy = True

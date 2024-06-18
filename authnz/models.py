from django.contrib.auth.models import AbstractUser, Group as BaseGroup

__all__ = ["User", "Group"]


class User(AbstractUser):
    pass


class Group(BaseGroup):
    class Meta:
        proxy = True

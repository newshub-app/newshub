from django.db import models

from authnz.models import User

__all__ = ["Newsletter", "Category", "Link"]


class Newsletter(models.Model):
    date_sent = models.DateTimeField(auto_now_add=True)
    mailout_success = models.BooleanField(default=False)
    recipients = models.ManyToManyField(User)


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "categories"


class Link(models.Model):
    url = models.URLField(unique=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    newsletter = models.ForeignKey(
        Newsletter, on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self):
        return self.title

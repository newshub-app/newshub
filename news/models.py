from django.conf import settings
from django.db import models

__all__ = ["Newsletter", "Category", "Link"]


class Newsletter(models.Model):
    date_sent = models.DateTimeField(auto_now_add=True)
    recipients = models.ManyToManyField(settings.AUTH_USER_MODEL)

    def get_links_data(self):
        return self.link_set.values(
            "title",
            "url",
            "description",
            "category__name",
            "created_by__first_name",
            "created_by__last_name",
            "created_by__username",
        ).order_by("category__name")


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
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    newsletter = models.ForeignKey(
        Newsletter, on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return self.title

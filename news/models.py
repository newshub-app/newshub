from django.conf import settings
from django.db import models

__all__ = ["Newsletter", "Category", "Link"]


class Newsletter(models.Model):
    date_sent = models.DateTimeField(auto_now_add=True)
    recipients = models.ManyToManyField(settings.AUTH_USER_MODEL)

    def get_links_categories(self):
        categories = set()
        for link in self.link_set.all():
            categories.add(link.category.name)
        return categories


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
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    newsletter = models.ForeignKey(
        Newsletter, on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self):
        return self.title

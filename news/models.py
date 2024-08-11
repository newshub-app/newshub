import feedparser
from django.contrib.auth import get_user_model
from django.db import models

__all__ = ["Newsletter", "Category", "Link", "Feed", "FeedLink"]

User = get_user_model()


class Newsletter(models.Model):
    date_sent = models.DateTimeField(auto_now_add=True)
    recipients = models.ManyToManyField(User)

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


# TODO: use signals to automatically subscribe users
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    subscribers = models.ManyToManyField(
        User,
        related_name="subscribed_categories",
        default=User.objects.all(),
    )

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
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    newsletter = models.ForeignKey(
        Newsletter, on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return self.title


class Feed(models.Model):
    class FeedType(models.TextChoices):
        RSS = "rss"

    url = models.URLField(unique=True)
    title = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    type = models.CharField(
        max_length=50, choices=FeedType.choices, default=FeedType.RSS
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    last_feed_update = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title or self.url

    def save(self, *args, **kwargs):
        if not self.pk:
            if None in (self.title, self.description):
                if self.type == Feed.FeedType.RSS:
                    data = feedparser.parse(self.url)
                    if self.title is None:
                        self.title = data.feed.get("title")
                    if self.description is None:
                        desc_field = None
                        if data.feed.version.startswith("rss"):
                            desc_field = "description"
                        elif data.feed.version.startswith("atom"):
                            desc_field = "subtitle"
                        if desc_field is not None:
                            self.description = data.feed.get(desc_field)
        return super().save(*args, **kwargs)


class FeedLink(models.Model):
    url = models.URLField(unique=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    author = models.CharField(max_length=100)
    date_published = models.DateTimeField()
    selected = models.BooleanField(default=False)
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE, related_name="links")

    def __str__(self):
        return self.url

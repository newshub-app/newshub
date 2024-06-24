from django.contrib import admin

from .models import *


class NewsletterAdmin(admin.ModelAdmin):
    list_display = ["date_sent", "mailout_success"]
    search_fields = [
        "recipients__username",
        "recipients__email",
        "links__title",
        "links__description",
        "links__url",
        "links__category__name",
    ]
    list_filter = ["date_sent", "mailout_success"]
    date_hierarchy = "date_sent"


class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]


class LinkAdmin(admin.ModelAdmin):
    list_display = ["title", "category", "url", "created", "updated"]
    search_fields = ["title", "category__name", "url", "description"]
    list_filter = [
        "category",
        "created",
        "newsletter__date_sent",
        "newsletter__mailout_success",
    ]
    date_hierarchy = "created"


admin.site.register(Newsletter, NewsletterAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Link, LinkAdmin)

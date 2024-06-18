from django.contrib import admin
from django.contrib.auth.admin import (
    UserAdmin,
    GroupAdmin
)

from .models import *


class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]


class LinkAdmin(admin.ModelAdmin):
    list_display = ["title", "category", "created", "updated"]
    search_fields = ["title", "description", "category__name"]
    list_filter = ["category", "created", "updated"]
    date_hierarchy = "created"


admin.site.register(User, UserAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Link, LinkAdmin)

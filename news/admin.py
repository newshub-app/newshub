from django.contrib import admin
from django_celery_beat.admin import (
    ClockedScheduleAdmin as BaseClockedScheduleAdmin,
    CrontabScheduleAdmin as BaseCrontabScheduleAdmin,
    PeriodicTaskAdmin as BasePeriodicTaskAdmin,
    PeriodicTaskForm,
    TaskSelectWidget,
)
from django_celery_beat.models import (
    PeriodicTask,
    IntervalSchedule,
    CrontabSchedule,
    SolarSchedule,
    ClockedSchedule,
)
from unfold.admin import ModelAdmin
from unfold.widgets import UnfoldAdminSelectWidget, UnfoldAdminTextInputWidget

from .models import *

admin.site.unregister(PeriodicTask)
admin.site.unregister(IntervalSchedule)
admin.site.unregister(CrontabSchedule)
admin.site.unregister(SolarSchedule)
admin.site.unregister(ClockedSchedule)


@admin.register(Newsletter)
class NewsletterAdmin(ModelAdmin):
    list_display = ["date_sent"]
    search_fields = [
        "recipients__username",
        "recipients__email",
        "links__title",
        "links__description",
        "links__url",
        "links__category__name",
    ]
    list_filter = ["date_sent"]
    date_hierarchy = "date_sent"


@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ["name", "subscribers_count"]
    search_fields = ["name", "subscribers__username", "subscribers__email"]

    @staticmethod
    def subscribers_count(obj):
        return obj.subscribers.count()


@admin.register(Link)
class LinkAdmin(ModelAdmin):
    list_display = ["title", "category", "url", "date_created", "date_updated"]
    search_fields = ["title", "category__name", "url", "description"]
    list_filter = [
        "category",
        "date_created",
        "newsletter__date_sent",
    ]
    date_hierarchy = "date_created"


@admin.register(Feed)
class FeedAdmin(ModelAdmin):
    list_display = ["title", "description", "last_feed_update"]
    search_fields = ["url", "title", "description"]
    list_filter = ["last_feed_update"]
    date_hierarchy = "last_feed_update"


class UnfoldTaskSelectWidget(UnfoldAdminSelectWidget, TaskSelectWidget):
    pass


class UnfoldPeriodicTaskForm(PeriodicTaskForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["task"].widget = UnfoldAdminTextInputWidget()
        self.fields["regtask"].widget = UnfoldTaskSelectWidget()


@admin.register(PeriodicTask)
class PeriodicTaskAdmin(BasePeriodicTaskAdmin, ModelAdmin):
    form = UnfoldPeriodicTaskForm


@admin.register(IntervalSchedule)
class IntervalScheduleAdmin(ModelAdmin):
    pass


@admin.register(CrontabSchedule)
class CrontabScheduleAdmin(BaseCrontabScheduleAdmin, ModelAdmin):
    pass


@admin.register(SolarSchedule)
class SolarScheduleAdmin(ModelAdmin):
    pass


@admin.register(ClockedSchedule)
class ClockedScheduleAdmin(BaseClockedScheduleAdmin, ModelAdmin):
    pass

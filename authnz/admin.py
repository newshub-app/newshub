from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, GroupAdmin

from .models import *

admin.site.register(User, UserAdmin)
admin.site.register(Group, GroupAdmin)

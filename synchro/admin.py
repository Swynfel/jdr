from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import *


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False

class ProfileUserAdmin(UserAdmin):
    inlines = (ProfileInline, )

admin.site.unregister(User)
admin.site.register(User, ProfileUserAdmin)

admin.site.register(Profile)
admin.site.register(Slot)
admin.site.register(Tag)
admin.site.register(System)
admin.site.register(Activity)
admin.site.register(PlayerRequest)
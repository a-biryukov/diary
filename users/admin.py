from django.contrib import admin

from users.models import User, Log


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'nickname',)


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ('id', 'time', 'status', 'server_response', 'user',)

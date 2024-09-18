from django.contrib import admin

from entries.models import Entry


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'text', 'published_at', 'changed_at', 'owner',)

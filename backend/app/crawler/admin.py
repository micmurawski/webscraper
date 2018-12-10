from django.contrib import admin

from .models.page import Page
from .models.task import Task


@admin.register(Task)
class Task(admin.ModelAdmin):
    list_display = ('id', 'target_url', 'done',)


@admin.register(Page)
class Page(admin.ModelAdmin):
    list_display = ('id', 'target_url', 'task', 'error', 'done')

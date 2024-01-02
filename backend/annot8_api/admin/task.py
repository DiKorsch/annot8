from django.contrib import admin

from annot8_api import models

@admin.register(models.Task)
class TaskAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "queued_task",
        "created",
        "finished",
    )

    list_filter = (
        "created",
        "finished",
    )

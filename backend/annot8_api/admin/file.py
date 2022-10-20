from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from annot8_api import models

from pathlib import Path

@admin.register(models.File)
class FileAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "project_info",
        "path",
        "created",
    )

    list_filter = (
        "created",
    )

    @admin.display(empty_value='-', ordering="project__name")
    def project_info(self, obj):
        url = reverse('admin:annot8_api_file_changelist')

        query = f"project_id__exact={obj.project.id}"
        name = f"{obj.project.name} (#{obj.project.id})"

        return format_html(f"<a title='show only files of this project' href='{url}?{query}'>{name}</a>")


    @admin.display(empty_value='-', ordering="path")
    def name(self, obj):
        return Path(obj.path.name).name

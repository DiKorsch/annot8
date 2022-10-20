from django.contrib import admin
from annot8_api import models

@admin.register(models.Project)
class ProjectAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "user",
        "collaborator_list",
        "created",
        "description",
        "root_folder",
    )

    list_filter = (
        "created",
    )


    @admin.display(ordering="collaborators__count")
    def collaborator_list(self, obj):
        return ", ".join([col.username for col in obj.collaborators.all()])

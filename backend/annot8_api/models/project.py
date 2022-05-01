import uuid
import logging

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

from pathlib import Path

from pycs_api.models import base

def new_root_folder():
    return f"{settings.PROJECTS_DIR}/{uuid.uuid4()}"

class Project(base.BaseModel):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="projects",
        related_query_name="project",
    )

    description = models.TextField()

    root_folder = models.CharField(max_length=255,
        default=new_root_folder,
        unique=True)

    serializer_fields = base.BaseModel.serializer_fields + [
        "description",
        "data_folder",
        "root_folder",
    ]

    read_only_fields = base.BaseModel.read_only_fields + [
        "data_folder",
        "root_folder",
    ]


@receiver(models.signals.pre_save, sender=Project)
def project_pre_save(sender, instance, **kwargs):
    is_external = instance.data_folder != ''

    logging.info(f"Using external folder: {'yes' if is_external else 'no'}")
    instance.external_data = is_external

    if not is_external:
        logging.info("Setting data folder")
        instance.data_folder = instance.root_folder + "/data"
        Path(instance.data_folder).mkdir(parents=True)



    # TODO: copy model to root_folder / "model"
    # TODO: create temp folder root_folder / "temp"

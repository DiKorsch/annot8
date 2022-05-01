import enum
import uuid

from django.core.files.uploadedfile import UploadedFile
from django.db import models

from pathlib import Path

from annot8_api.models import base
from annot8_api.models.project import Project


class Extensions(enum.Enum):
    JPG = ".jpg"
    JPEG = ".jpeg"
    PNG = ".png"


def project_directory(instance: "File", filename: str):
    return f"{instance.project.data_folder}/{filename}"


class File(base.BaseModel):

    EXTENSIONS = [
        (Extensions.JPG, "JPG Image"),
        (Extensions.JPEG, "JPEG Image"),
        (Extensions.PNG, "PNG Image"),
    ]

    class Meta:
        unique_together = [
            "project",
            "path"
        ]

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="files",
        related_query_name="file",
    )

    path = models.ImageField(upload_to=project_directory)

    serializer_fields = base.BaseModel.serializer_fields + [
        "project",
        "url",
    ]


    @property
    def url(self):
        return self.path.url


    @classmethod
    def create(cls, uploaded_file: UploadedFile, project: Project):

        file = cls.objects.create(
            project=project,
            path=uploaded_file
        )

        return file

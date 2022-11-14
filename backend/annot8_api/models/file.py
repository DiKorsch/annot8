import enum
import uuid

from django.conf import settings
from django.core.files.uploadedfile import UploadedFile
from django.db import models
from django.dispatch import receiver
from django_q.tasks import async_task

from PIL import Image
from pathlib import Path

from annot8_api.models import describable_object
from annot8_api.models.project import Project


class Extensions(enum.Enum):
    JPG = ".jpg"
    JPEG = ".jpeg"
    PNG = ".png"


def project_directory(instance: "File", filename: str):
    data_folder = Path(instance.project.data_folder).relative_to(settings.MEDIA_ROOT)
    return f"{data_folder}/{filename}"


class File(describable_object.DescribableObject):
    __name__ = "File"

    EXTENSIONS = [
        (Extensions.JPG, "JPG Image"),
        (Extensions.JPEG, "JPEG Image"),
        (Extensions.PNG, "PNG Image"),
    ]

    THUMBNAILS = [
        ("small", 360),
        ("medium", 960),
        ("large", 1920),
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

    serializer_fields = describable_object.DescribableObject.serializer_fields + [
        "project",
        "url",
        "thumbs"
    ]


    @property
    def url(self):
        return self.path.url

    @property
    def thumbs(self):
        thumbs = {}
        for th_name, _ in self.THUMBNAILS:
            path = Path(self.path.path)
            url = Path(self.path.url)
            name = path.name

            thumb = path.parent / "thumbs" / th_name / name
            thumb_url = url.parent / "thumbs" / th_name / name

            if thumb.exists():
                thumbs[th_name] = str(thumb_url)
            else:
                thumbs[th_name] = str(url)

        return thumbs

    @classmethod
    def create(cls, uploaded_file: UploadedFile, project: Project):

        file = cls.objects.create(
            project=project,
            path=uploaded_file
        )

        return file

    def create_thumbnails(self):
        path = Path(self.path.path)
        folder = path.parent / "thumbs"
        name = path.name
        with Image.open(path) as im:
            for th_name, size in self.THUMBNAILS:
                dest = folder / th_name / name

                w, h = im.size
                ratio = size / w
                newW, newH = int(ratio * w), int(ratio * h)

                thumb = im.resize((newW, newH))
                dest.parent.mkdir(exist_ok=True, parents=True)
                thumb.save(dest)

@receiver(models.signals.post_save, sender=File)
def create_thumbnails(sender, instance, created, raw, **kwargs):
    if not raw and created:
        async_task(instance.create_thumbnails)

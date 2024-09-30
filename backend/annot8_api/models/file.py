import enum
import logging
import humanize
import numpy as np

from django.conf import settings
from django.core.files.uploadedfile import UploadedFile
from django.db import models
from django.dispatch import receiver
from django_q.tasks import async_task
from contextlib import contextmanager
from tqdm.auto import tqdm

from PIL import Image
from pathlib import Path

from annot8_api import models as api_models
from annot8_api.models import base
from annot8_ai.detector.tracks import creation_date, CreationDateError

class Extensions(enum.Enum):
    JPG = ".jpg"
    JPEG = ".jpeg"
    PNG = ".png"
    TIFF = ".tiff"
    TIF = ".tif"


def project_directory(instance: "File", filename: str):
    data_folder = Path(instance.project.data_folder).relative_to(settings.MEDIA_ROOT)
    return f"{data_folder}/{filename}"


class File(base.DescribableObject):
    __name__ = "File"

    DATE_FMT = "%d.%m.%Y %H:%M:%S"

    EXTENSIONS = [
        (Extensions.JPG, "JPG Image"),
        (Extensions.JPEG, "JPEG Image"),
        (Extensions.PNG, "PNG Image"),
        (Extensions.TIF, "TIF Image"),
        (Extensions.TIFF, "TIFF Image"),
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
        api_models.Project,
        on_delete=models.CASCADE,
        related_name="files",
        related_query_name="file",
    )

    path = models.ImageField(upload_to=project_directory)

    serializer_fields = base.DescribableObject.serializer_fields + [
        "project",
        "url",
        "thumbs",
        "meta",
    ]


    @property
    def url(self):
        return self.path.url

    @property
    def meta(self):
        n_boxes = self.bboxes.count()

        try:
            record_date = creation_date(self)
        except CreationDateError:
            record_date = self.created

        return [
            ("Bounding boxes", n_boxes),
            ("Resolution", f"{self.path.width}x{self.path.height}px"),
            ("Size", humanize.naturalsize(self.path.size)),
            ("Recorded on", record_date.strftime(File.DATE_FMT)),
            ("Uploaded on", self.created.strftime(File.DATE_FMT)),
        ]

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
    def create(cls, uploaded_file: UploadedFile, project: api_models.Project):

        file = cls.objects.create(
            project=project,
            path=uploaded_file
        )

        return file

    @contextmanager
    def load_image(self):
        with Image.open(Path(self.path.path)) as im:
            yield im

    def as_numpy(self):
        with self.load_image() as im:
            return np.asarray(im)

    def save(self, *args, **kwargs):
        path = Path(self.path.path)
        if path.suffix.lower() in (".tiff", ".tif"):
            im = Image.open(self.path.file)
            im = im.convert("RGB")
            path = path.with_suffix(".jpg")
            im.save(path, 'JPEG', quality=100)
            self.path.name = path.name  # Update path in the instance

        super().save(*args, **kwargs)

    def create_thumbnails(self):
        path = Path(self.path.path)
        folder = path.parent / "thumbs"
        # name = path.stem + ".png" if path.suffix.lower() in (".tiff", ".tif") else path.name
        name = path.name
        with self.load_image() as im:
            for th_name, size in self.THUMBNAILS:
                dest = folder / th_name / name

                w, h = im.size
                ratio = size / w
                newW, newH = int(ratio * w), int(ratio * h)

                thumb = im.resize((newW, newH))
                dest.parent.mkdir(exist_ok=True, parents=True)
                thumb.save(dest)

    def detect_boxes(self):

        project = self.project

        # Get detector.
        detector = project.get_detector()
        if detector is None:
            logging.error(f"Project {project.id} does not have a detector")
            return

        # Remove all prior pipeline-generated bounding boxes.
        api_models.BoundingBox.objects.filter(described_file=self, pipeline_generated=True).delete()

        # Perform detection.
        generated_bboxes = detector(self.as_numpy())
        logging.info(f"Estimated {len(generated_bboxes)} detections")

        for bbox in generated_bboxes:
            # Generate bounding boxes.
            w = bbox.x1 - bbox.x0
            h = bbox.y1 - bbox.y0
            if not bbox.is_valid or w <= 0 or h <= 0:
                continue
            api_models.BoundingBox.create(self, bbox.x0, bbox.y0, w, h, True)

    def classify_boxes(self):
        project = self.project
        boxes = self.bboxes

        # Get classifier.
        classifier = project.get_classifier()
        if classifier is None:
            logging.error(f"Project {project.id} does not have a classifier")
            return

        logging.info(f"Estimating species for {len(boxes)} valid boxes")
        for bbox in tqdm(boxes):
            # If possible, generate predictions.
            try:
                label, logits = classifier(bbox.as_numpy())
                bbox.prediction_add(label, logits, project.classifier)
            except Exception as e:
                logging.error("Generating prediction for bounding box failed due to: " + str(e))

@receiver(models.signals.post_save, sender=File)
def create_thumbnails(sender, instance, created, raw, **kwargs):
    if not raw and created:
        async_task(instance.create_thumbnails)

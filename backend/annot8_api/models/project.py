import logging
import uuid

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver
from django.utils.functional import classproperty
from django_q.tasks import async_iter

from pathlib import Path

from annot8_ai.classifier.base import BaseClassifier
from annot8_ai.detector.base import BaseDetector
from annot8_api import models as api_models
from annot8_api.models import base

def new_root_folder():
    return f"{settings.PROJECTS_DIR}/{uuid.uuid4()}"

class Project(base.BaseModel):
    __name__ = "Project"

    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="projects",
        related_query_name="project",
    )

    collaborators = models.ManyToManyField(
        User,
        related_name="collaborators",
        related_query_name="collaborators",
    )

    description = models.TextField()

    root_folder = models.CharField(max_length=255,
        default=new_root_folder,
        unique=True)

    data_folder = models.CharField(max_length=255)

    CLASSIFIER_CHOICES = [(c, c) for c in [cls.name for cls in BaseClassifier.__subclasses__()]]
    DETECTOR_CHOICES = [(d, d) for d in [cls.name for cls in BaseDetector.__subclasses__()]]
    classifier = models.CharField(max_length=255, choices=CLASSIFIER_CHOICES)
    detector = models.CharField(max_length=255, choices=DETECTOR_CHOICES)

    serializer_fields = base.BaseModel.serializer_fields + [
        "name",
        "user",
        "collaborators",
        "description",
        "classifier",
        "detector",
        "data_folder",
        "root_folder",
        "classifiers",
        "detectors",
        "stats",
    ]

    read_only_fields = base.BaseModel.read_only_fields + [
        "data_folder",
        "root_folder",
        "classifiers",
        "detectors",
        "stats",
    ]

    @property
    def stats(self):
        return dict(
            nFiles=self.files.count(),
            nBoxes=self.boxes.count(),
        )

    @property
    def boxes(self):
        return api_models.BoundingBox.objects.filter(
            described_file__project=self.id
        )

    def reload_detector(self):
        if self.detector is None:
            return

        for det in BaseDetector.__subclasses__():
            if det.name == self.detector:
                return det()
        self.det = None

    def get_detector(self):
        if not hasattr(self, "det"):
            return self.reload_detector()
        return self.det

    def reload_classifier(self):
        if self.classifier is not None:
            for cls in BaseClassifier.__subclasses__():
                if cls.name == self.classifier:
                    self.cls = cls()
                    return
        self.cls = None

    def get_classifier(self):
        if not hasattr(self, "cls"):
            self.reload_classifier()
        return self.cls

    @classproperty
    def classifiers(cls):
        return [cls.name for cls in BaseClassifier.__subclasses__()]

    @classproperty
    def detectors(cls):
        return [cls.name for cls in BaseDetector.__subclasses__()]

    def run_detector(self):
        file_ids = self.files.values_list("pk", flat=True)
        return async_iter(detect_boxes, list(file_ids)), len(file_ids)

def detect_boxes(file_id):
    res = api_models.File.objects.get(pk=file_id).detect_boxes()
    return file_id, res


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

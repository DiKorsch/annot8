import logging
import numpy as np


from PIL import Image
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db import models
from pathlib import Path

from annot8_api.models import base
from annot8_api import models as api_models

class BoundingBox(base.DescribableObject):
    __name__ = "BoundingBox"

    described_file = models.ForeignKey(
        api_models.File,
        on_delete=models.CASCADE,
        related_name="bboxes",
        related_query_name="bbox",
    )


    pipeline_generated = models.BooleanField(default=True)
    creator = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
    )

    x = models.FloatField()
    y = models.FloatField()
    width = models.FloatField()
    height = models.FloatField()

    serializer_fields = base.DescribableObject.serializer_fields + [
        "described_file",
        "pipeline_generated",
        "creator",
        "x",
        "y",
        "width",
        "height",
        "thumbs"
    ]

    @property
    def area(self) -> float:
        return self.width * self.height

    @property
    def center(self) -> (float, float):
        return self.x + self.width/2, self.y + self.height/2

    @property
    def thumbs(self):
        thumbs = {}

        try:
            folder = self.crop_folder
            url = self.crop_url
            name = self.crop_fname

            if (folder / name).exists():
                thumbs["original"] = str(url / name)

            for th_name, _ in api_models.File.THUMBNAILS:

                crop = folder / th_name / name
                if crop.exists():
                    thumbs[th_name] = str(url / th_name / name)
        except Exception as e:
            logging.error(str(e))
        return thumbs

    @property
    def crop_folder(self):
        fobj = self.described_file
        path = Path(fobj.path.path)
        return path.parent / "crops" / path.stem

    @property
    def crop_url(self):
        fobj = self.described_file
        path = Path(fobj.path.url)
        return path.parent / "crops" / path.stem

    @property
    def crop_fname(self):
        fobj = self.described_file
        path = Path(fobj.path.path)
        return f"{path.stem}_{self.id:08d}{path.suffix}"

    def remove_crops(self):

        folder = self.crop_folder
        name = self.crop_fname
        (folder / name).unlink(missing_ok=True)
        for th_name, size in api_models.File.THUMBNAILS:
            (folder / th_name / name).unlink(missing_ok=True)


    def create_crops(self):

        folder = self.crop_folder
        name = self.crop_fname

        with self.described_file.load_image() as im:
            W, H = im.size
            x0, y0 = self.x * W, self.y * H
            x1, y1 = x0 + self.width * W, y0 + self.height * H

            crop = im.crop(box=(x0, y0, x1, y1))
            folder.mkdir(exist_ok=True, parents=True)
            crop.save(folder / name)

            w, h = crop.size
            for th_name, size in api_models.File.THUMBNAILS:
                ratio = size / W
                new_size = int(ratio * w), int(ratio * h)
                thumb = crop.resize(new_size)

                dest = folder / th_name / name
                dest.parent.mkdir(exist_ok=True, parents=True)
                thumb.save(dest)

    def update(self, x: float, y: float, width: float, height: float, user: User, label=None):

        if user is not None:
            self.pipeline_generated = False
            self.creator = user

        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.save()

    def as_numpy(self):
        path = Path(self.described_file.path.path)
        with Image.open(path) as im:
            # Note: x, y, with and height are in [0,1].
            w, h = im.size
            x0, y0 = int(self.x * w), int(self.y * h)
            x1, y1 = int((self.x + self.width) * w), int((self.y + self.height) * h)

            im = np.asarray(im)
            crop = im[y0:y1, x0:x1]

        return crop

    def new_prediction(self, gbif_id, logits, classifier_name):
        api_models.Prediction.objects.filter(described_object=self).delete()
        prediction_obj = api_models.Prediction.create(described_object=self,
                                        gbif_id=gbif_id,
                                        model=classifier_name)
        for (_gbif_id, lgt) in logits:
            api_models.Logit.create(prediction = prediction_obj,
                            gbif_id = _gbif_id,
                            logit = lgt)

        return prediction_obj

    def predict(self):

        project = self.described_file.project
        classifier = project.get_classifier()
        if classifier is None:
            return

        # Generate prediction.
        label, logits = classifier(self.as_numpy())

        # Add to database (logits and prediction).
        self.new_prediction(label, logits, project.classifier)

    def annotate(self, label, annotator):

        try:
            annotation = self.annotation
        except api_models.Annotation.DoesNotExist:
            annotation = api_models.Annotation(described_object=self)

        # Create a corresponding annotation / update the existing one.
        annotation.label = label
        annotation.annotator = annotator
        annotation.save()
        annotation.confirmators.clear()
        annotation.save()

        return annotation

    @classmethod
    def create(cls, described_file: api_models.File, x: float, y: float, width: float,
            height: float, pipeline_generated: bool = False, user: User = None):

        if pipeline_generated:
            if user is not None:
                raise ValueError("Omit the 'user' parameter for"
                    "pipeline generated bounding boxes!")
        else:
            if user is None:
                raise ValueError("The 'user' parameter is required for"
                    "manually annotated bounding boxes!")

        bbox = cls.objects.create(
            described_file = described_file,
            pipeline_generated = pipeline_generated,
            creator = user,
            x = x,
            y = y,
            width = width,
            height = height
        )

        return bbox


@receiver(models.signals.post_save, sender=BoundingBox)
def create_crops(sender, instance, created, raw, update_fields, **kwargs):
    if not raw:
        instance.create_crops()

@receiver(models.signals.pre_delete, sender=BoundingBox)
def remove_crops(sender, instance, **kwargs):
    instance.remove_crops()

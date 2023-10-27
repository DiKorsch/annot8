import numpy as np


from PIL import Image
from django.contrib.auth.models import User
from django.db import models
from pathlib import Path

from annot8_api.models import base
from annot8_api.models import file
from annot8_api.models import logit
from annot8_api.models import prediction

class BoundingBox(base.DescribableObject):
    described_file = models.ForeignKey(
        file.File,
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
    ]

    def update(self, x: float, y: float, width: float, height: float, user: User, label=None):

        if user is not None:
            self.pipeline_generated = False
            self.creator = user

        self.x = x
        self.y = y
        self.width = width
        self.height = height

        # if label

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

    def prediction_add(self, label, logits, classifier_name):
        prediction.Prediction.objects.filter(described_object=self).delete()
        prediction_obj = prediction.Prediction.create(described_object=self,
                                        top_1_label=label,
                                        model=classifier_name)
        for (label_id, lgt) in logits:
            logit.Logit.create(prediction = prediction_obj,
                            label = label_id,
                            logit = lgt)

        return prediction_obj

    @classmethod
    def create(cls, described_file: file.File, x: float, y: float, width: float,
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

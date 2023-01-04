from django.db import models
from django.contrib.auth.models import User

import numpy as np
from PIL import Image
from pathlib import Path

from annot8_api.models import describable_object
from annot8_api.models import file
from annot8_api.models import prediction
from annot8_api.models import logit

class BoundingBox(describable_object.DescribableObject):
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

    serializer_fields = describable_object.DescribableObject.serializer_fields + [
        "described_file",
        "pipeline_generated",
        "creator",
        "x",
        "y",
        "width",
        "height",
    ]

    def as_numpy(self):
        path = Path(self.described_file.path.path)
        with Image.open(path) as im:
            # Note: x, y, with and height are in [0,1].
            w, h = im.size
            bbox = np.asarray(im)[int(self.x*w):int((self.x+self.width)*w), int(self.y*h):int((self.y+self.height)*h)]
        return bbox

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
    def create(cls, described_file: file.File, x: int, y: int, width: int,
            height: int, pipeline_generated: bool = False, user: User = None):

        if user is None and pipeline_generated is True:
            bbox = cls.objects.create(
                described_file = described_file,
                pipeline_generated = True,
                x = x,
                y = y,
                width = width,
                height = height
            )
        elif user is not None and pipeline_generated is False:
            bbox = cls.objects.create(
                described_file = described_file,
                pipeline_generated = False,
                creator = user,
                x = x,
                y = y,
                width = width,
                height = height
            )
        else:
            raise ValueError("Supply a creator if the bounding box is created by a user and ommit it if it is not.")

        return bbox

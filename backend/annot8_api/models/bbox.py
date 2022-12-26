
from django.db import models
from annot8_api.models import describable_object
from annot8_api.models import file

class BoundingBox(describable_object.DescribableObject):
    described_file = models.ForeignKey(
        file.File,
        on_delete=models.CASCADE,
        related_name="bboxes",
        related_query_name="bbox",
    )

    x = models.FloatField()
    y = models.FloatField()
    width = models.FloatField()
    height = models.FloatField()

    serializer_fields = describable_object.DescribableObject.serializer_fields + [
        "described_file",
        "x",
        "y",
        "width",
        "height",
    ]

    @classmethod
    def create(cls, described_file: file.File, x: int, y: int, width: int,
            height: int):

        bbox = cls.objects.create(
            described_file = described_file,
            x = x,
            y = y,
            width = width,
            height = height
        )

        return bbox

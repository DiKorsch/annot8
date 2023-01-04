
from django.db import models
from annot8_api.models import base
from annot8_api.models import describable_object
# from labeltree.models import label

class Prediction(base.BaseModel):

    # A prediction describes a describable object. If the describable object
    # is deleted, the prediction should be too.
    described_object = models.OneToOneField(
        describable_object.DescribableObject,
        on_delete=models.CASCADE,
        related_name = "prediction",
        related_query_name = "prediction",
    )

    top_1_label = models.IntegerField() # label.Label()

    model = models.CharField(max_length=255)

    serializer_fields = base.BaseModel.serializer_fields + [
        "described_object",
        "top_1_label",
        "model",
    ]

    @classmethod
    def create(cls, described_object: describable_object.DescribableObject, top_1_label: int, model: str):

        prediction = cls.objects.create(
            described_object = described_object,
            top_1_label = top_1_label,
            model = model,
        )

        return prediction

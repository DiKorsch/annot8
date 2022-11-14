
from django.db import models
from annot8_api.models import base
from annot8_api.models import describable_object
from labeltree.models import label

class Prediction(base.BaseModel):

    # A prediction describes a describable object. If the describable object
    # is deleted, the prediction should be too.
    described_object = models.ForeignKey(
        describable_object.DescribableObject,
        on_delete=models.CASCADE,
        related_name="predictions",
        related_query_name="prediction",
    )

    top_1_label = label.Label()

    serializer_fields = base.BaseModel.serializer_fields + [
        "described_object",
        "top_1_label",
    ]

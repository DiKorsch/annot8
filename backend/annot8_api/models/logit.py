
from django.db import models
from annot8_api.models import base
from annot8_api.models import prediction
from labeltree.models import label

class Logit(base.BaseModel):

    # One prediction can have multiple logits, but logits cannot exist without
    # a corresponding prediction.
    prediction = ForeignKey(
        prediction.Prediction,
        on_delete=models.CASCADE,
        related_name="logits",
        related_query_name = "logit",
    )

    label = label.Label()

    logit = models.FloatField()

    serializer_fields = base.BaseModel.serializer_fields + [
        "prediction",
        "label",
        "logit",
    ]

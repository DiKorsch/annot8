
from django.db import models
from annot8_api.models import base
from annot8_api.models import Prediction
# from labeltree.models import label

class Logit(base.BaseModel):

    # One prediction can have multiple logits, but logits cannot exist without
    # a corresponding prediction.
    prediction = models.ForeignKey(
        Prediction,
        on_delete=models.CASCADE,
        related_name="logit",
        related_query_name = "logit",
    )

    label = models.IntegerField() # label.Label()

    logit = models.FloatField()

    serializer_fields = base.BaseModel.serializer_fields + [
        "prediction",
        "label",
        "logit",
    ]

    @classmethod
    def create(cls, prediction: Prediction, label: int, logit: float):

        logit = cls.objects.create(
            prediction = prediction,
            label = label,
            logit = logit,
        )

        return prediction

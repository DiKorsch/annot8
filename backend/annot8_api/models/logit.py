
from annot8_api.models import base
from annot8_api.models import prediction as pred_mod

from django.db import models
from labeltree.models import Label

class Logit(base.BaseModel):

    # One prediction can have multiple logits, but logits cannot exist without
    # a corresponding prediction.
    prediction = models.ForeignKey(
        pred_mod.Prediction,
        on_delete=models.CASCADE,
        related_name="logit",
        related_query_name = "logit",
    )

    label = models.ForeignKey(Label,
        on_delete=models.CASCADE
    )
    logit = models.FloatField()

    serializer_fields = base.BaseModel.serializer_fields + [
        "prediction",
        "label",
        "logit",
    ]

    @classmethod
    def create(cls, prediction: pred_mod.Prediction, gbif_id: int, logit: float):

        logit = cls.objects.create(
            prediction=prediction,
            label=Label.objects.get(pk=gbif_id),
            logit=logit,
        )

        return prediction

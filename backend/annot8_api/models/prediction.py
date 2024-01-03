
from django.db import models
from annot8_api.models import base
from labeltree.models import Label

class Prediction(base.BaseModel):

    # A prediction describes a describable object. If the describable object
    # is deleted, the prediction should be too.
    described_object = models.OneToOneField(
        base.DescribableObject,
        on_delete=models.CASCADE,
        related_name = "prediction",
        related_query_name = "prediction",
    )

    top_1_label = models.ForeignKey(Label,
        on_delete=models.CASCADE
    )

    model = models.CharField(max_length=255)

    serializer_fields = base.BaseModel.serializer_fields + [
        "described_object",
        "top_1_label",
        "model",
    ]

    @classmethod
    def create(cls, described_object: base.DescribableObject,
        gbif_id: int, model: str):

        prediction = cls.objects.create(
            described_object=described_object,
            top_1_label=Label.objects.get(pk=gbif_id),
            model=model,
        )

        return prediction

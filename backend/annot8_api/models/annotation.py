
from django.db import models
from annot8_api.models import base
from django.contrib.auth.models import User
from labeltree.models import Label

class Annotation(base.BaseModel):

    # An annotation describes a describable object. If the describable object
    # is deleted, the annotation should be too.
    described_object = models.OneToOneField(
        base.DescribableObject,
        on_delete=models.CASCADE,
        related_name = "annotation",
        related_query_name = "annotation",
    )

    label = models.ForeignKey(Label,
        on_delete=models.CASCADE
    )

    annotator = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
    )

    confirmators = models.ManyToManyField(
        User,
        related_name="confirmators",
        related_query_name="confirmator",
    )

    serializer_fields = base.BaseModel.serializer_fields + [
        "described_object",
        "label",
        "annotator",
        "confirmators",
    ]

    @classmethod
    def create(cls, described_object: base.DescribableObject, label: str,
        annotator: User):

        annotation = cls.objects.create(
            described_object = described_object,
            label = label,
            annotator = annotator,
        )

        return annotation

from django.db import models
from polymorphic import models as polymorphic_models

class BaseModel(polymorphic_models.PolymorphicModel):

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

    serializer_fields = [
        "id",
        "created",
    ]

    read_only_fields = [
        "created",
    ]


class DescribableObject(BaseModel):
    pass

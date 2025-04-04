
from rest_framework import serializers
from annot8_api import models
from labeltree.models import LabelSerializer

class BaseSerializer(serializers.ModelSerializer):
    pass

class UserListingField(serializers.RelatedField):
    def to_representation(self, user):
        return user.username

class ProjectSerializer(BaseSerializer):
    # We want the collaborators and the creator to not be serialized by their id,
    # but instead by their username.
    # Field is read only - alternatively one could specify a queryset.
    collaborators = UserListingField(many=True, read_only=True)
    user = serializers.StringRelatedField()

    class Meta:
        model = models.Project
        fields = models.Project.serializer_fields
        read_only_fields = models.Project.read_only_fields

class TaskSerializer(BaseSerializer):
    # We want the collaborators and the creator to not be serialized by their id,
    # but instead by their username.
    # Field is read only - alternatively one could specify a queryset.
    user = serializers.StringRelatedField()

    class Meta:
        model = models.Task
        fields = models.Task.serializer_fields
        read_only_fields = models.Task.read_only_fields

class PredictionSerializer(BaseSerializer):
    top_1_label = LabelSerializer()

    class Meta:
        model = models.Prediction
        fields = models.Prediction.serializer_fields
        read_only_fields = models.Prediction.read_only_fields

class AnnotationSerializer(BaseSerializer):
    # We want the confirmators and the annotator to not be serialized by their id,
    # but instead by their username.
    # Field is read only - alternatively one could specify a queryset.
    confirmators = UserListingField(many=True, read_only=True)
    label = LabelSerializer()
    annotator = serializers.StringRelatedField()

    class Meta:
        model = models.Annotation
        fields = models.Annotation.serializer_fields
        read_only_fields = models.Annotation.read_only_fields

class FileSerializer(BaseSerializer):
    annotation = AnnotationSerializer()

    class Meta:
        model = models.File
        fields = models.File.serializer_fields + ["annotation"]
        read_only_fields = models.File.read_only_fields

class BoundingBoxSerializer(BaseSerializer):
    annotation = AnnotationSerializer()
    prediction = PredictionSerializer()

    class Meta:
        model = models.BoundingBox
        fields = models.BoundingBox.serializer_fields + ["annotation", "prediction"]
        read_only_fields = models.BoundingBox.read_only_fields

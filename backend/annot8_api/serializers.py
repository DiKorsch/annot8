
from rest_framework import serializers
from annot8_api import models

class BaseSerializer(serializers.ModelSerializer):
    pass

class CollaboratorListingField(serializers.RelatedField):
    def to_representation(self, user):
        return user.username

class ProjectSerializer(BaseSerializer):
    # We want the collaborators and the creator to not be serialized by their id,
    # but instead by their username.
    # Field is read only - alternatively one could specify a queryset.
    collaborators = CollaboratorListingField(many=True, read_only=True)
    user = serializers.StringRelatedField()

    class Meta:
        model = models.Project
        fields = models.Project.serializer_fields
        read_only_fields = models.Project.read_only_fields

class FileSerializer(BaseSerializer):

    class Meta:
        model = models.File
        fields = models.File.serializer_fields
        read_only_fields = models.File.read_only_fields

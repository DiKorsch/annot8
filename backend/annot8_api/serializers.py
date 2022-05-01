
from rest_framework import serializers
from annot8_api import models

class BaseSerializer(serializers.ModelSerializer):
    pass

class ProjectSerializer(BaseSerializer):

    class Meta:
        model = models.Project
        fields = models.Project.serializer_fields
        read_only_fields = models.Project.read_only_fields

class FileSerializer(BaseSerializer):

    class Meta:
        model = models.File
        fields = models.File.serializer_fields
        read_only_fields = models.File.read_only_fields

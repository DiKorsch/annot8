from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.decorators import permission_classes
from rest_framework.response import Response

from annot8_api.models import File
from annot8_api.models import Project
from annot8_api.serializers import ProjectSerializer
# from annot8_api.serializers import FileSerializer
from annot8_api.views.base import BaseViewSet


class ProjectViewSet(BaseViewSet):

    serializer_class = ProjectSerializer

    def get_queryset(self):
        return self.request.user.projects

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

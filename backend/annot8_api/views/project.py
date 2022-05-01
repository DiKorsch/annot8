from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.decorators import permission_classes
from rest_framework.response import Response

from annot8_api.models import File
from annot8_api.models import Project
from annot8_api.serializers import ProjectSerializer
from annot8_api.serializers import FileSerializer
from annot8_api.views.base import BaseViewSet


class ProjectViewSet(BaseViewSet):

    serializer_class = ProjectSerializer

    def get_queryset(self):
        return self.request.user.projects

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def file(self, request, pk=None):
        if "file" not in request.FILES:
            return Response({"status": "File missing"},
                status=status.HTTP_400_BAD_REQUEST)
        project = self.get_object()

        try:
            file = File.create(request.FILES['file'], project)

        except Exception as e:
            return Response({"status": str(e)},
                status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({'status': 'File uploaded'})

    @action(detail=True)
    def files(self, request, pk=None):
        project = self.get_object()

        files = project.files

        serializer = FileSerializer(files, many=True)
        return Response(serializer.data)

from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.decorators import permission_classes
from rest_framework.response import Response

from annot8_api.models import File
from annot8_api.models import Project
from annot8_api.serializers import FileSerializer
from annot8_api.serializers import ProjectSerializer
from annot8_api.views.base import BaseViewSet


class ProjectViewSet(BaseViewSet):

    serializer_class = ProjectSerializer

    def get_queryset(self):
        return Project.objects.filter(Q(user=self.request.user) | Q(collaborators__in=[self.request.user])).distinct()

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

    @action(detail=True, methods=['post'])
    def add_collaborator(self, request, pk=None):
        if "collaborator_username" not in request.POST:
            return Response({"status": "Collaborator username missing"},
                status=status.HTTP_400_BAD_REQUEST)

        project = self.get_object()
        creator = project.user

        collaborator = request.POST['collaborator_username']
        collaborator = get_object_or_404(User, username=collaborator)

        if creator.username == collaborator.username:
            return Response({"status": "Collaborator cannot be the creator of the project"},
                status=status.HTTP_400_BAD_REQUEST)

        if collaborator in project.collaborators.all():
            return Response({"status": "User to add is already a collaborator of the project"},
                status=status.HTTP_400_BAD_REQUEST)

        project.collaborators.add(collaborator)
        return Response({'status': 'Collaborator added'})

    @action(detail=True, methods=['post'])
    def remove_collaborator(self, request, pk=None):
        if "collaborator_username" not in request.POST:
            return Response({"status": "Collaborator username missing"},
                status=status.HTTP_400_BAD_REQUEST)

        project = self.get_object()

        collaborator = request.POST['collaborator_username']
        collaborator = get_object_or_404(User, username=collaborator)

        if not collaborator in project.collaborators.all():
            return Response({"status": "User to remove is not a collaborator of the project"},
                status=status.HTTP_400_BAD_REQUEST)

        project.collaborators.remove(collaborator)
        return Response({'status': 'Collaborator added'})

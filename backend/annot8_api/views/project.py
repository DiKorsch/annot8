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

    def is_owner(self):
        return self.get_object().user == self.request.user

    def destroy(self, request, *args, **kwargs):
        if not self.is_owner():
            return Response({"status": "Only the owner can delete a project"},
                status=status.HTTP_400_BAD_REQUEST)
        return super().destroy(request, *args, **kwargs)


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



    @action(detail=True, methods=["post"], url_path="collaborator")
    def collaborator_add(self, request, pk=None):
        name = request.POST.get("username")
        project = self.get_object()
        creator = project.user

        if name is None:
            return Response({"status": "Collaborator username missing"},
                status=status.HTTP_400_BAD_REQUEST)

        if request.user != creator:
            return Response({"status": "Only the creator can modify the collaborators of a project"},
                status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(User, username=name)
        if creator.username == user.username:
            return Response({"status": "Collaborator cannot be the creator of the project"},
                status=status.HTTP_400_BAD_REQUEST)

        if user in project.collaborators.all():
            return Response({"status": "User to add is already a collaborator of the project"},
                status=status.HTTP_400_BAD_REQUEST)

        project.collaborators.add(user)
        return Response({'status': 'Collaborator added'})


    @action(detail=True, methods=['delete'], url_path=r"collaborator/(?P<name>[a-z0-9]+)")
    def collaborator_remove(self, request, pk=None, name=None):
        project = self.get_object()
        creator = project.user

        user = get_object_or_404(User, username=name)

        if user != request.user and request.user != creator:
            return Response({"status": "Only the creator can modify the collaborators of a project"},
                status=status.HTTP_400_BAD_REQUEST)

        if user not in project.collaborators.all():
            return Response({"status": "User to remove is not a collaborator of the project"},
                status=status.HTTP_400_BAD_REQUEST)

        project.collaborators.remove(user)
        return Response({'status': 'Collaborator added'})

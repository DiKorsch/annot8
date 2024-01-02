from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from annot8_api import models as api_models
from annot8_api import serializers
from annot8_api.views import base
from annot8_api.pipeline.tracks import group_tracks


class ProjectViewSet(base.BaseViewSet):

    serializer_class = serializers.ProjectSerializer

    def get_queryset(self):
        return api_models.Project.objects.filter(
            Q(user=self.request.user) |
            Q(collaborators__in=[self.request.user])
        ).distinct()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def is_owner(self):
        return self.get_object().user == self.request.user

    def destroy(self, request, *args, **kwargs):
        if not self.is_owner():
            return Response({"status": "Only the owner can delete a project"},
                status=status.HTTP_400_BAD_REQUEST)
        return super().destroy(request, *args, **kwargs)

    @action(detail=True)
    def crops(self, request, pk=None):
        project = self.get_object()

        boxes = project.boxes
        files = project.files

        boxes_ser = serializers.BoundingBoxSerializer(boxes, many=True)
        files_ser = serializers.FileSerializer(files, many=True)
        data = dict(boxes=boxes_ser.data, files=files_ser.data)

        if request.GET.get("group_tracks") == "true":
            data["tracks"] = group_tracks(boxes.all(), files.all())
        return Response(data)

    @action(detail=True, methods=['post'])
    def file(self, request, pk=None):
        if "file" not in request.FILES:
            return Response({"status": "File missing"},
                status=status.HTTP_400_BAD_REQUEST)
        project = self.get_object()

        try:
            file = api_models.File.create(request.FILES['file'], project)
        except Exception as e:
            print(e)
            return Response({"status": str(e)},
                status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = serializers.FileSerializer(file)
            return Response(serializer.data)

    @action(detail=True)
    def files(self, request, pk=None):
        project = self.get_object()

        files = project.files

        serializer = serializers.FileSerializer(files, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["post"], url_path="classifier")
    def classifier_select(self, request, pk=None):
        classifier = request.POST.get("classifier")
        project = self.get_object()

        if classifier is None:
            return Response({"status": "Classifier missing"},
                status=status.HTTP_400_BAD_REQUEST)
        if classifier not in api_models.Project.classifiers:
            return Response({"status": "Classifier name is invalid"},
                status=status.HTTP_400_BAD_REQUEST)

        project.classifier = classifier
        project.save()
        project.reload_classifier()
        return Response({'status': 'Classifier selected'})


    @action(detail=True, methods=["post"], url_path="detector")
    def detector_select(self, request, pk=None):
        detector = request.POST.get("detector")
        project = self.get_object()

        if detector is None:
            return Response({"status": "Detector missing"},
                status=status.HTTP_400_BAD_REQUEST)
        if detector not in api_models.Project.detectors:
            return Response({"status": "Detector name is invalid"},
                status=status.HTTP_400_BAD_REQUEST)

        project.detector = detector
        project.save()
        project.reload_detector()
        print("Selected detector " + project.detector)
        return Response({'status': 'Detector selected'})

    @action(detail=True, methods=["post"], url_path="run_detector")
    def run_detector(self, request, pk=None):
        project = self.get_object()
        uuid, nqueued = project.run_detector()

        task = api_models.Task.new(
            user=request.user, task_uuid=uuid, nqueued=nqueued)
        task_ser = serializers.TaskSerializer(task)
        return Response(task_ser.data)


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
        return Response({'status': 'Collaborator removed'})

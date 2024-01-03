from django.db.models import Q

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from annot8_api import models as api_models
from annot8_api import serializers
from annot8_api.views.base import BaseViewSet

class FileViewSet(BaseViewSet):

    serializer_class = serializers.FileSerializer
    def get_queryset(self):
        user = self.request.user
        return api_models.File.objects.filter(
            Q(project__user=user) |
            Q(project__collaborators__in=[user])
        ).distinct()

    @action(detail=True)
    def bboxes(self, request, pk=None):
        file = self.get_object()

        bboxes = file.bboxes

        serializer = serializers.BoundingBoxSerializer(bboxes, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["post"], url_path="bbox_generate")
    def bbox_generate(self, request, pk=None):
        file = self.get_object()

        task = api_models.Task.start_async(file.detect_boxes,
            user=request.user)
        task_ser = serializers.TaskSerializer(task)
        return Response(task_ser.data)

    @action(detail=True, methods=["post"], url_path="bbox_predict")
    def bbox_predict(self, request, pk=None):
        file = self.get_object()
        bbox_ids = file.bboxes.values_list("pk", flat=True)

        task = api_models.Task.start_async(bbox_predict,
            user=request.user, items=list(bbox_ids))
        task_ser = serializers.TaskSerializer(task)
        return Response(task_ser.data)


    @action(detail=True, methods=["post"], url_path="bbox")
    def bbox_add(self, request, pk=None):
        x, y, width, height, label = [request.data.get(key) for key in ["x", "y", "width", "height", "label"]]

        if None in [y, x, width, height]:
            return Response({"status": "Argument for bbox missing"},
                status=status.HTTP_400_BAD_REQUEST)

        file = self.get_object()
        user = self.request.user

        try:
            bbox = BoundingBox.create(file, x, y, width, height, False, user)
            if label is not None:
                Annotation.create(described_object=bbox, label=label, annotator=user)

        except Exception as e:
            print(e)
            return Response({"status": str(e)},
                status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({'status': 'BBox added'})

    @action(detail=True, methods=["put"], url_path="label")
    def label_set(self, request, pk=None):
        label = request.data.get("label")
        if label is None:
            return Response({"status": "Label missing"},
                status=status.HTTP_400_BAD_REQUEST)

        user = self.request.user
        file = self.get_object()

        # Create a corresponding annotation / update the existing one.
        try:
            annotation, created = Annotation.objects.get_or_create(described_object=file)
            annotation.label = label
            annotation.annotator = user
            annotation.confirmators.clear()
            annotation.save()
        except Exception as e:
            print(e)
            return Response({"status": str(e)},
                status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({'status': 'Label added to file'})




def bbox_predict(box_id):
    res = api_models.BoundingBox.objects.get(pk=box_id).predict()
    return box_id, res

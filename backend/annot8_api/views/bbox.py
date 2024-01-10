from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from annot8_api import models as api_models
from annot8_api import serializers
from annot8_api.views.base import BaseViewSet
from annot8_api.views.pagination import DefaultPagination

from labeltree.models import Label

class BBoxViewSet(BaseViewSet):
    serializer_class = serializers.BoundingBoxSerializer
    pagination_class = DefaultPagination

    def get_queryset(self, distinct: bool = True):
        user = self.request.user
        qset = api_models.BoundingBox.objects.filter(
            Q(described_file__project__user=user) |
            Q(described_file__project__collaborators__in=[user])
        )

        if distinct:
            return qset.distinct()
        return qset

    def update(self, request, pk=None, *args, **kwargs):
        bbox = self.get_object()
        data = [request.data.get(arg) for arg in ["x", "y", "width", "height"]]

        if None in data:
            return Response({"status": "Argument for bbox update missing"},
                status=status.HTTP_400_BAD_REQUEST)
        try:
            bbox.update(*data, user=request.user, label=request.data.get("label"))
        except Exception as e:
            print(e)
            return Response({"status": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({'status': 'BoundingBox updated'})

    @action(detail=True, methods=["post"], url_path="predict")
    def predict(self, request, pk=None):
        bbox = self.get_object()

        task = api_models.Task.start_async(bbox.predict,
            user=request.user)
        task_ser = serializers.TaskSerializer(task)
        return Response(task_ser.data)

    @action(detail=False, methods=["post"], url_path="predict")
    def predict_many(self, request, pk=None):
        idxs = request.data.get("idxs")
        if idxs is None:
            return Response({"status": "IDs missing"},
                status=status.HTTP_400_BAD_REQUEST)
        bboxes = self.get_queryset(distinct=False).filter(pk__in=idxs)
        idxs = bboxes.values_list("pk", flat=True)

        task = api_models.Task.start_async(
            api_models.BoundingBox.bbox_predict,
            user=request.user, items=list(idxs))

        task_ser = serializers.TaskSerializer(task)
        return Response(task_ser.data)

    @action(detail=True, methods=["put"], url_path="label")
    def set_label(self, request, pk=None):
        label = request.data.get("label")
        if label is None:
            return Response({"status": "Label missing"},
                status=status.HTTP_400_BAD_REQUEST)
        label = get_object_or_404(Label, pk=label["id"])

        user = self.request.user
        bbox = self.get_object()

        try:
            with transaction.atomic():
                bbox.annotate(label, user)
        except Exception as e:
            print(e)
            return Response({"status": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        else:
            return Response({'status': f'Label {label} set to bounding box'})

    @action(detail=False, methods=["put"], url_path="label")
    def set_labels(self, request, pk=None):
        label = request.data.get("label")
        idxs = request.data.get("idxs")
        if label is None:
            return Response({"status": "Label missing"},
                status=status.HTTP_400_BAD_REQUEST)
        if idxs is None:
            return Response({"status": "IDs missing"},
                status=status.HTTP_400_BAD_REQUEST)


        label = get_object_or_404(Label, pk=label["id"])

        user = self.request.user
        bboxes = self.get_queryset().filter(pk__in=idxs)
        idxs = list(bboxes.values_list("pk", flat=True))

        try:
            with transaction.atomic():
                for bbox in bboxes:
                    bbox.annotate(label, user)
        except Exception as e:
            print(e)
            return Response({"status": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({
                'status': f'Label {label} set to {len(idxs)} bounding boxes',
                'idxs': idxs
            })

    @action(detail=False, methods=["delete"], url_path="many")
    def delete_many(self, request):
        idxs = request.data.get("idxs")
        if idxs is None:
            return Response({"status": "IDs missing"},
                status=status.HTTP_400_BAD_REQUEST)
        objects = self.get_queryset(distinct=False).filter(pk__in=idxs)
        idxs = list(objects.values_list("pk", flat=True))
        try:
            objects.delete()
        except Exception as e:
            print(e)
            return Response({"status": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({
            'status': f'{len(idxs)} Bounding boxes deleted successfully!',
            'idxs': idxs
            })

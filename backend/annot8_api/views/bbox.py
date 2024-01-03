from django.db.models import Q

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from annot8_api import models as api_models
from annot8_api import serializers
from annot8_api.views.base import BaseViewSet
from annot8_api.views.pagination import DefaultPagination

class BBoxViewSet(BaseViewSet):
    serializer_class = serializers.BoundingBoxSerializer
    pagination_class = DefaultPagination

    def get_queryset(self):
        user = self.request.user
        return api_models.BoundingBox.objects.filter(
            Q(described_file__project__user=user) |
            Q(described_file__project__collaborators__in=[user])
        ).distinct()

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

        # Get classifier.
        project = bbox.described_file.project
        classifier = project.get_classifier()
        if classifier is None:
            return Response({"status": "Project does not have a classifier"},
                status=status.HTTP_400_BAD_REQUEST)

        # Generate prediction.
        label, logits = classifier(bbox.as_numpy())

        # Add to database (logits and prediction).
        bbox.prediction_add(label, logits, project.classifier)

        return Response({'status': 'Prediction added to bounding box'})

    @action(detail=True, methods=["put"], url_path="label")
    def set_label(self, request, pk=None):
        label = request.data.get("label")
        if label is None:
            return Response({"status": "Label missing"},
                status=status.HTTP_400_BAD_REQUEST)

        user = self.request.user
        bbox = self.get_object()

        # Create a corresponding annotation / update the existing one.
        try:
            annotation, created = api_models.Annotation.objects.get_or_create(described_object=bbox)
            annotation.label = label
            annotation.annotator = user
            annotation.confirmators.clear()
            annotation.save()
        except Exception as e:
            print(e)
            return Response({"status": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        else:
            return Response({'status': 'Label added to bounding box'})

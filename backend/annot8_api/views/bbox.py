from django.db.models import Q

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from annot8_api.models import BoundingBox
from annot8_api.models import Annotation
from annot8_api.serializers import BoundingBoxSerializer
from annot8_api.views.base import BaseViewSet

class BBoxViewSet(BaseViewSet):
    serializer_class = BoundingBoxSerializer
    def get_queryset(self):
        user = self.request.user
        return BoundingBox.objects.filter(
            Q(described_file__project__user=user) |
            Q(described_file__project__collaborators__in=[user])
        ).distinct()

    @action(detail=True, methods=["post"], url_path="predict")
    def predict(self, request, pk=None):
        bbox = self.get_object()

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

    @action(detail=True, methods=["post"], url_path="label")
    def label_set(self, request, pk=None):
        if "label" not in request.POST:
            return Response({"status": "Label missing"},
                status=status.HTTP_400_BAD_REQUEST)
        label = request.POST.get("label")
        user = self.request.user
        bbox = self.get_object()

        # Create a corresponding annotation / update the existing one.
        try:
            annotation, created = Annotation.objects.get_or_create(described_object=bbox)
            annotation.label = label
            annotation.annotator = user
            annotation.confirmators.clear()
            annotation.save()
        except Exception as e:
            print(e)
            return Response({"status": str(e)},
                status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({'status': 'Label added to bounding box'})

from django.db.models import Q
from django.shortcuts import get_object_or_404

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

    @action(detail=True, methods=["post"], url_path="label")
    def label_set(self, request, pk=None):
        if not "label" in request.POST:
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

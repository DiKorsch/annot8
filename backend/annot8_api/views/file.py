from django.db.models import Q

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from annot8_api.models import File
from annot8_api.models import BoundingBox
from annot8_api.models import Annotation
from annot8_api.serializers import BoundingBoxSerializer
from annot8_api.serializers import FileSerializer
from annot8_api.views.base import BaseViewSet

class FileViewSet(BaseViewSet):

    serializer_class = FileSerializer
    def get_queryset(self):
        user = self.request.user
        return File.objects.filter(
            Q(project__user=user) |
            Q(project__collaborators__in=[user])
        ).distinct()

    @action(detail=True)
    def bboxes(self, request, pk=None):
        file = self.get_object()

        bboxes = file.bboxes

        serializer = BoundingBoxSerializer(bboxes, many=True)
        response = Response(serializer.data)
        return Response(serializer.data)

    @action(detail=True, methods=["post"], url_path="bbox")
    def bbox_add(self, request, pk=None):
        if not set(["x", "y", "width", "height"]).issubset(request.POST):
            return Response({"status": "Argument for bbox missing"},
                status=status.HTTP_400_BAD_REQUEST)
        file = self.get_object()
        user = self.request.user

        try:
            bbox = BoundingBox.create(file, request.POST.get("x"),
                        request.POST.get("y"), request.POST.get("width"),
                        request.POST.get("height")
                )

            if "label" in request.POST:
                annotation = Annotation.create(described_object=bbox,
                            label=request.POST.get("label"), annotator=user
                    )

        except Exception as e:
            print(e)
            return Response({"status": str(e)},
                status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({'status': 'BBox added'})

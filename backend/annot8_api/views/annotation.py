from django.db.models import Q

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from annot8_api.models import Annotation

from annot8_api.serializers import AnnotationSerializer
from annot8_api.views.base import BaseViewSet

class AnnotationViewSet(BaseViewSet):

    serializer_class = AnnotationSerializer
    def get_queryset(self):
        user = self.request.user
        return Annotation.objects.filter(
            Q(described_object__boundingbox__described_file__project__user=user) |
            Q(described_object__boundingbox__described_file__project__collaborators__in=[user]) |
            Q(described_object__file__project__user=user) |
            Q(described_object__file__project__collaborators__in=[user])
        ).distinct()

    @action(detail=True, methods=["post"], url_path="toggle_confirmator")
    def confirmator_toggle(self, request, pk=None):
        annotation = self.get_object()
        user = request.user

        if user == annotation.annotator:
            return Response({"status": "The annotator cannot confirm its own annotations."},
                status=status.HTTP_400_BAD_REQUEST)

        if user in annotation.confirmators.all():
            annotation.confirmators.remove(user)
        else:
            annotation.confirmators.add(user)
        return Response({'status': 'Confirmator added'})

    @action(detail=True, methods=["post"], url_path="confirmator")
    def confirmator_add(self, request, pk=None):
        annotation = self.get_object()
        user = request.user

        if user == annotation.annotator:
            return Response({"status": "The annotator cannot confirm its own annotations."},
                status=status.HTTP_400_BAD_REQUEST)

        if user in annotation.confirmators.all():
            return Response({"status": "User has already confirmed the annotation"},
                status=status.HTTP_400_BAD_REQUEST)

        annotation.confirmators.add(user)
        return Response({'status': 'Confirmator added'})

    @action(detail=True, methods=['delete'], url_path=r"confirmator")
    def confirmator_remove(self, request, pk=None, name=None):
        annotation = self.get_object()
        user = request.user

        if user not in annotation.confirmators.all():
            return Response({"status": "User to remove is not a confirmator of the annotation"},
                status=status.HTTP_400_BAD_REQUEST)

        annotation.confirmators.remove(user)
        return Response({'status': 'Confirmator removed'})

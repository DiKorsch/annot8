from django.db.models import Q

from annot8_api.models import File
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

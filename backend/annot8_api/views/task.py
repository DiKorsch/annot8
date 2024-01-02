import datetime as dt

from django.utils import timezone
from django.db.models import Q

from annot8_api import models as api_models
from annot8_api import serializers
from annot8_api.views import base

class TaskViewSet(base.BaseViewSet):

    serializer_class = serializers.TaskSerializer

    def get_queryset(self):
        now = timezone.now()
        delta = dt.timedelta(minutes=5)
        return api_models.Task.objects.filter(
            Q(user=self.request.user) &
            (Q(finished__isnull=True) | Q(finished__gte=now - delta))
        ).distinct()


from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django_q.models import Success
from django_q.models import Task as QTask
from django_q.models import Failure
from django_q.tasks import fetch, count_group_cached

from annot8_api.models import base

class Task(base.BaseModel):
    user = models.ForeignKey(User,
        on_delete=models.CASCADE,
        related_name="tasks",
        related_query_name="task",
    )

    task_uuid = models.CharField(max_length=255,
        editable=False)

    nqueued = models.PositiveIntegerField(default=0)

    finished = models.DateTimeField(blank=True, null=True)


    serializer_fields = base.BaseModel.serializer_fields + [
        "user",
        "task_uuid",
        "nqueued",
        "nready",
        "finished",
        "task_info",
    ]


    read_only_fields = base.BaseModel.read_only_fields + [
        "user",
        "task_uuid",
        "nqueued",
        "nready",
        "finished",
        "task_info",
    ]

    @property
    def queued_task(self):
        return fetch(self.task_uuid)

    @property
    def nready(self):
        task = self.queued_task
        if task is None:
            return count_group_cached(self.task_uuid)
        else:
            return self.nqueued

    @property
    def task_info(self):
        task = self.queued_task
        if task is None:
            return dict(ready=False)

        return dict(
            ready=True,
            args=task.args,
            result=task.result
        )

    @classmethod
    def new(cls,*, save: bool = True, **kwargs):
        obj = cls(**kwargs)

        if save:
            obj.save()

        return obj

@receiver(models.signals.post_delete, sender=QTask)
@receiver(models.signals.post_delete, sender=Failure)
@receiver(models.signals.post_delete, sender=Success)
def cascade(sender, instance, *args, **kwargs):
    try:
        Task.objects.get(task_uuid=instance.id).delete()
    except Task.DoesNotExist:
        pass

@receiver(models.signals.post_save, sender=Failure)
@receiver(models.signals.post_save, sender=Success)
@receiver(models.signals.post_save, sender=QTask)
def set_finished(sender, instance, *args, **kwargs):
    try:
        task = Task.objects.get(task_uuid=instance.id)
        task.finished = instance.stopped
        task.save()
    except Task.DoesNotExist as e:
        print(e)
        pass

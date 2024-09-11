from annot8_api.views import project
from annot8_api.views import task
from annot8_api.views import file
from annot8_api.views import label
from annot8_api.views import bbox
from annot8_api.views.base import BaseViewSet
from annot8_api.views import annotation

from rest_framework import routers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView as BaseTokenObtainView
from rest_framework_simplejwt.views import TokenRefreshView as BaseTokenRefreshView

class CustomTokenSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)

        # Add custom data
        data['username'] = self.user.username

        return data

class TokenObtainPairView(BaseTokenObtainView):
    serializer_class = CustomTokenSerializer


class TokenRefreshView(BaseTokenRefreshView):
    # serializer_class = CustomTokenSerializer
    pass

class UserViewSet(BaseViewSet):

    @action(detail=False, methods=['post'], url_path='change-password')
    def change_password(self, request, *args, **kwargs):
        user = request.user
        if not user.check_password(request.data['old_password']):
            return Response({"status": "Old password is incorrect"}, status=400)
        user.set_password(request.data['new_password'])
        user.save()

        return Response({"status": "Password changed"})

router = routers.DefaultRouter()
router.register(r'user', UserViewSet, "user")
router.register(r'project', project.ProjectViewSet, "project")
router.register(r'task', task.TaskViewSet, "task")
router.register(r'file', file.FileViewSet, "file")
router.register(r'bbox', bbox.BBoxViewSet, "bbox")
router.register(r'annotation', annotation.AnnotationViewSet, "annotation")
router.register(r'label', label.LabelViewSet, "label")
router.register(r'label-group', label.LabelGroupViewSet, "label-group")

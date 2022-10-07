from annot8_api.views import project
from annot8_api.views import label

from rest_framework import routers
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


router = routers.DefaultRouter()
router.register(r'project', project.ProjectViewSet, "project")
router.register(r'label', label.LabelViewSet, "label")
router.register(r'label-group', label.LabelGroupViewSet, "label-group")

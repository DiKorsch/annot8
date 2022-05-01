from django import http
from django import views
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.response import Response

class JsonResponseView(views.View):

    @classmethod
    def respond(cls, obj = {}):
        return http.JsonResponse(obj, safe=False)


class BaseViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]


    def new_response(self, obj, **kwargs):
        serializer = self.get_serializer(obj, **kwargs)
        return Response(serializer.data)

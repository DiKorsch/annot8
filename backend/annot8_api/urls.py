"""pycs_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import include
from django.urls import path
from annot8_api import views


urlpatterns = [
    path('', include(views.router.urls)),

    path('api-token/',
        views.TokenObtainPairView.as_view(), name="obtain-token"),

    path('api-token-refresh/',
        views.TokenRefreshView.as_view(), name="refresh-token"),
]

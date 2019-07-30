"""mud_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from .views import sanity_check

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', sanity_check, name='sanity-check'),
    path('api/auth/',
         TokenObtainPairView.as_view(),
         name="token-obtain-pair"),
    path('api/auth/verify/',
         TokenVerifyView.as_view(),
         name="token-verification"),
    path('api/auth/refresh/',
         TokenRefreshView.as_view(),
         name="token-refresh"),
]

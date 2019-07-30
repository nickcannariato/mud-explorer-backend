from django.contrib import admin
from django.urls import path, include

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
    path('api/game/', include('mud_explorer.urls'))
]

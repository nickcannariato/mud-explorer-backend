from django.urls import path

from .views import init_pass

urlpatterns = [
    path('init', init_pass, name="game-init")
]

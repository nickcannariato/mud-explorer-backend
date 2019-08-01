from django.urls import path

from .views import init_pass, init_move, init_take, init_drop, init_sell, init_confirm_sell, init_status, init_examine, init_change_name, init_pray, init_flight, init_dash, get_all_rooms

urlpatterns = [
    path('init/', init_pass, name="game-init"),
    path('move/', init_move, name="game-move"),
    path('take/', init_take, name="game-take"),
    path('drop/', init_drop, name="game-drop"),
    path('sell/', init_sell, name="game-sell"),
    path('sell/confirm/', init_confirm_sell, name="game-sell-confirm"),
    path('status/', init_status, name="game-status"),
    path('examine/', init_examine, name="game-examine"),
    path('change_name/', init_change_name, name="game-change_name"),
    path('pray/', init_pray, name="game-pray"),
    path('fly/', init_flight, name="game-fly"),
    path('dash/', init_dash, name="game-dash"),




]

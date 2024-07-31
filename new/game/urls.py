from django.urls import path
from .views import GameUsers
from . import views

urlpatterns = [
    path('rooms/', views.rooms, name='rooms'),
    path('game/<str:room_name>/', views.game, name='game'),
    path('player_history/<str:player_name>/', GameUsers.as_view() , name='player_history'),
]

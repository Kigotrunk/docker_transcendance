from django.urls import path
from . import views

urlpatterns = [
    path('history/<int:user_id>/', views.GameUsers.as_view() , name='player_history'),
    path('status/', views.UserStatus.as_view(), name='status'),
]

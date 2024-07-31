from django.urls import path
from myaccount.views import (
    profil_view,
)
app_name = "myaccount"

urlpatterns = [
    path('<user_id>/', profil_view, name='profile'),
]

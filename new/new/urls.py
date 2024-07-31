"""
URL configuration for new project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.contrib.auth import views as auth_views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from front import views
from django.conf.urls import include
from django.urls import include
from chat.views import ConversationListView, ConversationDetailView, BlockUserView, CheckBlockStatusView, AskCidView
from game.views import GameUsers
urlpatterns = [
    path('accounts/', include('allauth.urls')),
]


#from myaccount.views import (
    #register_view,
    #login_view,
    #logout_view,
    #update_user_view,
#)

# from game.views import (
#     pong
# )

from django.urls import path
from myaccount.views import (
    RegisterAPIView, 
    LoginAPIView, 
    RefreshTokenAPIView, 
    LogoutAPIView, 
    ProfileAPIView, 
    UserSearchAPIView, 
    PasswordResetRequestView,
    PasswordResetConfirmView,
)

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from rest_framework_simplejwt.views import TokenBlacklistView

from friends.views import SendInvitationView, RespondInvitationView, RemoveFriendView, FriendStatusView, FriendListView, ConnectionStatusAPIView

from api.views import (
    AuthStudent
)
urlpatterns = [
    # VIEW RESET DJANGO
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # OTHER
    path('api/reset_password_confirm/', PasswordResetConfirmView.as_view(), name='reset_password_confirm'),
    path('api/reset_password/', PasswordResetRequestView.as_view(), name='reset_password'),
    path('send_invitation/', SendInvitationView.as_view(), name='send_invitation'),
    path('respond_invitation/', RespondInvitationView.as_view(), name='respond_invitation'),
    path('remove_friend/', RemoveFriendView.as_view(), name='remove_friend'),
    path('friend_status/', FriendStatusView.as_view(), name='friend_status'),
    path('friend_list/', FriendListView.as_view(), name='friend_list'),
    path('block_status/', CheckBlockStatusView.as_view(), name='block_status'),
    path('block_user/', BlockUserView.as_view(), name='block_user'),
    path('connection_status/<int:user_id>/', ConnectionStatusAPIView.as_view(), name='connection_status'),
    path('api/conversations/', ConversationListView.as_view(), name='conversations'),
    path('api/conversations/<int:conversation_id>/', ConversationDetailView.as_view(), name='messages'),
    path('ask_cid/', AskCidView.as_view(), name='ask_cid'),
    path('api/users/', UserSearchAPIView.as_view(), name='user_search'),
    path('api/register/', RegisterAPIView.as_view(), name='register'),
    path('api/login/', LoginAPIView.as_view(), name='login'),
    path('api/refresh/', RefreshTokenAPIView.as_view(), name='refresh'),
    path('api/logout/', LogoutAPIView.as_view(), name='logout'),
    path('api/profile/<int:user_id>/', ProfileAPIView.as_view(), name='profile'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    #path('chat/<str:username1>/<str:username2>', chat_view, name='chat_view'),
    path('accounts/', include('allauth.urls')),
    path('', include('game.urls')),
    path('api/', AuthStudent, name='api'),
    path('api/history/<int:user_id>/', GameUsers.as_view() , name='history'),
    #path('player_history/<str:player_name>/', views.player_history , name='player_history'),
]



# old view django
    #path('register/', register_view, name='register'),
    #path('logout/', logout_view, name='logout'),
    #path('login/', login_view, name='login'),
    #path('reset_password/', auth_views.PasswordResetView.as_view(), name='reset_password'),
    #path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    #path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    #path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    #path('profil/', include('myaccount.urls', namespace = 'account')),
    #path('update/', update_user_view, name='update_user'),
    #path('profile/', views.profile , name='profile'),

if settings.DEBUG:
    urlpatterns+= static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns+= static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

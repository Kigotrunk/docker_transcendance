from rest_framework import serializers
from .models import Friend, Invitation
from myaccount.models import Account


class FriendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id', 'username', 'email', 'hide_email', 'profile_picture', 'date_joined', 'last_login', 'is_active', 'is_in_game', 'nb_win', 'nb_loose', 'is_connected')


class InvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invitation
        fields = ['sender', 'receiver', 'status', 'time']
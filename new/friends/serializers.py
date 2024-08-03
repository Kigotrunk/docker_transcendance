from rest_framework import serializers
from .models import Friend, Invitation
from myaccount.models import Account


class FriendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id', 'username', 'profile_picture', 'is_in_game', 'is_connected')


class InvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invitation
        fields = ['sender', 'receiver', 'status', 'time']
from rest_framework import serializers
from myaccount.models import Account
from .models import UserBlock

class UserBlockSerializer(serializers.ModelSerializer):
    blocker = serializers.SlugRelatedField(slug_field='username', queryset=Account.objects.all())
    blocked = serializers.SlugRelatedField(slug_field='username', queryset=Account.objects.all())

    class Meta:
        model = UserBlock
        fields = ['id', 'blocker', 'blocked', 'timestamp']
        read_only_fields = ['timestamp']
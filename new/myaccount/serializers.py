from rest_framework import serializers
from .models import Account
from django.contrib.auth import login, authenticate
from chat.models import Conversation, PrivateMessage

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id', 'username', 'profile_picture', 'nb_win', 'nb_loose', 'elo', 'nb_top8', 'nb_top4', 'nb_top2', 'nb_top1', 'highest_score')


class PrivateMessageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrivateMessage
        fields = ('id', 'conversation', 'message', 'issuer', 'receiver', 'moment')

class PrivateMessageSerializer(serializers.ModelSerializer):
    issuer = AccountSerializer()
    receiver = AccountSerializer()

    class Meta:
        model = PrivateMessage
        fields = ('id', 'conversation', 'message', 'issuer', 'receiver', 'moment')

class ConversationSerializer(serializers.ModelSerializer):
    user1 = AccountSerializer()
    user2 = AccountSerializer()

    class Meta:
        model = Conversation
        fields = ('id', 'user1', 'user2', 'time')

class RegistrationSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = Account
        fields = ('username', 'email', 'password1', 'password2')

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("Les mots de passe ne correspondent pas.")
        return data

    def create(self, validated_data):
        user = Account(
            email=validated_data['email'],
            username=validated_data['username'],
        )
        user.set_password(validated_data['password1'])
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        if email and password:
            user = authenticate(email=email, password=password)
            if user:
                data['user'] = user
            else:
                raise serializers.ValidationError("Les identifiants sont incorrects.")
        else:
            raise serializers.ValidationError("L'email et le mot de passe sont nécessaires.")
        return data


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('username', 'email', 'hide_email', 'profile_picture', 'is_active', 'is_in_game')

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.hide_email = validated_data.get('hide_email', instance.hide_email)
        instance.profile_picture = validated_data.get('profile_picture', instance.profile_picture)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.is_in_game = validated_data.get('is_in_game', instance.is_in_game)
        instance.save()
        return instance

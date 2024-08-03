from django.shortcuts import render, redirect, get_object_or_404
from friends.models import Friend
from myaccount.models import Account
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from myaccount.models import Account
from .models import Friend, Invitation
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import AccessToken
from .serializers import FriendSerializer
from myaccount.serializers import AccountSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

# Create your views here.


class SendInvitationView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user

        receiver_id = request.query_params.get('receiver_id')
        if not receiver_id:
            return Response({"error": "Receiver ID not provided"}, status=status.HTTP_400_BAD_REQUEST)

        receiver = get_object_or_404(Account, id=receiver_id)
        if Invitation.objects.filter(sender=user, receiver=receiver).exists():
            return Response({"error": "Invitation already sent"}, status=status.HTTP_400_BAD_REQUEST)
        
        if Invitation.objects.filter(sender=receiver, receiver=user).exists():
            Friend.objects.create(user=user, friend=receiver)
            Invitation.objects.filter(sender=receiver, receiver=user).delete()
            return Response({"detail": "Friend add successfully"}, status=status.HTTP_201_CREATED)
        Invitation.objects.create(sender=user, receiver=receiver)
        return Response({"detail": "Invitation sent successfully"}, status=status.HTTP_201_CREATED)


class RespondInvitationView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        sender_id = request.query_params.get('sender_id')
        if not sender_id:
            return Response({"error": "Sender ID not provided"}, status=status.HTTP_400_BAD_REQUEST)
        action = request.query_params.get('action')
        if action not in ['accept', 'reject']:
            return Response({"error": "Invalid action"}, status=status.HTTP_400_BAD_REQUEST)
        sender = get_object_or_404(Account, id=sender_id)
        invitation = get_object_or_404(Invitation, sender=sender, receiver=user)
        if action == 'accept':
            invitation.status = Invitation.ACCEPTED
            invitation.save()
            Friend.objects.create(user=user, friend=invitation.sender)
            Invitation.objects.filter(sender=sender, receiver=user).delete()
            return Response({"detail": "Invitation accepted successfully"}, status=status.HTTP_200_OK)
        elif action == 'reject':
            invitation.status = Invitation.REJECTED
            invitation.save()
            return Response({"detail": "Invitation rejected successfully"}, status=status.HTTP_200_OK)

class RemoveFriendView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        friend_id = request.query_params.get('friend_id')
        if not friend_id:
            return Response({"error": "Friend ID not provided"}, status=status.HTTP_400_BAD_REQUEST)
        friend = get_object_or_404(Account, id=friend_id)
        if Friend.objects.filter(user=user, friend=friend).exists():
            Friend.objects.filter(user=user, friend=friend).delete()
        elif Friend.objects.filter(user=friend, friend=user).exists():
            Friend.objects.filter(user=friend, friend=user).delete()
        else:
            return Response({"error": "Not friends"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "Friend removed successfully"}, status=status.HTTP_200_OK)
    

class FriendStatusView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        friend_id = request.query_params.get('friend_id')
        if not friend_id:
            return Response({"error : Invalid ID"}, status=status.HTTP_400_BAD_REQUEST)
        try : 
            friend = Account.objects.get(id=friend_id)
            if Friend.objects.filter(user=user, friend=friend).exists() or Friend.objects.filter(user=friend, friend=user).exists():
                return Response({"friendStatus": "friends"}, status=status.HTTP_200_OK)
            elif Invitation.objects.filter(sender=user, receiver=friend).exists():
                return Response({"friendStatus": "sent"}, status=status.HTTP_200_OK)
            elif Invitation.objects.filter(sender=friend, receiver=user).exists():
                return Response({"friendStatus": "received"}, status=status.HTTP_200_OK)
            else:
                return Response({"friendStatus": "none"}, status=status.HTTP_200_OK)
        except friend.DoesNotExist:
            return Response({"error : Invalid Friend"}, status=status.HTTP_400_BAD_REQUEST)
        

class FriendListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        friendlist = Friend.objects.filter(user=user) | Friend.objects.filter(friend=user)
        id_accounts = set()
        for friend in friendlist:
            id_accounts.add(friend.user.id)
            id_accounts.add(friend.friend.id)
        id_accounts.discard(user.id)
        accounts = Account.objects.filter(id__in=id_accounts)
        serializer = FriendSerializer(accounts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ConnectionStatusAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        user = request.user
        friend = get_object_or_404(Account, id=user_id)
        if not friend:
            return Response({"error": "Invalid ID"}, status=status.HTTP_400_BAD_REQUEST)
        if user == friend:
            return Response({"is_friend": True, "is_connected": True, "is_in_game": friend.is_in_game}, status=status.HTTP_200_OK)
        if not Friend.objects.filter(user=user.id, friend=friend.id).exists() and not Friend.objects.filter(user=friend.id, friend=user.id).exists():
            return Response({"is_friend": False, "is_connected": False, "is_in_game": False}, status=status.HTTP_200_OK)
        return Response({"is_friend": True, "is_connected": friend.is_connected, "is_in_game": friend.is_in_game}, status=status.HTTP_200_OK)

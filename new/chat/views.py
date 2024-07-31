from django.shortcuts import render, get_object_or_404, redirect
from .models import PrivateMessage, UserBlock, Conversation
from myaccount.models import Account
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseForbidden
from .forms import FormMessage
from django.urls import reverse
from django.db.models import Prefetch, Q
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import generics
from myaccount.serializers import ConversationSerializer, PrivateMessageSerializer, AccountSerializer, PrivateMessageCreateSerializer
from rest_framework.generics import ListAPIView
from .utils import get_user
from rest_framework.exceptions import AuthenticationFailed
from asgiref.sync import sync_to_async
from django.contrib.auth.models import AnonymousUser
from rest_framework import status
import asyncio
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.pagination import PageNumberPagination
from django.utils import timezone
from .serializers import UserBlockSerializer

# Create your views here.

class ConversationListView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        conversations = Conversation.objects.filter(user1=user) | Conversation.objects.filter(user2=user) # ??????????????
        for conversation in conversations:
            last_message = PrivateMessage.objects.filter(conversation=conversation).order_by('-moment').first()
            if last_message:
                conversation.last_message_sent_at = last_message.moment
                conversation.save()
        conversations = conversations.order_by('-last_message_sent_at')
        
        paginator = PageNumberPagination()
        paginator.page_size = 10
        result_page = paginator.paginate_queryset(conversations, request)
        
        serializer = ConversationSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

class ConversationDetailView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, conversation_id, *args, **kwargs):
        user = request.user
        conversation = get_object_or_404(Conversation, id=conversation_id)
        
        if user != conversation.user1 and user != conversation.user2:
            raise AuthenticationFailed('Not authorized to view this conversation')
        
        user2 = conversation.user2 if user == conversation.user1 else conversation.user1

        # if UserBlock.objects.filter(blocker=user, blocked=user2).exists() or UserBlock.objects.filter(blocker=user2, blocked=user).exists():
        #         return Response({"blocked": True}, status=status.HTTP_200_OK)
        
        messages = PrivateMessage.objects.filter(conversation=conversation).order_by('-moment')
        
        paginator = PageNumberPagination()
        paginator.page_size = 20
        result_page = paginator.paginate_queryset(messages, request)
        
        serializer = PrivateMessageSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    
class AskCidView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        print(user)
        user2_id = request.query_params.get('user2_id')
        if not user2_id:
            return Response({"error" : "user2_id missing"}, status=status.HTTP_400_BAD_REQUEST)
        user2 = get_object_or_404(Account, id=user2_id)
        if not user2:
            return Response({"error" : "user2 not found"}, status=status.HTTP_404_NOT_FOUND)
        print(user2)
        conversation = Conversation.objects.filter(Q(user1=user, user2=user2) | Q(user1=user2, user2=user)).first()
        if not conversation:
            return Response({"id" : None}, status=status.HTTP_200_OK)
        serializer = ConversationSerializer(conversation)
        return Response(serializer.data, status=status.HTTP_200_OK)

class RefreshTokenView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        user = request.user
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })

class BlockUserView(APIView) :

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
        
    def post(self, request, *args, **kwargs):
        user = request.user
        blocker_id = request.query_params.get('blocked_id')
        unblock = request.query_params.get('unblock')
        if not blocker_id:
            return Response({"error" : "user_id missing"}, status=status.HTTP_400_BAD_REQUEST)
        blocked_user = get_object_or_404(Account, id=blocker_id)
        if unblock:
            if not UserBlock.objects.filter(blocker=user, blocked=blocked_user).exists():
                return Response({"error" : "you have not block this user"},status=status.HTTP_400_BAD_REQUEST)
            UserBlock.objects.filter(blocker=user, blocked=blocked_user).delete()
            return Response({"success" : "User unblocked"}, status=status.HTTP_200_OK)
        if UserBlock.objects.filter(blocker=user, blocked=blocked_user).exists():
            return Response({"error" : "you have already block this user"},status=status.HTTP_400_BAD_REQUEST)
        UserBlock.objects.create(blocker=user, blocked=blocked_user)
        return Response({"success" : "User blocked"}, status=status.HTTP_200_OK)


class CheckBlockStatusView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        other_user_id = request.query_params.get('other_id')
        conversation_id = request.query_params.get('conversation_id')
        if not other_user_id and not conversation_id:
            return Response({"error" : "other_user or conversation_id missing"}, status=status.HTTP_400_BAD_REQUEST)
        if other_user_id:
            other_user = get_object_or_404(Account, id=other_user_id)
            if UserBlock.objects.filter(blocker=user, blocked=other_user).exists():
                return Response({"blocked": True}, status=status.HTTP_200_OK)
            return Response({"blocked": False}, status=status.HTTP_200_OK)
        conversation = get_object_or_404(Conversation, id=conversation_id)
        other_user = conversation.user1 if user == conversation.user2 else conversation.user2
        if UserBlock.objects.filter(blocker=user, blocked=other_user).exists() or UserBlock.objects.filter(blocker=other_user, blocked=user).exists():
            return Response({"blocked": True}, status=status.HTTP_200_OK)
        return Response({"blocked": False}, status=status.HTTP_200_OK)
        

class RemoveBlockView(APIView):

    def post(self, request, *args, **kwargs):
        user = request.user
        blocked_id = request.query_params.get('blocked_id')
        if not blocked_id:
            return Response({"error": "blocked ID not provided"}, status=status.HTTP_400_BAD_REQUEST)

        blocked = get_object_or_404(Account, id=blocked_id)
        if not UserBlock.objects.filter(blocker=user, blocked=blocked).exists():
            return Response({"error": "Not friends"}, status=status.HTTP_400_BAD_REQUEST)

        UserBlock.objects.filter(blocker=user, blocked=blocked).delete()
        return Response({"detail": "unblock successfully"}, status=status.HTTP_200_OK)
    

class BlockedListView(APIView):

    def get(self, request, *args, **kwargs):
        user = request.user
        blockedList = UserBlock.objects.filter(blocker=user)
        serializer = UserBlockSerializer(blockedList, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from django.http import JsonResponse
from .models import partie
from myaccount.models import Account
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import AccessToken
from django.db.models import Prefetch, Q
from .serializers import GameSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.authentication import JWTAuthentication
from .consumers import PongConsumer

"""
def player_history(request, player_name):

    try:
        history = partie.objects.filter(Q(player1=user) | Q(player2=user)).order_by('-time')[:10]
        #all_parties = sorted(
            #list(parties_as_player1) + list(parties_as_player2),
            #key=lambda x: x.id,
            #reverse=True
        #)[:10]

        response_data = [
            {
                'player1': game.player1.username,
                'player2': game.player2.username,
                'score_player1': game.score_player1,
                'score_player2': game.score_player2,
            }
            for game in history
        ]
        return JsonResponse(response_data, safe=False)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
"""

"""class GameUsers(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        id_user = user_id
        if not id_user:
            return JsonResponse({'error': 'Missing id'}, status=400)
        userhisto = get_object_or_404(Account, id=id_user)
        try:
            history = partie.objects.filter(Q(player1=userhisto) | Q(player2=userhisto)).order_by('-time')[:10]
            serializer = GameSerializer(history, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)"""
        

class GameUsers(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        userhistory = get_object_or_404(Account, id=user_id)
        try:
            history = partie.objects.filter(Q(player1=userhistory) | Q(player2=userhistory)).order_by('-time') #[:10]
            paginator = PageNumberPagination()
            paginator.page_size = 10
            history_page = paginator.paginate_queryset(history, request)
            serializer = GameSerializer(history_page, many=True)
            return paginator.get_paginated_response(serializer.data)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=404)

class UserStatus(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return JsonResponse({"in_lobby": PongConsumer.in_lobby}, status=200)

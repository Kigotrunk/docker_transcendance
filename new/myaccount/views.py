from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, login, logout
from .serializers import AccountSerializer, RegistrationSerializer, LoginSerializer, UserUpdateSerializer
from .models import Account
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import AccessToken
from django.conf import settings
from threading import Timer

class UserSearchAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
        
    def get(self, request): 
        search_term = request.query_params.get('search', '')
        if search_term:
            users = Account.objects.filter(username__icontains=search_term)
        else:
            users = Account.objects.none()  
        serializer = AccountSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class RegisterAPIView(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            email = serializer.validated_data['email']
            raw_password = serializer.validated_data['password1']
            user = authenticate(email=email, password=raw_password)
            if user:
                login(request, user)
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'user': AccountSerializer(user).data
                }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginAPIView(APIView):
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)  
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': AccountSerializer(user).data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class RefreshTokenAPIView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            user = Account.objects.get(id=token['user_id'])
            access_token = token.access_token
            return Response({
                'access': str(access_token),
                'user': AccountSerializer(user).data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": "Invalid refresh token"}, status=status.HTTP_400_BAD_REQUEST)


class LogoutAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            user = request.user
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class ProfileAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        account = get_object_or_404(Account, pk=user_id)
        serializer = AccountSerializer(account)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, user_id):
        user = request.user
        account = get_object_or_404(Account, pk=user_id)
        if user != account:
            return Response({"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)

        serializer = UserUpdateSerializer(account, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetRequestView(APIView):
    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({"error": "Email is missing"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = Account.objects.get(email=email)
        except Account.DoesNotExist:
            return Response({"error": "Invalid Email"}, status=status.HTTP_404_NOT_FOUND)
        
        token_generator = PasswordResetTokenGenerator()
        token = token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        reset_link = f"http://localhost:5173/reset/{uid}/{token}/"
        
        send_mail(
            'Password Reset',
            f'Click to reset your password: {reset_link}',
            'haouni@student.42nice.fr',
            [email],
            fail_silently=False,
        )
        
        return Response({"message": "Password reset email sent"}, status=status.HTTP_200_OK)

class PasswordResetConfirmView(APIView):
    def post(self, request, *args, **kwargs):
        uidb64 = request.data.get('uidb64')
        token = request.data.get('token')
        password = request.data.get('password')
        password2 = request.data.get('password2')      
        if not password:
            return Response({"error": "Password is required"}, status=status.HTTP_400_BAD_REQUEST)
        if not password2:
            return Response({"error": "Password confirmation is required"}, status=status.HTTP_400_BAD_REQUEST)     
        if password != password2:
            return Response({"error": "Passwords must be identical"}, status=status.HTTP_400_BAD_REQUEST)    
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = Account.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
            user = None       
        token_generator = PasswordResetTokenGenerator()
        if user is not None and token_generator.check_token(user, token):
            user.set_password(password)
            user.save()
            return Response({"message": "Password has been reset"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)


class Test(APIView):
    def test_a(self):
        subject = 'Password reinitialisation'
        message = 'ICI CLIC'
        addr_user = ["shadowmimpose@gmail.com"]
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, addr_user)


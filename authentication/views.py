from rest_framework import generics,permissions
from rest_framework.response import Response
from django.contrib.auth import authenticate
from knox.models import AuthToken
from . models import PasswordResetTokenCode
from .serializers import *
from django.contrib.auth import get_user_model
from rest_framework import status
from django.template.loader import render_to_string
from datetime import timedelta
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from django.utils.crypto import get_random_string
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password
from common.paginations import ReferralPagination,StandardResultsPagination
from common.filters import UserFilter 
from rest_framework import generics, filters as rest_filters
from django_filters.rest_framework import DjangoFilterBackend
import socket

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()  # Save and get the user instance

        # Check for a referral code
        referrer_id = request.data.get('referral_code')
        if referrer_id:
            try:
                referrer = User.objects.get(id=referrer_id)
                user.referred_by = referrer  # Assign the referrer
            except User.DoesNotExist:
                pass  # Ignore invalid referral code
        
        user.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class LoginView(generics.GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]  # Allow access to any user

    def post(self, request, *args, **kwargs):
        print(request.data)
        # Extract email, password, and is_admin from request data
        email = request.data.get('email')
        password = request.data.get('password')
        # is_admin_requested = request.data.get('is_admin', False)  # Get is_admin if provided
        
        try:
            # Authenticate the user
            user = authenticate(request, email=email, password=password)
            if not user:
                return Response({"error": "Invalid credentials"}, status=400)

            # Check if is_admin was requested and if it matches the user’s is_admin status
            # if user.is_admin != is_admin_requested:
            #     return Response({"error": "Authentification status mismatch"}, status=400)

            # Create Knox token
            _, token = AuthToken.objects.create(user)
            user_data = UserSerializer(user).data
            
            # Return user data and token
            return Response({
                'user': user_data,
                'token': token
            })
        except (socket.error, BrokenPipeError):
            print(socket.error)

class PasswordResetRequestView(APIView):
    def post(self, request):
        email = request.data.get('email')
        
        # Check if a user with the given email exists
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "Utilisateur non trouvé."}, status=status.HTTP_404_NOT_FOUND)
        #Invalidate or delete existing tokens for the user
        PasswordResetTokenCode.objects.filter(user=user).delete()
        # Generate a reset token and code
        reset_token = get_random_string(length=32)  # Generate a secure token
        reset_code = get_random_string(length=6)  # Generate a 6-digit code
        expiration_time = timezone.now() + timedelta(minutes=5)  # Set expiration time to 5 minutes

        # Save the token and code in the PasswordResetTokenCode model
        PasswordResetTokenCode.objects.create(user=user, token=reset_token, code=reset_code, expires_at=expiration_time)

        # Send the reset code via email
        subject = "Demande de Réinitialisation de Mot de Passe"
        html_message = render_to_string("password_reset_email.html", {"reset_code": reset_code})
        send_mail(subject, "", settings.DEFAULT_FROM_EMAIL, [email], html_message=html_message)
        
        return Response({"message": "Le code de réinitialisation de mot de passe a été envoyé."}, status=status.HTTP_200_OK)


class PasswordResetConfirmView(APIView):
    def post(self, request):
        email = request.data.get('email')
        code = request.data.get('code')

        if not email or not code:
            return Response({"error": "Email et code sont requis."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Retrieve the user by email
            user = User.objects.get(email=email)
            # Retrieve the reset token code from the database
            reset_token = PasswordResetTokenCode.objects.get(user=user, code=code)
            
            # Check if the code is still valid
            if not reset_token.is_valid():
                # Code is valid; generate a new token for password reset
                new_token = get_random_string(length=32)  # Generate a new token
                reset_token.token = new_token  # Update the token in the database but keep the previous code
                reset_token.save()  # Save the changes

            # Respond with the new token
            return Response({
                "message": "Le code est valide. Vous pouvez réinitialiser votre mot de passe.",
                "token": reset_token.token,
                }, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({"error": "Utilisateur non trouvé."}, status=status.HTTP_404_NOT_FOUND)  # User not found
        except PasswordResetTokenCode.DoesNotExist:
            return Response({"error": "Code invalide."}, status=status.HTTP_404_NOT_FOUND)


class PasswordResetView(APIView):
    def post(self, request):
        token = request.data.get('token')  
        new_password = request.data.get('new_password')

        if not token or not new_password:
            return Response({"error": "Token, code, and new password are required."},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            # Retrieve the token from the database
            reset_token = PasswordResetTokenCode.objects.get(token=token)

            # Check if the token is still valid
            if not reset_token.is_valid():
                return Response({"error": "Le code a expiré."}, status=status.HTTP_400_BAD_REQUEST)

            # Update the user's password
            user = reset_token.user
            user.password = make_password(new_password)  # Hash the new password
            user.save()

            # Optionally, delete the token after successful reset
            reset_token.delete()

            return Response({"message": "Le mot de passe a été réinitialisé avec succès."},
                            status=status.HTTP_200_OK)

        except PasswordResetTokenCode.DoesNotExist:
            return Response({"error": "Code invalide."}, status=status.HTTP_404_NOT_FOUND)
        
        
class ReferralListView(generics.ListAPIView):
    serializer_class = GetUserSerializer
    pagination_class = ReferralPagination
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(referred_by=self.request.user).order_by("-date_joined")
    

class UserListView(generics.ListAPIView):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    pagination_class = StandardResultsPagination
    filter_backends = [DjangoFilterBackend, rest_filters.SearchFilter]  # Use DjangoFilterBackend explicitly
    filterset_class = UserFilter
    search_fields = ['first_name', 'last_name', 'email','i_admin']  # Fields to search by
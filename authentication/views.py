from rest_framework import generics,permissions
from rest_framework.response import Response
from django.contrib.auth import authenticate
from knox.models import AuthToken
from .serializers import UserSerializer

class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer

class LoginView(generics.GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]  # Allow access to any user

    def post(self, request, *args, **kwargs):
        # Extract email and password from request data
        email = request.data.get('email')
        password = request.data.get('password')

        # Authenticate the user
        user = authenticate(request, email=email, password=password)
        if not user:
            return Response({"error": "Invalid credentials"}, status=400)

        # Create Knox token
        _, token = AuthToken.objects.create(user)

        # Return user data and token
        return Response({
            'user': UserSerializer(user).data,
            'token': token
        })

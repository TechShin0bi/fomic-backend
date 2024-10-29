from rest_framework import generics
from rest_framework.response import Response
from knox.views import LoginView as KnoxLoginView
from knox.models import AuthToken
from .serializers import UserSerializer

class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer

class LoginView(KnoxLoginView):
    def post(self, request, format=None):
        serializer = AuthToken.objects.create(request.user)
        return Response({
            'token': serializer[0],
            'user_id': request.user.id,
            'username': request.user.username
        })

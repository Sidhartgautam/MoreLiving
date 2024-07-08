from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .serializers import UserRegisterSerializer, UserLoginSerializer
from django.contrib.auth import login
from rest_framework_simplejwt.tokens import RefreshToken
from core.utils.response import PrepareResponse

class UserRegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = PrepareResponse(
                success=True,
                message="User registered successfully",
                data=serializer.data
            )
            return response.send(code=status.HTTP_201_CREATED)
        else:
            response = PrepareResponse(
                success=False,
                message="User registration failed",
                data=serializer.errors
            )
            return response.send(400)
    
class UserLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)

            refresh = RefreshToken.for_user(user)
            response = PrepareResponse(
                success=True,
                message="Login successful",
                data={
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'user': {
                        'username': user.username,
                        'email': user.email,
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                    }
                }
            )
            return response.send()
        else:
            response = PrepareResponse(
                success=False,
                message="Login failed",
                data=serializer.errors
            )
            return response.send(400)

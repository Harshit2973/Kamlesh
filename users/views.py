from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from .serializers import SignUpSerializer, EmailLoginSerializer

class SignupView(APIView):
    http_method_names = ['post']

    def post(self, request):
        print(request.data)  # Debugging: print incoming data
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            print(serializer.validated_data)  # Debugging: print validated data
            serializer.save()
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        print(serializer.errors)  # Debugging: print serializer errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    http_method_names = ['post']

    def post(self, request):
        print(request.data)  # Debugging: print incoming data
        serializer = EmailLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            print(f"User authenticated: {user}")  # Debugging: print authenticated user
            return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
        print(serializer.errors)  # Debugging: print serializer errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            token = Token.objects.get(user=request.user)
            token.delete()
            return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            return Response({"message": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)

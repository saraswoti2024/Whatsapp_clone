from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from django.contrib.auth.models import User
from .serializers import RegistrationSerializer
from rest_framework import permissions,status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
# Create your views here.
class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer
    
class LoginAfter(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        username = request.user.username
        return Response(f"welcome user {username}")
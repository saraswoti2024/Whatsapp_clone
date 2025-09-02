from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from django.contrib.auth.models import User
from .serializers import *
from .models import *
from rest_framework import permissions,status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

class ProfileView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


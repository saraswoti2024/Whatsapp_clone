from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView,ListAPIView
from django.contrib.auth.models import User
from .serializers import *
from .models import *
from rest_framework import permissions,status
from rest_framework.views import APIView
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q

class ProfileView(CreateAPIView,ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SearchBarPersonal(ListAPIView):
   permission_classes = [IsAuthenticated]
   def get(self,request):
    value = self.request.query_params.get('search',None)
    if value:
        v1 = Message.objects.filter(Q(content__icontains=search) | Q(reciever__icontains=search) | Q(sender_icontains=search)| Q(timestamp__icontains=int(search)))
        native = MessageSerializer(v1,many=True)
        return Response(native.data)

class SearchBarGroup(APIView):
   permission_classes = [IsAuthenticated]
   def get(self,request):
    value = self.request.query_params.get('search',None)
    if value:
        v1 = GroupMessage.objects.filter(Q(content__icontains=search) | Q(group_name1__group_name__icontains=search) | Q(sender__icontains=search)| Q(timestamp__icontains=int(search)))
        native = GroupSerializer(v1,many=True)
        return native


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

   def get(self,request,reciever_id):
    search = self.request.query_params.get('search',None)
    if search:
        v1 = Message.objects.filter(Q(sender__id=request.user.id) & Q(receiver__id = reciever_id )).filter(Q(content__icontains=search) | Q(receiver__username__icontains=search) | Q(sender__username__icontains=search)).select_related('sender','receiver')
        native = MessageSerializer(v1,many=True)
        return Response(native.data)

class SearchBarGroup(APIView):
   permission_classes = [IsAuthenticated]
   def get(self,request,group_name):
    search = self.request.query_params.get('search',None)    
    if search:
        v1 = GroupMessage.objects.filter(group_name1__group_name=group_name).filter(Q(content__icontains=search) | Q(group_name1__group_name__icontains=search) | Q(sender__icontains=search)).select_related('sender','group_name1')
        native = GroupSerializer(v1,many=True)
        return Response(native.data)


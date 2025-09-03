from .models import *
from rest_framework import serializers

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'
        read_only_fields = ['user']


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message 
        fields = '__all__'

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupMessage 
        fields = '__all__'

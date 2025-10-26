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

class AttachmentPersonalSerializer(serializers.ModelSerializer):
    message = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = AttachmentPersonal
        fields = ['photos','timestamp','files_i' , 'message']

class AttachmentGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttachmentGroup
        fields = '__all__'
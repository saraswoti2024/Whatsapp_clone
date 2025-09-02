from rest_framework import serializers
from django.contrib.auth.models import User

class RegistrationSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
  
    class Meta:
        model = User
        fields = ('username','password','first_name','last_name','email','password1')
    
    def validate_email(self,value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('email already exists!')
        return value
    
    def validate(self,attrs):
        if attrs['password']!=attrs['password1']:
            raise serializers.ValidationError('password and password1 didn\'t match')
        return attrs
    
       
    def create(self,validated_data):
        password1 = validated_data.pop('password1')
        email = validated_data.get('email','')
        if not email:
            raise serializers.ValidationError('email is required!')
            
        user = User(first_name=validated_data.get('first_name',''),
        username = validated_data['username'],
        email = validated_data['email'])
        user.set_password(password1)
        user.save()
        return user
        last_name = validated_data.get('last_name',''),
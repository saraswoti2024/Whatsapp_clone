from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} → {self.receiver}: {self.content}"


class Group(models.Model):
      group_name = models.SlugField(max_length=200,default='no_name')
      def __str__(self):
        return self.group_name

class GroupMessage(models.Model):
    sender = models.ForeignKey(User,on_delete=models.CASCADE,related_name='group_sent')
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    group_name1 = models.ForeignKey(Group,on_delete = models.CASCADE,related_name="group_message")

    def __str__(self):
        return f"{self.group_name1}"

class GroupMember(models.Model):
    approved = models.BooleanField(default=False) 
    user_name = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_Group')
    approved_date = models.DateTimeField(auto_now_add=True)
    group_name = models.ForeignKey(Group,on_delete = models.CASCADE,related_name="group_member")

    class Meta:
        unique_together = ['user_name', 'group_name']

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='user_profile')
    image = models.ImageField(upload_to="profile_image",null=True,blank=True)
    about = models.TextField()
    phone = PhoneNumberField(blank=True,null=True)
    status = models.BooleanField(default=False)
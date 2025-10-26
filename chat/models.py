from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100,default="no_name")

    def __str__(self):
        return f"{self.sender} → {self.receiver}: {self.content}"


class Group(models.Model):
    group_name = models.CharField(max_length=200,default='no_name',unique=True)

    def save(self, *args, **kwargs):
        if self.group_name:
            self.group_name = self.group_name.capitalize()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.group_name

class GroupMember(models.Model):
    approved = models.BooleanField(default=False) 
    approved_date = models.DateTimeField(auto_now_add=True)
    group_name = models.ForeignKey(Group,on_delete = models.CASCADE,related_name="group_member")

    user_name = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_Group')
    class Meta:
        unique_together = ['user_name', 'group_name']
    
    def __str__(self):
        return f"{str(self.approved)}"

class GroupMessage(models.Model):
    sender = models.ForeignKey(User,on_delete=models.CASCADE,related_name='group_sent')
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    group_name1 = models.ForeignKey(Group,on_delete = models.CASCADE,related_name="group_message")
    group_member = models.ForeignKey(GroupMember,on_delete=models.CASCADE,related_name="group_members",null=True,blank=True)

    def __str__(self):
        return f"{self.group_name1}"



class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='user_profile')
    image = models.ImageField(upload_to="profile_image",null=True,blank=True)
    about = models.TextField()
    phone = PhoneNumberField(blank=True,null=True)
    status = models.BooleanField(default=False)

class AttachmentGroup(models.Model):
    group_name = models.ForeignKey(Group,on_delete=models.CASCADE,related_name='group_name_att',blank=True,null=True)
    group_msg = models.ForeignKey(GroupMessage,on_delete=models.CASCADE,related_name='group_attachments',blank=True,null=True)
    photos = models.ImageField(upload_to="group_image",blank=True,null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    files_i = models.FileField(upload_to="file_videos",blank=True,null=True)

class AttachmentPersonal(models.Model):
    message = models.ForeignKey(Message,on_delete=models.CASCADE,blank=True,null=True,related_name="attachments")
    photos = models.ImageField(upload_to="group_image",blank=True,null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    files_i = models.FileField(upload_to="file_videos",blank=True,null=True)
from django.contrib import admin

from .models import *

@admin.register(GroupMessage)
class MessageAdmin(admin.ModelAdmin):
    list_display = [ 'sender', 'content']

admin.site.register(Group)
admin.site.register(Message)


@admin.register(GroupMember)
class MemberGroup(admin.ModelAdmin):
    list_display = [ 'approved', 'user_name', 'approved_date','group_name']
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from .models import *
from django.db.models import Q
from asgiref.sync import sync_to_async
from django.core.serializers.json import DjangoJSONEncoder

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        print(self.scope,'scops')
        
        #authenticated user id
        self.me = self.scope.get('user_id')
        # self.me['user_id'] =  #sender
        # self.me = await sync_to_async (User.objects.get)(id=self.scope["user_id"])
        # self.me['id'] = self.scope['user_id']
        print('____________________________________')
        print(self.me,'value from self.me')
        print('____________________________________')
        # self.other_userid = self.scope['url_route']['kwargs'].get('user_id') #reciever
        
        # print(f"DEBUG: self.me = {self.me}, id = {self.me.id}")
        # print(f"DEBUG: other_userid from URL = {self.other_userid}")

        #from endpoint path bata aako id
        self.other_userid = self.scope.get('url_route').get('kwargs').get('user_id') #reciever 
        print(self.other_userid,'other user id')

        self.room_name = None
        self.room_group_name = None

        if self.other_userid is None:
            await self.close()
            return

        if not self.me :
            await self.accept()
            await self.send(text_data=json.dumps({"error": "Authentication required"}))
            await self.close()
            return 

        self.room_name = self.get_room_name(self.me, self.other_userid)
        self.room_group_name = f'chat_{str(self.room_name)}'   
        await self.channel_layer.group_add(self.room_group_name,self.channel_name)
        await self.accept()
    
    async def disconnect(self,code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
    

    async def receive(self,text_data):
        print(text_data,'data in text')
        data = json.loads(text_data)
        message = data['message']
        receiver = await sync_to_async(User.objects.get)(id = self.other_userid )
        history = await self.get_chat_history(self.me,self.other_userid)
        
        await sync_to_async(Message.objects.create)(
            sender_id = self.me,
            receiver = receiver,
            content = message,
        )

        await self.channel_layer.group_send(
            self.room_group_name,{
                'type' : 'chat_message',
                'message' : message,
                'userid' : self.me,
            }
        )    

        await self.channel_layer.group_send(
            self.room_group_name,{
                'type' : 'chat_history',
                'history1' : history,
                'userid' : self.me,
            }
        )    
    async def chat_message(self,event):
            await self.send(text_data = json.dumps({
                'message' : event['message'],
                'userid'  : event['userid'],
            }))
    
    async def chat_history(self,event):
            await self.send(text_data = json.dumps({
                'message' : event['history1'],
                'userid'  : event['userid'],
            },cls=DjangoJSONEncoder))
       

    def get_room_name(self, id1, id2):
        return f"{min(int(id1), int(id2))}_{max(int(id1), int(id2))}"
    
    @sync_to_async
    def get_chat_history(self,id1,id2):
        message  = Message.objects.filter(
                Q(sender_id = id1, receiver_id = id2)| 
                Q(sender_id = id2, receiver_id = id1)
            ).order_by('timestamp').values(
                'sender__username', 'content', 'timestamp')
        return list(message)

class GroupConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.me = self.scope.get('user_id')
        self.user = self.scope['user'].username
        self.group_name = self.scope['url_route']['kwargs']['group_name']

        if not self.me:
            await self.accept()
            await self.send(text_data = json.dumps({'error':'not authenticated'}))
            await self.close()
            return 
        self.country = await sync_to_async(Group.objects.get)(group_name=self.group_name)

        if await sync_to_async( lambda: GroupMember.objects.filter(group_name_id=self.country.id, user_name_id=self.me,approved=True).exists()
            )():
            await self.channel_layer.group_add(self.group_name,self.channel_name)
            await self.accept()

        else:
            await sync_to_async(GroupMember.objects.get_or_create)(
            user_name_id = self.me,
            group_name_id = self.country.id,
            )
            await self.accept()
            await self.send(text_data = json.dumps({'error': 'you are not a member wait for admin approval'}))
            await self.close()
            return

    async def disconnect(self,code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self,text_data):
         data = json.loads(text_data)
         print('---------------------------')
         print(data)
         print('---------------------------')
         message = data['message']

         group_obj,created = await sync_to_async(Group.objects.get_or_create)(
            group_name = self.group_name
         )
         
         await sync_to_async(GroupMessage.objects.create)(
            sender_id = self.me,
            content = message,
            group_name1 = group_obj,
         )

         await self.channel_layer.group_send(self.group_name,{  
            'type': 'group_message',
            'message' : message,
            'username' : self.scope['user'].username
         })
         self.country = await sync_to_async(Group.objects.get)(group_name=self.group_name)
         self.c =  await sync_to_async(lambda: GroupMember.objects.filter(group_name_id=self.country.id, user_name_id=self.me))()
        
         await sync_to_async(self.c.update)(approved=True)
    
    async def group_message(self,event):
            await self.send(text_data = json.dumps({
                'message': event['message'],
                'username' : event['username']
            }))
        




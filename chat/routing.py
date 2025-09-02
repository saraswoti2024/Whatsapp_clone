from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path("ws/chat/<int:user_id>/", consumers.ChatConsumer.as_asgi()),
    path("ws/group_chat/<str:group_name>/", consumers.GroupConsumer.as_asgi()),
]
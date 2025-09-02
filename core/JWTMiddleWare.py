from channels.middleware import BaseMiddleware
from rest_framework_simplejwt.tokens import AccessToken
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

User = get_user_model()

class JWTAuthMiddleware(BaseMiddleware):

    async def __call__(self, scope, receive, send):
        token = self.get_token_from_scope(scope)

        if token:
            user, user_id = await self.get_user_and_id_from_token(token)
            if user:
                scope['user'] = user         # ✅ Full user object
                scope['user_id'] = user_id   # ✅ Raw user ID
            else:
                scope['user'] = AnonymousUser()
                scope['user_id'] = None
        else:
            scope['user'] = AnonymousUser()
            scope['user_id'] = None

        return await super().__call__(scope, receive, send)

    def get_token_from_scope(self, scope):
        headers = dict(scope.get("headers", []))
        auth_header = headers.get(b'authorization', b'').decode('utf-8')

        if auth_header.startswith('Bearer '):
            return auth_header.split(' ')[1]
        return None

    @database_sync_to_async
    def get_user_and_id_from_token(self, token):
        try:
            access_token = AccessToken(token)
            user_id = access_token['user_id']
            user = User.objects.get(id=user_id)
            return user, user_id
        except Exception:
            return None, None

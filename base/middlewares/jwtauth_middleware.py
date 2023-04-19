from django.contrib.auth.models import AnonymousUser
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from channels.generic.http import AsyncHttpConsumer

from user.models import User
from base.utils.jwt_decoder import decode_jwt


@database_sync_to_async
def get_user(token):
    try:
        user_id = decode_jwt(token)
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        return AnonymousUser()


def error_response(self, message):
    message = str(message)
    return AsyncHttpConsumer.send_response(self, 401, body=message.encode())


class JWTAuthMiddleware(BaseMiddleware):
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        headers = dict(scope["headers"])
        if b"authorization" in headers:
            try:
                token = headers[b"authorization"]
                scope["user"] = await get_user(token)
            except Exception as e:
                return error_response(e)
        else:
            return error_response("JWT not found")

        return await super().__call__(scope, receive, send)

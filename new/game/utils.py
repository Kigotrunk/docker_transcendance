from urllib.parse import parse_qs
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from django.contrib.auth.models import AnonymousUser
from channels.db import database_sync_to_async
from rest_framework_simplejwt.authentication import JWTAuthentication
from myaccount.models import Account

@database_sync_to_async
def get_user(validated_token):
    try:
        user_id = validated_token.payload['user_id']  # relire la doc pour voir ce que fait validated_token[JWTAuthentication.user_id_field]
        user = Account.objects.get(id=user_id)
        return user
    except (Account.DoesNotExist, KeyError):
        return AnonymousUser()

class JWTAuthMiddleware:
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        query_string = scope['query_string'].decode()
        query_params = parse_qs(query_string)
        token = query_params.get('token', [None])[0]

        if token:
            try:
                UntypedToken(token)
                validated_token = JWTAuthentication().get_validated_token(token)
                user = await get_user(validated_token)
                scope['user'] = user
            except (InvalidToken, TokenError):
                scope['user'] = AnonymousUser()
        else:
            scope['user'] = AnonymousUser()

        return await self.inner(scope, receive, send)

def JWTAuthMiddlewareStack(inner):
    return JWTAuthMiddleware(inner)



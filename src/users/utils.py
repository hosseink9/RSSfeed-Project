import jwt
from config import settings
from django.core.cache import cache
from uuid import uuid4
from rest_framework.views import Response
from datetime import timedelta, datetime


def generate_jti():
    return str(uuid4().hex)

class JwtHelper:

    @staticmethod
    def generate_jwt_token(user_id, secret_key, expires_in_minutes):

        payload = {
            'user_id': user_id,
            'exp': datetime.utcnow() + timedelta(minutes=expires_in_minutes),
            'iat': datetime.utcnow(),
            'jti':generate_jti()
        }
        return jwt.encode(payload, secret_key, algorithm='HS256')

    @staticmethod
    def validate_jwt_token(token, secret_key):
        try:
            payload = jwt.decode(token, secret_key, algorithms=['HS256'])
            return payload.get('user_id')
        except jwt.DecodeError:
            return None



def refresh_token_cache(refresh_token):
    payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=['HS256'])
    user_id = payload.get("user_id")
    jti = payload.get("jti")
    exp_date = payload.get('exp')
    iat = payload.get('iat')
    timeout = exp_date - iat

    cache.set(key=f"user_{user_id} | {jti}", value=f'{iat}', timeout=timeout)


def check_cache(user_id, jti):
    checking_cache = cache.get(f"user_{user_id} | {jti}")
    if checking_cache:
        return checking_cache
    return None


def validate_cache(refresh_token):
    payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=['HS256'])
    user_id = payload.get('user_id')
    jti = payload.get('jti')
    iat = payload.get('iat')
    cached_token = check_cache(user_id, jti)

    if cached_token is None:
        return False

    return cached_token == str(iat)


def check_expired_date(exp_date):
    return datetime.now() < exp_date


# def refresh_token_gen(user_id: int):

#     refresh_token = token_encode({
#         'token_type':'refresh',
#         'user_id':user_id,
#         'exp': datetime.utcnow() + timedelta(days=1),
#         'iat': datetime.utcnow(),
#         'jti':gen_jti()
#     })

#     return refresh_token






# def token_encode(payload):
#     token = jwt.encode(payload=payload, key=settings.SECRET_KEY, algorithm='HS256').decode('utf-8')
#     return token



# def token_decode(token):
#     payload = jwt.decode(jwt=token, key=settings.SECRET_KEY, algorithms=['HS256'])
#     return payload
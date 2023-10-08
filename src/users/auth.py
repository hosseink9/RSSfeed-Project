from django.contrib.auth.backends import BaseBackend
from .models import User

from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
import logging

from .utils import JwtHelper
from config.settings import SECRET_KEY
from .models import User

logger = logging.getLogger('django_API')

class UserAuthBackend(BaseBackend):
    def authenticate(self, request, phone=None, password=None, **kwargs):
        try:
            user = User.objects.get(phone=phone)
            logger.error("User does not exist!!")
        except User.DoesNotExist:
            return None

        if user.check_password(password):
            return user
        logger.error("Password is invalid!!")



    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            logger.error("User does not exist!!")
            return None



class JwtAuthentication(BaseAuthentication):

    def authenticate(self, request):
        auth_header=request.META.get("HTTP_AUTHORIZATION")
        if not auth_header:
            logger.error("Access token is invalid!!")
            raise AuthenticationFailed
        prefix,token=auth_header.split()
        if not prefix=='Bearer': #front set
            logger.error("Prefix is not equal Bearer!!")
            raise AuthenticationFailed
        user_id=JwtHelper.validate_jwt_token(token,SECRET_KEY)
        if not user_id:
            logger.error("User id is not found!!")
            raise AuthenticationFailed
        user=User.objects.get(id=user_id)
        return user,token


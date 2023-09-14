from rest_framework.views import Response, APIView
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import update_last_login
from rest_framework.views import Response
from django.contrib.auth import authenticate

import jwt,datetime

from .models import User
from .serializers import UserSerializer


class RegisterView(APIView):
    def post(self, request):
        user_serializer = UserSerializer(data=request.data)
        user_serializer.is_valid(raise_exception=True)
        user_serializer.save()
        return Response(user_serializer.data, status=status.HTTP_201_CREATED)


class LoginView(APIView):

    def post(self, request):
        phone = request.data['phone']
        password = request.data['password']

        user = User.objects.filter(phone=phone).first()

        if user is None:
            raise AuthenticationFailed('User is not found')

        if not user.check_password(password):
            raise AuthenticationFailed('Password is not correct')

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret',algorithm='HS256')

        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt':token
            }

        update_last_login(None, user)
        return response

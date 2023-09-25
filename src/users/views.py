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


class SendOTPView(APIView):
    def post(self, request):
        serializer=SerializerLogin(data=request.data, context={'request':request})
        if serializer.is_valid(raise_exception=True):
            serializer.create_otp(request, serializer.data['phone'])
            return Response (data={'message':"200"})


class VerifyOTP(APIView):

    def post(self, request):
        serliazer=LoginOTPSerializer(data=request.data, context={'request':request})
        if serliazer.is_valid(raise_exception=True):
            user=User.objects.get(phone=request.session.get('phone'))
            access_token=user.get_access_token()
            refresh_token=user.get_refresh_token()
            return Response(data={'message':"success", "AT":access_token, "RT":refresh_token})


        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt':token
            }

        update_last_login(None, user)
        return response

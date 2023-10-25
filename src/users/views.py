from rest_framework.views import Response, APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework.views import Response
from main.publisher import Publish
from django.utils.translation import gettext as _

# import logging
import jwt,datetime

from .models import User
from .serializers import UserSerializer, SerializerLogin, LoginOTPSerializer, ChangePasswordSerializer
from .auth import JwtAuthentication
from .utils import refresh_token_cache, validate_cache, JwtHelper
from config import settings

# logger = logging.getLogger('django_API')


class RegisterView(APIView):
    def post(self, request):
        user_serializer = UserSerializer(data=request.data)
        user_serializer.is_valid(raise_exception=True)
        user_serializer.save()
        request_META = request.META.get('HTTP_USER_AGENT')
        username = request.data.get('username')
        Publish().register(username=username, request_META=request_META)
        return Response(_('User is created successfully'), status=status.HTTP_201_CREATED)


class SendOTPView(APIView):
    def post(self, request):
        serializer=SerializerLogin(data=request.data, context={'request':request})
        serializer.is_valid(raise_exception=True)
        serializer.create_otp(request, serializer.data['phone'])
        return Response(_("OTP was sent"),status=status.HTTP_201_CREATED)


class VerifyOTP(APIView):

    def post(self, request):
        serializer=LoginOTPSerializer(data=request.data, context={'request':request})
        serializer.is_valid(raise_exception=True)
        user=User.objects.get(phone=request.session.get('phone'))
        access_token=user.get_access_token()
        refresh_token=user.get_refresh_token()
        refresh_token_cache(refresh_token)

        data = {"AT":access_token, "RT":refresh_token}

        request_META = request.META.get('HTTP_USER_AGENT')
        username = user.username
        Publish().login(username=username, request_META=request_META)
        return Response(data=(_("login is success"), data))


class RefreshTokenView(APIView):

    def post(self, request):

        refresh_token = request.data.get('refresh_token')
        try:
            payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=['HS256'])
        except:
            jwt.ExpiredSignatureError


        if not validate_cache(refresh_token):
            return Response(data= _("invalid refresh token"), status=status.HTTP_401_UNAUTHORIZED)
        user_id = payload.get('user_id')

        try:
            user = User.objects.get(id=user_id)
        except:
            User.DoesNotExist

        access_token=user.get_access_token()
        refresh_token=user.get_refresh_token()

        refresh_token_cache(refresh_token)

        data = {
            "access": access_token,
            "refresh": refresh_token,
        }
        return Response(data, status=status.HTTP_201_CREATED)


class LoginRequiredView(APIView):
    authentication_classes = [JwtAuthentication]
    permission_classes=[IsAuthenticated]

    def get(self, request):
        return Response({'message':_("success"),"phone":request.user.phone})


class LogoutAPIView(APIView):

    def post(self, request):
        response = Response()
        response.delete_cookie(key="AT")
        response.data =  _("success")
        return response

class ChangePasswordView(APIView):

    authentication_classes = [JwtAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def patch(self,request,pk):
        user = User.objects.get(pk=pk)
        serializer = self.serializer_class(data=request.data,instance=user,context={'request':request})
        serializer.is_valid(raise_exception=True)
        serializer.update()
        return Response(_('Change password is success!'))
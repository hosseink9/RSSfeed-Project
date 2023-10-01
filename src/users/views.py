from rest_framework.views import Response, APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework.views import Response

import jwt,datetime

from .models import User
from .serializers import UserSerializer, SerializerLogin, LoginOTPSerializer, ChangePasswordSerializer
from .auth import JwtAuthentication
from .utils import refresh_token_cache, validate_cache, JwtHelper
from config import settings



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
            refresh_token_cache(refresh_token)
            return Response(data={'message':"success", "AT":access_token, "RT":refresh_token})


class RefreshTokenView(APIView):

    def post(self, request):

        refresh_token = request.data.get('refresh_token')
        try:
            payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=['HS256'])
        except: jwt.ExpiredSignatureError


        if not validate_cache(refresh_token):
            return Response(data={"message": "invalid refresh token"}, status=status.HTTP_401_UNAUTHORIZED)

        user_id = payload.get('user_id')

        try:
            user = User.objects.get(id=user_id)
        except: User.DoesNotExist

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
        print(request.user.id)
        return Response({'message':"success","phone":request.user.phone})


class LogoutAPIView(APIView):

    def post(self, request):
        response = Response()
        response.delete_cookie(key="AT")
        response.data = {"message": "success"}
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
        return Response({'message':'OK'})
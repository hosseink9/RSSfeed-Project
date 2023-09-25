from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import gettext_lazy as _
import random
from datetime import timedelta
from django.utils import timezone

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','phone','password']


    def create(self, validate_data):
        password = validate_data.pop("password",None)
        instance = self.Meta.model(**validate_data)
        if password is not None:
            instance.set_password(password)
        else:
            raise ("You don't add password" )
        instance.save()
        return instance


class SerializerLogin(serializers.Serializer):

    phone = serializers.CharField(required=True, allow_null=False)


    def validate(self, data):
        phone = data.get('phone')

        if not User.objects.filter(phone=phone).exists():
            raise serializers.ValidationError



        return data

    @staticmethod
    def create_otp(request, phone):
        request.session["otp"] = random.randint(1000, 9999)
        request.session["otp_expire"] = (timezone.now() + timedelta(minutes=10)).strftime("%d/%m/%Y, %H:%M:%S")
        request.session['phone']=phone
        print(f"generated:{request.session['otp']}  until:{request.session['otp_expire']}")



class LoginOTPSerializer(serializers.Serializer):
    otp=serializers.IntegerField(required=True, allow_null=False)

    def validate(self, data):
        otp=data.get('otp')
        request=self.context.get('request')
        if not otp==request.session.get('otp'):
            raise serializers.ValidationError
        if not User.objects.filter(phone=request.session.get('phone')).exists():
            raise serializers.ValidationError

        return data



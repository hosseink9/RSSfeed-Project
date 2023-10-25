from rest_framework import serializers
from .models import User
from django.contrib.auth.password_validation import validate_password
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
    password = serializers.CharField(required=True,  allow_null=False)

    def validate(self, data):
        phone = data.get('phone')
        password = data.get('password')

        if not User.objects.filter(phone=phone).exists():
            raise serializers.ValidationError

        user = User.objects.get(phone=phone)
        if not user.check_password(password):
            raise serializers.ValidationError('Invalid Password')

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


class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField()
    password2 = serializers.CharField()
    old_password = serializers.CharField()

    class Meta:
        model = User
        fields = ['password','password2','old_password']


    def validate(self, data):
        user = self.context['request'].user
        if not data['password'] == data['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        elif data['password'] == data['old_password']:
            raise serializers.ValidationError({"password": "New password likes old password!"})

        if not user.check_password(data['old_password']):
            raise serializers.ValidationError({"old_password": "Old password is not correct"})
        return data


    def update(self):
        instance = self.context['request'].user
        instance.set_password(self.validated_data['password'])
        instance.save()

        return instance
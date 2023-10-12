from django.db import models

import re
import os

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.exceptions import ValidationError

from main.models import BaseModel
from .utils import JwtHelper
from config import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

PHONE_REGEX_PATTERN = r"(((\+|00)(98))|0)?(?P<operator>9\d{2})-?(?P<middle3>\d{3})-?(?P<last4>\d{4})"

def phone_validator(phone:str):
    if not (matched := re.fullmatch(PHONE_REGEX_PATTERN, phone.strip())):
        raise ValidationError("Invalid phone number")
    return matched


class UserManager(BaseUserManager):

    def create_user(self, phone, password, **other_fields):
        if phone is None:
            raise ValueError("Phone not given")

        user = self.model(phone=phone, **other_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(phone, password, **other_fields)


class PhoneNumberField(models.CharField):
    def get_prep_value(self, value):
        if value is None:
            return value

        try:
            regex = phone_validator(value)
        except ValidationError:
            raise

        phone_parts = regex.groupdict()
        phone = phone_parts["operator"]+phone_parts["middle3"]+phone_parts["last4"]
        return phone



class User(AbstractBaseUser,PermissionsMixin, BaseModel):
    phone = PhoneNumberField(validators=[phone_validator], unique=True, max_length=20)

    username = models.CharField(max_length=50,unique=True,null=True,blank=True)
    email = models.EmailField(unique=True,null=True,blank=True)
    first_name = models.CharField(max_length=50,null=True,blank=True)
    last_name = models.CharField(max_length=50,null=True,blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    def get_access_token(self):
        return JwtHelper.generate_jwt_token(self.id,settings.SECRET_KEY,60)

    def get_refresh_token(self):
        return JwtHelper.generate_jwt_token(self.id,settings.SECRET_KEY,480)

    def __str__(self):
        return f"{self.phone}"


class NotificationInfo(BaseModel):
        message = models.TextField()

        def __str__(self):
            return f'{self.message}'

class Notification(BaseModel):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    message = models.ForeignKey(NotificationInfo, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user} || {self.message} || {self.created_at}'
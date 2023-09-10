from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser, BaseUserManager
# Create your models here.



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
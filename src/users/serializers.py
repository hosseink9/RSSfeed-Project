from rest_framework import serializers

from .models import User

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
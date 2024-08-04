from rest_framework import serializers
from book.models import *

class Userserializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','username','email','password']
        extra_kwargs={
            'password':{'write_only':True}
        }

    def create(self, validated_data):
        password=validated_data.pop('password')
        user=User(**validated_data)
        user.set_password(password)
        user.save()
        return user
        
class Bookserializer(serializers.ModelSerializer):
    class Meta:
        model=Book
        fields='__all__'
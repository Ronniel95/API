from django.contrib.auth.models import User, Group
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from models import Check


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')

class CheckSerializer(serializers.ModelSerializer):

    #image = serializers.ImageField(max_length=None,use_url=True)

    def create(self, validated_data):

        validated_data['name'] = 'static_name'

        return Check.objects.create(**validated_data)

    class Meta:
        model = Check
        fields = ('name', 'date_created', 'image')



    #def create(self, validated_data):
        #validated_data['name'] = 'static_name'
        #return validated_data



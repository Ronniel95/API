from django.contrib.auth.models import User
from django.utils.deconstruct import deconstructible
from dropbox import Dropbox
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, datetime

from API.settings import MEDIA_URL
from BillSays.models import Check, Friend


class CheckSerializer(serializers.ModelSerializer):

    image = serializers.ImageField(max_length=None,use_url=False)

    class Meta:
        model = Check
        fields = ('name', 'date_created', 'image')

class FriendSerializer(serializers.ModelSerializer):


    class Meta:
        model = Friend

    def create(self, validated_data):

        validated_data['date_changed'] = datetime.datetime.now()

        return super(FriendSerializer, self).create(validated_data)








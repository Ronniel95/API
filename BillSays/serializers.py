from django.contrib.auth.models import User
from django.utils.deconstruct import deconstructible
from dropbox import Dropbox
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, datetime

from API.settings import MEDIA_URL
from BillSays.models import Check, Friend




class FriendSerializer(serializers.ModelSerializer):

    class Meta:
        model = Friend



class CheckSerializer(serializers.ModelSerializer):

    image_url = serializers.ImageField(max_length=None,use_url=True)


    class Meta:
        model = Check
        fields = ('fk_user', 'date_created', 'image_url')





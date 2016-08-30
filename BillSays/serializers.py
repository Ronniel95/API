from django.contrib.auth.models import User
from django.utils.deconstruct import deconstructible
from dropbox import Dropbox
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

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

    def is_valid(self, raise_exception=False):

        if User.objects.filter(id=self.initial_data['fk_user_friend']).count() != 1:
            return raise_exception




        return super(FriendSerializer, self).is_valid(raise_exception)





from django.utils.deconstruct import deconstructible
from dropbox import Dropbox
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from API.settings import MEDIA_URL
from BillSays.models import Check


class CheckSerializer(serializers.ModelSerializer):

    image = serializers.ImageField(max_length=None,use_url=False)

    class Meta:
        model = Check
        fields = ('name', 'date_created', 'image')

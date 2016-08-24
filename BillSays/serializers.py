from django.utils.deconstruct import deconstructible
from dropbox import Dropbox
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from BillSays.models import Person


class PersonSerializer(ModelSerializer):

    image_url = serializers.ImageField(max_length=None, use_url=True)
    class Meta:
        model = Person
        fields = ('photo','image_url')


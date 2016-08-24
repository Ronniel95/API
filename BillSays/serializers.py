from django.utils.deconstruct import deconstructible
from dropbox import Dropbox
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from BillSays.models import Check


class CheckSerializer(serializers.ModelSerializer):

    image = serializers.ImageField(max_length=None,use_url=True)

    def create(self, validated_data):

        validated_data['name'] = 'static_name'

        return Check.objects.create(**validated_data)

    class Meta:
        model = Check
        fields = ('name', 'date_created', 'image')

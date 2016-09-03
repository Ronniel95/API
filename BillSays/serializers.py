from django.contrib.auth import get_user, get_user_model
from django.contrib.auth.models import User
from rest_auth.serializers import UserDetailsSerializer, LoginSerializer
from rest_framework import serializers

from BillSays.models import Check, Friend, CheckElement, Mention, UserCheckElement


class FriendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friend


class CheckSerializer(serializers.ModelSerializer):
    image_url = serializers.ImageField(max_length=None, use_url=True)

    class Meta:
        model = Check
        fields = ('fk_user', 'date_created', 'image_url', 'fk_waitress', 'total_cost')


class CheckElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckElement
        fields = ('id', 'name', 'cost', 'quantity')


class MentionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mention


class RecognizedCheckSerializer(serializers.ModelSerializer):
    fk_check = CheckElementSerializer(many=True, read_only=True)

    class Meta:
        model = Check
        fields = ('fk_user', 'date_created', 'image_url', 'fk_waitress', 'total_cost', 'fk_check')


class UserCheckElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCheckElement


class UserSerializerPublic(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class UserSerializer(UserDetailsSerializer):
    id = serializers.IntegerField(source='User.id')

    class Meta(UserDetailsSerializer.Meta):
        fields = UserDetailsSerializer.Meta.fields + ('id',)

class UserSerializer1(LoginSerializer):
    id = serializers.IntegerField(source='User.id')

    class Meta(LoginSerializer.Meta):
        fields = LoginSerializer.Meta.fields + ('id',)


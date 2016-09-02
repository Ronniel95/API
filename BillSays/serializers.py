from rest_framework import serializers

from BillSays.models import Check, Friend, CheckElement, Mention


class FriendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friend


class CheckSerializer(serializers.ModelSerializer):
    image_url = serializers.ImageField(max_length=None, use_url=True)

    class Meta:
        model = Check
        fields = ('fk_user', 'date_created', 'image_url','fk_waitress','total_cost')


class CheckElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckElement
        fields = ('name','cost','quantity')

class MentionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mention


class RecognizedCheckSerializer(serializers.ModelSerializer):
    dishes = CheckElementSerializer(many=True, read_only=True)

    class Meta:
        model = Check
        fields = ('id_waitress', 'dishes')

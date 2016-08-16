from rest_framework.serializers import ModelSerializer
from BillSays.models import Achievement, Checkelement, Checks, Debtelement, Dictachievement, DjangoMigrations, Friend, Usercheckelement, Users


class AchievementSerializer(ModelSerializer):

    class Meta:
        model = Achievement


class CheckelementSerializer(ModelSerializer):

    class Meta:
        model = Checkelement


class ChecksSerializer(ModelSerializer):

    class Meta:
        model = Checks


class DebtelementSerializer(ModelSerializer):

    class Meta:
        model = Debtelement


class DictachievementSerializer(ModelSerializer):

    class Meta:
        model = Dictachievement


class DjangoMigrationsSerializer(ModelSerializer):

    class Meta:
        model = DjangoMigrations


class FriendSerializer(ModelSerializer):

    class Meta:
        model = Friend


class UsercheckelementSerializer(ModelSerializer):

    class Meta:
        model = Usercheckelement


class UsersSerializer(ModelSerializer):

    class Meta:
        model = Users
        fields = ('id_user','name','facebook_id','date_registration','password_user')

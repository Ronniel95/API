# Create your models here.
from __future__ import unicode_literals
from django.db import models

# Create your models here.
from django.contrib.auth.models import User, Group
from django.db.models import Model

class Achievement(models.Model):
    user_id_user = models.ForeignKey('Users', models.DO_NOTHING, db_column='user_id_user', blank=True, null=True)
    dict_achievement_id_dict_achievement = models.ForeignKey('Dictachievement', models.DO_NOTHING, db_column='dict_achievement_id_dict_achievement', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'achievement'


class Checkelement(models.Model):
    id_check_element = models.IntegerField(primary_key=True)
    user_id_user = models.ForeignKey('Users', models.DO_NOTHING, db_column='user_id_user', blank=True, null=True)
    checks_id_check = models.ForeignKey('Checks', models.DO_NOTHING, db_column='checks_id_check', blank=True, null=True)
    element_name = models.CharField(max_length=255, blank=True, null=True)
    element_cost = models.FloatField(blank=True, null=True)
    amount = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'checkelement'


class Checks(models.Model):
    id_check = models.IntegerField(primary_key=True)
    date_created = models.DateField(blank=True, null=True)
    total_cost = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'checks'


class Debtelement(models.Model):
    id_dept_element = models.IntegerField(primary_key=True)
    user_id_user = models.ForeignKey('Users', models.DO_NOTHING, db_column='user_id_user', blank=True, null=True)
    friend_id_friend = models.ForeignKey('Friend', models.DO_NOTHING, db_column='friend_id_friend', blank=True, null=True)
    value_dept = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'debtelement'


class Dictachievement(models.Model):
    id_dict_achievement = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    condition = models.CharField(max_length=255, blank=True, null=True)
    target_value = models.IntegerField(blank=True, null=True)
    image_path = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dictachievement'


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class Friend(models.Model):
    id_friend = models.IntegerField(primary_key=True)
    user_id_user = models.ForeignKey('Users', models.DO_NOTHING, db_column='user_id_user', blank=True, null=True)
    rating = models.FloatField(blank=True, null=True)
    is_registred = models.NullBooleanField()

    class Meta:
        managed = False
        db_table = 'friend'
#

class Usercheckelement(models.Model):
    id_user_check_element = models.IntegerField(primary_key=True)
    checkelement_id_checkelement = models.ForeignKey(Checkelement, models.DO_NOTHING, db_column='checkelement_id_checkelement', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'usercheckelement'


class Users(models.Model):
    id_user = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    facebook_id = models.CharField(max_length=255, blank=True, null=True)
    date_registration = models.DateField(blank=True, null=True)
    password_user = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'

# Create your models here.
from __future__ import unicode_literals
from django.db import models

# Create your models here.
from django.contrib.auth.models import User, Group
from django.db.models import Model, TextField
from django.db.models.fields.related import ForeignKey
from rest_framework import viewsets
from rest_framework.fields import FileField
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer


class Check(models.Model):
    name = models.CharField(max_length=255)
    date_created = models.DateField()
    image = models.ImageField(null=True, max_length=255)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        return
        #dd
        #super(Check, self).save(force_insert, force_update, using, update_fields)



    def __str__(self):
        return "%s"%self.name


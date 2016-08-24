# Create your models here.
from __future__ import unicode_literals

import os

from django.db import models

# Create your models here.
from django.contrib.auth.models import User, Group
from django.db.models import Model


class Check(models.Model):
    name = models.CharField(max_length=255)
    date_created = models.DateField()
    image = models.ImageField(null=True, max_length=255)
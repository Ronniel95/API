# Create your models here.
from __future__ import unicode_literals

import os
import random

from django.db import models

# Create your models here.
from django.contrib.auth.models import User, Group
from django.db.models import Model, settings


class Friend(models.Model):
    """

    Representation of Friend table

    fk_user - int
    id - int


    """
    # reference to User
    fk_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # primary key for model Friend, and Foreign key for model Check
    id = models.OneToOneField(Check, primary_key=True)

    #


class Check(models.Model):
    """
    Representation of Check

    """
    # reference to User
    fk_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # reference to Waitress
    fk_waitress = models.ForeignKey(Waitress, on_delete=models.CASCADE, null=True)

    # date of check creation
    date_created = models.DateTimeField(null=True)

    # check URL( check stores as image on 3-d party cloud server)
    image_url = models.ImageField(null=True, max_length=255)

    # total receipt cost
    total_cost = models.DecimalField()


class Waitress(models.Model):
    """

    Representation of Waitress

    """

    # waitress identificator on receipt
    name = models.CharField(max_length=255)






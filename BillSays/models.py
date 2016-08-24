# Create your models here.
from __future__ import unicode_literals
from django.db import models

# Create your models here.
from django.contrib.auth.models import User, Group
from django.db.models import Model
from django_dropbox.storage import DropboxStorage

STORAGE = DropboxStorage()

class Person(models.Model):
     photo = models.ImageField(upload_to='photos', storage=STORAGE, null=True, blank=True)
     resume = models.FileField(upload_to='resumes', storage=STORAGE, null=True, blank=True)

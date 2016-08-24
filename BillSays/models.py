# Create your models here.
from __future__ import unicode_literals

import os

from django.db import models

# Create your models here.
from django.contrib.auth.models import User, Group
from django.db.models import Model
from django_dropbox.storage import DropboxStorage



STORAGE = DropboxStorage()

class Person(models.Model):
     photo =  models.ImageField(null=True, max_length=255)

     def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
         model = TestDropbox()
         model.file_test.save(self.file_name, ContentFile(self.file_content))

         return

     def __str__(self):
         return os.path.basename(self.file_test.name)

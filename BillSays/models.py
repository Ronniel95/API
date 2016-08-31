# Create your models here.
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from django.contrib.auth.models import User, Group
from django.db.models import Model


# level 1

class Friend(models.Model):
    """

    Representation of 'friend' table that contains references to user friends

    """
    # reference to User which is owner of friend
    fk_user_owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='fk_user_owner',null=True)

    # reference to User which presented as friend
    fk_user_friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name='fk_user_friend',null=True)

    # friend rating in list
    rating = models.IntegerField(null=True)

    # friend relation status
    status = models.CharField(max_length=1)
    # date changed
    date_changed = models.DateField(null=True,auto_now=True)

class Owner(models.Model):
    """

    Representation of 'owner' table that representing restaurant owners

    """
    # owner name
    name = models.CharField(max_length=255)

    # owner email
    email = models.CharField(max_length=255)

    #owner password
    password = models.CharField(max_length=255)

class Food(models.Model):
    food_type = models.CharField(max_length=255)

class DictAchievement(models.Model):
    name = models.CharField(max_length=255)

    condition = models.CharField(max_length=255)

    target_value = models.IntegerField()

    image_path = models.ImageField()

# level 2

class DebtElement(models.Model):

    fk_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='fk_user_debt_owner', null=True)

    fk_friend = models.ForeignKey(Friend, on_delete=models.CASCADE, related_name='fk_user_debt_friend', null=True)

    value_debt = models.DecimalField(max_digits=5,decimal_places=4)

class Achievement(models.Model):
    fk_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    fk_dict_achievement = models.ForeignKey(DictAchievement, on_delete=models.CASCADE,
                                            related_name='fk_dict_achievement', null=True)

    user_value = models.DecimalField(max_digits=5,decimal_places=4)

    date_achieved = models.DateField(auto_now_add=True)

class Location(models.Model):
    fk_owner = models.ForeignKey(Owner, related_name='fk_owner')
    id_check = models.CharField(max_length=255)
    name = models.CharField(max_length=255)

# level 3

class Waitress(models.Model):
    """

    Representation of 'waitriess' table

    """
    # waitress identificator on receipt
    name = models.CharField(max_length=255)



# level 4

class Check(models.Model):
    """
    Representation of 'check' table that contains processed check meta data

    """
    # reference to User
    fk_user = models.ForeignKey(User)

    # reference to Waitress
    fk_waitress = models.ForeignKey(Waitress, on_delete=models.CASCADE, null=True)

    # date of check creation
    date_created = models.DateTimeField(null=True)

    # check URL( check stores as image on 3-d party cloud server)
    image_url = models.ImageField(null=True, max_length=255)

    # total receipt cost
    total_cost = models.DecimalField(max_digits=10,decimal_places=4)


# level 5

class CheckElement(models.Model):
    fk_check = models.ForeignKey(Check, on_delete=models.CASCADE, related_name='fk_check', null=True)


class Mention(models.Model):
    id = models.OneToOneField(Check,on_delete=models.CASCADE, primary_key=True)

    comment = models.CharField(max_length=500)

    waitress_rate = models.IntegerField()

    food_rate = models.IntegerField()

    atmosphere_rate = models.IntegerField()


class UserCheckElement(models.Model):
    fk_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='fk_user', null=True)

    fk_check_element = models.ForeignKey(CheckElement,related_name='fk_user')

    cost = models.DecimalField(decimal_places=4,max_digits=5)

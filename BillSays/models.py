# Create your models here.
from __future__ import unicode_literals

from allauth.account.utils import perform_login
from allauth.socialaccount.signals import pre_social_login
from django.db import models

# Create your models here.
from django.contrib.auth.models import User, Group
from django.db.models import Model, settings
from django.db.models.signals import pre_save
from django.dispatch import receiver


class Friend(models.Model):
    """

    Representation of 'friend' table that contains references to user friends

    """
    # reference to User which is owner of friend
    fk_user_owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='fk_user_owner', null=True)

    # reference to User which presented as friend
    fk_user_friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name='fk_user_friend', null=True)

    # friend rating in list
    rating = models.IntegerField(null=True)

    # friend relation status
    status = models.CharField(max_length=1)
    # date changed
    date_changed = models.DateField(null=True, auto_now=True)


class Owner(models.Model):
    """

    Representation of 'owner' table that representing restaurant owners

    """
    # owner name
    name = models.CharField(max_length=255)

    # owner email
    email = models.CharField(max_length=255)

    # owner password
    password = models.CharField(max_length=255)


class Food(models.Model):
    # type of food in checks
    food_type = models.CharField(max_length=255)


class DictAchievement(models.Model):
    # achievement name
    name = models.CharField(max_length=255)
    # text representation of condition
    condition = models.CharField(max_length=255)

    # value for get achievement
    target_value = models.IntegerField()

    # image path to achievement icon
    image_path = models.ImageField()


class DebtElement(models.Model):
    fk_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='fk_user_debt_owner', null=True)

    fk_friend = models.ForeignKey(Friend, on_delete=models.CASCADE, related_name='fk_user_debt_friend', null=True)

    value_debt = models.DecimalField(max_digits=5, decimal_places=4)


class Achievement(models.Model):
    fk_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    fk_dict_achievement = models.ForeignKey(DictAchievement, on_delete=models.CASCADE,
                                            related_name='fk_dict_achievement', null=True)

    user_value = models.DecimalField(max_digits=5, decimal_places=4)

    date_achieved = models.DateField(auto_now_add=True)


class Location(models.Model):
    fk_owner = models.ForeignKey(Owner, related_name='fk_owner', null=True)
    # id_check = models.CharField(max_length=255)
    name = models.CharField(max_length=255)


# level 3

class Waitress(models.Model):
    """

    Representation of 'waitriess' table

    """

    fk_location = models.ForeignKey(Location, related_name='fk_location')
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
    total_cost = models.DecimalField(max_digits=10, decimal_places=4, null=True)


# level 5

class CheckElement(models.Model):
    fk_check = models.ForeignKey(Check, on_delete=models.CASCADE, related_name='fk_check', null=True)

    name = models.CharField(max_length=255)

    cost = models.DecimalField(max_digits=10, decimal_places=4)

    quantity = models.IntegerField()


class Mention(models.Model):
    id = models.OneToOneField(Check, on_delete=models.CASCADE, primary_key=True)

    comment = models.CharField(max_length=500, null=True)

    waitress_rate = models.IntegerField()

    food_rate = models.IntegerField()

    atmosphere_rate = models.IntegerField()


class UserCheckElement(models.Model):
    fk_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='fk_user', null=True)

    fk_check_element = models.ForeignKey(CheckElement, related_name='fk_user')

    cost = models.DecimalField(decimal_places=4, max_digits=7)


@receiver(pre_save, sender=User)
def update_username_from_email(sender, instance, **kwargs):
    instance.username = instance.email



@receiver(pre_social_login)
def link_to_local_user(sender, request, sociallogin, **kwargs):
    email_address = sociallogin.account.extra_data['email']
    users = User.objects.filter(email=email_address)
    if users:
        perform_login(request, users[0], email_verification=settings.EMAIL_VERIFICATION)
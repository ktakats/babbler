# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.

class Room(models.Model):

    title=models.CharField(max_length=200)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('room', args=[self.title])

class MyUserManager(BaseUserManager):

    def create_user(self, email, password, first_name):
        """"
        Creates and saves a User with the given email, first name and password
        """
        if not email:
            raise ValueError('Users must have and email address')

        user=self.model(email=self.normalize_email(email), first_name=first_name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, first_name):

        user=self.create_user(email, password=password, first_name=first_name)
        user.is_admin=True
        user.save(using=self._db)
        return user


@python_2_unicode_compatible
class User(AbstractBaseUser):
    email=models.EmailField(verbose_name='email address', max_length=255, unique=True,)
    first_name=models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    is_admin=models.BooleanField(default=False)

    USERNAME_FIELD='email'
    REQUIRED_FIELDS = ['first_name']

    objects=MyUserManager()

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return self.first_name

    def get_short_name(self):
        return self.first_name

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_superuser(self):
        return self.is_admin

    @property
    def is_staff(self):
        return self.is_admin


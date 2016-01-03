# -*- coding: utf-8 -*-
from django.core.exceptions import ValidationError
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core import validators
from django.db.models import Max
from django.contrib.auth.models  import User as AuthUser, BaseUserManager
from sdf.base_settings import *
from datetime import datetime
import glob

from app_payment.models import SellerRating


def user_directory_path(instance, filename):
    if instance.id is None:
        id_max = MyUserManager.objects.all().aggregate(Max('id'))['id__max']
        id_next = id_max + 1 if id_max else 1
        instance.id = id_next
    ext = filename.split('.')[-1]
    upload_dir_path = 'images/profiles/profile_{0}.{1}'.format(instance.id, ext)
    profile_images = glob.glob(os.path.join(MEDIA_ROOT, 'images/profiles/profile_{0}.*'.format(instance.id)))
    for image in profile_images:
        os.remove(image)
    return upload_dir_path

class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None, username=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.username = username
        user.save(using=self._db)
        return user

    def create_superuser(self, email, date_of_birth, password):
        user = self.create_user(email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AuthUser):
    # auth_user fields: username, first_name, last_name, email, password, is_staff, is_active, is_super
    AuthUser._meta.get_field('username')._blank = True
    AuthUser._meta.get_field('username')._null = True
    AuthUser._meta.get_field('username').blank = True
    AuthUser._meta.get_field('username').null = True

    AuthUser._meta.get_field('username').error_messages = {'unique': 'Das gewählte Pseudonym ist bereits vergeben.',
                                                        'invalid': 'Bitte ein gültiges Pseudonym eingeben. Dieses darf nur Buchstaben, Ziffern und @/./+/-/_ enthalten.',
                                                        'name_collision': 'Das Pseudonym entspricht einem bereits registrierten Klarnamen.'}
    AuthUser._meta.get_field('username').verbose_name = "Pseudonym (optional)"

    AuthUser._meta.get_field('email')._unique = True
    AuthUser._meta.get_field('email').error_messages = {'unique': 'Diese E-Mail-Adresse ist bereits registriert.',
                                                        'invalid': 'Bitte eine gültige E-Mail-Adresse angeben.'}

    emailConfirm = models.BooleanField(default=False,verbose_name='E-mail bestätigt')
    profileImage = models.ImageField(upload_to=user_directory_path, null=True)
    location = models.CharField(('Ort'),max_length=255, default='')
    paypal = models.CharField(max_length=50)
    user_ptr = models.OneToOneField(AuthUser)
    showcaseDisabled = models.BooleanField(default=False, verbose_name='Schaufenster gesperrt')

    objects = MyUserManager()
    AuthUser.USERNAME_FIELD = 'email'
    AuthUser.REQUIRED_FIELDS = ['']

    def __str__(self):
        return str(self.user_ptr) + ", " + self.paypal + ", " + self.location

    def has_profile_image(self):
        return bool(self.profileImage)

    def pseudonym_or_full_name(self):
        if self.username and self.username != "":
            return self.username
        else:
            return self.full_name()

    def full_name(self):
        return ' '.join([self.first_name, self.last_name])

    def rating(self):
        return SellerRating.calculate_stars_for_user(self.id)

    def image_url_or_blank(self):
        if self.has_profile_image():
            return MEDIA_URL + str(self.profileImage)
        return STATIC_URL + "img/blank-user-profile.png"

    def image_url_or_blank_for_showcase(self):
        if self.has_profile_image():
            return MEDIA_URL + str(self.profileImage)
        return STATIC_URL + "img/blank-showcase.png"

class ConfirmEmail(models.Model):
    uuid = models.CharField(max_length=50)
    user = models.OneToOneField(User)

class PasswordReset(models.Model):
    uuid = models.CharField(max_length=50)
    user = models.OneToOneField(User)

class ChangeUserData(models.Model):
    user = models.OneToOneField(User)
    username = models.CharField(('Username'), max_length=30, unique=True,
         error_messages={'unique': 'Das gewählte Pseudonym ist bereits vergeben.',
            'invalid': 'Bitte ein gültiges Pseudonym eingeben. Dieses darf nur Buchstaben, Ziffern und @/./+/-/_ enthalten.',
            'name_collision': 'Das Pseudonym entspricht einem bereits registrierten Klarnamen.'})
    first_name = models.CharField(('Vorname'), max_length=30, blank=True)
    last_name = models.CharField(('Nachname'), max_length=30, blank=True)
    email = models.EmailField(('E-Mailadresse'), blank=True)
    location = models.CharField(('Ort'),max_length=255, blank=True)



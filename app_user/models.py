# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models  import User as AuthUser, BaseUserManager

def user_directory_path(instance, filename):
    ext = filename.split('.')[-1]
    return 'images/profiles/profile_{0}.{1}'.format(instance.id, ext)

class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
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
    AuthUser._meta.get_field('email')._unique = True
    AuthUser._meta.get_field('username')._blank = True
    AuthUser._meta.get_field('username')._null = True
    AuthUser._meta.get_field('username').blank = True
    AuthUser._meta.get_field('username').null = True

    #TODO generalize renaming for internationalization
    AuthUser._meta.get_field('username').verbose_name = "Pseudonym (optional)"
    AuthUser._meta.get_field('email').error_messages = {'unique': 'Diese E-Mail-Adresse ist bereits registriert.',
                                                        'invalid': 'Bitte eine gültige E-Mail-Adresse angeben.'}

    emailConfirm = models.BooleanField(default=False,verbose_name='E-mail bestätigt')
    profileImage = models.FileField(upload_to=user_directory_path, null=True)
    location = models.CharField(max_length=255, default='')
    paypal = models.CharField(max_length=50)
    user_ptr = models.OneToOneField(AuthUser)
    showcaseDisabled = models.BooleanField(default=False, verbose_name='Schaufenster gesperrt')

    objects = MyUserManager()
    AuthUser.USERNAME_FIELD = 'email'
    AuthUser.REQUIRED_FIELDS = ['']

    def __str__(self):
        return str(self.user_ptr) + ", " + self.paypal + ", " + self.location

    def pseudonym_or_full_name(self):
        if self.username and self.username != "":
            return self.username
        else:
            return self.full_name()

    def full_name(self):
        return ' '.join([self.first_name, self.last_name])

class ConfirmEmail(models.Model):
    uuid = models.CharField(max_length=50)
    user = models.OneToOneField(User)

class PasswordReset(models.Model):
    uuid = models.CharField(max_length=50)
    user = models.OneToOneField(User)

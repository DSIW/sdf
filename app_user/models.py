from django.db import models
from django.contrib.auth.models  import User as AuthUser


class User(AuthUser):
    # auth_user fields: username, first_name, last_name, email, password, is_staff, is_active, is_super

    emailConfirm = models.BooleanField(default=False)
    location = models.CharField(max_length=255, default='')
    paypal = models.CharField(max_length=50)
    user_ptr = models.OneToOneField(AuthUser)

    def __str__(self):
        return self.user_ptr + ", " + self.paypal + ", " + self.location

    def pseudonym_or_full_name(self):
        if self.username != "":
            return self.username
        else:
            return self.full_name()

    def full_name(self):
        return ' '.join([self.first_name, self.last_name])


class ConfirmEmail(models.Model):
    uuid = models.CharField(max_length=50)
    user = models.OneToOneField(User)

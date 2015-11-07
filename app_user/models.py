
from django.db import models
from django.contrib.auth.models  import User as AuthUser

class User(AuthUser):
    location = models.CharField(max_length=255)
    user_ptr = models.OneToOneField(AuthUser)
    paypal = models.CharField(max_length=50)
    emailConfirm = models.BooleanField(default=False);

    def __str__(self):
        return self.location + ", " + self.user_ptr + ", " + self.paypal

    def full_name(self):
        if self.first_name != "" and self.last_name != "":
            return "%s %s" % (self.first_name, self.last_name)
        else:
            return self.username

class ConfirmEmail(models.Model):
    uuid = models.CharField(max_length=50)
    user = models.OneToOneField(User)

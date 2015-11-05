
from django.db import models
from django.contrib.auth.models  import User


class User(User):
    user_ptr = models.OneToOneField(User)
    paypal = models.CharField(max_length=50)
    emailConfirm = models.BooleanField(default=False);

class ConfirmEmail(models.Model):
    uuid = models.CharField(max_length=50)
    user = models.OneToOneField(User)

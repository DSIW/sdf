
from django.db import models
from django.contrib.auth.models  import User


class User(User):
    user_ptr = models.OneToOneField(User)
    paypal = models.CharField(max_length=50)


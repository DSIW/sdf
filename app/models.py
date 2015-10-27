# coding=utf-8
from django.db import models
from django.contrib.auth.models  import User

# Create your models here.
class Book(models.Model):
    name= models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    language = models.CharField(max_length=100)
    releaseDate = models.DateField('release_date')
    pageNumber = models.IntegerField(default=1)
    isbn10 = models.CharField(max_length=100)
    isbn13 = models.CharField(max_length=100)
    isOnStoreWindow = models.BooleanField(default=False)
    # TODO Use id out of database
    user_id = 1

    def __str__(self):
        return self.name + ", " + self.author + " (" + self.language + ", " + str(self.releaseDate) + ")"

class User(User):
    user_ptr = models.OneToOneField(User)
    paypal = models.CharField(max_length=50)

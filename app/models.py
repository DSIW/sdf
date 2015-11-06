# coding=utf-8
from django.db import models
from django.contrib.auth.models  import User as AuthUser

class User(AuthUser):
    # auth_user fields: username, first_name, last_name, email, password, is_staff, is_active, is_superuser, date_joined, last_login
    location = models.CharField(max_length=255)
    user_ptr = models.OneToOneField(AuthUser)
    paypal = models.CharField(max_length=255)
    #TODO: userRating: rating: <int> 0..10, rating_text, reviewer_user_id, user_id, timestamp

    def __str__(self):
        return self.location + ", " + self.user_ptr + ", " + self.paypal

    def full_name(self):
        if self.first_name != "" and self.last_name != "":
            return "%s %s" % (self.first_name, self.last_name)
        else:
            return self.username



# Create your models here. Unique primary key ids are automatically generated !
class Book(models.Model):
    user = models.ForeignKey(User, default=None)

    #TODO: bookCover
    name= models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    language = models.CharField(max_length=100)
    releaseDate = models.DateField('release_date')
    pageNumber = models.IntegerField(default=1)
    isbn10 = models.CharField(max_length=100)
    isbn13 = models.CharField(max_length=100)
    description = models.TextField(default="")

    def __str__(self):
        return self.name + ", " + self.author + " (" + self.language + ", " + str(self.releaseDate) + ")"


class Offer(models.Model):
    seller_user = models.ForeignKey(User, default=None)
    book = models.ForeignKey(Book, default=None)
    price = models.FloatField()
    shipping_price = models.FloatField()

    #TODO: resolve id to names
    def __str__(self):
        return "" + str(self.seller_user_id) + ", " + str(self.book) + ", " + str(self.price) + ", " + str(self.shipping_price)

    def totalPrice(self):
        return self.price + self.shipping_price
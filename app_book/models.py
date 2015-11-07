from django.db import models

from app_user.models import User

# Create your models here.
class Book(models.Model):
    user = models.ForeignKey(User, default=None)

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
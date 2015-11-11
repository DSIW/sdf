from django.db import models

from app_user.models import User

# Create your models here.
class Book(models.Model):
    user = models.ForeignKey(User)

    name= models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    language = models.CharField(max_length=100)
    releaseDate = models.DateField('release_date')
    pageNumber = models.IntegerField(default=0)
    isbn10 = models.CharField(max_length=100)
    isbn13 = models.CharField(max_length=100)
    description = models.TextField(default="", blank=True)

    def __str__(self):
        return self.name + ", " + self.author + " (" + self.language + ", " + str(self.releaseDate) + ")"

    def is_published(self):
        return self.offer_set.count() > 0 and self.offer_set.first().active


class Offer(models.Model):
    seller_user = models.ForeignKey(User)
    book = models.ForeignKey(Book)
    price = models.FloatField()
    shipping_price = models.FloatField()
    active = models.BooleanField(default=False)

    class Meta:
        unique_together = ("seller_user", "book")

    #TODO: resolve id to names
    def __str__(self):
        return "" + str(self.seller_user_id) + ", " + str(self.book) + ", " + str(self.price) + ", " + str(self.shipping_price)

    def totalPrice(self):
        return self.price + self.shipping_price

from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Listings(models.Model):
    category_choices=(
    ('T','Toys'),
    ('F','Fashion'),
    ('E','Electronics'),
    ('H','Home'),
    ('S','Sports'),
    ('O','Others')
    )
    created_by=models.CharField(max_length=200, null=True)
    title= models.CharField(max_length=200)
    description=models.CharField(max_length=200)
    date=models.DateField()
    starting_bid=models.IntegerField()
    Categories=models.CharField(choices=category_choices, max_length=10)
    image= models.ImageField(upload_to='images/', null=True)
    watchlist=models.BooleanField(null=True)
    highest_bidder=models.CharField(max_length=100, null=True)
    close_bid= models.BooleanField(null=True)


    def __str__(self):
        return f"{self.id}: {self.title}, {self.description}, {self.date}, {self.starting_bid}, {self.Categories}"

class Comments(models.Model):
    user=models.CharField(null=True, max_length=100)
    comment=models.CharField(null=True, max_length=500)
    item_id=models.IntegerField(null=True)

class Bids(models.Model):
    user=models.CharField(null=True, max_length=100)
    bid=models.IntegerField(null=True)
    item_id=models.IntegerField(null=True)

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    categorys = models.CharField(max_length=64)

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    price = models.DecimalField(max_digits=11, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name="category")
    image_url = models.ImageField(upload_to="uploads/")
    time_listed = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user")
    is_active = models.BooleanField(default=True)
    
class Bid(models.Model):
    time_bid = models.DateTimeField(blank=True, null=True)
    price = models.DecimalField(max_digits=11, decimal_places=2)
    listing = models.ForeignKey(Listing, blank=True, null=True, on_delete=models.CASCADE, related_name="bid")

class Comment(models.Model):
    time_comment = models.DateTimeField(blank=True, null=True)
    listing_comment= models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")

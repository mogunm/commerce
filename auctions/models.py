from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    category_name = models.CharField(max_length=64)

    def __str__(self):
        return self.category_name
    
class Bid(models.Model):
    bid = models.DecimalField(max_digits=11, decimal_places=2, default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="bidUser")

    def __str__(self):
        return f"{float(self.bid)}" 

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    price = models.ForeignKey(Bid, on_delete=models.CASCADE, blank=True, null=True, related_name="bidPrice")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name="category")
    image_url = models.ImageField(null=True, blank=True, upload_to='images/')
    time_listed = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user")
    is_active = models.BooleanField(default=True)
    # a listing can be in multiple users watchlist 
    watchlist = models.ManyToManyField(User, blank=True, null=True, related_name="watchlist")
    
    def __str__(self):
        return self.title
    

class Comment(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="owner")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=True, null=True, related_name="listing")
    message = models.CharField(max_length=300)

    def __str__(self):
        return f"{self.owner} comment on {self.listing}"
    


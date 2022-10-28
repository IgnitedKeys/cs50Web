from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


CAT_CHOICES = (
    ('Fiction',"FICTION"),
    ('Children','CHILDREN'),
    ('Fantasy','FANTASY'),
    ('NonFiction','NON-FICTION'),
    ('Sci-Fi',"SCI-FI"),
    ('Young Adult', 'YOUNG ADULT'),
    ('Mystery','MYSTERY'),
    ('Historical Fiction', 'HISTORICAL FICTION'),
    ('Classics', 'CLASSICS'),
    ('Comics', 'COMICS')
)

class Bids(models.Model):
    price = models.DecimalField(max_digits=7, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_bids")

class Comments(models.Model):
    comment = models.CharField(max_length=200, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comment")

class Listings(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    category = models.CharField(max_length=30, choices=CAT_CHOICES, default='')
    description = models.CharField(max_length=500, blank=True, null=True)
    price = models.DecimalField(max_digits=7,decimal_places=2)
    image = models.ImageField(blank=True,null=True) #upload_to='images',
    bids = models.ManyToManyField(Bids, blank=True, related_name= "bids")
    comments = models.ManyToManyField(Comments, blank=True, related_name="comments")
    closed = models.BooleanField(default=False)
    lister = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listers")
    def __str__(self):
        return self.title

class Watchlist(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist")
    listing= models.ForeignKey(Listings, on_delete=models.CASCADE, related_name="listing")




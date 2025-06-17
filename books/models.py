from django.db import models

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publisher = models.CharField(max_length=100)
    isbn = models.CharField(max_length=13, unique=True)
    photo_small = models.ImageField(upload_to="photos/%Y/%m/%d/", blank=True, null=True)
    photo_large = models.ImageField(upload_to="photos/%Y/%m/%d/", blank=True, null=True)
    introduction = models.TextField(blank=True)
    category = models.CharField(max_length=50)
    subcategory = models.CharField(max_length=50)
    language = models.CharField(max_length=30)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    hots = models.BooleanField(default=False)
    newbook = models.BooleanField(default=False)
    recommend = models.BooleanField(default=False)

    def __str__(self):
        return self.title
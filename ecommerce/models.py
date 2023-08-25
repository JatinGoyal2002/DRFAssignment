from django.db import models
from django.utils import timezone

# Create your models here.

class Category(models.Model):
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null = True, blank = True, related_name="subcategories")
    title = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = "Categories"

class Product(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    product_category = models.ForeignKey(Category, on_delete=models.SET_NULL, null = True, blank = True)
    
    def __str__(self):
        return self.title
    
class Image(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null = True, blank = True)
    source = models.ImageField()
    alt_text = models.CharField(max_length=200) 
    updated_at = models.DateTimeField(auto_now = True)
    
    def __str__(self):
        return self.alt_text
    
    @property
    def imageURL(self):
        try:
            url = self.source.url
        except:
            url = ''
        return url

class Variant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    available_for_sale = models.BooleanField(default = True)
    price = models.FloatField()
    def __str__(self):
        return self.product.title + " " + self.title

    
class Collection(models.Model):
    products = models.ManyToManyField(Product)
    title = models.CharField(max_length=100)
    published = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now = True)
    
    def __str__(self):
        return self.title
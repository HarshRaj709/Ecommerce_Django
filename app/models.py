from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Extrainfo(models.Model):
    Users = models.OneToOneField(User,on_delete=models.CASCADE)
    Address = models.CharField(max_length=5000)
    contact_no = models.CharField(max_length=10)

    def __str__(self):
        return self.Users.username
    
class Contact(models.Model):
    name = models.ForeignKey(User,on_delete=models.CASCADE)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name.username
    
class Product_category(models.Model):
    category = models.CharField(max_length=250)
    def __str__(self):
        return self.category

class Subcategory(models.Model):
    category = models.ForeignKey(Product_category,on_delete=models.CASCADE,related_name="subcategories")
    sub_category = models.CharField(max_length=300)

    def __str__(self):
        return f"{self.category.category} - {self.sub_category}"
    
class Products(models.Model):
    product_name = models.CharField(max_length=50,default='')
    category = models.ForeignKey(Product_category,on_delete=models.CASCADE)           #ill add category foreign key
    subcategory = models.ForeignKey(Subcategory,on_delete=models.CASCADE)        #and this also
    price = models.IntegerField(default=0)
    desc = models.CharField(max_length=300)
    image = models.ImageField(upload_to='shop/images',default='')

    def __str__(self):
        return self.product_name

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)         #single user - single cart

    def __str__(self):
        return f"Cart of {self.user.username}"

class CartItem(models.Model):           #other things cart must have have
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.product_name} in {self.cart.user.username}'s cart"

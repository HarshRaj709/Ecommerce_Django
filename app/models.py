from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Users extra info
class Extrainfo(models.Model):
    Users = models.OneToOneField(User,on_delete=models.CASCADE)
    state = models.CharField(max_length=500)
    country = models.CharField(max_length=500)
    Address = models.CharField(max_length=5000)
    zip = models.IntegerField(default=000000)
    contact_no = models.CharField(max_length=10)

    def __str__(self):
        return self.Users.username
    
#users contacted us
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
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='cart')         #single user - single cart

    def __str__(self):
        return f"Cart of {self.user.username}"

class CartItem(models.Model):           #other things cart must have have
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.id} {self.quantity} x {self.product.product_name} in {self.cart.user.username}'s cart"
    
class User_Orders(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name='orders')
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE,related_name='my_cart')
    created_at = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    delivered = models.BooleanField(default=False)
    delivered_on = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.delivered and not self.delivered_on:
            self.delivered_on = timezone.now()
        super(User_Orders, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.user.username} created at {self.created_at}'


class OrderItem(models.Model):          #used for my_orders details
    order = models.ForeignKey(User_Orders, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Price at the time of purchase

    def __str__(self):
        return f'{self.product.product_name} x {self.quantity}'

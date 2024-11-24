from django.contrib import admin
from .models import Extrainfo,Contact,Products,Product_category,Subcategory,Cart,CartItem,User_Orders,OrderItem

# Register your models here.
@admin.register(Extrainfo)
class ExtraAdmin(admin.ModelAdmin):
    list_display=[field.name for field in Extrainfo._meta.fields]

# admin.site.register(Contact)
@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Contact._meta.fields]


@admin.register(Products)
class ContactAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Products._meta.fields]

admin.site.register(Product_category)
admin.site.register(Subcategory)
admin.site.register(CartItem)
admin.site.register(Cart)
# admin.site.register(User_Orders)
@admin.register(User_Orders)
class AdminUserorder(admin.ModelAdmin):
    list_display = [field.name for field in User_Orders._meta.fields]
admin.site.register(OrderItem)
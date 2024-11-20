from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('/<str:category>/',views.home,name='home'),
    path('profile/',views.userProfile,name='profile'),
    path('contact_us/',views.contact,name='contact'),
    path('cart/', views.cart, name='cart'),
    path('cart/<int:product>/', views.cart, name='cart'),
    path('remove/<int:product>/',views.remove_cart,name='remove_cart'),
    path('cart/quantity/<int:product>/',views.Cart_quantity,name='quantity')

]

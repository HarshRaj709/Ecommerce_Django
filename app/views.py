from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import ProfileForm,Extraform,ContactForm
from .models import Extrainfo,Contact,Products,Product_category,Subcategory,Cart,CartItem
from math import ceil

# Create your views here.
def userProfile(request):
    current = request.user
    try:
        extra_info = Extrainfo.objects.get(Users=current)
    except Extrainfo.DoesNotExist:
        extra_info = None
    # print(current.email)
    if request.method == 'POST':
        form = ProfileForm(request.POST,user=current)
        Extra = Extraform(request.POST,instance=extra_info)
        if form.is_valid() and Extra.is_valid():
            # If the form is valid, update the user information
            form.save(user=current) 
            extra_instance = Extra.save(commit=False)
            extra_instance.Users = current  # Ensure the relationship is set
            extra_instance.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('profile')
        else:
            for error in form.errors.values():
                messages.error(request, error)
            for error in Extra.errors.values():
                messages.error(request, error)
            # print(Extra.errors)
            return redirect('profile')
        
        #below code is also working fine

        # username = request.POST.get('username')
        # if User.objects.filter(username=username).exists():
        #     messages.error(request,'Username already used try different username.')
        #     return redirect('profile')
        # print(username)
        # first = request.POST.get('first')
        # last = request.POST.get('last')
        # email = request.POST.get('email')

        # current.username = username
        # current.first_name = first
        # current.last_name = last
        # current.email = email
        # current.save() 
        # return redirect('profile')
    else:
        context = {'current':current,'extra':extra_info}
        return render(request,'app/profile.html',context)
    

def contact(request):
    if request.method == 'POST':
        fm = ContactForm(request.POST)
        if fm.is_valid():
            form=fm.save(commit=False)
            form.name = request.user
            form.save()
            messages.success(request,'We received your request,we will contact you soon..')
            return redirect('contact')
        else:
            for error in fm.errors.values():
                messages.error(request,error)
            return redirect('contact')
    return render(request,'app/contact.html')

def home(request,category=None):
    categories = Product_category.objects.all()
    # print(categories)
    if not category:

        allProds = []
        catprods = Products.objects.values('category','id')         #generates output as dictionary
        #print(catprods)                 #[{'category': 'clothing', 'id': 1}, {'category': 'Ear phones', 'id': 2}, {'category': 'cars', 'id': 3}]>
        cats = {item['category'] for item in catprods}
        #print(cats)                     #{'Ear phones', 'clothing', 'cars'} set type
        for cat in cats:
            prod = Products.objects.filter(category=cat)
            n=len(prod)
            nslides = n//4 + ceil((n/4)-(n//4))
            allProds.append([prod,range(1,nslides),nslides])
        params = {'allProds':allProds,'categories':categories}
        return render(request,'app/index.html',params)
    #print(allProds)
    else:
        #print(category)
        products = Products.objects.filter(category__category=category)
        # print(products)
        return render(request,'app/index.html',{'products':products,'categories':categories})

def cart(request, product=None):
    if not request.user.is_authenticated:
        messages.error(request, "You need to log in to add items to the cart.")
        return redirect('signin')

    user_cart, created = Cart.objects.get_or_create(user=request.user)
    # user_cart = Cart.objects.create(user=request.user)              #this will try to create cart each time when user clicks on cart.
    if request.method == 'POST' and product:
        product_to_add = get_object_or_404(Products, id=product)    #first find that product exists or not
                  
        # Item = Products.objects.get(id=product)                 #problem with this is that user can add same product multiple times
        CartItem.objects.get_or_create(cart=user_cart, product=product_to_add)

        # CartItem.objects.create(cart=user_cart, product=Item)

        messages.success(request, 'Product added to the cart!')
        return redirect('home')
    cart_items = CartItem.objects.filter(cart=user_cart)
    return render(request, 'app/cart.html', {'carts': cart_items})


def remove_cart(request,product):
    # print(product)
    # item = CartItem.objects.get(product_id=product)
    # item = CartItem.objects.get(cart = request.user.cart,product_id=product)
    item = get_object_or_404(CartItem,cart=request.user.cart,product_id=product)
    item.delete()
    # left = CartItem.objects.filter(cart = request.user.cart)            #request.user.cart refers to the single cart that is tied to the logged-in user
    # print(item)
    return redirect('cart')
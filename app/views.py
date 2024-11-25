from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import ProfileForm,Extraform,ContactForm
from .models import Extrainfo,Contact,Products,Product_category,Subcategory,Cart,CartItem,User_Orders,OrderItem
from math import ceil
from django.contrib.auth.decorators import login_required
from datetime import timedelta

# Create your views here.
@login_required(login_url='signin')
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
    
@login_required(login_url='signin')
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
    active = True
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
        return render(request,'app/index.html',{'products':products,'categories':categories,'active':active})

@login_required(login_url='signin')
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
    
    #Adding money
    total_cart = CartItem.objects.filter(cart = user_cart)
    # print('Total Cart',total_cart)
    total = 0
    for item in total_cart:
        total+=item.product.price * item.quantity           #item__product__price is a lookup style used in filtering or querying, not for accessing fields of an instance.
    
    cart_items = CartItem.objects.filter(cart=user_cart)
    return render(request, 'app/cart.html', {'carts': cart_items,'grand_total':total})


@login_required(login_url='signin')
def remove_cart(request,product):
    # print(product)
    # item = CartItem.objects.get(product_id=product)
    # item = CartItem.objects.get(cart = request.user.cart,product_id=product)
    item = get_object_or_404(CartItem,cart=request.user.cart,product_id=product)
    item.delete()
    # left = CartItem.objects.filter(cart = request.user.cart)            #request.user.cart refers to the single cart that is tied to the logged-in user
    # print(item)
    return redirect('cart')


@login_required(login_url='signin')
def Cart_quantity(request,product):
    if request.method == 'POST':
        clicked = request.POST.get('action')
        cart_item = get_object_or_404(CartItem,product__id=product)
        # product = Products.objects.get(id=product)
        # cart_item = CartItem.objects.get(product=product)
        print(clicked)
        if clicked == 'increase':
            cart_item.quantity +=1
            cart_item.save()
            messages.success(request,'Product Quantity increased by 1.')
            # print(cart_item.quantity)
        elif clicked == 'decrease':
            if cart_item.quantity>1:
                cart_item.quantity -=1
                cart_item.save()
                messages.success(request,'Product Quantity decreased by 1.')
            else:
                messages.error(request,"Can't make item 0, if you want to remove product click to 'Remove' button.")
        return redirect('cart')
    

@login_required(login_url='signin')
def Checkout(request):
    user = request.user
    info = Extrainfo.objects.get(Users=user)
    total_cart = CartItem.objects.filter(cart__user = user)
    # print('Total Cart',total_cart)
    total = 0
    for item in total_cart:
        total+=item.product.price * item.quantity 

    if request.method == 'POST':
        # Create the order
        order = User_Orders.objects.create(user=user, cart=user.cart,total = total)


#creating a Paytm Integration
        # user_email = order.user.email
        # print(user_email)
        # id = order.id 
        # print(id)
        # oid = str(id)+'ZombieCart'
        # param_dict = {
        #     'MID':keys.MID,
        #     'ORDER_ID':oid,
        #     'TXN_AMOUNT': str(total),
        #     'CUST_ID': user_email,
        #     'INDUSTRY_TYPE_ID': 'Retail',
        #     'WEBSITE': 'WEBSTAGING',
        #     'CHANNEL_ID':'web',
        #     'CALLBACK_URL':'http://127.0.0.1:8000/handlerequest/',
        # }

        # param_dict['CHECKSUMHASH'] = Checksum.generate_

        # Create order items for the order
        for item in total_cart:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )
        
        total_cart.delete()  # This will delete the cart items after the order is placed
        return redirect('ord_success',order_id=order.id)
    else:
        return render(request,'app/Checkout.html',{'user':info,'personal':user,'total':total})

@login_required(login_url='signin')
def My_order(request):
    user = request.user
    orders = user.orders.all().order_by('-created_at')

    #add new expected_delivery attribute to the order
    for order in orders:
        order.expected_delivery = order.created_at + timedelta(days=5) 
    # order_value=User_Orders.objects.get(user=user)
    # total = order_value.total
    return render(request,'app/my_orders.html',{'orders': orders})

@login_required(login_url='signin')
def order_success(request,order_id):
    order_info = User_Orders.objects.get(id=order_id)
    order_info.expected_delivery = order_info.created_at + timedelta(days=5)
    return render(request,'app/order_success.html',{'order_info':order_info})

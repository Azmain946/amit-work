from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms 
from django.db.models import Q
from .forms import *

from payment.forms import *
from payment.models import *

import json
from cart.cart import Cart

def about_for_site(request):
    about = AboutWebsite.objects.all().last()
    return render(request, 'about.html', {'about': about})

def my_nav(request):
    categories = Category.objects.all()
    return render(request, 'base.html', {'categories': categories})

def search(request):
    categories = Category.objects.all()
    if request.method == "POST":
        searched = request.POST['searched']
        searched = Product.objects.filter(Q(name__icontains = searched) | Q(description__icontains=searched))

        if not searched:
            messages.success(request, "That product does not exist...Try Again..")
            return render(request, "search.html", {})
        else:
            return render(request, "search.html", {'searched':searched,})
    
    else:    
        return render(request, "search.html", {})


def update_info(request):
    if request.user.is_authenticated:
        current_user = get_object_or_404(Profile, user__id=request.user.id)
        #current_user = Profile.objects.get(user__id=request.user.id)
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        
        form = UserInfoForm(request.POST or None, instance=current_user)
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)


        if form.is_valid() or shipping_form.is_valid():
            form.save()

            shipping_form.save()
            messages.success(request, "User has been Updated!")
            return redirect('home')
        
        return render(request, 'update_info.html', {'form': form, 'shipping_form':shipping_form})
    else: 
        messages.success(request, "You must be logged in to update!")
        return redirect('home')
    





def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user

        if request.method == 'POST':
            form = ChangePasswordForm(current_user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Your password had been changed")
                login(request, current_user)
                return redirect('update_user')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                    return redirect('update_password')
        else:
            form = ChangePasswordForm(current_user)
            return render(request, 'update_password.html', {'form': form})
    else:
        messages.success(request, "You must be logged in to update!")
        return redirect('home')


def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=current_user)

        if user_form.is_valid():
            user_form.save()

            login(request, current_user)
            messages.success(request, "User has been Updated!")
            return redirect('home')
        
        return render(request, 'update_user.html', {'user_form': user_form})
    else: 
        messages.success(request, "You must be logged in to update!")
        return redirect('home')
    



def category_summary(request):
    categories = Category.objects.all()
    return render(request, 'category_summary.html', {"categories":categories})
            

def category(request, foo):

    foo = foo.replace('-', ' ')
    
    try:
        category = Category.objects.get(name=foo)
        products = Product.objects.filter(category=category)
        return render(request, 'category.html', {
            'products':products,
            'category': category,
        })
    except:
        messages.success(request, ('That category doesnot exist'))

        return redirect('home')

def product(request, pk):
    product = Product.objects.get(id=pk)
    categories = Category.objects.all()
    sizes = Product_Size.objects.all()
    return render(request, 'product.html', {'product':product, 'categories':categories, 'sizes': sizes})



def home(request):
    covers = ImageForCover.objects.all()
    products = Product.objects.all()
    categories = Category.objects.annotate(product_count=models.Count('product')).filter(product_count__gt=0)
    category_products = {
        category: Product.objects.filter(category=category).order_by('-id')[:5]
        for category in categories
    }
    return render(request, 'home.html', {'covers':covers,'category_products':category_products,'products':products, 'categories':categories})

def about(request):
    categories = Category.objects.all()
    return render(request, 'about.html', {'categories':categories})

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            current_user = Profile.objects.get(user__id=request.user.id)
            saved_cart = current_user.old_cart

            if saved_cart:
                try:
                    print("Raw saved cart", saved_cart)
                    sanitized_cart = saved_cart.replace('""', '"').replace('\\"', '"')
                    
                    print("Sanitized Cart", sanitized_cart)
                    converted_cart = json.loads(sanitized_cart)

                    print("Converted cart", converted_cart)
                    cart = Cart(request)

                    for key, value in converted_cart.items():
                        cart.db_add(product=key, quantity=value['quantity'], size=value['size'])
                except json.JSONDecodeError:
                    messages.error(request, "Failed to load saved card data due to invalid request")

            messages.success(request, ("You have been logged in"))
            return redirect('home')
            
        else:
            messages.success(request, ("There was an error, please try again."))
            return redirect('login')
    
    else:
        return render(request, 'login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, ('You have been logged out'))
    return redirect('home')

def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            #login 

            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("Account Created. Please update your information."))
            return redirect('update_info')

        else:
            messages.success(request, ('Ops, got into a problem'))
            return redirect('register')
    
    else:
        return render(request, 'register.html', {'form':form})

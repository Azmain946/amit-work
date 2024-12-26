from django.shortcuts import render, redirect, get_object_or_404
from cart.cart import Cart
from .forms import *
from django.contrib import messages
from django.contrib.auth.models import User
from payment.models import Order, OrderItem, ShippingAddress, deliveryCharge
from store.models import Product, Profile, Product_Size
import datetime



def process_buy_now_order(request):
    if request.method == "POST":

        product_id = request.POST.get('product_id')
        product_qty = int(request.POST.get('product_qty'))
        size_id = int(request.POST.get('product_size'))

        selected_size = Product_Size.objects.get(id=size_id)

        product = Product.objects.get(id = product_id)

        if product.is_sale:
            price = product.sale_price
        else:
            price = product.price
        
        delivery_charge = deliveryCharge.objects.all().last().shipping_charge
        total_price = (price*product_qty) + delivery_charge

        shipping_form = ShippingForm(request.POST)

        if shipping_form.is_valid():
            full_name = shipping_form.cleaned_data['shipping_full_name']
            email = shipping_form.cleaned_data['shipping_email']
            phone = shipping_form.cleaned_data['shipping_phone']
            shipping_address = f"{shipping_form.cleaned_data['shipping_address1']}\n{shipping_form.cleaned_data['shipping_address2']}\n{shipping_form.cleaned_data['shipping_city']}\n{shipping_form.cleaned_data['shipping_state']}\n{shipping_form.cleaned_data['shipping_zipcode']}\n{shipping_form.cleaned_data['shipping_country']}"
            print("Printing under form",full_name, email)
        

        
        
        if request.user.is_authenticated:
            user = request.user
            order = Order(user=user, full_name=full_name, phone=phone, email=email, shipping_address=shipping_address, amount_paid = total_price)
            order.save()
        else:
            order = Order(full_name=full_name,phone=phone, email=email, shipping_address=shipping_address, amount_paid = total_price)
            order.save()
        order_item = OrderItem(order=order,  product=product, quantity = product_qty, price = price, size=selected_size)
        order_item.save()

        if 'my_shipping' in request.session:
            del request.session['my_shipping']
        
        messages.success(request, "Your orer has been placed!")
        return redirect('home')
    
    else:
        messages.success(request, "Access Denied")
        return redirect('home')
    

def buy_now(request):
    

    if request.method == 'POST':
        
        print("request POST data:", request.POST)
        
        try: 
            product_id = int(request.POST.get('product_id'))
            product_qty = int(request.POST.get('product_qty'))
            size_id = int(request.POST.get('product_size'))
            selected_size = get_object_or_404(Product_Size, id=size_id)
            print(f"Product ID: {product_id}, Quantity: {product_qty}")
        
            product = get_object_or_404(Product, id=product_id)
            total_price = float(product.price) * product_qty


            delivery_charge = deliveryCharge.objects.all().last()

            if delivery_charge:
                total_price += delivery_charge.shipping_charge

            if request.user.is_authenticated:
                shipping_user = ShippingAddress.objects.get(user__id = request.user.id)
                shipping_form = ShippingForm(instance=shipping_user)
            else:
                shipping_form = ShippingForm()

            context = {
                "product": product,
                "quantity": product_qty,
                "selected_size": selected_size,
                "total_price": total_price,
                "shipping_form": shipping_form,
            }  

            print("context: ", context)


            return render(request, "payment/buy_now.html", context)
        except Exception as e:
            print("Error occured: ", e)
            return render(request, 'payment/buy_now.html', {"error": str(e)})
       
    else:
        messages.success(request, "Access Denied")
        return redirect('home')


              

def orders(request, pk):
    if request.user.is_authenticated and request.user.is_superuser:
        order = Order.objects.get(id=pk)
        items = OrderItem.objects.filter(order=pk)
        now = datetime.datetime.now()

        if request.POST:
            status = request.POST['shipping_status']
            if status == "true":
                order = Order.objects.filter(id=pk)
                
                order.update(shipped=True, date_shipped=now)

            else:
                order = Order.objects.filter(id=pk)
                order.update(shipped=False)

            messages.success(request, "Shipping Status Updated")
            return redirect('home')


        return render(request, 'payment/orders.html', {"order": order, "items": items})
    


    else:
        messages.success(request, "Order Placed")
        return redirect("home")


def not_shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped=False)

        if request.POST:
            status = request.POST['shipping_status']
            num = request.POST['num']
            now = datetime.datetime.now()
            order = Order.objects.filter(id=num)

            order.update(shipped=True, date_shipped=now)

            messages.success(request, "Shipping Status Updated")
            return redirect('home')


        return render(request, "payment/not_shipped.html", {"orders": orders})
    else:
        messages.success(request, "Order Placed")
        return redirect("home")
    
def user_orders(request):
    if request.user.is_authenticated:
        orders = Order.objects.filter(user=request.user)

        orders_with_items = []

        for order in orders:
            items = OrderItem.objects.filter(order=order)
            orders_with_items.append({
                "order": order,
                "items": items,
            })
        
        return render(request, 'payment/user_orders.html', {"orders_with_items": orders_with_items})

    else:
        messages.success(request, "Login into your account")
        return redirect('login')
    
def shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped=True)

        if request.POST:
            status = request.POST['shipping_status']
            num = request.POST['num']
            now = datetime.datetime.now()
            order = Order.objects.filter(id=num)

            order.update(shipped=False)

            messages.success(request, "Shipping Status Updated")
            return redirect('home')
        return render(request, "payment/shipped.html", {"orders": orders})
    else:
        messages.success(request, "Order Placed")
        return redirect("home")

#def process_order(request):
    if request.POST:
        cart = Cart(request)
        cart_products = cart.get_prods
        quantities = cart.get_quants
        totals = cart.total() 
        payment_form = PaymentForm(request.POST or None)

        my_shipping = request.session.get('my_shipping')
        full_name = my_shipping['shipping_full_name']
        email = my_shipping['shipping_email']

        shipping_address = f"{my_shipping['shipping_address1']}\n{my_shipping['shipping_address2']}\n{my_shipping['shipping_city']}\n{my_shipping['shipping_zipcode']}\n{my_shipping['shipping_country']}"
        amount_paid = totals
        if request.user.is_authenticated:
            user = request.user
            create_order = Order(user= user, full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid)
            create_order.save()
            order_id = create_order.pk
            for product in cart_products():
                product_id = product.id
                if product.is_sale:
                    price = product.sale_price
                else:
                    price = product.price
                for key,value in quantities().items():
                    if int(key)==product.id:
                        create_order_item = OrderItem(order_id=order_id, product_id=product_id, user=user, quantity=value,price=price,)
                        create_order_item.save()

            for key in list(request.session.keys()):
                if key == "session_key":
                    del request.session[key]
              
                
             
        else:
            create_order = Order(full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid)
            create_order.save()
            order_id = create_order.pk
            for product in cart_products():
                product_id = product.id
                if product.is_sale:
                    price = product.sale_price
                else:
                    price = product.price
                for key,value in quantities().items():
                    if int(key)==product.id:
                        create_order_item = OrderItem(order_id=order_id, product_id=product_id, quantity=value,price=price,)
                        create_order_item.save()

            

            for key in list(request.session.keys()):
                if key == "session_key":
                    del request.session[key]

            current_user = Profile.objects.filter(user__id = request.user.id)
            current_user.update(old_cart="")

       
        messages.success(request, "Order Placed")
        return redirect("home")

    else:
        messages.success(request, "Access Denied")
        return redirect('home')

def process_order(request):
    if request.POST:
        # Get the cart
        cart = Cart(request)
        cart_products = cart.get_prods
        quantities = cart.get_quants
        sizes = cart.get_sizes()
          
        a = deliveryCharge.objects.all().last()
        
        
        totals = cart.total() + a.shipping_charge

        # Get Billing Info from the last page
        payment_form = PaymentForm(request.POST or None)
        # Get Shipping Session Data
        my_shipping = request.session.get('my_shipping')

        # Gather Order Info
        full_name = my_shipping['shipping_full_name']
        phone = my_shipping['shipping_phone']
        email = my_shipping['shipping_email']
        # Create Shipping Address from session info
        shipping_address = f"{my_shipping['shipping_address1']}\n{my_shipping['shipping_address2']}\n{my_shipping['shipping_city']}\n{my_shipping['shipping_state']}\n{my_shipping['shipping_zipcode']}\n{my_shipping['shipping_country']}"
        amount_paid = totals

        # Create an Order
        if request.user.is_authenticated:
            # logged in
            user = request.user
            # Create Order
            create_order = Order(user=user, full_name=full_name,phone=phone, email=email, shipping_address=shipping_address, amount_paid=amount_paid)
            create_order.save()

            # Add order items
            
            # Get the order ID
            order_id = create_order.pk
            
            # Get product Info
            for product in cart_products():
                # Get product ID
                product_id = product.id
                # Get product price
                if product.is_sale:
                    price = product.sale_price
                else:
                    price = product.price

                # Get quantity
                size = "Did not selected any size"
                for key,value in sizes.items():
                    if int(key) == product.id:
                        size = value
                
                for key,value in quantities().items():
                    if int(key) == product.id:
                        # Create order item
                        create_order_item = OrderItem(order_id=order_id, product_id=product_id, user=user, quantity=value, price=price, size=size)
                        create_order_item.save()

            # Delete our cart
            for key in list(request.session.keys()):
                if key == "session_key":
                    # Delete the key
                    del request.session[key]

            # Delete Cart from Database (old_cart field)
            current_user = Profile.objects.filter(user__id=request.user.id)
            # Delete shopping cart in database (old_cart field)
            current_user.update(old_cart="")


            messages.success(request, "Order Placed!")
            return redirect('home')

            

        else:
            # not logged in
            # Create Order
            create_order = Order(full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid)
            create_order.save()

            # Add order items
            
            # Get the order ID
            order_id = create_order.pk
            
            # Get product Info
            for product in cart_products():
                # Get product ID
                product_id = product.id
                # Get product price
                if product.is_sale:
                    price = product.sale_price
                else:
                    price = product.price

                # Get quantity
                size = "Did not selected any size"
                for key,value in sizes.items():
                    if int(key) == product.id:
                        size = value
                for key,value in quantities().items():
                    if int(key) == product.id:
                        # Create order item
                        create_order_item = OrderItem(order_id=order_id, product_id=product_id, quantity=value, price=price, size=size)
                        create_order_item.save()

            # Delete our cart
            for key in list(request.session.keys()):
                if key == "session_key":
                    # Delete the key
                    del request.session[key]



            messages.success(request, "Order Placed!")
            return redirect('home')


    else:
        messages.success(request, "Access Denied")
        return redirect('home')

def billing_info(request):
    if request.POST:
        cart = Cart(request)
        cart_products = cart.get_prods
        quantities = cart.get_quants
        sizes = cart.get_sizes()
        a = deliveryCharge.objects.all().last()
        totals = cart.total() + a.shipping_charge

        my_shipping = request.POST
        request.session['my_shipping']= my_shipping

        if request.user.is_authenticated:
            billing_form = PaymentForm()
            return render(request, 'payment/billing_info.html', {"cart_products": cart_products, "quantities": quantities, "totals": totals,"sizes":sizes, "shipping_info":request.POST, "billing_form": billing_form})
        else: 
            billing_form = PaymentForm()

            return render(request, 'payment/billing_info.html', {"cart_products": cart_products, "quantities": quantities, "totals": totals, "sizes":sizes, "shipping_info":request.POST, "billing_form": billing_form})


        shipping_form = request.POST
        return render(request, 'payment/billing_info.html', {"cart_products": cart_products, "quantities": quantities, "totals": totals, "shipping_form":shipping_form} )
    else:
        messages.success(request, "Access Denied!")
        return redirect('home') 


def checkout(request):
    
        cart = Cart(request)
        cart_products = cart.get_prods
        quantities = cart.get_quants
        sizes = cart.get_sizes()
        print(sizes)

        a = deliveryCharge.objects.all().last()
    
    
    
        totals = cart.total() + a.shipping_charge
        if request.user.is_authenticated:
            shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
            shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
            return render(request, 'payment/checkout.html', {"cart_products": cart_products, "quantities": quantities,"sizes":sizes, "totals": totals, "shipping_form":shipping_form} )
        else:
            shipping_form = ShippingForm(request.POST or None)
            return render(request, 'payment/checkout.html', {"cart_products": cart_products, "quantities": quantities,"sizes":sizes, "totals": totals, "shipping_form":shipping_form} )

    



def payment_success(request):
    return render(request, "payment/payment_success.html", {})

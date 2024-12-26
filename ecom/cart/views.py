from django.shortcuts import render, get_object_or_404
from .cart import Cart
from store.models import Product, Product_Size
from payment.models import deliveryCharge
from django.http import JsonResponse
from django.contrib import messages


def cart_summary(request):
    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.total()
    sizes = cart.get_sizes()
    all_sizes = Product_Size.objects.all()
    shipping_charge = deliveryCharge.objects.all().last()
    
    return render(request, 'cart_summary.html', {"cart_products": cart_products, "quantities": quantities, "totals": totals,"shipping_charge":shipping_charge, 'sizes':sizes, 'all_sizes':all_sizes} )


def cart_add(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        size_id = int(request.POST.get('size'))
        product_qty = int(request.POST.get('product_qty'))
        product = get_object_or_404(Product, id=product_id)
        selected_size = get_object_or_404(Product_Size, id = size_id)
        cart.add(product = product, quantity = product_qty, size=selected_size)
        cart_quantity = cart.__len__()
        
        response = JsonResponse({
           'qty': cart_quantity,

        })
        messages.success(request, ("Product added to cart...."))

        return response
    

def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))

        cart.delete(product = product_id)

        response = JsonResponse({'product': product_id})
        messages.success(request, ("Item deleted from shopping cart...."))
        
        return response

def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        print("request POST data:", request.POST)
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        size_id = int(request.POST.get('product_size'))
        selected_size = get_object_or_404(Product_Size, id=size_id)
        print("Selected size: ", selected_size)

        

        cart.update(product=product_id, quantity = product_qty, size=selected_size)

        response = JsonResponse({'qty': product_qty})
        messages.success(request, ("Your cart has been updated...."))
        
        return response
    
from django.shortcuts import get_object_or_404
from store.models import *

class Cart():
    def __init__(self, request):
        self.session = request.session

        self.request = request
        cart = self.session.get('session_key')

        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        self.cart = cart 
    
    def db_add(self, product, quantity, size=None):
        product_id = str(product)
        product_qty = str(quantity)
        if product_id in self.cart:
            self.cart[product_id]['quantity'] += int(product_qty)
            self.cart[product_id]['size'] = size if isinstance(size, str) else size.size if size else self.cart[product_id]['size']

        else:
            self.cart[product_id] = {
            'quantity': product_qty,
            'size': size if isinstance(size, str) else size.size if size else None
        }

        self.session.modified = True

        if self.request.user.is_authenticated:

            current_user = Profile.objects.filter(user__id=self.request.user.id)
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            current_user.update(old_cart=str(carty))

    
    def add(self, product, quantity, size=None):
        product_id = str(product.id)
        product_qty = str(quantity)
        if product_id in self.cart:
            self.cart[product_id]['quantity'] += int(quantity)
            self.cart[product_id]['size'] = size.size if size else None

        else:
            self.cart[product_id] = {
                'quantity': int(product_qty),
                'size': size.size if size else None
            }

        self.session.modified = True

        if self.request.user.is_authenticated:

            current_user = Profile.objects.filter(user__id=self.request.user.id)
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            current_user.update(old_cart=str(carty))

    def total(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        

        total_p = 0

        for key, value in self.cart.items():
            key = int(key)
            quantity = int(value['quantity'])
            for product in products:
                if product.id == key:
                    if product.is_sale:
                        total_p += (product.sale_price * quantity) 
                    else:
                        total_p += (product.price * quantity) 
        return total_p

    def __len__(self):
        return len(self.cart)
    
    def get_sizes(self):
        return {key: value['size'] for key, value in self.cart.items()}
    
    
    def get_prods(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in = product_ids)
    
        return products
    
    def get_quants(self):
        
        return {key: value['quantity'] for key, value in self.cart.items()} 
    
    def update(self, product, quantity, size):
        prdct = get_object_or_404(Product, id=product)
        #print(f"Found product: {prdct}")

        product_id = str(prdct.id)
        product_qty = int(quantity)

        print("Size passed in cart.update ", size)

    
        

        if product_id in self.cart:

            self.cart[product_id]['quantity'] = product_qty
            if size:
                self.cart[product_id]['size']= size.size
                print(f"Updated cart: {self.cart[product_id]['size']}")
            else:
                self.cart[product_id]['size']= None

            self.session['cart'] = self.cart
            self.session.modified = True
            print("session updated: ", self.session.get('cart'))

        if self.request.user.is_authenticated:

            current_user = Profile.objects.filter(user__id=self.request.user.id)
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            current_user.update(old_cart=str(carty))

        return self.cart
    
    
    def delete(self, product):
        product_id = str(product)
        if product_id in self.cart:
            del self.cart[product_id]

        self.session.modified = True
        
        if self.request.user.is_authenticated:

            current_user = Profile.objects.filter(user__id=self.request.user.id)
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            current_user.update(old_cart=str(carty))



    





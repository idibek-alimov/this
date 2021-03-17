from decimal import Decimal
from django.conf import settings
from shop.models import Product

class Cart(object):

    def __init__(self,request):
        """
        initializing the thing to work
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self,product,quantity=1, override_quantity=False):
        """
        Add  a product to the cart
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity':0,
                                     'price':str(product.price)}
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        # mark theh session as modified
        self.session.modified = True

    def remove(self):
        """
        Remove product from the cart
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """
        iterate over the thing and see all of them
        :return:
        """
        product_ids = self.cart.keys()
        # get the product objects from the sesssion
        products = Product.objects.filter(id__in=product_ids)

        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        Coutn all the product in the cart
        """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum (Decimal(item['price']) * item['quantity'] for item
                    in self.cart.values())

    def clear(self):
        # remove cart from session
        del self.session[settings.CART_SESSION_ID]
        self.save()
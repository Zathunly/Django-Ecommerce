from store.models import Product
from .models import CartItem  
from django.contrib.auth.signals import user_logged_out
from django.dispatch import receiver

class Cart:
    def __init__(self, request):
        self.session = request.session
        self.user = request.user
        self.cart = self.session.get('session_key', {})

        if not self.cart:
            self.session['session_key'] = self.cart

        if self.user.is_authenticated:
            self._load_user_cart()

    def _load_user_cart(self):
        db_cart_items = CartItem.objects.filter(user=self.user)
        for item in db_cart_items:
            product_id = str(item.product.id)

            attribute_key = "-".join(f"{value}" for value in item.attributes.values())
            unique_key = f"{product_id}-{attribute_key}" if attribute_key else product_id

            self.cart[unique_key] = {
                'id': item.product.id,  
                'quantity': item.quantity,
                'price': float(item.price),
                'attributes': item.attributes  
            }
            
        self.session.modified = True


    def add(self, product, quantity, price, **attributes):
        product_id = str(product.id)
        attribute_key = "-".join(f"{value}" for value in attributes.values())
        unique_key = f"{product_id}-{attribute_key}" if attribute_key else product_id

        if unique_key in self.cart:
            self.cart[unique_key]['quantity'] += quantity
        else:
            self.cart[unique_key] = {
                'id': product.id,  
                'quantity': quantity,
                'price': price,
                'attributes': attributes 
            }

        self.session['session_key'] = self.cart
        self.session.modified = True


        if self.user.is_authenticated:
            cart_item, created = CartItem.objects.get_or_create(
                user=self.user,
                product=product,
                defaults={'quantity': 0, 'price': price}
            )
            if not created:
                cart_item.quantity += quantity
            else:
                cart_item.quantity = quantity

            cart_item.price = price
            cart_item.attributes = attributes
            cart_item.save()

    def update(self, updated_data):
        for product_key, quantity in updated_data.items():
            if '-' in product_key:
                product_id, size = product_key.split('-', 1)
            else:
                product_id, size = product_key, None

            if product_key in self.cart:
                self.cart[product_key]['quantity'] = quantity

                if self.user.is_authenticated:
                    try:
                        product = Product.objects.get(id=product_id)
                        
                        cart_item, created = CartItem.objects.update_or_create(
                            user=self.user,
                            product=product,
                            defaults={
                                'price': self.cart[product_key]['price'],
                                'size': size  
                            }
                        )
                        if not created:
                            cart_item.quantity = quantity
                            cart_item.save()

                    except Product.DoesNotExist:
                        print(f"Product with ID {product_id} does not exist.")
                    except Exception as e:
                        print(f"Error updating CartItem: {e}")

        # Mark the session as modified to save the changes
        self.session.modified = True


    def delete(self, product_keys):
        if not isinstance(product_keys, list):
            product_keys = [product_keys]  

        for unique_key in product_keys:
            if unique_key in self.cart:
                del self.cart[unique_key]

                if self.user.is_authenticated:
                    product_id, *attribute_values = unique_key.split("-")
                    attributes = self._extract_attributes(attribute_values)

                    CartItem.objects.filter(user=self.user, product_id=product_id, attributes=attributes).delete()

        self.session.modified = True

    def _extract_attributes(self, attribute_values):
        """
        Helper method to reconstruct attribute dictionary from list of attribute values.
        Assumes attribute_values order is consistent.
        """
        attribute_keys = ['size', 'color']  
        return {key: value for key, value in zip(attribute_keys, attribute_values) if value}

    def total_price(self):
        total = sum(item['quantity'] * item['price'] for item in self.cart.values())
        return total

    def __len__(self):
        return len(self.cart)

    def get_products(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        return products

    def get_session_data(self):
        return self.cart

    def clear(self):
        if 'session_key' in self.session:
            del self.session['session_key']  
            self.session.modified = True  

        if self.user.is_authenticated:
            CartItem.objects.filter(user=self.user).delete()

    @receiver(user_logged_out)
    def clear_session_cart(sender, request, **kwargs):
        if 'session_key' in request.session:
            del request.session['session_key']


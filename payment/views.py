from django.shortcuts import render, redirect, get_object_or_404
from .models import ShippingAddress, Order, OrderItem, PaymentMethod
from userprofile.models import Profile
from cart.cart import Cart
from store.models import Product, Stock, Size, Color
from django.contrib import messages
from django.db import transaction

def payment_success(request):
    return render(request, 'payment_success.html', {})

def checkout(request):
    if request.method == 'POST':
        cart = Cart(request)
        cart_products = cart.get_session_data()  
        cart_quantities = cart.__len__()
        cart_total = cart.total_price()
        payment_methods = PaymentMethod.objects.all()

        insufficient_stock = False  

        for product_key, item_data in cart_products.items():
            try:
                product_id = item_data['id']
                quantity_requested = item_data['quantity']
                attributes = item_data.get('attributes', {})
                size_name = attributes.get('size')  
                color_name = attributes.get('color')  

                if not size_name or not color_name:
                    raise ValueError(f"Missing size or color for product {product_id}.")

                size = Size.objects.get(name=size_name)
                color = Color.objects.get(name=color_name)

                stock = Stock.objects.get(product_id=product_id, size=size, color=color)
                product_stock_quantity = stock.quantity

                if quantity_requested > product_stock_quantity:
                    messages.warning(
                        request,
                        f"Insufficient stock for {stock.product.name} "
                        f"(Size: {size_name}, Color: {color_name}). "
                    )
                    insufficient_stock = True

            except Size.DoesNotExist:
                messages.warning(request, f"Invalid size '{size_name}' for product {product_id}.")
                insufficient_stock = True
            except Color.DoesNotExist:
                messages.warning(request, f"Invalid color '{color_name}' for product {product_id}.")
                insufficient_stock = True
            except Stock.DoesNotExist:
                messages.warning(
                    request,
                    f"No stock available for {Product.objects.get(id=product_id).name} "
                    f"(Size: {size_name}, Color: {color_name})."
                )
                insufficient_stock = True
            except ValueError as e:
                messages.error(request, str(e))
                return redirect('cart_summary')

        if insufficient_stock:
            return redirect('cart_summary')  

        if request.user.is_authenticated:
            shipping_addresses = ShippingAddress.objects.filter(user=request.user)
            default_address = shipping_addresses.filter(is_default=True).first()

            if not default_address:
                messages.warning(request, "Please update your default address before proceeding to checkout.")
                return redirect('cart_summary') 

            profile, created = Profile.objects.get_or_create(user=request.user)
            return render(request, 'checkout.html', {
                'user': request.user,
                'shipping_addresses': shipping_addresses,
                'cart_products': cart_products,
                'cart_quantities': cart_quantities,
                'cart_total_price': cart_total,
                'profile': profile,
                'payment_methods': payment_methods,
            })
        else:
            messages.warning(request, "Please sign in to proceed with checkout")
            return redirect('login')
    else:
        messages.warning(request, "Access Denied")
        return redirect('home')

def place_order(request):
    if request.method == 'POST':
        cart = Cart(request)
        cart_products = cart.get_session_data()
        cart_total = cart.total_price()

        if not cart_products:
            messages.warning(request, "Your cart is empty. Add items before placing an order.")
            return redirect('cart_summary')

        if request.user.is_authenticated:
            shipping_address_id = request.POST.get('shipping_address')
            payment_method_id = request.POST.get('payment_method')

            shipping_address = get_object_or_404(ShippingAddress, id=shipping_address_id, user=request.user)
            payment_method = get_object_or_404(PaymentMethod, id=payment_method_id)

            formatted_shipping_address = (
                f"{shipping_address.address1}\n"
                f"{shipping_address.address2 or ''}\n"
                f"{shipping_address.district}, {shipping_address.city_province}"
            )

            with transaction.atomic():
                order = Order.objects.create(
                    user=request.user,
                    full_name=shipping_address.full_name,
                    email=request.user.email,
                    shipping_address=formatted_shipping_address,
                    amount_paid=cart_total,
                    payment_method=payment_method
                )

                for key, item in cart_products.items():
                    product_id = item['id']
                    quantity = item['quantity']
                    price = item['price']
                    attributes = item['attributes']

                    size_name = attributes.get('size')
                    color_name = attributes.get('color')

                    if not size_name:
                        messages.error(request, f"Size is required for {product_id}.")
                        return redirect('cart_summary')

                    try:
                        size = Size.objects.get(name=size_name)
                        color = Color.objects.get(name=color_name) if color_name else None

                        if color:
                            stock = Stock.objects.get(product_id=product_id, size=size, color=color)
                        else:
                            stock = Stock.objects.get(product_id=product_id, size=size, color__isnull=True)

                        if stock.quantity >= quantity:
                            # Create the OrderItem
                            attributes_str = f"Size: {size.name}" + (f", Color: {color.name}" if color else "")
                            OrderItem.objects.create(
                                order=order,
                                user=request.user,
                                product_id=product_id,
                                quantity=quantity,
                                price=price,
                                attributes=attributes_str
                            )

                            stock.quantity -= quantity
                            stock.save()
                        else:
                            messages.error(
                                request,
                                f"Insufficient stock for {product_id} (Size: {size.name}, Color: {color_name or 'None'})."
                            )
                            return redirect('cart_summary')

                    except (Size.DoesNotExist, Color.DoesNotExist, Stock.DoesNotExist):
                        messages.error(
                            request,
                            f"Stock not found for {product_id} with Size: {size_name} and Color: {color_name or 'None'}."
                        )
                        return redirect('cart_summary')

                # Clear the cart after placing the order
                cart.clear()

            messages.success(request, "Your order has been placed successfully.")
            return redirect('home')
        else:
            messages.warning(request, "Please log in to place an order.")
            return redirect('login')
    else:
        messages.warning(request, "Invalid request.")
        return redirect('checkout')




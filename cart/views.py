from django.shortcuts import render, get_object_or_404, redirect
from .cart import Cart
from store.models import Product
from django.http import JsonResponse
import json
from django.contrib import messages
    
def cart_summary(request):
    cart = Cart(request)
    cart_total_price = cart.total_price()
    cart_products = cart.get_session_data()  # Example structure: {'1-L-Green': {...}}
    # Fetch all product IDs from the cart
    product_ids = [value['id'] for key, value in cart_products.items()]

    # Fetch Product instances for these IDs
    products = Product.objects.filter(id__in=product_ids)

    return render(request, 'cart_summary.html', {
        "cart_total_price": cart_total_price,
        "cart_products": cart_products,
        "products": products,  # Pass Product model instances
    })


def cart_add(request):
    if request.method != 'POST' or request.POST.get('action') != 'post':
        return JsonResponse({"status": "failed", "message": "Invalid request method or action"}, status=400)
    
    try:
        cart = Cart(request)
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        product_price = float(request.POST.get('product_price'))
        attributes = json.loads(request.POST.get('attributes', '{}'))  
        product = get_object_or_404(Product, id=product_id)
        
        cart.add(product=product, quantity=product_qty, price=product_price, **attributes)
        
        messages.success(request, f"{product.name} has been successfully added to your cart!")
        cart_quantity = cart.__len__()

        return JsonResponse({"status": "success", "qty": cart_quantity})
    
    except (ValueError, Product.DoesNotExist, json.JSONDecodeError) as e:
        return JsonResponse({"status": "failed", "error": str(e)}, status=400)

def cart_update(request):
    if request.method != 'POST' or request.POST.get('action') != 'update':
        return JsonResponse({"status": "failed", "message": "Invalid request method or action"}, status=400)

    try:
        cart = Cart(request)
        updated_data = json.loads(request.POST.get('updated_data')) 
        cart.update(updated_data)
        return JsonResponse({"status": "success", "updated_data": updated_data})
    except (json.JSONDecodeError, TypeError, ValueError) as e:
        return JsonResponse({"status": "failed", "error": str(e)}, status=400)
                            
def cart_delete(request):
    if request.method != 'POST' or request.POST.get('action') != 'delete':
        return JsonResponse({"status": "failed", "message": "Invalid request method or action"}, status=400)

    try:
        cart = Cart(request)
        product_keys = json.loads(request.POST.get('product_keys', '[]'))
        cart.delete(product_keys)
        return JsonResponse({"status": "success", "deleted_products": product_keys})
    except (ValueError, Product.DoesNotExist) as e:
        return JsonResponse({"status": "failed", "error": str(e)}, status=400)
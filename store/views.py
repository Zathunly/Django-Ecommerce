from django.shortcuts import get_object_or_404, render, redirect
from rest_framework import generics
from django.contrib import messages
from django.http import JsonResponse
from .forms import RegisterForm
from django.contrib.auth import authenticate, login, logout 
from .models import Product,SubCategory, Category, Size, Color
from payment.models import Order
from .serializers import ProductSerializer
from .forms import LoginForm
from .products import filter_products, paginate_products
from django.core.files.storage import default_storage
from django.db.models import Sum


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            messages.success(request, 'Registration successful! You can now log in.')
            login(request, user)
            return redirect('initialize_profile')
        else:
            messages.error(request, 'Registration failed. Please try again.')
            return render(request, 'register.html', {'form': form})
    else:
        form = RegisterForm()  
        return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user) 
                messages.success(request, 'Login successful') 
                return redirect('home') 
            else:
                messages.error(request, 'Incorrect username or password, please try again.') 
                return redirect('login') 
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    if request.user.is_authenticated: 
        logout(request)
        request.session.flush()  
        messages.success(request, 'You have been logged out.')
    return redirect('home')

# def base_view(request):
#     try:
#         customize_theme = Theme.objects.get(name="Customize")
#     except Theme.DoesNotExist:
#         customize_theme = None  
#     return render(request, 'base.html', {'customize_theme': customize_theme})


def home_view(request):
    return render(request, 'home.html', {'user': request.user})

def products_view(request):
    selected_category = request.GET.get('category', '')
    selected_subcategory = request.GET.get('subcategory', '')
    price_range = request.GET.get('price_range', '') 
    page_number = request.GET.get('page', 1)

    products, subcategories = filter_products(
        selected_category=selected_category,
        selected_subcategory=selected_subcategory,
        price_range=price_range
    )

    paginated_products = paginate_products(products, page_number)
    categories = Category.objects.all()

    context = {
        'products': paginated_products,
        'categories': categories,
        'subcategories': subcategories,
        'selected_category': selected_category,
        'selected_subcategory': selected_subcategory,
        'price_range': price_range,  
    }
    return render(request, 'products.html', context)

def search_products(request):
    query = request.GET.get('q') 
    products = Product.objects.filter(name__icontains=query) if query else None 

    context = {
        'products': products,
        'query': query,
    }
    return render(request, 'products.html', context)

def product_detail_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    sizes = Size.objects.filter(stocks__product=product).distinct()
    colors = Color.objects.filter(stocks__product=product).distinct()

    selected_color = request.GET.get('color')  
    if selected_color:
        stock = product.stocks.filter(color__name=selected_color).first()  
        selected_image = stock.image.url if stock and stock.image else None
    else:
        stock = None
        selected_image = None

    return render(request, 'product-details.html', {
        'product': product,
        'sizes': sizes,
        'colors': colors,
        'selected_color': selected_color,  
        'default_image': product.image.url if product.image else None,  
        'selected_image': selected_image, 
    })

def about_us_view(request):
    return render(request, 'about-us.html', {})

def get_subcategories(request):
    category_id = request.GET.get('category_id')
    subcategories = SubCategory.objects.filter(category_id=category_id).values('id', 'name') if category_id else SubCategory.objects.none()
    return JsonResponse({'subcategories': list(subcategories)})



# Dashboard
def calculate_revenue():
    total_revenue = Order.objects.aggregate(total_revenue=Sum('amount_paid'))['total_revenue']
    return total_revenue or 0 

def dashboard_callback(request, context):
    total_orders_pending = Order.objects.filter(status='Pending').count()
    total_orders_cancel = Order.objects.filter(status='Cancel').count()
    total_orders_complete = Order.objects.filter(status='Complete').count()

    total_revenue = calculate_revenue()

    context.update({
        "total_orders_pending": total_orders_pending,
        "total_orders_cancel": total_orders_cancel,
        "total_orders_complete": total_orders_complete,
        "total_revenue": total_revenue,
    })
    return context

class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

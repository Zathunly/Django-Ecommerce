from django.core.paginator import Paginator
from .models import Product, SubCategory

def filter_products(selected_category=None, selected_subcategory=None, price_range=None):
    products = Product.objects.all()
    
    # Filter by Category and Subcategory
    if selected_category:
        products = products.filter(subcategory__category_id=selected_category)
        subcategories = SubCategory.objects.filter(category_id=selected_category)
        
        if selected_subcategory and subcategories.filter(id=selected_subcategory).exists():
            products = products.filter(subcategory_id=selected_subcategory)
        else:
            selected_subcategory = ''  
    else:
        subcategories = SubCategory.objects.all()

    # Filter by Price Range
    if price_range == "0-100000":
        products = products.filter(price__gte=0, price__lte=100000)
    elif price_range == "100000-500000":
        products = products.filter(price__gte=100000, price__lte=500000)
    elif price_range == "500000-1000000":
        products = products.filter(price__gte=500000, price__lte=1000000)
    elif price_range == "1000000-2000000":
        products = products.filter(price__gte=1000000, price__lte=2000000)
    elif price_range == "2000000+":
        products = products.filter(price__gte=2000000)

    return products, subcategories

def paginate_products(products, page_number, per_page=10):
    paginator = Paginator(products, per_page)
    return paginator.get_page(page_number)

from django.urls import resolve, reverse
from store.models import Product, Category, SubCategory  

def get_breadcrumbs(request):
    breadcrumbs = []
    url_name = resolve(request.path_info).url_name
    query_params = request.GET.dict()  
    resolved_kwargs = resolve(request.path_info).kwargs  

    category_id = query_params.get('category', '')
    subcategory_id = query_params.get('subcategory', '')
    product_id = resolved_kwargs.get('product_id')

    category_name = None
    subcategory_name = None
    product_name = None

    try:
        if category_id:
            category = Category.objects.get(id=category_id)
            category_name = category.name  
        if subcategory_id:
            subcategory = SubCategory.objects.get(id=subcategory_id)
            subcategory_name = subcategory.name 
        if product_id:
            product = Product.objects.get(id=product_id)
            product_name = product.name 
    except (Category.DoesNotExist, SubCategory.DoesNotExist, Product.DoesNotExist):
        pass  


    breadcrumb_mapping = {
        'home': lambda kwargs: [{'name': 'Home', 'url': reverse('home')}],
        'products-view': lambda kwargs: [
            {'name': 'Home', 'url': reverse('home')},
            {'name': 'Products', 'url': reverse('products-view')},
            *(
                [{'name': category_name, 'url': f"{reverse('products-view')}?category={category_id}"}]
                if category_name
                else []
            ),
            *(
                [{'name': subcategory_name, 'url': f"{reverse('products-view')}?category={category_id}&subcategory={subcategory_id}"}]
                if subcategory_name
                else []
            ),
        ],
        'product-details-view': lambda kwargs: [
            {'name': 'Home', 'url': reverse('home')},
            {'name': 'Products', 'url': reverse('products-view')},
            *(
                [{'name': category_name, 'url': f"{reverse('products-view')}?category={category_id}"}]
                if category_name
                else []
            ),
            *(
                [{'name': subcategory_name, 'url': f"{reverse('products-view')}?category={category_id}&subcategory={subcategory_id}"}]
                if subcategory_name
                else []
            ),
            *(
                [{'name': product_name, 'url': None}]
                if product_name
                else []
            ),
        ],
        'about-us': lambda kwargs: [
            {'name': 'Home', 'url': reverse('home')},
            {'name': 'About Us', 'url': reverse('about-us')},
        ],
    }

    if url_name in breadcrumb_mapping:
        breadcrumbs = breadcrumb_mapping[url_name](resolved_kwargs)

    return breadcrumbs

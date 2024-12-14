from django import template
from store.models import Stock

register = template.Library()

@register.filter
def get_stock_image(product):
    if not isinstance(product, dict):
        raise ValueError("Expected a dictionary, got %s" % type(product).__name__)

    product_id = product.get('id')
    color = product['attributes'].get('color')
    size = product['attributes'].get('size')

    # Query the Stock model to find a matching entry
    stock = Stock.objects.filter(product_id=product_id, color__name=color, size__name=size).first()
    return stock.image.url if stock and stock.image else None

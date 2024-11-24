from django import template

register = template.Library()

@register.filter(name='multiply')
def multiply(value, arg):
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return ''  
    
@register.filter
def format_price(value):
    try:
        value = float(value)
        if value.is_integer():
            value = int(value)
            return f"{value:,.0f}".replace(",", ".")  
        else:
            return f"{value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except (ValueError, TypeError):
        return value  

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

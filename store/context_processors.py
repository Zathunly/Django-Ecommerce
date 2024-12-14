from .breadcrumbs import get_breadcrumbs

def breadcrumbs_context(request):
    """
    Add breadcrumbs to the template context dynamically.
    """
    return {'breadcrumbs': get_breadcrumbs(request)}

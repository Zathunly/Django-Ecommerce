from django.conf import settings

class DomainRoutingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        host = request.get_host().split(':')[0]
        print(f"Host received: {host}")  # Debugging log
        if host == 'admin.localhost':
            request.urlconf = 'ecom.urls_admin'  # Use admin URL configuration
        elif host == 'localhost':
            request.urlconf = 'ecom.urls'  # Use regular URL configuration
        else:
            from django.http import HttpResponseBadRequest
            return HttpResponseBadRequest(f"Invalid Host: {host}")
        return self.get_response(request)

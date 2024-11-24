# from admin_interface.models import Theme

# def customize_theme_processor(request):
#     try:
#         customize_theme = Theme.objects.get(name="Customize")
#     except Theme.DoesNotExist:
#         customize_theme = None
#     return {'customize_theme': customize_theme}
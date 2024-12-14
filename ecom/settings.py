from pathlib import Path
import os
import environ 
from django.templatetags.static import static
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.conf import settings  # Import to ensure 'settings' is defined


env = environ.Env()

ALLOWED_HOSTS = ['localhost', 'admin.localhost']

BASE_DIR = Path(__file__).resolve().parent.parent

# Media settings
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Reading .env file
environ.Env.read_env(os.path.join(BASE_DIR, 'django/.env'))

environ.Env.read_env(os.path.join(BASE_DIR, '.env'))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-2y-y%&00wn8s#jri%7nc_#^s^ie)m5l5f&1wy@4wfpdp3yi))d'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Application definition

INSTALLED_APPS = [
    'unfold',
    "unfold.contrib.filters",  
    "unfold.contrib.forms",
    "unfold.contrib.import_export",
    'store',
    'cart',
    'payment',
    'userprofile',
    'pageview',
    'django.conf',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'import_export',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'ecom.middleware.DomainRoutingMiddleware',
]

ROOT_URLCONF = 'ecom.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'cart.context_processors.cart',
                'store.context_processors.breadcrumbs_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'ecom.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': env('DATABASE_NAME'),
        'USER': env('DATABASE_USER'),
        'PASSWORD': env('DATABASE_PASSWORD'),
        'HOST': env('DATABASE_HOST', default='localhost'),
        'PORT': env('DATABASE_PORT', default='3306'),
        'OPTIONS': {
            'init_command': 'ALTER DATABASE python CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci',
            'charset'   : 'utf8mb4',
            },
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

USE_THOUSAND_SEPARATOR = True

THOUSAND_SEPARATOR = '.'

USE_L10N = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

X_FRAME_OPTIONS = 'SAMEORIGIN'

LOGIN_REDIRECT_URL = 'home'        

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

ADMIN_SEARCH_MAX_RESULTS = 100

def permission_callback(request):
    return request.user.has_perm("store.change_model")

UNFOLD = {
    "SITE_HEADER": "Its Lit",
    "SITE_URL": "/",
    "SITE_LOGO": {
        "light": lambda request: f"{settings.MEDIA_URL}logo/MTPC_Logo.png",  # light mode
        "dark": lambda request: f"{settings.MEDIA_URL}logo/MTPC_Logo.png",   # dark mode
    },
    "DASHBOARD_CALLBACK": "store.views.dashboard_callback",
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": True,
        "navigation": [
            {
                "title": _("Navigation"),
                "separator": True,  # Top border
                "items": [
                    {
                        "title": _("Dashboard"),
                        "icon": "dashboard",  # Supported icon set
                        "link": reverse_lazy("admin:index"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                ],
            },
            {
                "title": _("Authentications"),
                "separator": True,  # Top border
                "items": [
                    {
                        "title": _("Users"),
                        "icon": "person", 
                        "link": reverse_lazy("admin:auth_user_changelist"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("Groups"),
                        "icon": "people",  
                        "link": reverse_lazy("admin:auth_group_changelist"),
                        "permission": lambda request: request.user.is_superuser,
                    }
                ]
            },
            {
                "title": _("Page Customization"),
                "separator": True,  
                "items": [
                    {
                        "title": _("HomeBanner"),
                        "icon": "inbox_customize",  
                        "link": reverse_lazy("admin:pageview_homebanner_changelist"),
                        "permission": lambda request: request.user.is_superuser,
                    }
                ]
            },
            {
                "title": _("Store"),
                "separator": True,  # Top border
                "items": [
                    {
                        "title": _("Products"),
                        "icon": "apparel",
                        "link": reverse_lazy("admin:store_product_changelist"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("Sale Collection Manage"),
                        "icon": "keyboard_double_arrow_down",
                        "link": reverse_lazy("admin:store_salecollection_changelist"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("Stocks"),
                        "icon": "inventory_2",  
                        "link": reverse_lazy("admin:store_stock_changelist"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("Category"),
                        "icon": "stacks", 
                        "link": reverse_lazy("admin:store_category_changelist"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("Sub-Category"),
                        "icon": "category", 
                        "link": reverse_lazy("admin:store_subcategory_changelist"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("Color"),
                        "icon": "edit_attributes", 
                        "link": reverse_lazy("admin:store_color_changelist"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("Size"),
                        "icon": "palette", 
                        "link": reverse_lazy("admin:store_size_changelist"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                ]
            },
            {
                "title": _("Payment"),
                "separator": True,  
                "items": [
                    {
                        "title": _("Orders"),
                        "icon": "orders",
                        "link": reverse_lazy("admin:payment_order_changelist"),
                        "permission": lambda request: request.user.is_superuser
                    },
                    {
                        "title": _("Payment Methods"),
                        "icon": "payment",
                        "link": reverse_lazy("admin:payment_paymentmethod_changelist"),
                        "permission": lambda request: request.user.is_superuser
                    },
                    {
                        "title": _("Shipping Addresses"),
                        "icon": "local_shipping",
                        "link": reverse_lazy("admin:payment_shippingaddress_changelist"),
                        "permission": lambda request: request.user.is_superuser
                    },
                ]
            }
            
        ],
    },
    "TABS": [
        {
            "models": [
                "store.salecollection",
            ],
            "items": [
                {
                    "title": _("Sale Pack"),
                    "link": reverse_lazy("admin:store_sale_changelist"),
                    "permission": "store.views.permission_callback",
                },
            ],
        },
    ],
}

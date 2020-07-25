from django.conf import settings

# Site Settings
SITE_NAME = getattr(settings, "SITE_NAME", "JadedGamer")
SITE_DESC = getattr(settings, "SITE_DESC", "Just another news site")
SITE_URL = getattr(settings, "SITE_URL", "http://localhost")
SITE_AUTHOR = getattr(settings, "SITE_AUTHOR", "Tyler Rilling")
PAGINATE = 25

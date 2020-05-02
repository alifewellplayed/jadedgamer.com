from django.urls import include, path
from django.contrib.sitemaps.views import sitemap
from django.contrib import admin
from django.conf import settings
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from coreExtend import views as core_views
from coreExtend import settings as site_settings

admin.autodiscover()
admin.site.site_header = site_settings.SITE_NAME

urlpatterns = [
    #admin
    path('admin96/', admin.site.urls),

    #API
    path('v2/auth/', include('rest_framework.urls')),
    path('v2/', include('api.urls')),

    # Static
    path('404/', TemplateView.as_view(template_name="404.html"), name="page_404"),
    path('500/', TemplateView.as_view(template_name="500.html"), name="page_500"),

    #Handle redirects
    path('r/', include('redirect.urls')),


    # django-push
    path('subscriber/', include('django_push.subscriber.urls')),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

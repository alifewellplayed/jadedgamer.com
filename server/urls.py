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
    #url(r'^api/docs/', include('rest_framework_swagger.urls')),
    path('api/v2/auth/', include('rest_framework.urls')),
    #path('api/v2/', include('api.urls')),

    # Static
    path('404/', TemplateView.as_view(template_name="404.html"), name="404_page"),
    path('500/', TemplateView.as_view(template_name="500.html"), name="500_page"),
    path('robots.txt', TemplateView.as_view(template_name="robots.txt", content_type='text/plain')),
    path('humans.txt', TemplateView.as_view(template_name="humans.txt", content_type='text/plain')),
    path('manifest.json', TemplateView.as_view(template_name="manifest.json", content_type='application/json')),

    # Apps
    path('r/', include('redirect.urls')),
    path('', include('coreExtend.urls')),
    path('', include('aggregator.urls')),

    #Sitemap
    #url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),

    # django-push
    path('subscriber/', include('django_push.subscriber.urls')),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

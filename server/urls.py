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
    path('404/', TemplateView.as_view(template_name="404.html"), name="page_404"),
    path('500/', TemplateView.as_view(template_name="500.html"), name="page_500"),
    path('robots.txt', TemplateView.as_view(template_name="robots.txt", content_type='text/plain')),
    path('humans.txt', TemplateView.as_view(template_name="humans.txt", content_type='text/plain')),
    path('manifest.json', TemplateView.as_view(template_name="manifest.json", content_type='application/json')),

    #Static Page
    path('about/', TemplateView.as_view(template_name="static/about.html"), name='page_about'),
    path('terms/', TemplateView.as_view(template_name="static/terms.html"), name='page_terms'),
    path('privacy/', TemplateView.as_view(template_name="static/privacy.html"), name='page_privacy'),
    path('tour/', TemplateView.as_view(template_name="static/tour.html"), name='page_tour'),

    # Apps
    path('r/', include('redirect.urls')),
    path('news/', include('news.urls')),
    path('', include('coreExtend.urls')),
    path('', include('aggregator.urls')),

    #Sitemap
    #url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),

    # django-push
    path('subscriber/', include('django_push.subscriber.urls')),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

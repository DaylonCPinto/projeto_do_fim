# Em core/urls.py

from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

urlpatterns = [
    # URLs específicas DEVEM VIR PRIMEIRO
    path('django-admin/', admin.site.urls),
    path('admin/', include(wagtailadmin_urls)),
    path('documents/', include(wagtaildocs_urls)),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('accounts.urls')),

    # A URL "catch-all" do Wagtail DEVE SER A ÚLTIMA
    path('', include(wagtail_urls)),
]

# Esta parte não muda, continua no final
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
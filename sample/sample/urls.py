from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
    url(r'^', include('demo.urls', namespace='demo')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^renderer/', include('renderer.urls', namespace='renderer')),
]

if settings.AWS_SECRET_ACCESS_KEY is not None:
    urlpatterns = urlpatterns + static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )

admin.site.site_header = 'Image Renderer Sample'

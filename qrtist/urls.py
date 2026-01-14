from django.contrib import admin
from django.urls import include, path
from django.views.static import serve
from generator.views import api_docs_view, home_view, qr_history_view, stats_view
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    
    # Template URLs
    path('', home_view, name='home'),
    path('history/', qr_history_view, name='history'),
    path('stats/', stats_view, name='stats'),
    path('docs/', api_docs_view, name='api_docs'),

]

# Serve media files in both development and production
if settings.DEBUG:
    # Development: use static() helper
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    # Production: use serve() view with proper restrictions
    urlpatterns += [
        path('media/<path:path>', serve, {
            'document_root': settings.MEDIA_ROOT,
            'show_indexes': False,
        }),
    ]
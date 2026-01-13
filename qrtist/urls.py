from django.contrib import admin
from django.urls import include, path

from generator.views import api_docs_view, home_view, qr_history_view, stats_view



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    
    # Template URLs
    path('', home_view, name='home'),
    path('history/', qr_history_view, name='history'),
    path('stats/', stats_view, name='stats'),
    path('docs/', api_docs_view, name='api_docs'),

]

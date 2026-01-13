from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView




urlpatterns = [
    path('qr/', include('generator.urls')),
    
    # API Schema and Docs
    path('schema/', SpectacularAPIView.as_view(), name='api_schema'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='api_schema'), name='api_swagger_ui'),
    path('redoc/', SpectacularRedocView.as_view(url_name='api_schema'), name='api_redoc'),
]

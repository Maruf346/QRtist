from django.urls import path, include




urlpatterns = [
    path('generator/', include('generator.urls')),
]

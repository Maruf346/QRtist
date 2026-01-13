from django.contrib import admin
from django.urls import include, path

from generator.views import home_view



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('', home_view, name='home'),

]

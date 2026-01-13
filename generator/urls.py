from django.urls import path
from .views import *

urlpatterns = [
    # Template URLs
    path('history/', qr_history_view, name='history'),
    path('stats/', stats_view, name='stats'),
    path('docs/', api_docs_view, name='api_docs'),
    
    # QR Download
    path('download/<uuid:qr_id>/', download_qr_view, name='download_qr'),
    
    # base URLs
    path('text/', TextQRView.as_view(), name='api_qr_text'),
    path('url/', URLQRView.as_view(), name='api_qr_url'),
    path('pdf/', PDFQRView.as_view(), name='api_qr_pdf'),
    path('image/', ImageQRView.as_view(), name='api_qr_image'),

    # QR Code Management API
    path('list', QRCodeListView.as_view(), name='api_qr_list'),
    path('detail/<uuid:qr_id>/', QRCodeDetailView.as_view(), name='api_qr_detail'),
]
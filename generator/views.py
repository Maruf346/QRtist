from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.generics import ListAPIView
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
import base64
from io import BytesIO
import json
from django.utils import timezone
from .models import QRCode
from .serializers import *
from .utils import save_qr_to_model, get_qr_as_base64, generate_download_response
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


class BaseQRView(APIView):
    """Base view for QR generation"""
    
    def create_response(self, qr_instance):
        """Create API response from QRCode instance"""
        qr_base64 = get_qr_as_base64(qr_instance)
        
        return Response({
            'success': True,
            'qr_id': str(qr_instance.id),
            'qr_code': f"data:image/png;base64,{qr_base64}" if qr_base64 else None,
            'content': qr_instance.get_content_preview(),
            'download_url': f"/download/{qr_instance.id}/",
            'created_at': qr_instance.created_at.isoformat(),
        })

@method_decorator(csrf_exempt, name='dispatch')
class TextQRView(BaseQRView):
    serializer_class = TextQRSerializer
    def post(self, request):
        serializer = TextQRSerializer(data=request.data)
        if serializer.is_valid():
            qr_instance = save_qr_to_model(
                content_type='text',
                original_content=serializer.validated_data['text'],
                file_obj=None,
                size=serializer.validated_data.get('size', 10),
                fill_color=serializer.validated_data.get('fill_color', '#000000'),
                back_color=serializer.validated_data.get('back_color', '#FFFFFF'),
                request=request
            )
            return self.create_response(qr_instance)
        
        return Response({
            'success': False,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(csrf_exempt, name='dispatch')
class URLQRView(BaseQRView):
    serializer_class = URLQRSerializer
    def post(self, request):
        serializer = URLQRSerializer(data=request.data)
        if serializer.is_valid():
            qr_instance = save_qr_to_model(
                content_type='url',
                original_content=serializer.validated_data['url'],
                file_obj=None,
                size=serializer.validated_data.get('size', 10),
                fill_color=serializer.validated_data.get('fill_color', '#000000'),
                back_color=serializer.validated_data.get('back_color', '#FFFFFF'),
                request=request
            )
            return self.create_response(qr_instance)
        
        return Response({
            'success': False,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(csrf_exempt, name='dispatch')
class PDFQRView(BaseQRView):
    serializer_class = PDFQRSerializer
    parser_classes = [MultiPartParser, FormParser]
    
    def post(self, request):
        serializer = PDFQRSerializer(data=request.data)
        if serializer.is_valid():
            qr_instance = save_qr_to_model(
                content_type='pdf',
                original_content='',
                file_obj=serializer.validated_data['file'],
                size=serializer.validated_data.get('size', 10),
                fill_color='#000000',
                back_color='#FFFFFF',
                request=request
            )
            return self.create_response(qr_instance)
        
        return Response({
            'success': False,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(csrf_exempt, name='dispatch')
class ImageQRView(BaseQRView):
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = ImageQRSerializer
    
    def post(self, request):
        serializer = ImageQRSerializer(data=request.data)
        if serializer.is_valid():
            qr_instance = save_qr_to_model(
                content_type='image',
                original_content='',
                file_obj=serializer.validated_data['file'],
                size=serializer.validated_data.get('size', 10),
                fill_color='#000000',
                back_color='#FFFFFF',
                request=request
            )
            return self.create_response(qr_instance)
        
        return Response({
            'success': False,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class QRCodeListView(ListAPIView):
    """List all QR codes (for admin/stats)"""
    queryset = QRCode.objects.all().order_by('-created_at')
    serializer_class = QRCodeSerializer
    pagination_class = None  # Or use PageNumberPagination
    
    def get_queryset(self):
        # Optional: Limit to last 100 entries
        return QRCode.objects.all().order_by('-created_at')[:100]

class QRCodeDetailView(APIView):
    """Get details of a specific QR code"""
    
    def get(self, request, qr_id):
        try:
            qr_instance = QRCode.objects.get(id=qr_id)
            serializer = QRCodeSerializer(qr_instance)
            return Response(serializer.data)
        except QRCode.DoesNotExist:
            return Response({
                'success': False,
                'error': 'QR code not found'
            }, status=status.HTTP_404_NOT_FOUND)

# Template Views
def home_view(request):
    """Render the main page"""
    # Get recent QR codes for display
    recent_qrs = QRCode.objects.all().order_by('-created_at')[:5]
    
    # Get statistics
    total_qrs = QRCode.objects.count()
    stats = {
        'total': total_qrs,
        'text': QRCode.objects.filter(content_type='text').count(),
        'url': QRCode.objects.filter(content_type='url').count(),
        'pdf': QRCode.objects.filter(content_type='pdf').count(),
        'image': QRCode.objects.filter(content_type='image').count(),
    }
    
    return render(request, 'home.html', {
        'recent_qrs': recent_qrs,
        'stats': stats,
    })

def download_qr_view(request, qr_id):
    """Download QR code as PNG file"""
    qr_instance = get_object_or_404(QRCode, id=qr_id)
    
    response = generate_download_response(qr_instance)
    if response:
        return response
    
    return JsonResponse({'error': 'QR code not found'}, status=404)

def qr_history_view(request):
    """View QR code history"""
    qr_codes = QRCode.objects.all().order_by('-created_at')[:50]
    return render(request, 'history.html', {'qr_codes': qr_codes})

def api_docs_view(request):
    """Render API documentation page"""
    return render(request, 'api_docs.html')

def stats_view(request):
    """View statistics page"""
    stats = {
        'total_qrs': QRCode.objects.count(),
        'total_downloads': sum(qr.download_count for qr in QRCode.objects.all()),
        'by_type': {
            'text': QRCode.objects.filter(content_type='text').count(),
            'url': QRCode.objects.filter(content_type='url').count(),
            'pdf': QRCode.objects.filter(content_type='pdf').count(),
            'image': QRCode.objects.filter(content_type='image').count(),
        },
        'today_count': QRCode.objects.filter(
            created_at__date=timezone.now().date()
        ).count(),
        'most_downloaded': QRCode.objects.order_by('-download_count').first(),
        'recent_activity': QRCode.objects.order_by('-last_downloaded').filter(
            last_downloaded__isnull=False
        )[:10],
    }
    return render(request, 'stats.html', {'stats': stats})
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
from io import BytesIO
import base64
from PIL import Image
import os
from django.core.files.base import ContentFile
from .models import QRCode
import uuid
from django.http import HttpResponse


def hex_to_rgb(hex_color):
    """Convert hex color to RGB tuple"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def generate_qr_code(data, size=10, fill_color="#000000", back_color="#FFFFFF"):
    """
    Generate QR code from given data
    Returns: BytesIO object containing PNG image
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=size,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    # Convert hex colors to RGB
    fill_rgb = hex_to_rgb(fill_color)
    back_rgb = hex_to_rgb(back_color)
    
    img = qr.make_image(
        fill_color=fill_rgb,
        back_color=back_rgb,
        image_factory=StyledPilImage,
        module_drawer=RoundedModuleDrawer()
    )
    
    # Convert to BytesIO
    img_io = BytesIO()
    img.save(img_io, format='PNG', quality=100)
    img_io.seek(0)
    
    return img_io

def save_qr_to_model(content_type, original_content, file_obj, size, fill_color, back_color, request):
    """
    Generate QR code and save to database
    Returns: QRCode instance
    """
    # Prepare data for QR code
    if content_type in ['text', 'url']:
        qr_data = original_content
    else:
        # For files, we'll create a placeholder text with filename
        qr_data = f"File: {file_obj.name}"
    
    # Generate QR code image
    img_io = generate_qr_code(
        qr_data,
        size=size,
        fill_color=fill_color,
        back_color=back_color
    )
    
    # Create QRCode instance
    qr_instance = QRCode(
        content_type=content_type,
        size=size,
        fill_color=fill_color,
        back_color=back_color,
    )
    
    # Set content based on type
    if content_type in ['text', 'url']:
        qr_instance.original_content = original_content
    elif file_obj:
        qr_instance.file.save(file_obj.name, file_obj)
    
    # Save QR image
    qr_filename = f"qr_{uuid.uuid4().hex}.png"
    qr_instance.qr_image.save(qr_filename, ContentFile(img_io.getvalue()))
    
    # Optional: Save request metadata
    if request:
        qr_instance.ip_address = get_client_ip(request)
        qr_instance.user_agent = request.META.get('HTTP_USER_AGENT', '')
    
    qr_instance.save()
    
    return qr_instance

def get_client_ip(request):
    """Get client IP address from request"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_qr_as_base64(qr_instance):
    """Get QR code image as base64 string"""
    if qr_instance.qr_image:
        img_io = BytesIO()
        img = Image.open(qr_instance.qr_image.path)
        img.save(img_io, format='PNG')
        img_io.seek(0)
        return base64.b64encode(img_io.getvalue()).decode('utf-8')
    return None

def generate_download_response(qr_instance):
    """Generate download response for QR code"""
    if qr_instance.qr_image:
        qr_instance.increment_download()
        
        with open(qr_instance.qr_image.path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='image/png')
            response['Content-Disposition'] = f'attachment; filename="qr_{qr_instance.id}.png"'
            return response
    return None
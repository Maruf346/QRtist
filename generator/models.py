from django.db import models
import os
import uuid
from django.utils import timezone


def qr_code_upload_path(instance, filename):
    """Generate upload path for QR code images"""
    # Generate unique filename
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4().hex}.{ext}"
    return os.path.join('qr_codes', filename)

def upload_file_path(instance, filename):
    """Generate upload path for source files"""
    # Generate unique filename
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4().hex}.{ext}"
    return os.path.join('uploads', instance.content_type, filename)

class QRCode(models.Model):
    CONTENT_TYPE_CHOICES = [
        ('text', 'Text'),
        ('url', 'URL'),
        ('pdf', 'PDF'),
        ('image', 'Image'),
    ]
    
    # Basic information
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    content_type = models.CharField(max_length=10, choices=CONTENT_TYPE_CHOICES)
    original_content = models.TextField(blank=True)  # For text/URL
    file = models.FileField(upload_to=upload_file_path, null=True, blank=True)  # For PDF/Image
    
    # QR Code image
    qr_image = models.ImageField(upload_to=qr_code_upload_path)
    
    # Customization options
    size = models.PositiveSmallIntegerField(default=10)  # QR box size
    fill_color = models.CharField(max_length=7, default='#000000')  # Hex color
    back_color = models.CharField(max_length=7, default='#FFFFFF')  # Hex color
    
    # Metadata
    created_at = models.DateTimeField(default=timezone.now)
    ip_address = models.GenericIPAddressField(null=True, blank=True)  # Track IP (optional)
    user_agent = models.TextField(blank=True)  # Track browser info (optional)
    
    # Analytics
    download_count = models.PositiveIntegerField(default=0)
    last_downloaded = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['created_at']),
            models.Index(fields=['content_type']),
        ]
    
    def __str__(self):
        return f"{self.content_type.upper()} QR - {self.created_at.strftime('%Y-%m-%d %H:%M')}"
    
    def get_content_preview(self):
        """Get a preview of the content"""
        if self.content_type in ['text', 'url']:
            return self.original_content[:50] + ('...' if len(self.original_content) > 50 else '')
        elif self.file:
            return self.file.name
        return "No content"
    
    def get_file_size(self):
        """Get file size in human readable format"""
        if self.file:
            size_bytes = self.file.size
            for unit in ['B', 'KB', 'MB', 'GB']:
                if size_bytes < 1024.0:
                    return f"{size_bytes:.1f} {unit}"
                size_bytes /= 1024.0
        return None
    
    def increment_download(self):
        """Increment download counter"""
        self.download_count += 1
        self.last_downloaded = timezone.now()
        self.save(update_fields=['download_count', 'last_downloaded'])
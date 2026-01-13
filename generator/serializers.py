from rest_framework import serializers
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError as DjangoValidationError
from .models import QRCode


class TextQRSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=2000, required=True)
    size = serializers.IntegerField(min_value=5, max_value=20, default=10)
    fill_color = serializers.CharField(max_length=7, default="#000000")
    back_color = serializers.CharField(max_length=7, default="#FFFFFF")

class URLQRSerializer(serializers.Serializer):
    url = serializers.CharField(max_length=500, required=True)
    size = serializers.IntegerField(min_value=5, max_value=20, default=10)
    fill_color = serializers.CharField(max_length=7, default="#000000")
    back_color = serializers.CharField(max_length=7, default="#FFFFFF")
    
    def validate_url(self, value):
        validator = URLValidator()
        try:
            validator(value)  # This validates the URL
        except DjangoValidationError:
            raise serializers.ValidationError("Please enter a valid URL")
        
        # Ensure URL has protocol
        if not value.startswith(('http://', 'https://')):
            value = 'https://' + value
        return value

class FileQRSerializer(serializers.Serializer):
    file = serializers.FileField(required=True)
    size = serializers.IntegerField(min_value=5, max_value=20, default=10)
    
    def validate_file(self, value):
        # Limit file size to 10MB
        max_size = 10 * 1024 * 1024
        if value.size > max_size:
            raise serializers.ValidationError("File size should not exceed 10MB")
        return value

class PDFQRSerializer(FileQRSerializer):
    def validate_file(self, value):
        super().validate_file(value)
        if not value.name.lower().endswith('.pdf'):
            raise serializers.ValidationError("Only PDF files are allowed")
        return value

class ImageQRSerializer(FileQRSerializer):
    def validate_file(self, value):
        super().validate_file(value)
        allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']
        if not any(value.name.lower().endswith(ext) for ext in allowed_extensions):
            raise serializers.ValidationError(
                "Only image files (JPG, PNG, GIF, BMP, WEBP) are allowed"
            )
        return value

# Model Serializer
class QRCodeSerializer(serializers.ModelSerializer):
    content_preview = serializers.SerializerMethodField()
    file_size = serializers.SerializerMethodField()
    qr_image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = QRCode
        fields = [
            'id',
            'content_type',
            'content_preview',
            'file_size',
            'size',
            'fill_color',
            'back_color',
            'created_at',
            'download_count',
            'qr_image_url',
        ]
        read_only_fields = ['id', 'created_at', 'download_count']
    
    def get_content_preview(self, obj):
        return obj.get_content_preview()
    
    def get_file_size(self, obj):
        return obj.get_file_size()
    
    def get_qr_image_url(self, obj):
        if obj.qr_image:
            return obj.qr_image.url
        return None
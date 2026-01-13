from django.contrib import admin
from .models import QRCode

@admin.register(QRCode)
class QRCodeAdmin(admin.ModelAdmin):
    list_display = ('id', 'content_type', 'get_content_preview', 'size', 
                   'download_count', 'created_at', 'last_downloaded')
    list_filter = ('content_type', 'created_at')
    search_fields = ('original_content', 'file')
    readonly_fields = ('id', 'created_at', 'download_count', 'last_downloaded',
                      'ip_address', 'user_agent')
    fieldsets = (
        ('Basic Information', {
            'fields': ('id', 'content_type', 'original_content', 'file')
        }),
        ('QR Code', {
            'fields': ('qr_image', 'size', 'fill_color', 'back_color')
        }),
        ('Metadata', {
            'fields': ('created_at', 'download_count', 'last_downloaded')
        }),
        ('Technical Info', {
            'fields': ('ip_address', 'user_agent'),
            'classes': ('collapse',)
        }),
    )
    
    def get_content_preview(self, obj):
        return obj.get_content_preview()
    get_content_preview.short_description = 'Content'
    
    def has_add_permission(self, request):
        return False  # Disable adding via admin (only via API)
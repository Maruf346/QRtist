from django.db import models

class QRCodeModel(models.Model):
    data = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"QRCodeModel(id={self.id}, data={self.data})"
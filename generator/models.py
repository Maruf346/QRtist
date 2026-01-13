from django.db import models

<<<<<<< HEAD
class QRCodeModel(models.Model):
    data = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"QRCodeModel(id={self.id}, data={self.data})"
=======
# Create your models here.
>>>>>>> 4196f4e3fdbed7570f1340223b56edb87376e705

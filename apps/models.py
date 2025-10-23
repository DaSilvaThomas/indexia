from django.db import models
import os

class UploadedFile(models.Model):
    file = models.FileField(upload_to='')
    filename = models.CharField(max_length=255, blank=True)
    extension = models.CharField(max_length=10, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    text_content = models.TextField(blank=True, null=True)
    cleaned_text = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        """Remplit automatiquement filename et extension"""
        if self.file:
            base_name = os.path.basename(self.file.name)
            name, ext = os.path.splitext(base_name)
            self.filename = name
            self.extension = ext[1:].lower() if ext else ''
        super().save(*args, **kwargs)

    def __str__(self):
        return self.filename or os.path.basename(self.file.name)
    
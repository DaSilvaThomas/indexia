from django.db import models

class UploadedFile(models.Model):
    file = models.FileField(upload_to='')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    text_content = models.TextField(blank=True, null=True)
    cleaned_text = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.file.name
    
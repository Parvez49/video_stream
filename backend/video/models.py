from django.db import models

class Video(models.Model):
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    # Original video file
    original_video = models.FileField(upload_to='videos/originals/')

    # Processed videos in different resolutions
    low_resolution_video = models.FileField(upload_to='videos/low/', blank=True, null=True)
    medium_resolution_video = models.FileField(upload_to='videos/medium/', blank=True, null=True)
    high_resolution_video = models.FileField(upload_to='videos/high/', blank=True, null=True)

    def __str__(self):
        return self.title

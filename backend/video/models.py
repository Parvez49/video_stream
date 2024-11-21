from django.db import models

class Video(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    original_video = models.FileField(upload_to="videos/originals/")
    hls_master_playlist = models.FileField(upload_to="videos/hls/", blank=True, null=True)
    hls_output_dir = models.CharField(max_length=255, blank=True, null=True)  # Path to HLS output folder

    def __str__(self):
        return self.title

from celery import shared_task
from django.conf import settings
from .models import Video
import os
import ffmpeg

@shared_task
def process_video_resolutions(video_id):
    try:
        video = Video.objects.get(id=video_id)
        original_path = video.original_video.path

        # Define output paths for resolutions within MEDIA_ROOT
        low_path = os.path.join(settings.MEDIA_ROOT, 'videos/low', f'low_{video.title}.mp4')
        medium_path = os.path.join(settings.MEDIA_ROOT, 'videos/medium', f'medium_{video.title}.mp4')
        high_path = os.path.join(settings.MEDIA_ROOT, 'videos/high', f'high_{video.title}.mp4')

        # Ensure output directories exist
        os.makedirs(os.path.dirname(low_path), exist_ok=True)
        os.makedirs(os.path.dirname(medium_path), exist_ok=True)
        os.makedirs(os.path.dirname(high_path), exist_ok=True)

        # Transcode to different resolutions
        ffmpeg.input(original_path).output(low_path, vf='scale=640:480').run()
        ffmpeg.input(original_path).output(medium_path, vf='scale=1280:720').run()
        ffmpeg.input(original_path).output(high_path, vf='scale=1920:1080').run()

        # Save the new file paths to the Video model
        video.low_resolution_video.name = os.path.relpath(low_path, start=settings.MEDIA_ROOT)
        video.medium_resolution_video.name = os.path.relpath(medium_path, start=settings.MEDIA_ROOT)
        video.high_resolution_video.name = os.path.relpath(high_path, start=settings.MEDIA_ROOT)
        video.save()

        return f"Video {video_id} processed and saved successfully."
    except Video.DoesNotExist:
        return f"Video {video_id} not found."
    except Exception as e:
        return str(e)

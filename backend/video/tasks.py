from celery import shared_task
from .models import Video
import os
import ffmpeg

@shared_task
def process_video_resolutions(video_id):
    try:
        video = Video.objects.get(id=video_id)
        original_path = video.original_video.path

        # Define output paths for resolutions
        base_dir = os.path.dirname(original_path)
        low_path = os.path.join(base_dir, f'low_{os.path.basename(original_path)}')
        medium_path = os.path.join(base_dir, f'medium_{os.path.basename(original_path)}')
        high_path = os.path.join(base_dir, f'high_{os.path.basename(original_path)}')

        # Transcode to low resolution (480p)
        ffmpeg.input(original_path).output(low_path, vf='scale=640:480').run()

        # Transcode to medium resolution (720p)
        ffmpeg.input(original_path).output(medium_path, vf='scale=1280:720').run()

        # Transcode to high resolution (1080p)
        ffmpeg.input(original_path).output(high_path, vf='scale=1920:1080').run()

        # Save paths to the model
        video.low_resolution_video.name = os.path.relpath(low_path, start='media/')
        video.medium_resolution_video.name = os.path.relpath(medium_path, start='media/')
        video.high_resolution_video.name = os.path.relpath(high_path, start='media/')
        video.save()

        return f"Video {video_id} processed successfully."
    except Video.DoesNotExist:
        return f"Video {video_id} does not exist."
    except ffmpeg.Error as e:
        return f"FFmpeg error: {e.stderr.decode()}"
    except Exception as e:
        return str(e)

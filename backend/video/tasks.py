from celery import shared_task
from django.conf import settings
from .models import Video
import os
import subprocess
import ffmpeg


@shared_task
def process_video_to_hls(video_id):
    video = Video.objects.get(id=video_id)

    input_path = video.original_video.path
    output_dir = os.path.join(settings.MEDIA_ROOT, "videos", "hls", f"video_{video_id}")
    os.makedirs(output_dir, exist_ok=True)

    hls_command = [
        "ffmpeg",
        "-i", input_path,
        "-preset", "veryfast",
        "-g", "48",
        "-sc_threshold", "0",
        "-map", "0:v:0", "-map", "0:a:0", "-s:v:0", "426x240", "-b:v:0", "400k",
        "-maxrate:v:0", "856k", "-bufsize:v:0", "1200k",
        "-map", "0:v:0", "-map", "0:a:0", "-s:v:1", "640x360", "-b:v:1", "800k",
        "-maxrate:v:1", "1712k", "-bufsize:v:1", "2400k",
        "-map", "0:v:0", "-map", "0:a:0", "-s:v:2", "1280x720", "-b:v:2", "2500k",
        "-maxrate:v:2", "5350k", "-bufsize:v:2", "7500k",
        "-c:v", "libx264", "-c:a", "aac",
        "-f", "hls",
        "-hls_time", "4",
        "-hls_playlist_type", "vod",
        "-master_pl_name", os.path.join(output_dir, "master.m3u8"),
        "-var_stream_map", "v:0,a:0 v:1,a:1 v:2,a:2",
        "-hls_segment_filename", os.path.join(output_dir, "v%v/segment_%03d.ts"),
        os.path.join(output_dir, "v%v/prog.m3u8")
    ]

    try:
        subprocess.run(hls_command, check=True)
        # Update the model with HLS paths
        video.hls_master_playlist = os.path.join("videos", "hls", f"video_{video_id}", "master.m3u8")
        video.hls_output_dir = os.path.join("videos", "hls", f"video_{video_id}")
        video.save()
        return {"status": "success", "master_playlist": video.hls_master_playlist}
    except Exception as e:
        return {"status": "error", "message": str(e)}

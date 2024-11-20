from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Video
from . import serializers
from .tasks import process_video_resolutions

class VideoUploadView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = serializers.VideoSerializer(data=request.data)
        if serializer.is_valid():
            video = serializer.save()
            # Trigger Celery task to process resolutions
            process_video_resolutions.delay(video.id)
            return Response({"message": "Video uploaded successfully, processing started."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, *args, **ksargs):
        videos = Video.objects.all()

        return Response(serializers.VideoSerializer(videos, many=True).data, status=status.HTTP_200_OK)

class VideoUploadRetrieveUpdateDestroyAPIView(APIView):
    def get(self, request, *args, **kwargs):
        video = Video.objects.get(id=kwargs.get('id'))

        return Response(serializers.VideoSerializer(video).data, status=status.HTTP_200_OK)
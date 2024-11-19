from django.urls import path
from . import views


urlpatterns = [
    path('', views.VideoUploadView.as_view(), name='video-upload'),
]

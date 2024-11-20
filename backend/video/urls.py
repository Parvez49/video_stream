from django.urls import path
from . import views


urlpatterns = [
    path('', views.VideoUploadView.as_view(), name='video-upload'),
    path('/<int:id>',views.VideoUploadRetrieveUpdateDestroyAPIView.as_view(), name='video-retrieve'),
]

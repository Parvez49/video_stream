import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';

const VideoPlayer = () => {
  const { videoId } = useParams(); // Get video ID from the URL
  const [videoData, setVideoData] = useState(null);
  const [videoSrc, setVideoSrc] = useState(null);

  useEffect(() => {
    // Fetch video details by ID
    const fetchVideoData = async () => {
      try {
        const response = await axios.get(`http://localhost:8000/videos/${videoId}`); // Assuming endpoint for individual video
        setVideoData(response.data);
      } catch (error) {
        console.error('Error fetching video data:', error);
      }
    };

    fetchVideoData();
  }, [videoId]);

  useEffect(() => {
    if (videoData) {
      const connection = navigator.connection || navigator.mozConnection || navigator.webkitConnection;
      const downloadSpeed = connection ? connection.downlink : 10; // In Mbps, default to 10 if no connection data
      console.log('DownloadSpeed: ',downloadSpeed);

      // Choose video resolution based on network speed
      if (downloadSpeed < 1) {
        setVideoSrc(videoData.low_resolution_video);
      } else if (downloadSpeed < 3) {
        setVideoSrc(videoData.medium_resolution_video);
      } else {
        setVideoSrc(videoData.high_resolution_video);
      }
    }
  }, [videoData]);

  if (!videoData) {
    return <p className="text-center">Loading video...</p>;
  }

  return (
    <div className="p-4 bg-gray-100 min-h-screen">
      <h1 className="text-2xl font-bold text-center mb-4">{videoData.title}</h1>
      <p className="text-center text-gray-600 mb-4">{videoData.description}</p>
      {videoSrc ? (
        <div className="flex justify-center">
          <video controls className="w-full md:w-3/4 lg:w-1/2">
            <source src={`http://localhost:8000/${videoSrc}`} type="video/mp4" />
            Your browser does not support the video tag.
          </video>
        </div>
      ) : (
        <p className="text-center">Determining the best resolution...</p>
      )}
      <div className="text-center mt-4">
        <p>
          <strong>Uploaded:</strong> {new Date(videoData.uploaded_at).toLocaleString()}
        </p>
      </div>
    </div>
  );
};

export default VideoPlayer;

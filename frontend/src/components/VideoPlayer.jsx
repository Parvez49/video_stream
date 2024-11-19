import React, { useState, useEffect } from 'react';
import ReactPlayer from 'react-player';
import axios from 'axios';

const VideoPlayer = ({ videoId }) => {
  const [videoUrl, setVideoUrl] = useState('');
  const [networkSpeed, setNetworkSpeed] = useState(''); // Optional for logs or debugging

  useEffect(() => {
    // Fetch the HLS/DASH URL from the backend
    const fetchVideoUrl = async () => {
      try {
        const response = await axios.get(`/api/videos/${videoId}/`);
        setVideoUrl(response.data.video_url);
      } catch (error) {
        console.error('Error fetching video URL:', error);
      }
    };

    fetchVideoUrl();
  }, [videoId]);

  return (
    <div className="flex justify-center items-center min-h-screen bg-gray-100">
      <div className="w-full max-w-4xl">
        {videoUrl ? (
          <ReactPlayer
            url={videoUrl}
            controls
            width="100%"
            height="auto"
            playing
          />
        ) : (
          <p className="text-center text-gray-500">Loading video...</p>
        )}
      </div>
    </div>
  );
};

export default VideoPlayer;

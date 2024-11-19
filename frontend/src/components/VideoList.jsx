import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';

const VideoList = () => {
  const [videos, setVideos] = useState([]);

  useEffect(() => {
    const fetchVideos = async () => {
      try {
        const response = await axios.get('/api/videos/');
        setVideos(response.data);
      } catch (error) {
        console.error('Error fetching videos:', error);
      }
    };

    fetchVideos();
  }, []);

  return (
    <div className="p-4 bg-gray-100 min-h-screen">
      <h1 className="text-2xl font-bold text-center mb-4">Available Videos</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {videos.map((video) => (
          <div key={video.id} className="bg-white shadow-md p-4 rounded">
            <h2 className="text-xl font-medium">{video.title}</h2>
            <Link
              to={`/video/${video.id}`}
              className="text-blue-500 hover:underline"
            >
              Watch Video
            </Link>
          </div>
        ))}
      </div>
    </div>
  );
};

export default VideoList;

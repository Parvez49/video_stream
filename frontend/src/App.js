import logo from "./logo.svg";
import "./App.css";
import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import VideoList from "./components/VideoList";
import VideoPlayer from "./components/VideoPlayer";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<VideoList />} />
        <Route path="/video/:videoId" element={<VideoPlayer />} />
      </Routes>
    </Router>
  );
}

export default App;

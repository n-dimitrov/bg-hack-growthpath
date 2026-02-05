import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import './CareerPathVisualizer.css';

const CareerPathVisualizer = () => {
  const [tracks, setTracks] = useState([]);
  const [selectedTrack, setSelectedTrack] = useState('software_engineer');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchCareerPaths();
  }, []);

  const fetchCareerPaths = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/career/paths');
      const data = await response.json();
      setTracks(data.tracks);
      setLoading(false);
    } catch (err) {
      setError('Failed to load career paths');
      setLoading(false);
    }
  };

  if (loading) return <div className="loading">Loading career paths...</div>;
  if (error) return <div className="error">{error}</div>;

  const currentTrack = tracks.find(t => t.key === selectedTrack);

  return (
    <div className="career-path-visualizer">
      <div className="header">
        <h1>Career Path Explorer</h1>
        <p>Visualize your growth journey and understand what it takes to advance</p>
      </div>

      <div className="track-selector">
        {tracks.map(track => (
          <button
            key={track.key}
            className={`track-btn ${selectedTrack === track.key ? 'active' : ''}`}
            onClick={() => setSelectedTrack(track.key)}
          >
            {track.name}
          </button>
        ))}
      </div>

      {currentTrack && (
        <div className="track-details">
          <div className="track-header">
            <h2>{currentTrack.name}</h2>
            <p>{currentTrack.description}</p>
            <span className="level-count">{currentTrack.levels} levels</span>
          </div>

          <div className="career-ladder">
            {currentTrack.level_details.map((level, index) => (
              <div key={level.pay_class} className="level-card">
                <div className="level-number">{level.level}</div>
                <div className="level-content">
                  <h3>{level.title}</h3>
                  <span className="pay-class">{level.pay_class}</span>
                  <p className="summary">{level.summary}</p>
                  <Link
                    to={`/career/${currentTrack.key}/${level.pay_class}`}
                    className="view-details"
                  >
                    View Competencies →
                  </Link>
                </div>
                {index < currentTrack.level_details.length - 1 && (
                  <div className="level-arrow">↓</div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default CareerPathVisualizer;

import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import './CompetencyDetails.css';

const CompetencyDetails = () => {
  const { track, payClass } = useParams();
  const [levelData, setLevelData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchLevelDetails();
  }, [track, payClass]);

  const fetchLevelDetails = async () => {
    try {
      const response = await fetch(`http://localhost:8000/api/career/paths/${track}/${payClass}`);
      if (!response.ok) {
        throw new Error('Failed to fetch level details');
      }
      const data = await response.json();
      setLevelData(data);
      setLoading(false);
    } catch (err) {
      setError(err.message);
      setLoading(false);
    }
  };

  if (loading) return <div className="loading">Loading competency details...</div>;
  if (error) return <div className="error">Error: {error}</div>;
  if (!levelData) return <div className="error">No data found</div>;

  return (
    <div className="competency-details">
      <div className="breadcrumb">
        <Link to="/career-paths">← Back to Career Paths</Link>
      </div>

      <div className="level-header">
        <h1>{levelData.title}</h1>
        <div className="level-meta">
          <span className="pay-class-badge">{levelData.pay_class}</span>
          <span className="level-badge">Level {levelData.level}</span>
        </div>
        <p className="level-summary">{levelData.summary}</p>
        <p className="impact-scope"><strong>Impact Scope:</strong> {levelData.impact_scope}</p>
      </div>

      <div className="competencies-section">
        <h2>Required Competencies ({levelData.total_competencies})</h2>
        <p className="section-description">
          These are the core competencies expected at the {levelData.title} level.
        </p>

        <div className="competencies-grid">
          {levelData.competencies && levelData.competencies.map((competency, index) => (
            <div key={index} className="competency-card">
              <div className="competency-header">
                <h3>{competency.area}</h3>
                {competency.scope && (
                  <span className="scope-badge">{competency.scope}</span>
                )}
              </div>

              {competency.description && (
                <p className="competency-description">{competency.description}</p>
              )}

              <div className="expectations">
                <h4>What's Expected:</h4>
                <p>{competency.expectations}</p>
              </div>
            </div>
          ))}
        </div>

        {(!levelData.competencies || levelData.competencies.length === 0) && (
          <div className="no-competencies">
            <p>No specific competencies defined for this level.</p>
          </div>
        )}
      </div>

      <div className="actions">
        <Link to="/gap-analysis" className="btn-primary">
          Analyze Skills Gap
        </Link>
        <Link to="/career-paths" className="btn-secondary">
          Back to Career Paths
        </Link>
      </div>
    </div>
  );
};

export default CompetencyDetails;

import React, { useState, useEffect } from 'react';
import './Dashboard.css';

const Dashboard = () => {
  const [gapAnalysis, setGapAnalysis] = useState(null);
  const [competencies, setCompetencies] = useState([]);
  const [currentLevel, setCurrentLevel] = useState('PC07');
  const [targetLevel, setTargetLevel] = useState('PC08');
  const [loading, setLoading] = useState(false);
  const [developmentPlan, setDevelopmentPlan] = useState(null);
  const [showPlan, setShowPlan] = useState(false);

  const payClasses = [
    { value: 'PC06', label: 'PC06 - Junior Software Engineer' },
    { value: 'PC07', label: 'PC07 - Software Engineer' },
    { value: 'PC08', label: 'PC08 - Senior Software Engineer' },
    { value: 'PC09', label: 'PC09 - Lead Software Engineer' },
    { value: 'PC10', label: 'PC10 - Principal Software Engineer' }
  ];

  useEffect(() => {
    analyzeSkillsGap();
  }, [currentLevel, targetLevel]);

  const analyzeSkillsGap = async () => {
    if (currentLevel === targetLevel) {
      setGapAnalysis(null);
      return;
    }

    setLoading(true);
    try {
      const response = await fetch(
        `http://localhost:8000/api/career/skills-gap?current_level=${currentLevel}&target_level=${targetLevel}`,
        { method: 'POST' }
      );
      const data = await response.json();
      setGapAnalysis(data);
    } catch (err) {
      console.error('Failed to analyze skills gap:', err);
    }
    setLoading(false);
  };

  const generateDevelopmentPlan = async () => {
    const userId = 1; // Demo user ID
    setLoading(true);
    try {
      const response = await fetch(
        `http://localhost:8000/api/career/development-plan?user_id=${userId}&current_level=${currentLevel}&target_level=${targetLevel}`,
        { method: 'POST' }
      );
      const data = await response.json();
      setDevelopmentPlan(data);
      setShowPlan(true);
    } catch (err) {
      console.error('Failed to generate plan:', err);
      alert('Failed to generate development plan');
    }
    setLoading(false);
  };

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <h1>Career Development Dashboard</h1>
        <p>Analyze your skills gap and plan your growth journey</p>
      </div>

      <div className="level-selector-card">
        <h2>Select Your Career Levels</h2>
        <div className="level-selectors">
          <div className="selector-group">
            <label>Current Level</label>
            <select
              value={currentLevel}
              onChange={(e) => setCurrentLevel(e.target.value)}
              className="level-select"
            >
              {payClasses.map(pc => (
                <option key={pc.value} value={pc.value}>{pc.label}</option>
              ))}
            </select>
          </div>

          <div className="arrow-indicator">→</div>

          <div className="selector-group">
            <label>Target Level</label>
            <select
              value={targetLevel}
              onChange={(e) => setTargetLevel(e.target.value)}
              className="level-select"
            >
              {payClasses.map(pc => (
                <option key={pc.value} value={pc.value}>{pc.label}</option>
              ))}
            </select>
          </div>
        </div>
      </div>

      {loading && <div className="loading">Analyzing skills gap...</div>}

      {gapAnalysis && !loading && (
        <>
          <div className="stats-cards">
            <div className="stat-card">
              <div className="stat-number">{gapAnalysis.total_gaps}</div>
              <div className="stat-label">Competency Gaps</div>
            </div>
            <div className="stat-card">
              <div className="stat-number">{currentLevel}</div>
              <div className="stat-label">Current Level</div>
            </div>
            <div className="stat-card">
              <div className="stat-number">{targetLevel}</div>
              <div className="stat-label">Target Level</div>
            </div>
          </div>

          <div className="gaps-section">
            <div className="section-header">
              <h2>Skills & Competency Gaps</h2>
              <button onClick={generateDevelopmentPlan} className="btn-primary">
                Generate Development Plan
              </button>
            </div>

            <div className="gaps-list">
              {gapAnalysis.gaps.map((gap, index) => (
                <div key={index} className="gap-card">
                  <div className="gap-header">
                    <h3>{gap.area}</h3>
                    <span className="gap-badge">Gap Identified</span>
                  </div>

                  {gap.description && (
                    <p className="gap-description">{gap.description}</p>
                  )}

                  <div className="gap-comparison">
                    <div className="gap-section">
                      <h4>Current Level ({currentLevel})</h4>
                      <p className="current-state">{gap.current}</p>
                    </div>

                    <div className="gap-divider">
                      <span>→</span>
                    </div>

                    <div className="gap-section">
                      <h4>Required for {targetLevel}</h4>
                      <p className="target-state">{gap.required}</p>
                    </div>
                  </div>
                </div>
              ))}
            </div>

            {gapAnalysis.gaps.length === 0 && (
              <div className="no-gaps">
                <p>No competency gaps found between these levels!</p>
                <p>You may already meet the requirements for {targetLevel}</p>
              </div>
            )}
          </div>
        </>
      )}

      {!gapAnalysis && !loading && currentLevel === targetLevel && (
        <div className="info-message">
          <p>Select different current and target levels to see your skills gap analysis</p>
        </div>
      )}

      {showPlan && developmentPlan && (
        <div className="development-plan-section">
          <div className="plan-header">
            <h2>🎯 Your Development Plan</h2>
            <button onClick={() => setShowPlan(false)} className="close-btn">✕</button>
          </div>

          <div className="plan-summary">
            <div className="plan-info">
              <div className="info-item">
                <span className="label">Plan ID:</span>
                <span className="value">#{developmentPlan.plan_id}</span>
              </div>
              <div className="info-item">
                <span className="label">Created:</span>
                <span className="value">{developmentPlan.created_date}</span>
              </div>
              <div className="info-item">
                <span className="label">Target Date:</span>
                <span className="value">{developmentPlan.target_date}</span>
              </div>
              <div className="info-item">
                <span className="label">Duration:</span>
                <span className="value">{developmentPlan.estimated_timeframe}</span>
              </div>
              <div className="info-item">
                <span className="label">Progress:</span>
                <span className="value">{developmentPlan.current_level} → {developmentPlan.target_level}</span>
              </div>
            </div>
          </div>

          <div className="objectives-section">
            <h3>Learning Objectives ({developmentPlan.total_objectives})</h3>
            <div className="objectives-list">
              {developmentPlan.objectives.map((objective) => (
                <div key={objective.id} className="objective-card">
                  <div className="objective-header">
                    <span className="objective-number">#{objective.id}</span>
                    <h4>{objective.competency}</h4>
                    <span className={`priority-badge ${objective.priority.toLowerCase()}`}>
                      {objective.priority} Priority
                    </span>
                  </div>

                  <div className="objective-details">
                    <div className="detail-row">
                      <strong>Current State:</strong>
                      <p>{objective.current_state}</p>
                    </div>
                    <div className="detail-row">
                      <strong>Target State:</strong>
                      <p>{objective.target_state}</p>
                    </div>
                  </div>

                  <div className="objective-status">
                    <span className="status-badge">{objective.status.replace('_', ' ')}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="plan-actions">
            <button onClick={() => setShowPlan(false)} className="btn-secondary">
              Close Plan
            </button>
            <button className="btn-primary" onClick={() => window.print()}>
              Print Plan
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default Dashboard;

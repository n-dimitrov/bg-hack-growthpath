import React, { useState, useEffect } from 'react';
import './ProgressTracker.css';

const ProgressTracker = () => {
  const [plans, setPlans] = useState([]);
  const [selectedPlan, setSelectedPlan] = useState(null);
  const [planDetails, setPlanDetails] = useState(null);
  const [loading, setLoading] = useState(true);
  const [updating, setUpdating] = useState(false);
  const userId = 1; // Demo user ID

  useEffect(() => {
    loadUserPlans();
  }, []);

  useEffect(() => {
    if (selectedPlan) {
      loadPlanDetails(selectedPlan);
    }
  }, [selectedPlan]);

  const loadUserPlans = async () => {
    setLoading(true);
    try {
      const response = await fetch(`http://localhost:8000/api/career/user-plans/${userId}`);
      const data = await response.json();
      setPlans(data.plans);
      if (data.plans.length > 0) {
        setSelectedPlan(data.plans[0].plan_id);
      }
      setLoading(false);
    } catch (err) {
      console.error('Failed to load plans:', err);
      setLoading(false);
    }
  };

  const loadPlanDetails = async (planId) => {
    try {
      const response = await fetch(`http://localhost:8000/api/career/development-plan/${planId}`);
      const data = await response.json();
      setPlanDetails(data);
    } catch (err) {
      console.error('Failed to load plan details:', err);
    }
  };

  const updateObjectiveStatus = async (objectiveId, newStatus) => {
    setUpdating(true);
    try {
      const response = await fetch(
        `http://localhost:8000/api/career/objective/${objectiveId}?status=${newStatus}`,
        { method: 'PUT' }
      );
      if (response.ok) {
        // Reload both plans list and details
        await loadUserPlans();
        await loadPlanDetails(selectedPlan);
      }
    } catch (err) {
      console.error('Failed to update objective:', err);
      alert('Failed to update objective status');
    }
    setUpdating(false);
  };

  const updatePlanStatus = async (planId, newStatus) => {
    setUpdating(true);
    try {
      const response = await fetch(
        `http://localhost:8000/api/career/plan/${planId}/status?status=${newStatus}`,
        { method: 'PUT' }
      );
      if (response.ok) {
        await loadUserPlans();
        await loadPlanDetails(planId);
      }
    } catch (err) {
      console.error('Failed to update plan:', err);
      alert('Failed to update plan status');
    }
    setUpdating(false);
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'completed': return '#28a745';
      case 'in_progress': return '#ffc107';
      case 'not_started': return '#6c757d';
      default: return '#6c757d';
    }
  };

  const getPlanStatusColor = (status) => {
    switch (status) {
      case 'active': return '#007bff';
      case 'completed': return '#28a745';
      case 'cancelled': return '#dc3545';
      default: return '#6c757d';
    }
  };

  if (loading) {
    return (
      <div className="progress-tracker">
        <div className="loading">Loading your development plans...</div>
      </div>
    );
  }

  if (plans.length === 0) {
    return (
      <div className="progress-tracker">
        <div className="tracker-header">
          <h1>Progress Tracker</h1>
          <p>Track your career development journey</p>
        </div>
        <div className="no-plans">
          <h3>No Development Plans Yet</h3>
          <p>Create your first development plan in the Gap Analysis section to start tracking your progress.</p>
          <a href="/gap-analysis" className="btn-primary">Go to Gap Analysis</a>
        </div>
      </div>
    );
  }

  const currentPlan = plans.find(p => p.plan_id === selectedPlan);

  return (
    <div className="progress-tracker">
      <div className="tracker-header">
        <h1>Progress Tracker</h1>
        <p>Monitor and update your career development progress</p>
      </div>

      <div className="plans-overview">
        <h2>Your Development Plans</h2>
        <div className="plans-grid">
          {plans.map(plan => (
            <div
              key={plan.plan_id}
              className={`plan-summary-card ${selectedPlan === plan.plan_id ? 'active' : ''}`}
              onClick={() => setSelectedPlan(plan.plan_id)}
            >
              <div className="plan-summary-header">
                <h3>{plan.current_level} → {plan.target_level}</h3>
                <span
                  className="plan-status-badge"
                  style={{ background: getPlanStatusColor(plan.status) }}
                >
                  {plan.status}
                </span>
              </div>
              <div className="plan-summary-stats">
                <div className="stat">
                  <span className="stat-value">{plan.completion_percentage}%</span>
                  <span className="stat-label">Complete</span>
                </div>
                <div className="stat">
                  <span className="stat-value">{plan.completed_objectives}/{plan.total_objectives}</span>
                  <span className="stat-label">Objectives</span>
                </div>
              </div>
              <div className="progress-bar">
                <div
                  className="progress-fill"
                  style={{ width: `${plan.completion_percentage}%` }}
                ></div>
              </div>
              <div className="plan-summary-dates">
                <small>Created: {plan.created_date}</small>
                {plan.target_date && <small>Target: {plan.target_date}</small>}
              </div>
            </div>
          ))}
        </div>
      </div>

      {planDetails && currentPlan && (
        <div className="plan-details-section">
          <div className="plan-details-header">
            <div>
              <h2>Plan Details</h2>
              <p>Track and update your learning objectives</p>
            </div>
            <div className="plan-actions">
              <select
                value={currentPlan.status}
                onChange={(e) => updatePlanStatus(selectedPlan, e.target.value)}
                disabled={updating}
                className="status-select"
              >
                <option value="active">Active</option>
                <option value="completed">Completed</option>
                <option value="cancelled">Cancelled</option>
              </select>
            </div>
          </div>

          <div className="objectives-progress">
            <h3>Learning Objectives ({planDetails.objectives.length})</h3>
            <div className="objectives-stats">
              <div className="stat-chip completed">
                <span className="stat-number">{currentPlan.completed_objectives}</span>
                <span>Completed</span>
              </div>
              <div className="stat-chip in-progress">
                <span className="stat-number">{currentPlan.in_progress_objectives}</span>
                <span>In Progress</span>
              </div>
              <div className="stat-chip not-started">
                <span className="stat-number">{currentPlan.not_started_objectives}</span>
                <span>Not Started</span>
              </div>
            </div>

            <div className="objectives-list-tracker">
              {planDetails.objectives.map((objective) => (
                <div key={objective.id} className="objective-tracker-card">
                  <div className="objective-tracker-header">
                    <div className="objective-info">
                      <h4>{objective.competency}</h4>
                      <p>{objective.description}</p>
                    </div>
                    <span className={`priority-badge ${objective.priority.toLowerCase()}`}>
                      {objective.priority}
                    </span>
                  </div>

                  <div className="objective-tracker-controls">
                    <div className="status-buttons">
                      <button
                        className={`status-btn ${objective.status === 'not_started' ? 'active' : ''}`}
                        onClick={() => updateObjectiveStatus(objective.id, 'not_started')}
                        disabled={updating}
                        style={{ borderColor: getStatusColor('not_started') }}
                      >
                        Not Started
                      </button>
                      <button
                        className={`status-btn ${objective.status === 'in_progress' ? 'active' : ''}`}
                        onClick={() => updateObjectiveStatus(objective.id, 'in_progress')}
                        disabled={updating}
                        style={{ borderColor: getStatusColor('in_progress') }}
                      >
                        In Progress
                      </button>
                      <button
                        className={`status-btn ${objective.status === 'completed' ? 'active' : ''}`}
                        onClick={() => updateObjectiveStatus(objective.id, 'completed')}
                        disabled={updating}
                        style={{ borderColor: getStatusColor('completed') }}
                      >
                        Completed
                      </button>
                    </div>
                  </div>

                  <div className="objective-status-indicator">
                    <div
                      className="status-bar"
                      style={{ background: getStatusColor(objective.status) }}
                    ></div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ProgressTracker;

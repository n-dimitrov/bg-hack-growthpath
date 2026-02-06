import { useState, useEffect } from 'react'
import axios from 'axios'
import './UserProfile.css'

const API_BASE_URL = 'http://localhost:8000'

const PROFICIENCY_LEVELS = {
  1: { name: 'Beginner', color: '#ffc107', width: 25 },
  2: { name: 'Intermediate', color: '#2196f3', width: 50 },
  3: { name: 'Advanced', color: '#4caf50', width: 75 },
  4: { name: 'Expert', color: '#9c27b0', width: 100 }
}

const CATEGORY_ICONS = {
  technical: '🔧',
  soft_skills: '💬',
  leadership: '👥',
  domain_knowledge: '💼'
}

function UserProfile({ userId, onClose }) {
  const [user, setUser] = useState(null)
  const [skills, setSkills] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [analyzing, setAnalyzing] = useState(false)
  const [analysis, setAnalysis] = useState(null)
  const [showAnalysis, setShowAnalysis] = useState(false)

  useEffect(() => {
    fetchUserProfile()
  }, [userId])

  const fetchUserProfile = async () => {
    setLoading(true)
    try {
      const [userResponse, skillsResponse] = await Promise.all([
        axios.get(`${API_BASE_URL}/users/${userId}`),
        axios.get(`${API_BASE_URL}/users/${userId}/skills`)
      ])

      setUser(userResponse.data)
      setSkills(skillsResponse.data.skills)
      setError(null)
    } catch (err) {
      setError('Failed to load user profile')
      console.error('Error fetching user profile:', err)
    } finally {
      setLoading(false)
    }
  }

  const getProficiencyInfo = (level) => {
    return PROFICIENCY_LEVELS[level] || PROFICIENCY_LEVELS[1]
  }

  const handlePrint = () => {
    window.print()
  }

  const handleAnalyze = async () => {
    setAnalyzing(true)
    setShowAnalysis(false)
    try {
      const response = await axios.post(`${API_BASE_URL}/users/${userId}/analyze-skills`)
      setAnalysis(response.data)
      setShowAnalysis(true)
    } catch (err) {
      console.error('Error analyzing skills:', err)
      alert(err.response?.data?.detail || 'Failed to analyze skills. Please check LLM configuration.')
    } finally {
      setAnalyzing(false)
    }
  }

  if (loading) {
    return (
      <div className="profile-modal-overlay">
        <div className="profile-modal">
          <div className="loading-profile">
            <div className="spinner"></div>
            <p>Loading profile...</p>
          </div>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="profile-modal-overlay">
        <div className="profile-modal">
          <div className="error-profile">
            <p>{error}</p>
            <button onClick={onClose} className="btn-close">Close</button>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="profile-modal-overlay" onClick={onClose}>
      <div className="profile-modal" onClick={(e) => e.stopPropagation()}>
        <button className="modal-close-btn" onClick={onClose}>✕</button>

        <div className="profile-header">
          <div className="profile-avatar-large">
            {user.name.split(' ').map(n => n[0]).join('').toUpperCase()}
          </div>
          <div className="profile-info">
            <h2>{user.name}</h2>
            <p className="profile-email">📧 {user.email}</p>
            <p className="profile-role">
              💼 {user.role.charAt(0).toUpperCase() + user.role.slice(1)}
            </p>
          </div>
        </div>

        <div className="profile-stats-summary">
          <div className="stat-box">
            <div className="stat-number">{user.skills_count}</div>
            <div className="stat-label">Total Skills</div>
          </div>
          {Object.entries(user.skills_by_category || {}).map(([category, count]) => (
            <div key={category} className="stat-box">
              <div className="stat-number">{count}</div>
              <div className="stat-label">
                {category.replace('_', ' ').charAt(0).toUpperCase() +
                 category.replace('_', ' ').slice(1)}
              </div>
            </div>
          ))}
        </div>

        <div className="profile-skills">
          {skills.length === 0 ? (
            <div className="no-skills">
              <p>No skills recorded for this user yet.</p>
            </div>
          ) : (
            skills.map((categoryGroup) => (
              <div key={categoryGroup.category} className="skills-category">
                <h3 className="category-title">
                  {CATEGORY_ICONS[categoryGroup.category] || '📋'}{' '}
                  {categoryGroup.category.replace('_', ' ').toUpperCase()}
                  <span className="category-count">
                    ({categoryGroup.competencies.length})
                  </span>
                </h3>
                <div className="skills-list">
                  {categoryGroup.competencies.map((skill) => {
                    const profInfo = getProficiencyInfo(skill.proficiency_level)
                    return (
                      <div key={skill.id} className="skill-item">
                        <div className="skill-header">
                          <h4 className="skill-name">{skill.name}</h4>
                          <span
                            className="proficiency-badge"
                            style={{ backgroundColor: profInfo.color }}
                          >
                            {profInfo.name}
                          </span>
                        </div>
                        {skill.description && (
                          <p className="skill-description">{skill.description}</p>
                        )}
                        <div className="proficiency-bar">
                          <div
                            className="proficiency-fill"
                            style={{
                              width: `${profInfo.width}%`,
                              backgroundColor: profInfo.color
                            }}
                          />
                        </div>
                      </div>
                    )
                  })}
                </div>
              </div>
            ))
          )}
        </div>

        {showAnalysis && analysis && (
          <div className="analysis-section">
            <div className="analysis-header">
              <h3>🤖 AI Skills Analysis</h3>
              <button
                className="close-analysis-btn"
                onClick={() => setShowAnalysis(false)}
              >
                ✕
              </button>
            </div>
            <div className="analysis-meta">
              <span>📊 Analyzed {analysis.skills_analyzed} skills</span>
              <span>🤖 Model: {analysis.model_used}</span>
            </div>
            <div className="analysis-content">
              {analysis.analysis.split('\n').map((line, index) => {
                if (line.trim().startsWith('#')) {
                  return <h4 key={index}>{line.replace(/^#+\s*/, '')}</h4>
                } else if (line.trim().startsWith('**') && line.trim().endsWith('**')) {
                  return <h5 key={index}>{line.replace(/\*\*/g, '')}</h5>
                } else if (line.trim().startsWith('-') || line.trim().startsWith('•')) {
                  return <li key={index}>{line.replace(/^[-•]\s*/, '')}</li>
                } else if (line.trim()) {
                  return <p key={index}>{line}</p>
                }
                return <br key={index} />
              })}
            </div>
          </div>
        )}

        <div className="profile-actions">
          <button className="btn-secondary" onClick={onClose}>
            Close
          </button>
          <button
            className="btn-analyze"
            onClick={handleAnalyze}
            disabled={analyzing}
          >
            {analyzing ? '🔄 Analyzing...' : '🤖 Analyze Skills'}
          </button>
          <button className="btn-primary" onClick={handlePrint}>
            Export PDF
          </button>
        </div>
      </div>
    </div>
  )
}

export default UserProfile

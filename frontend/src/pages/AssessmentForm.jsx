import { useState, useEffect } from 'react'
import { getCompetencies, createAssessment } from '../services/api'

function AssessmentForm() {
  const [competencies, setCompetencies] = useState([])
  const [assessments, setAssessments] = useState({})
  const [loading, setLoading] = useState(true)
  const [userId] = useState(1) // Mock user ID for now

  useEffect(() => {
    loadCompetencies()
  }, [])

  const loadCompetencies = async () => {
    try {
      // Try the new career competencies API first
      const response = await fetch('http://localhost:8000/api/career/competencies')
      const data = await response.json()

      if (data.competencies) {
        setCompetencies(data.competencies)
      } else {
        // Fallback to old API
        const oldData = await getCompetencies()
        setCompetencies(oldData)
      }
      setLoading(false)
    } catch (error) {
      console.error('Error loading competencies:', error)
      setLoading(false)
    }
  }

  const handleProficiencyChange = (competencyId, level) => {
    setAssessments({
      ...assessments,
      [competencyId]: parseInt(level)
    })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      for (const [competencyId, proficiencyLevel] of Object.entries(assessments)) {
        await createAssessment(userId, {
          competency_id: parseInt(competencyId),
          proficiency_level: proficiencyLevel
        })
      }
      alert('Assessment submitted successfully!')
      setAssessments({})
    } catch (error) {
      console.error('Error submitting assessment:', error)
      alert('Failed to submit assessment')
    }
  }

  const proficiencyLevels = [
    { value: 1, label: 'Beginner' },
    { value: 2, label: 'Intermediate' },
    { value: 3, label: 'Advanced' },
    { value: 4, label: 'Expert' }
  ]

  if (loading) {
    return (
      <div className="assessment-form">
        <div className="loading">Loading competencies...</div>
      </div>
    )
  }

  if (!competencies || competencies.length === 0) {
    return (
      <div className="assessment-form">
        <h2>Skill Self-Assessment</h2>
        <div className="no-data">
          <p>No competencies available yet.</p>
          <p>Please check the Career Paths or Gap Analysis sections to explore competencies.</p>
        </div>
      </div>
    )
  }

  return (
    <div className="assessment-form">
      <h2>Skill Self-Assessment</h2>
      <p>Rate your proficiency level for each competency ({competencies.length} total)</p>

      <form onSubmit={handleSubmit}>
        {competencies.map((competency) => (
          <div key={competency.id} className="competency-item">
            <div className="competency-info">
              <h3>{competency.name}</h3>
              <p className="category">{competency.category}</p>
              {competency.description && (
                <p className="description">{competency.description}</p>
              )}
            </div>

            <div className="proficiency-selector">
              {proficiencyLevels.map((level) => (
                <label key={level.value} className="radio-label">
                  <input
                    type="radio"
                    name={`competency-${competency.id}`}
                    value={level.value}
                    checked={assessments[competency.id] === level.value}
                    onChange={(e) => handleProficiencyChange(competency.id, e.target.value)}
                  />
                  <span>{level.label}</span>
                </label>
              ))}
            </div>
          </div>
        ))}

        <button type="submit" className="submit-button">
          Submit Assessment
        </button>
      </form>
    </div>
  )
}

export default AssessmentForm

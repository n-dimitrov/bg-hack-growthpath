import { Link } from 'react-router-dom'

function Dashboard() {
  return (
    <div className="dashboard">
      <h2>Welcome to GrowthPath</h2>
      <p>Track and develop your professional competencies</p>

      <div className="dashboard-actions">
        <Link to="/assessment" className="action-card">
          <h3>Take Assessment</h3>
          <p>Evaluate your current skill levels</p>
        </Link>

        <div className="action-card disabled">
          <h3>View Progress</h3>
          <p>Coming soon: Track your skill development over time</p>
        </div>

        <div className="action-card disabled">
          <h3>Learning Path</h3>
          <p>Coming soon: Get personalized recommendations</p>
        </div>
      </div>
    </div>
  )
}

export default Dashboard

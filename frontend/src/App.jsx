import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom'
import AssessmentForm from './pages/AssessmentForm'
import Dashboard from './pages/Dashboard'
import CareerPathVisualizer from './components/CareerPathVisualizer'
import SkillsCatalog from './components/SkillsCatalog'
import DashboardNew from './components/Dashboard'
import CompetencyDetails from './components/CompetencyDetails'
import './styles/App.css'

function App() {
  return (
    <Router>
      <div className="App">
        <header className="App-header">
          <h1>🚀 GrowthPath</h1>
          <p>Competence Management System</p>
          <nav style={{ marginTop: '1rem' }}>
            <Link to="/" style={linkStyle}>Home</Link>
            <Link to="/career-paths" style={linkStyle}>Career Paths</Link>
            <Link to="/skills" style={linkStyle}>Skills Catalog</Link>
            <Link to="/gap-analysis" style={linkStyle}>Gap Analysis</Link>
            <Link to="/assessment" style={linkStyle}>Assessment</Link>
          </nav>
        </header>
        <main>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/career-paths" element={<CareerPathVisualizer />} />
            <Route path="/career/:track/:payClass" element={<CompetencyDetails />} />
            <Route path="/skills" element={<SkillsCatalog />} />
            <Route path="/gap-analysis" element={<DashboardNew />} />
            <Route path="/assessment" element={<AssessmentForm />} />
          </Routes>
        </main>
      </div>
    </Router>
  )
}

const linkStyle = {
  color: '#61dafb',
  textDecoration: 'none',
  margin: '0 1rem',
  padding: '0.5rem 1rem',
  borderRadius: '4px',
  transition: 'background 0.3s'
}

export default App

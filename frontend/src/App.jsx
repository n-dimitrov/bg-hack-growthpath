import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import AssessmentForm from './pages/AssessmentForm'
import Dashboard from './pages/Dashboard'
import './styles/App.css'

function App() {
  return (
    <Router>
      <div className="App">
        <header className="App-header">
          <h1>GrowthPath</h1>
          <p>Competence Management System</p>
        </header>
        <main>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/assessment" element={<AssessmentForm />} />
          </Routes>
        </main>
      </div>
    </Router>
  )
}

export default App

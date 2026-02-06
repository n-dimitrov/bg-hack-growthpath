import { useState, useEffect } from 'react'
import axios from 'axios'
import '../styles/DataImport.css'

const API_BASE_URL = 'http://localhost:8000'

function DataImport() {
  const [file, setFile] = useState(null)
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)
  const [stats, setStats] = useState(null)
  const [dragActive, setDragActive] = useState(false)

  useEffect(() => {
    fetchStats()
  }, [])

  const fetchStats = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/import/status`)
      setStats(response.data)
    } catch (err) {
      console.error('Error fetching stats:', err)
    }
  }

  const handleDrag = (e) => {
    e.preventDefault()
    e.stopPropagation()
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true)
    } else if (e.type === "dragleave") {
      setDragActive(false)
    }
  }

  const handleDrop = (e) => {
    e.preventDefault()
    e.stopPropagation()
    setDragActive(false)

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const droppedFile = e.dataTransfer.files[0]
      if (droppedFile.name.endsWith('.xlsx') || droppedFile.name.endsWith('.xls')) {
        setFile(droppedFile)
        setError(null)
      } else {
        setError('Please upload an Excel file (.xlsx or .xls)')
      }
    }
  }

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      const selectedFile = e.target.files[0]
      if (selectedFile.name.endsWith('.xlsx') || selectedFile.name.endsWith('.xls')) {
        setFile(selectedFile)
        setError(null)
      } else {
        setError('Please upload an Excel file (.xlsx or .xls)')
        setFile(null)
      }
    }
  }

  const handleUpload = async () => {
    if (!file) {
      setError('Please select a file first')
      return
    }

    setLoading(true)
    setError(null)
    setResult(null)

    const formData = new FormData()
    formData.append('file', file)

    try {
      const response = await axios.post(
        `${API_BASE_URL}/import/planisware`,
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        }
      )

      setResult(response.data)
      setFile(null)
      fetchStats() // Refresh stats after successful import
    } catch (err) {
      setError(err.response?.data?.detail || 'Upload failed. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const handleClear = () => {
    setFile(null)
    setResult(null)
    setError(null)
  }

  return (
    <div className="data-import-container">
      <div className="import-header">
        <h2>Planisware Employee Data Import</h2>
        <p>Import employee skillset data from Excel files</p>
      </div>

      {stats && (
        <div className="stats-card">
          <h3>Current Database Statistics</h3>
          <div className="stats-grid">
            <div className="stat-item">
              <div className="stat-value">{stats.users}</div>
              <div className="stat-label">Users</div>
            </div>
            <div className="stat-item">
              <div className="stat-value">{stats.competencies}</div>
              <div className="stat-label">Competencies</div>
            </div>
            <div className="stat-item">
              <div className="stat-value">{stats.assessments}</div>
              <div className="stat-label">Assessments</div>
            </div>
          </div>
        </div>
      )}

      <div className="upload-card">
        <div
          className={`upload-zone ${dragActive ? 'drag-active' : ''}`}
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
        >
          <div className="upload-icon">📁</div>
          {file ? (
            <div className="file-info">
              <p className="file-name">{file.name}</p>
              <p className="file-size">{(file.size / 1024).toFixed(2)} KB</p>
            </div>
          ) : (
            <>
              <p className="upload-text">Drag and drop your Excel file here</p>
              <p className="upload-subtext">or</p>
            </>
          )}
          <label htmlFor="file-input" className="file-label">
            <span className="file-button">{file ? 'Change File' : 'Browse Files'}</span>
          </label>
          <input
            id="file-input"
            type="file"
            accept=".xlsx,.xls"
            onChange={handleFileChange}
            style={{ display: 'none' }}
          />
          <p className="file-format-hint">Accepts: .xlsx, .xls</p>
        </div>

        <div className="button-group">
          <button
            className="btn-upload"
            onClick={handleUpload}
            disabled={!file || loading}
          >
            {loading ? 'Uploading...' : 'Upload & Import'}
          </button>
          {file && (
            <button className="btn-clear" onClick={handleClear}>
              Clear
            </button>
          )}
        </div>
      </div>

      {error && (
        <div className="alert alert-error">
          <strong>Error:</strong> {error}
        </div>
      )}

      {result && (
        <div className="alert alert-success">
          <h3>✓ Import Completed Successfully!</h3>
          <div className="result-stats">
            <div className="result-section">
              <h4>Users</h4>
              <p>Created: <strong>{result.statistics.users_created}</strong></p>
              <p>Existing: <strong>{result.statistics.users_existing}</strong></p>
            </div>
            <div className="result-section">
              <h4>Competencies</h4>
              <p>Created: <strong>{result.statistics.competencies_created}</strong></p>
              <p>Existing: <strong>{result.statistics.competencies_existing}</strong></p>
            </div>
            <div className="result-section">
              <h4>Assessments</h4>
              <p>Created: <strong>{result.statistics.assessments_created}</strong></p>
              <p>Existing: <strong>{result.statistics.assessments_existing}</strong></p>
            </div>
            <div className="result-section">
              <h4>Processing</h4>
              <p>Processed: <strong>{result.statistics.rows_processed}</strong></p>
              <p>Skipped: <strong>{result.statistics.rows_skipped}</strong></p>
            </div>
          </div>
          {result.statistics.errors && result.statistics.errors.length > 0 && (
            <div className="errors-section">
              <h4>Errors ({result.statistics.errors.length})</h4>
              <ul>
                {result.statistics.errors.map((error, idx) => (
                  <li key={idx}>{error}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}

      <div className="info-card">
        <h3>Import Instructions</h3>
        <ol>
          <li>Prepare your Excel file with the required columns:
            <ul>
              <li><strong>Name</strong> - Employee name (required)</li>
              <li><strong>Skillset</strong> - Skill/competency name (required)</li>
              <li><strong>Skillset Level</strong> - Level: 1st, 2nd, 3rd, or 4th (required)</li>
              <li><strong>Skillsets.Description</strong> - Skill description (optional)</li>
              <li><strong>Skillsets.Category</strong> - Category (optional)</li>
            </ul>
          </li>
          <li>Upload the file using the area above</li>
          <li>Click "Upload & Import" to process the data</li>
          <li>Review the import results</li>
        </ol>
        <div className="level-mapping">
          <h4>Proficiency Level Mapping:</h4>
          <ul>
            <li>1st → Beginner</li>
            <li>2nd → Intermediate</li>
            <li>3rd → Advanced</li>
            <li>4th → Expert</li>
          </ul>
        </div>
      </div>
    </div>
  )
}

export default DataImport

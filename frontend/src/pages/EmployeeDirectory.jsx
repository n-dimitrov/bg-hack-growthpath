import { useState, useEffect } from 'react'
import axios from 'axios'
import UserProfile from '../components/UserProfile'
import '../styles/EmployeeDirectory.css'

const API_BASE_URL = 'http://localhost:8000'

function EmployeeDirectory() {
  const [users, setUsers] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [searchQuery, setSearchQuery] = useState('')
  const [selectedUser, setSelectedUser] = useState(null)
  const [showProfile, setShowProfile] = useState(false)

  useEffect(() => {
    fetchUsers()
  }, [searchQuery])

  const fetchUsers = async () => {
    setLoading(true)
    try {
      const params = searchQuery ? { search: searchQuery } : {}
      const response = await axios.get(`${API_BASE_URL}/users`, { params })
      setUsers(response.data.users)
      setError(null)
    } catch (err) {
      setError('Failed to load users. Please try again.')
      console.error('Error fetching users:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleViewProfile = (userId) => {
    setSelectedUser(userId)
    setShowProfile(true)
  }

  const handleCloseProfile = () => {
    setShowProfile(false)
    setSelectedUser(null)
  }

  const handleSearchChange = (e) => {
    setSearchQuery(e.target.value)
  }

  return (
    <div className="employee-directory">
      <div className="directory-header">
        <h1>Employee Directory</h1>
        <p>Browse and search employee profiles and skills</p>
      </div>

      <div className="search-section">
        <div className="search-box">
          <input
            type="text"
            placeholder="Search by name or email..."
            value={searchQuery}
            onChange={handleSearchChange}
            className="search-input"
          />
          <span className="search-icon">🔍</span>
        </div>
        {!loading && (
          <div className="results-count">
            Showing {users.length} {users.length === 1 ? 'employee' : 'employees'}
          </div>
        )}
      </div>

      {loading && (
        <div className="loading-state">
          <div className="spinner"></div>
          <p>Loading employees...</p>
        </div>
      )}

      {error && (
        <div className="error-state">
          <p>{error}</p>
          <button onClick={fetchUsers} className="retry-btn">Retry</button>
        </div>
      )}

      {!loading && !error && users.length === 0 && (
        <div className="empty-state">
          <div className="empty-icon">👥</div>
          <h3>No employees found</h3>
          <p>
            {searchQuery
              ? `No results for "${searchQuery}". Try a different search.`
              : 'No employees in the system yet. Import data to get started.'}
          </p>
        </div>
      )}

      {!loading && !error && users.length > 0 && (
        <div className="users-grid">
          {users.map((user) => (
            <div key={user.id} className="user-card">
              <div className="user-avatar">
                {user.name.split(' ').map(n => n[0]).join('').toUpperCase()}
              </div>
              <div className="user-info">
                <h3 className="user-name">{user.name}</h3>
                <p className="user-email">📧 {user.email}</p>
                <div className="user-stats">
                  <span className="stat-badge">
                    💼 {user.role.charAt(0).toUpperCase() + user.role.slice(1)}
                  </span>
                  <span className="stat-badge">
                    ✨ {user.skills_count} {user.skills_count === 1 ? 'skill' : 'skills'}
                  </span>
                </div>
              </div>
              <button
                className="view-profile-btn"
                onClick={() => handleViewProfile(user.id)}
              >
                View Profile
              </button>
            </div>
          ))}
        </div>
      )}

      {showProfile && selectedUser && (
        <UserProfile
          userId={selectedUser}
          onClose={handleCloseProfile}
        />
      )}
    </div>
  )
}

export default EmployeeDirectory

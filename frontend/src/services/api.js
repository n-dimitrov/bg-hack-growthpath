import axios from 'axios'

const API_BASE_URL = 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export const getCompetencies = async () => {
  const response = await api.get('/competencies/')
  return response.data
}

export const createCompetency = async (competency) => {
  const response = await api.post('/competencies/', competency)
  return response.data
}

export const createAssessment = async (userId, assessment) => {
  const response = await api.post(`/assessments/?user_id=${userId}`, assessment)
  return response.data
}

export const getUserAssessments = async (userId) => {
  const response = await api.get(`/assessments/user/${userId}`)
  return response.data
}

export default api

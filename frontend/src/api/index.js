import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 30000,
})

export const chatAPI = {
  getSessions(page = 1, pageSize = 20) {
    return api.get('/chat/sessions', { params: { page, page_size: pageSize } })
  },
  getMessages(sessionId) {
    return api.get(`/chat/sessions/${sessionId}/messages`)
  },
  deleteSession(sessionId) {
    return api.delete(`/chat/sessions/${sessionId}`)
  },
}

export const documentAPI = {
  upload(file, sessionId = '') {
    const formData = new FormData()
    formData.append('file', file)
    if (sessionId) formData.append('session_id', sessionId)
    return api.post('/documents/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
      timeout: 120000,
    })
  },
  getDocuments(sessionId = null, page = 1, pageSize = 20) {
    const params = { page, page_size: pageSize }
    if (sessionId) params.session_id = sessionId
    return api.get('/documents', { params })
  },
  deleteDocument(documentId) {
    return api.delete(`/documents/${documentId}`)
  },
}

export default api

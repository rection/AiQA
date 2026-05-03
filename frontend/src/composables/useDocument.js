import { ref } from 'vue'
import { documentAPI } from '../api/index.js'

export function useDocument() {
  const documents = ref([])
  const isUploading = ref(false)

  async function loadDocuments(sessionId = null) {
    const { data } = await documentAPI.getDocuments(sessionId)
    documents.value = data.documents
  }

  async function uploadDocument(file, sessionId = '') {
    isUploading.value = true
    try {
      await documentAPI.upload(file, sessionId)
      await loadDocuments(sessionId || undefined)
    } finally {
      isUploading.value = false
    }
  }

  async function deleteDocument(documentId) {
    await documentAPI.deleteDocument(documentId)
    documents.value = documents.value.filter(d => d.document_id !== documentId)
  }

  return { documents, isUploading, loadDocuments, uploadDocument, deleteDocument }
}

import { defineStore } from 'pinia'
import { ref } from 'vue'
import { chatAPI } from '../api/index.js'

export const useChatStore = defineStore('chat', () => {
  const sessions = ref([])
  const currentSessionId = ref('')
  const messages = ref([])
  const isLoading = ref(false)
  const isStreaming = ref(false)
  const currentToolCalls = ref([])

  async function loadSessions() {
    const { data } = await chatAPI.getSessions()
    sessions.value = data.sessions
  }

  async function loadMessages(sessionId) {
    if (!sessionId) return
    const { data } = await chatAPI.getMessages(sessionId)
    messages.value = data.messages
    currentSessionId.value = sessionId
  }

  function newSession() {
    currentSessionId.value = ''
    messages.value = []
    currentToolCalls.value = []
  }

  async function switchSession(sessionId) {
    await loadMessages(sessionId)
  }

  async function deleteSession(sessionId) {
    await chatAPI.deleteSession(sessionId)
    sessions.value = sessions.value.filter(s => s.session_id !== sessionId)
    if (currentSessionId.value === sessionId) {
      newSession()
    }
  }

  function addUserMessage(content) {
    messages.value.push({
      message_id: `temp-${Date.now()}`,
      role: 'user',
      content,
      created_at: new Date().toISOString(),
    })
  }

  function addAssistantPlaceholder() {
    messages.value.push({
      message_id: `streaming-${Date.now()}`,
      role: 'assistant',
      content: '',
      tool_calls: [],
      created_at: new Date().toISOString(),
    })
  }

  function appendAnswer(content) {
    const last = messages.value[messages.value.length - 1]
    if (last && last.role === 'assistant') {
      last.content += content
    }
  }

  function addToolCall(toolInfo) {
    currentToolCalls.value.push(toolInfo)
  }

  function clearToolCalls() {
    currentToolCalls.value = []
  }

  return {
    sessions,
    currentSessionId,
    messages,
    isLoading,
    isStreaming,
    currentToolCalls,
    loadSessions,
    loadMessages,
    newSession,
    switchSession,
    deleteSession,
    addUserMessage,
    addAssistantPlaceholder,
    appendAnswer,
    addToolCall,
    clearToolCalls,
  }
})

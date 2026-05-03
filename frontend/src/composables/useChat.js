import { useChatStore } from '../stores/chat.js'
import { useSSE } from './useSSE.js'

export function useChat() {
  const store = useChatStore()
  const { connect } = useSSE()

  async function sendMessage(message) {
    if (!message.trim() || store.isStreaming) return

    store.isLoading = true
    store.isStreaming = true
    store.clearToolCalls()
    store.addUserMessage(message)
    store.addAssistantPlaceholder()

    await connect('/api/chat/stream', {
      session_id: store.currentSessionId,
      message,
      stream: true,
    }, {
      onSession(data) {
        store.currentSessionId = data.session_id
      },
      onToolCall(data) {
        store.addToolCall({ ...data, status: 'running' })
      },
      onToolResult(data) {
        const idx = store.currentToolCalls.findIndex(t => t.tool === data.tool)
        if (idx >= 0) store.currentToolCalls[idx].status = 'done'
      },
      onAnswer(data) {
        store.appendAnswer(data.content)
      },
      onDone() {
        store.isStreaming = false
        store.isLoading = false
        store.loadSessions()
      },
      onError(data) {
        store.appendAnswer(`\n\n> 错误：${data.message}`)
        store.isStreaming = false
        store.isLoading = false
      },
    })
  }

  return { sendMessage }
}

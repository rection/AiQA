<template>
  <div class="chat-view">
    <Sidebar
      :sessions="store.sessions"
      :current-id="store.currentSessionId"
      @new-session="store.newSession"
      @switch-session="store.switchSession"
      @delete-session="store.deleteSession"
      @toggle-docs="showDocPanel = !showDocPanel"
    />

    <ChatArea
      :messages="store.messages"
      :is-streaming="store.isStreaming"
      :current-tool-calls="store.currentToolCalls"
      @send="handleSend"
      @upload="handleUpload"
    />

    <DocumentPanel
      :visible="showDocPanel"
      :documents="docStore.documents"
      :is-uploading="docStore.isUploading"
      @close="showDocPanel = false"
      @upload="handleDocUpload"
      @delete="docStore.deleteDocument"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import Sidebar from '../components/Sidebar.vue'
import ChatArea from '../components/ChatArea.vue'
import DocumentPanel from '../components/DocumentPanel.vue'
import { useChatStore } from '../stores/chat.js'
import { useChat } from '../composables/useChat.js'
import { useDocument } from '../composables/useDocument.js'

const store = useChatStore()
const docStore = useDocument()
const { sendMessage } = useChat()
const showDocPanel = ref(false)

onMounted(() => {
  store.loadSessions()
  docStore.loadDocuments()
})

function handleSend(message) {
  sendMessage(message)
}

function handleUpload(file) {
  docStore.uploadDocument(file, store.currentSessionId)
}

function handleDocUpload(file) {
  docStore.uploadDocument(file, store.currentSessionId)
}
</script>

<style scoped>
.chat-view {
  display: flex;
  width: 100%;
  height: 100vh;
}
</style>

<template>
  <div class="chat-area">
    <div class="messages-container" ref="messagesRef">
      <div v-if="!messages.length" class="welcome">
        <div class="welcome-icon">AI</div>
        <h2>AI 问答助手</h2>
        <p>上传文档开始问答，或直接提问</p>
      </div>

      <MessageBubble
        v-for="msg in messages"
        :key="msg.message_id"
        :message="msg"
        :is-streaming="isStreaming && msg === messages[messages.length - 1]"
      />

      <ToolIndicator :tool-calls="currentToolCalls" />
    </div>

    <InputBox
      :disabled="isStreaming"
      @send="$emit('send', $event)"
      @upload="$emit('upload', $event)"
    />
  </div>
</template>

<script setup>
import { ref, watch, nextTick } from 'vue'
import MessageBubble from './MessageBubble.vue'
import ToolIndicator from './ToolIndicator.vue'
import InputBox from './InputBox.vue'

const props = defineProps({
  messages: { type: Array, default: () => [] },
  isStreaming: { type: Boolean, default: false },
  currentToolCalls: { type: Array, default: () => [] },
})

defineEmits(['send', 'upload'])

const messagesRef = ref(null)

watch(
  () => props.messages.length + (props.messages[props.messages.length - 1]?.content?.length || 0),
  async () => {
    await nextTick()
    if (messagesRef.value) {
      messagesRef.value.scrollTop = messagesRef.value.scrollHeight
    }
  }
)
</script>

<style scoped>
.chat-area {
  flex: 1;
  display: flex;
  flex-direction: column;
  height: 100%;
  min-width: 0;
}
.messages-container {
  flex: 1;
  overflow-y: auto;
  padding: 20px 24px;
}
.welcome {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: var(--text-muted);
}
.welcome-icon {
  width: 64px;
  height: 64px;
  background: var(--accent-gradient);
  border-radius: var(--radius-lg);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  font-weight: 700;
  color: #fff;
  margin-bottom: 16px;
}
.welcome h2 {
  font-size: 22px;
  color: var(--text-primary);
  margin-bottom: 8px;
}
.welcome p {
  font-size: 14px;
}
</style>

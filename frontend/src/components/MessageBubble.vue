<template>
  <div :class="['message', message.role]">
    <div class="avatar">
      <span v-if="message.role === 'user'">U</span>
      <span v-else class="ai-avatar">AI</span>
    </div>
    <div class="bubble">
      <MarkdownRenderer v-if="message.role === 'assistant'" :content="message.content" />
      <div v-else class="user-content">{{ message.content }}</div>

      <div v-if="message.tool_calls?.length" class="tool-calls">
        <div v-for="(tc, i) in message.tool_calls" :key="i" class="tool-call-item">
          <span class="tool-name">{{ tc.tool }}</span>
          <span class="tool-output">{{ tc.output?.slice(0, 100) }}...</span>
        </div>
      </div>

      <div v-if="isStreaming && message.role === 'assistant' && !message.content" class="typing-indicator">
        <span></span><span></span><span></span>
      </div>
    </div>
  </div>
</template>

<script setup>
import MarkdownRenderer from './MarkdownRenderer.vue'

defineProps({
  message: { type: Object, required: true },
  isStreaming: { type: Boolean, default: false },
})
</script>

<style scoped>
.message {
  display: flex;
  gap: 14px;
  padding: 20px 0;
  max-width: 800px;
  margin: 0 auto;
}
.message.user {
  flex-direction: row-reverse;
}
.avatar {
  width: 36px;
  height: 36px;
  border-radius: var(--radius-sm);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 13px;
  flex-shrink: 0;
}
.user .avatar {
  background: var(--bg-tertiary);
  color: var(--text-secondary);
}
.ai-avatar {
  background: var(--accent-gradient);
  color: #fff;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--radius-sm);
}
.bubble {
  max-width: 75%;
  padding: 14px 18px;
  border-radius: var(--radius-lg);
  background: var(--bg-tertiary);
}
.user .bubble {
  background: rgba(102, 126, 234, 0.15);
  border: 1px solid rgba(102, 126, 234, 0.2);
}
.user-content {
  font-size: 14px;
  line-height: 1.6;
  white-space: pre-wrap;
}
.tool-calls {
  margin-top: 10px;
  padding-top: 10px;
  border-top: 1px solid var(--border-color);
}
.tool-call-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
  color: var(--text-muted);
  margin-bottom: 4px;
}
.tool-name {
  background: rgba(102, 126, 234, 0.1);
  color: var(--accent-primary);
  padding: 2px 8px;
  border-radius: 4px;
  font-family: monospace;
}
.typing-indicator {
  display: flex;
  gap: 4px;
  padding: 8px 0;
}
.typing-indicator span {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--accent-primary);
  animation: bounce 1.4s infinite ease-in-out both;
}
.typing-indicator span:nth-child(1) { animation-delay: -0.32s; }
.typing-indicator span:nth-child(2) { animation-delay: -0.16s; }
@keyframes bounce {
  0%, 80%, 100% { transform: scale(0); opacity: 0.4; }
  40% { transform: scale(1); opacity: 1; }
}
</style>

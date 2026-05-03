<template>
  <div class="input-container">
    <div class="input-box">
      <button class="upload-btn" @click="triggerUpload" :disabled="disabled">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M21.44 11.05l-9.19 9.19a6 6 0 0 1-8.49-8.49l9.19-9.19a4 4 0 0 1 5.66 5.66l-9.2 9.19a2 2 0 0 1-2.83-2.83l8.49-8.48"/>
        </svg>
      </button>
      <input type="file" ref="fileInput" @change="onFileSelected" style="display:none" />
      <textarea
        ref="textareaRef"
        v-model="inputText"
        :placeholder="placeholder"
        :disabled="disabled"
        rows="1"
        @keydown.enter.exact.prevent="handleSend"
        @input="autoResize"
      ></textarea>
      <button class="send-btn" @click="handleSend" :disabled="disabled || !inputText.trim()">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
          <path d="M22 2L11 13" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
          <path d="M22 2L15 22L11 13L2 9L22 2Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  disabled: { type: Boolean, default: false },
  placeholder: { type: String, default: '输入消息...' },
})

const emit = defineEmits(['send', 'upload'])

const inputText = ref('')
const textareaRef = ref(null)
const fileInput = ref(null)

function handleSend() {
  if (!inputText.value.trim() || props.disabled) return
  emit('send', inputText.value.trim())
  inputText.value = ''
  if (textareaRef.value) {
    textareaRef.value.style.height = 'auto'
  }
}

function autoResize() {
  const el = textareaRef.value
  if (!el) return
  el.style.height = 'auto'
  el.style.height = Math.min(el.scrollHeight, 150) + 'px'
}

function triggerUpload() {
  fileInput.value?.click()
}

function onFileSelected(e) {
  const file = e.target.files[0]
  if (file) {
    emit('upload', file)
    e.target.value = ''
  }
}
</script>

<style scoped>
.input-container {
  padding: 16px 24px 20px;
  max-width: 850px;
  margin: 0 auto;
  width: 100%;
}
.input-box {
  display: flex;
  align-items: flex-end;
  gap: 8px;
  background: var(--bg-secondary);
  border: 1px solid var(--border-glass);
  border-radius: var(--radius-lg);
  padding: 10px 14px;
  transition: border-color 0.2s, box-shadow 0.2s;
}
.input-box:focus-within {
  border-color: var(--accent-primary);
  box-shadow: var(--shadow-glow);
}
textarea {
  flex: 1;
  background: transparent;
  color: var(--text-primary);
  font-size: 14px;
  line-height: 1.5;
  resize: none;
  max-height: 150px;
  padding: 4px 0;
}
textarea::placeholder {
  color: var(--text-muted);
}
.upload-btn,
.send-btn {
  width: 36px;
  height: 36px;
  border-radius: var(--radius-sm);
  background: transparent;
  color: var(--text-muted);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
  flex-shrink: 0;
}
.upload-btn:hover,
.send-btn:hover {
  color: var(--accent-primary);
  background: var(--bg-hover);
}
.send-btn {
  background: var(--accent-gradient);
  color: #fff;
}
.send-btn:hover {
  opacity: 0.9;
  background: var(--accent-gradient);
  color: #fff;
}
.send-btn:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}
.upload-btn:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}
</style>

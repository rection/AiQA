<template>
  <aside class="sidebar">
    <div class="sidebar-header">
      <div class="logo">
        <span class="logo-icon">AI</span>
        <span class="logo-text">问答助手</span>
      </div>
      <button class="new-chat-btn" @click="$emit('new-session')">
        <span class="plus">+</span> 新对话
      </button>
    </div>

    <div class="session-list">
      <div
        v-for="session in sessions"
        :key="session.session_id"
        :class="['session-item', { active: session.session_id === currentId }]"
        @click="$emit('switch-session', session.session_id)"
      >
        <span class="session-title">{{ session.title || '新对话' }}</span>
        <button
          class="delete-btn"
          @click.stop="$emit('delete-session', session.session_id)"
        >x</button>
      </div>
    </div>

    <div class="sidebar-footer">
      <button class="doc-btn" @click="$emit('toggle-docs')">文档管理</button>
    </div>
  </aside>
</template>

<script setup>
defineProps({
  sessions: { type: Array, default: () => [] },
  currentId: { type: String, default: '' },
})
defineEmits(['new-session', 'switch-session', 'delete-session', 'toggle-docs'])
</script>

<style scoped>
.sidebar {
  width: var(--sidebar-width);
  height: 100%;
  background: var(--bg-secondary);
  border-right: 1px solid var(--border-color);
  display: flex;
  flex-direction: column;
  flex-shrink: 0;
}
.sidebar-header {
  padding: 16px;
  border-bottom: 1px solid var(--border-color);
}
.logo {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 14px;
}
.logo-icon {
  width: 36px;
  height: 36px;
  background: var(--accent-gradient);
  border-radius: var(--radius-sm);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 14px;
  color: #fff;
}
.logo-text {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
}
.new-chat-btn {
  width: 100%;
  padding: 10px;
  background: var(--bg-tertiary);
  border: 1px solid var(--border-glass);
  border-radius: var(--radius-sm);
  color: var(--text-primary);
  font-size: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  transition: all 0.2s;
}
.new-chat-btn:hover {
  background: var(--bg-hover);
  border-color: var(--accent-primary);
}
.plus {
  font-size: 18px;
  color: var(--accent-primary);
}
.session-list {
  flex: 1;
  overflow-y: auto;
  padding: 8px;
}
.session-item {
  padding: 10px 12px;
  border-radius: var(--radius-sm);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 2px;
  transition: background 0.15s;
}
.session-item:hover {
  background: var(--bg-hover);
}
.session-item.active {
  background: rgba(102, 126, 234, 0.15);
}
.session-title {
  font-size: 13px;
  color: var(--text-secondary);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  flex: 1;
}
.session-item.active .session-title {
  color: var(--text-primary);
}
.delete-btn {
  opacity: 0;
  background: none;
  color: var(--text-muted);
  font-size: 12px;
  padding: 2px 6px;
  border-radius: 4px;
  transition: opacity 0.15s;
}
.session-item:hover .delete-btn {
  opacity: 1;
}
.delete-btn:hover {
  color: #ff6b6b;
}
.sidebar-footer {
  padding: 12px 16px;
  border-top: 1px solid var(--border-color);
}
.doc-btn {
  width: 100%;
  padding: 10px;
  background: transparent;
  border: 1px solid var(--border-glass);
  border-radius: var(--radius-sm);
  color: var(--text-secondary);
  font-size: 13px;
  transition: all 0.2s;
}
.doc-btn:hover {
  background: var(--bg-hover);
  color: var(--text-primary);
  border-color: var(--accent-primary);
}
</style>

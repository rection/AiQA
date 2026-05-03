<template>
  <div v-if="toolCalls.length" class="tool-indicators">
    <div v-for="(tc, i) in toolCalls" :key="i" class="tool-indicator">
      <span class="tool-dot" :class="{ done: tc.status === 'done' }"></span>
      <span class="tool-label">{{ getToolLabel(tc.tool) }}</span>
      <span class="tool-status">{{ tc.status === 'done' ? '完成' : '执行中...' }}</span>
    </div>
  </div>
</template>

<script setup>
defineProps({
  toolCalls: { type: Array, default: () => [] },
})

function getToolLabel(name) {
  const labels = {
    rag_search: '文档检索',
    web_search: '网络搜索',
    mysql_query: '数据库查询',
  }
  return labels[name] || name
}
</script>

<style scoped>
.tool-indicators {
  max-width: 800px;
  margin: 0 auto;
  padding: 0 50px;
}
.tool-indicator {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px 12px;
  margin-bottom: 4px;
  font-size: 12px;
  color: var(--text-muted);
  background: rgba(22, 33, 62, 0.5);
  border-radius: var(--radius-sm);
  border-left: 2px solid var(--accent-primary);
}
.tool-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--accent-primary);
  animation: pulse 1.5s infinite;
}
.tool-dot.done {
  animation: none;
  background: #4ade80;
}
.tool-label {
  color: var(--accent-primary);
  font-weight: 500;
}
@keyframes pulse {
  0%, 100% { opacity: 0.4; }
  50% { opacity: 1; }
}
</style>

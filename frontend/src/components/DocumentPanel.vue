<template>
  <aside v-if="visible" class="doc-panel">
    <div class="panel-header">
      <h3>文档管理</h3>
      <button class="close-btn" @click="$emit('close')">x</button>
    </div>

    <div class="upload-area" @dragover.prevent @drop.prevent="onDrop">
      <input type="file" ref="fileInputEl" @change="onFileChange" style="display:none"
        accept=".pdf,.docx,.md,.txt,.csv" />
      <button class="upload-trigger" @click="fileInputEl?.click()" :disabled="isUploading">
        <span v-if="isUploading">上传中...</span>
        <span v-else>点击或拖拽上传文档</span>
        <small>支持 PDF/Word/Markdown/TXT/CSV</small>
      </button>
    </div>

    <div class="doc-list">
      <div v-for="doc in documents" :key="doc.document_id" class="doc-item">
        <div class="doc-icon">{{ getFileIcon(doc.file_type) }}</div>
        <div class="doc-info">
          <div class="doc-name">{{ doc.filename }}</div>
          <div class="doc-meta">
            {{ formatSize(doc.file_size) }} | {{ doc.chunk_count }} 块 |
            <span :class="['status', doc.status]">{{ getStatusText(doc.status) }}</span>
          </div>
        </div>
        <button class="doc-delete" @click="$emit('delete', doc.document_id)">x</button>
      </div>

      <div v-if="!documents.length" class="empty-docs">
        暂无文档，上传后可用于问答
      </div>
    </div>
  </aside>
</template>

<script setup>
import { ref } from 'vue'

defineProps({
  visible: { type: Boolean, default: false },
  documents: { type: Array, default: () => [] },
  isUploading: { type: Boolean, default: false },
})

const emit = defineEmits(['close', 'upload', 'delete'])

const fileInputEl = ref(null)

function onFileChange(e) {
  const file = e.target.files[0]
  if (file) emit('upload', file)
  e.target.value = ''
}

function onDrop(e) {
  const file = e.dataTransfer.files[0]
  if (file) emit('upload', file)
}

function getFileIcon(type) {
  const icons = { pdf: 'PDF', docx: 'DOC', md: 'MD', txt: 'TXT', csv: 'CSV' }
  return icons[type] || 'FILE'
}

function formatSize(bytes) {
  if (bytes < 1024) return bytes + ' B'
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB'
  return (bytes / (1024 * 1024)).toFixed(1) + ' MB'
}

function getStatusText(status) {
  return { processing: '处理中', indexed: '已就绪', failed: '失败' }[status] || status
}
</script>

<style scoped>
.doc-panel {
  width: var(--doc-panel-width);
  height: 100%;
  background: var(--bg-secondary);
  border-left: 1px solid var(--border-color);
  display: flex;
  flex-direction: column;
  flex-shrink: 0;
}
.panel-header {
  padding: 16px;
  border-bottom: 1px solid var(--border-color);
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.panel-header h3 {
  font-size: 15px;
  font-weight: 600;
}
.close-btn {
  background: none;
  color: var(--text-muted);
  font-size: 14px;
  padding: 4px 8px;
  border-radius: 4px;
}
.close-btn:hover {
  background: var(--bg-hover);
}
.upload-area {
  padding: 12px;
}
.upload-trigger {
  width: 100%;
  padding: 20px;
  background: var(--bg-tertiary);
  border: 1px dashed var(--border-glass);
  border-radius: var(--radius-md);
  color: var(--text-secondary);
  font-size: 13px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  transition: all 0.2s;
}
.upload-trigger:hover {
  border-color: var(--accent-primary);
  background: var(--bg-hover);
}
.upload-trigger small {
  color: var(--text-muted);
  font-size: 11px;
}
.doc-list {
  flex: 1;
  overflow-y: auto;
  padding: 8px 12px;
}
.doc-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px;
  border-radius: var(--radius-sm);
  margin-bottom: 4px;
  transition: background 0.15s;
}
.doc-item:hover {
  background: var(--bg-hover);
}
.doc-icon {
  width: 36px;
  height: 36px;
  background: rgba(102, 126, 234, 0.1);
  color: var(--accent-primary);
  border-radius: var(--radius-sm);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 10px;
  font-weight: 700;
  flex-shrink: 0;
}
.doc-info {
  flex: 1;
  min-width: 0;
}
.doc-name {
  font-size: 13px;
  color: var(--text-primary);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.doc-meta {
  font-size: 11px;
  color: var(--text-muted);
  margin-top: 2px;
}
.status.indexed { color: #4ade80; }
.status.processing { color: #fbbf24; }
.status.failed { color: #f87171; }
.doc-delete {
  opacity: 0;
  background: none;
  color: var(--text-muted);
  font-size: 12px;
  padding: 4px;
}
.doc-item:hover .doc-delete { opacity: 1; }
.doc-delete:hover { color: #f87171; }
.empty-docs {
  text-align: center;
  padding: 40px 20px;
  color: var(--text-muted);
  font-size: 13px;
}
</style>

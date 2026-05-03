<template>
  <div class="markdown-body" v-html="rendered"></div>
</template>

<script setup>
import { computed } from 'vue'
import MarkdownIt from 'markdown-it'
import hljs from 'highlight.js'
import 'highlight.js/styles/atom-one-dark.css'

const props = defineProps({
  content: { type: String, default: '' },
})

const md = new MarkdownIt({
  html: true,
  linkify: true,
  typographer: true,
  highlight(str, lang) {
    if (lang && hljs.getLanguage(lang)) {
      try {
        return `<pre class="hljs"><code class="language-${lang}">${
          hljs.highlight(str, { language: lang, ignoreIllegals: true }).value
        }</code></pre>`
      } catch (_) {}
    }
    return `<pre class="hljs"><code>${md.utils.escapeHtml(str)}</code></pre>`
  },
})

const rendered = computed(() => md.render(props.content || ''))
</script>

<style scoped>
.markdown-body {
  line-height: 1.7;
  font-size: 14px;
  color: var(--text-primary);
}
.markdown-body :deep(h1),
.markdown-body :deep(h2),
.markdown-body :deep(h3) {
  margin: 16px 0 8px;
  font-weight: 600;
}
.markdown-body :deep(p) {
  margin: 8px 0;
}
.markdown-body :deep(pre) {
  background: #1e1e2e;
  border-radius: var(--radius-sm);
  padding: 14px;
  overflow-x: auto;
  margin: 12px 0;
}
.markdown-body :deep(code) {
  font-family: 'JetBrains Mono', 'Fira Code', monospace;
  font-size: 13px;
}
.markdown-body :deep(p code) {
  background: rgba(102, 126, 234, 0.15);
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 13px;
}
.markdown-body :deep(table) {
  width: 100%;
  border-collapse: collapse;
  margin: 12px 0;
}
.markdown-body :deep(th),
.markdown-body :deep(td) {
  border: 1px solid var(--border-color);
  padding: 8px 12px;
  text-align: left;
}
.markdown-body :deep(th) {
  background: var(--bg-tertiary);
  font-weight: 600;
}
.markdown-body :deep(blockquote) {
  border-left: 3px solid var(--accent-primary);
  padding-left: 12px;
  margin: 12px 0;
  color: var(--text-secondary);
}
.markdown-body :deep(ul),
.markdown-body :deep(ol) {
  padding-left: 20px;
  margin: 8px 0;
}
.markdown-body :deep(a) {
  color: var(--accent-primary);
}
</style>

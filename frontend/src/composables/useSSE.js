export function useSSE() {
  async function connect(url, body, callbacks) {
    const response = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    })

    if (!response.ok) {
      const err = await response.json().catch(() => ({ detail: '请求失败' }))
      callbacks.onError?.({ code: 'HTTP_ERROR', message: err.detail || '请求失败' })
      return
    }

    const reader = response.body.getReader()
    const decoder = new TextDecoder()
    let buffer = ''

    while (true) {
      const { done, value } = await reader.read()
      if (done) break

      buffer += decoder.decode(value, { stream: true })

      const events = buffer.split('\n\n')
      buffer = events.pop() || ''

      for (const rawEvent of events) {
        const lines = rawEvent.split('\n')
        let eventType = ''
        let data = ''

        for (const line of lines) {
          if (line.startsWith('event: ')) {
            eventType = line.slice(7).trim()
          } else if (line.startsWith('data: ')) {
            data = line.slice(6)
          }
        }

        if (!eventType || !data) continue

        try {
          const parsed = JSON.parse(data)
          switch (eventType) {
            case 'session':
              callbacks.onSession?.(parsed)
              break
            case 'tool_call':
              callbacks.onToolCall?.(parsed)
              break
            case 'tool_result':
              callbacks.onToolResult?.(parsed)
              break
            case 'answer':
              callbacks.onAnswer?.(parsed)
              break
            case 'done':
              callbacks.onDone?.(parsed)
              return
            case 'error':
              callbacks.onError?.(parsed)
              return
          }
        } catch (e) {
          console.error('SSE parse error:', e, data)
        }
      }
    }
  }

  return { connect }
}

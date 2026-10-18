import { useEffect, useRef } from 'react'
import { renderMarkdown } from '../utils/markdown.js'
import './MessageList.css'

export default function MessageList({ messages, isPending }) {
  const bottomRef = useRef(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ block: 'end' })
  }, [messages, isPending])

  return (
    <div className="message-list">
      {messages.map((message) => (
        <MessageRow key={message.id} message={message} />
      ))}
      {isPending && <ThinkingRow />}
      <div ref={bottomRef} />
    </div>
  )
}

function MessageRow({ message }) {
  const isUser = message.role === 'user'
  const bubbleClass = [
    'message-bubble',
    isUser ? 'message-bubble--user' : 'message-bubble--assistant',
    message.isError ? 'message-bubble--error' : '',
  ]
    .filter(Boolean)
    .join(' ')

  return (
    <div className={`message-list__row${isUser ? ' message-list__row--end' : ''}`}>
      {isUser ? (
        <div className={bubbleClass}>{message.text}</div>
      ) : (
        <div
          className={bubbleClass}
          // Markdown is rendered then sanitized by DOMPurify in
          // utils/markdown.js before it ever reaches the DOM.
          dangerouslySetInnerHTML={{ __html: renderMarkdown(message.text) }}
        />
      )}
    </div>
  )
}

function ThinkingRow() {
  return (
    <div className="message-list__row">
      <div className="message-bubble message-bubble--assistant message-bubble--thinking" aria-label="Assistant is thinking">
        <span className="thinking-dot" />
        <span className="thinking-dot" />
        <span className="thinking-dot" />
      </div>
    </div>
  )
}

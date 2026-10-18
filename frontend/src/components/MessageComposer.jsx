import { useState } from 'react'
import SendIcon from '../icons/SendIcon.jsx'
import { MAX_WORDS, countWords, isSubmittable } from '../utils/text.js'
import './MessageComposer.css'

export default function MessageComposer({ onSend, disabled = false }) {
  const [text, setText] = useState('')
  const wordCount = countWords(text)
  const canSubmit = isSubmittable(text) && !disabled

  function handleChange(event) {
    const nextValue = event.target.value
    // Once the 500-word cap would be exceeded, reject the change outright
    // (typed keystroke or paste) instead of truncating -- this never cuts
    // off a word the user is still in the middle of typing.
    if (countWords(nextValue) > MAX_WORDS) return
    setText(nextValue)
  }

  function handleSubmit() {
    if (disabled) return
    const trimmed = text.trim()
    if (!trimmed) return
    onSend(trimmed)
    setText('')
  }

  function handleKeyDown(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault()
      handleSubmit()
    }
    // Shift+Enter falls through to the textarea's default behavior (newline).
  }

  return (
    <div className="composer">
      <div className="composer__box">
        <textarea
          className="composer__textarea"
          value={text}
          placeholder={disabled ? 'Waiting for a reply…' : 'Type a message…'}
          rows={1}
          disabled={disabled}
          onChange={handleChange}
          onKeyDown={handleKeyDown}
        />
        <div className="composer__footer">
          <span className="composer__count">
            {wordCount} / {MAX_WORDS} words
          </span>
          <button
            type="button"
            className="composer__send"
            onClick={handleSubmit}
            disabled={!canSubmit}
            aria-label="Send message"
          >
            <SendIcon />
          </button>
        </div>
      </div>
    </div>
  )
}

// Shared text helpers for the chat UI: word counting, submission validation,
// and sidebar title generation. Kept framework-free and pure so they're easy
// to reason about and (if ever needed) unit test in isolation.

export const MAX_WORDS = 500
const TITLE_WORD_LIMIT = 6

/**
 * Splits trimmed text on runs of whitespace (spaces, tabs, newlines) and
 * counts the resulting tokens. Multiple spaces / line breaks collapse into
 * a single separator, so they never inflate the count. Empty/whitespace-only
 * input counts as 0.
 */
export function countWords(text) {
  const trimmed = text.trim()
  if (!trimmed) return 0
  return trimmed.split(/\s+/).length
}

/** True if the text has at least one non-whitespace character. */
export function isSubmittable(text) {
  return text.trim().length > 0
}

/**
 * Generates a short sidebar title from a chat's first message: the first
 * TITLE_WORD_LIMIT words, with a trailing ellipsis if the message had more.
 */
export function deriveChatTitle(text) {
  const words = text.trim().split(/\s+/)
  if (words.length <= TITLE_WORD_LIMIT) {
    return words.join(' ')
  }
  return `${words.slice(0, TITLE_WORD_LIMIT).join(' ')}…`
}

/** Small unique-enough id generator for client-only, in-memory state. */
export function makeId() {
  return `${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 9)}`
}

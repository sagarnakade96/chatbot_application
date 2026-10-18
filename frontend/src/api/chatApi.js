// Talks to the backend's basic_chatbot app:
// POST {API_BASE_URL}/basic-chatbot/chat  { message, history } -> { reply }
// See backend/app/apps/basic_chatbot/router.py for the actual contract.

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1'

/**
 * Sends one chat turn to the backend and returns the assistant's reply text.
 *
 * @param {string} message - the new user message
 * @param {{role: 'user'|'assistant', content: string}[]} history - prior
 *   turns, oldest first (the backend graph has no memory of its own)
 * @returns {Promise<string>}
 */
export async function sendChatMessage(message, history) {
  let response
  try {
    response = await fetch(`${API_BASE_URL}/basic-chatbot/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message, history }),
    })
  } catch {
    throw new Error('Could not reach the backend. Is it running?')
  }

  if (!response.ok) {
    throw new Error(await extractErrorDetail(response))
  }

  const data = await response.json()
  return data.reply
}

async function extractErrorDetail(response) {
  try {
    const data = await response.json()
    if (typeof data.detail === 'string') return data.detail
    if (Array.isArray(data.detail)) {
      return data.detail.map((item) => item.msg).join('; ')
    }
  } catch {
    // response body wasn't JSON -- fall through to the generic message
  }
  return `Request failed (${response.status})`
}

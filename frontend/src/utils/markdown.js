import { marked } from 'marked'
import DOMPurify from 'dompurify'

marked.setOptions({ gfm: true, breaks: true })

/**
 * Renders LLM-reply markdown to sanitized HTML. DOMPurify strips any raw
 * script/event-handler markup that could otherwise slip through from a
 * model response, so this is safe to feed into dangerouslySetInnerHTML.
 */
export function renderMarkdown(text) {
  const html = marked.parse(text ?? '')
  return DOMPurify.sanitize(html)
}

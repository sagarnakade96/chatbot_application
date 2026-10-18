import MessageList from './MessageList.jsx'
import MessageComposer from './MessageComposer.jsx'
import './ChatWindow.css'

export default function ChatWindow({ activeChatId, messages, isPending, onSend }) {
  return (
    <section className="chat-window">
      <header className="chat-window__header">
        <h1>AI Assistant</h1>
      </header>

      <MessageList messages={messages} isPending={isPending} />

      {/* Remounting on chat switch clears any unsent draft text, so typing
          in one chat never leaks into another (including "New chat"). */}
      <MessageComposer key={activeChatId ?? 'draft'} onSend={onSend} disabled={isPending} />
    </section>
  )
}

import { useMemo, useState } from 'react'
import Sidebar from './Sidebar.jsx'
import ChatWindow from './ChatWindow.jsx'
import { sendChatMessage } from '../api/chatApi.js'
import { deriveChatTitle, makeId } from '../utils/text.js'
import './ChatLayout.css'

/**
 * Owns all chat state for the app (chats, which one is active, and each
 * chat's pending/sending status) and wires the sidebar to the chat window.
 * Everything lives in React state only -- nothing is persisted, so a
 * refresh resets the chats, by design.
 */
export default function ChatLayout() {
  const [chats, setChats] = useState([])
  // null = a fresh, not-yet-created chat ("New chat" state / initial load).
  const [activeChatId, setActiveChatId] = useState(null)

  const activeChat = useMemo(
    () => chats.find((chat) => chat.id === activeChatId) ?? null,
    [chats, activeChatId],
  )

  function handleNewChat() {
    setActiveChatId(null)
  }

  function handleSelectChat(chatId) {
    setActiveChatId(chatId)
  }

  function handleDeleteChat(chatId) {
    setChats((prev) => prev.filter((chat) => chat.id !== chatId))
    setActiveChatId((prev) => (prev === chatId ? null : prev))
  }

  async function handleSend(text) {
    const userMessage = { id: makeId(), role: 'user', text }
    let targetChatId = activeChatId
    let historyForApi = []

    if (activeChatId === null) {
      const newChat = {
        id: makeId(),
        title: deriveChatTitle(text),
        messages: [userMessage],
        pending: true,
      }
      targetChatId = newChat.id
      setChats((prev) => [newChat, ...prev])
      setActiveChatId(newChat.id)
    } else {
      setChats((prev) =>
        prev.map((chat) => {
          if (chat.id !== activeChatId) return chat
          // Captured here, inside the updater, so it reflects this chat's
          // messages at the moment of sending -- not a stale closure value.
          historyForApi = chat.messages
            .filter((message) => !message.isError)
            .map((message) => ({ role: message.role, content: message.text }))
          return { ...chat, messages: [...chat.messages, userMessage], pending: true }
        }),
      )
    }

    try {
      const reply = await sendChatMessage(text, historyForApi)
      appendAssistantMessage(targetChatId, { id: makeId(), role: 'assistant', text: reply })
    } catch (error) {
      appendAssistantMessage(targetChatId, {
        id: makeId(),
        role: 'assistant',
        text: error.message || 'Something went wrong. Please try again.',
        isError: true,
      })
    }
  }

  function appendAssistantMessage(chatId, message) {
    setChats((prev) =>
      prev.map((chat) =>
        chat.id === chatId
          ? { ...chat, pending: false, messages: [...chat.messages, message] }
          : chat,
      ),
    )
  }

  return (
    <div className="chat-layout">
      <Sidebar
        chats={chats}
        activeChatId={activeChatId}
        onNewChat={handleNewChat}
        onSelectChat={handleSelectChat}
        onDeleteChat={handleDeleteChat}
      />
      <ChatWindow
        activeChatId={activeChatId}
        messages={activeChat?.messages ?? []}
        isPending={activeChat?.pending ?? false}
        onSend={handleSend}
      />
    </div>
  )
}

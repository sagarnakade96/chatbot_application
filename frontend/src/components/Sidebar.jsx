import { useState } from 'react'
import PlusIcon from '../icons/PlusIcon.jsx'
import TrashIcon from '../icons/TrashIcon.jsx'
import CheckIcon from '../icons/CheckIcon.jsx'
import XIcon from '../icons/XIcon.jsx'
import './Sidebar.css'

export default function Sidebar({ chats, activeChatId, onNewChat, onSelectChat, onDeleteChat }) {
  // Two-step delete: clicking the trash icon on a chat arms it; a second
  // click (the check) actually deletes it, or the x cancels.
  const [pendingDeleteId, setPendingDeleteId] = useState(null)

  function handleNewChat() {
    setPendingDeleteId(null)
    onNewChat()
  }

  function handleSelectChat(chatId) {
    setPendingDeleteId(null)
    onSelectChat(chatId)
  }

  return (
    <aside className="sidebar">
      <button type="button" className="sidebar__new-chat" onClick={handleNewChat}>
        <PlusIcon />
        <span>New chat</span>
      </button>

      <h2 className="sidebar__heading">Recent chats</h2>

      <nav className="sidebar__list" aria-label="Recent chats">
        {chats.map((chat) => {
          const isActive = chat.id === activeChatId
          const isPendingDelete = chat.id === pendingDeleteId

          return (
            <div
              key={chat.id}
              className={`sidebar__item${isActive ? ' sidebar__item--active' : ''}`}
            >
              <button
                type="button"
                className="sidebar__item-label"
                aria-current={isActive ? 'true' : undefined}
                onClick={() => handleSelectChat(chat.id)}
              >
                {chat.title}
              </button>

              {isPendingDelete ? (
                <span className="sidebar__item-confirm">
                  <button
                    type="button"
                    className="sidebar__item-action sidebar__item-action--confirm"
                    aria-label={`Confirm delete "${chat.title}"`}
                    onClick={(event) => {
                      event.stopPropagation()
                      onDeleteChat(chat.id)
                      setPendingDeleteId(null)
                    }}
                  >
                    <CheckIcon />
                  </button>
                  <button
                    type="button"
                    className="sidebar__item-action"
                    aria-label="Cancel delete"
                    onClick={(event) => {
                      event.stopPropagation()
                      setPendingDeleteId(null)
                    }}
                  >
                    <XIcon />
                  </button>
                </span>
              ) : (
                <button
                  type="button"
                  className="sidebar__item-action sidebar__item-delete"
                  aria-label={`Delete "${chat.title}"`}
                  onClick={(event) => {
                    event.stopPropagation()
                    setPendingDeleteId(chat.id)
                  }}
                >
                  <TrashIcon />
                </button>
              )}
            </div>
          )
        })}
      </nav>
    </aside>
  )
}

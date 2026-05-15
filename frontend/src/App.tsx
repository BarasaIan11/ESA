import React, { useState, useCallback } from 'react'
import { Layout } from './components/layout/Layout'
import { ChatBox } from './components/chat/ChatBox'
import type { Message } from './types'

export interface Session {
  id: string
  title: string
  messages: Message[]
  createdAt: Date
}

function App() {
  const [sessions, setSessions] = useState<Session[]>([])
  const [activeSessionId, setActiveSessionId] = useState<string | null>(null)
  const [messages, setMessages] = useState<Message[]>([])
  const [backendSessionId, setBackendSessionId] = useState<string | undefined>()

  const handleNewChat = useCallback(() => {
    setMessages([])
    setActiveSessionId(null)
    setBackendSessionId(undefined)
  }, [])

  const handleSelectSession = useCallback((session: Session) => {
    setActiveSessionId(session.id)
    setMessages(session.messages)
  }, [])

  // Called by ChatBox whenever a new exchange completes
  const handleSessionUpdate = useCallback((
    newMessages: Message[],
    sessionId: string
  ) => {
    setMessages(newMessages)
    setBackendSessionId(sessionId)

    // Update or create the sidebar session entry
    setSessions(prev => {
      const existing = prev.find(s => s.id === sessionId)
      const title = newMessages.find(m => m.role === 'user')?.content.slice(0, 45) ?? 'New Chat'

      if (existing) {
        return prev.map(s => s.id === sessionId ? { ...s, messages: newMessages } : s)
      }
      const newSession: Session = {
        id: sessionId,
        title,
        messages: newMessages,
        createdAt: new Date(),
      }
      setActiveSessionId(sessionId)
      return [newSession, ...prev]
    })
  }, [])

  return (
    <Layout
      sessions={sessions}
      activeSessionId={activeSessionId}
      onNewChat={handleNewChat}
      onSelectSession={handleSelectSession}
    >
      <ChatBox
        messages={messages}
        backendSessionId={backendSessionId}
        onSessionUpdate={handleSessionUpdate}
      />
    </Layout>
  )
}

export default App

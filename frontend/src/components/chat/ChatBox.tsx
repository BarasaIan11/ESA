import React, { useState, useRef, useEffect } from 'react';
import { MessageBubble } from './MessageBubble';
import { ChatInput } from './ChatInput';
import { askQuestion } from '../../api/client';
import type { Message } from '../../types';
import { Bot } from 'lucide-react';

export const ChatBox: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [sessionId, setSessionId] = useState<string | undefined>();
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isLoading]);

  const handleSend = async (text: string) => {
    const userMsg: Message = {
      id: crypto.randomUUID(),
      role: 'user',
      content: text,
      timestamp: new Date(),
    };
    setMessages((prev) => [...prev, userMsg]);
    setIsLoading(true);

    try {
      const response = await askQuestion({ question: text, session_id: sessionId });
      setSessionId(response.session_id);

      const assistantMsg: Message = {
        id: crypto.randomUUID(),
        role: 'assistant',
        content: response.answer,
        sources: response.sources,
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, assistantMsg]);
    } catch (err) {
      const errorMsg: Message = {
        id: crypto.randomUUID(),
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please check the backend is running and try again.',
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errorMsg]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="chatbox">
      {/* Header */}
      <div className="chatbox-header">
        <div className="chatbox-header-icon">
          <Bot size={20} />
        </div>
        <div>
          <h2 className="chatbox-header-title">Business Central Assistant</h2>
          <p className="chatbox-header-subtitle">Powered by your company knowledge base</p>
        </div>
        <div className="chatbox-status">
          <span className="status-dot" />
          Online
        </div>
      </div>

      {/* Messages */}
      <div className="chatbox-messages">
        {messages.length === 0 && (
          <div className="empty-state">
            <div className="empty-state-icon">
              <Bot size={40} />
            </div>
            <h3>How can I help you today?</h3>
            <p>Ask me anything about Microsoft Dynamics 365 Business Central.</p>
            <div className="suggestion-chips">
              {[
                'How do I set up the Chart of Accounts?',
                'What are Payment Terms in BC?',
                'How do I post a General Journal?',
              ].map((s) => (
                <button key={s} className="suggestion-chip" onClick={() => handleSend(s)}>
                  {s}
                </button>
              ))}
            </div>
          </div>
        )}

        {messages.map((msg) => (
          <MessageBubble key={msg.id} message={msg} />
        ))}

        {isLoading && (
          <div className="message-row message-row--assistant">
            <div className="message-avatar message-avatar--assistant">
              <Bot size={16} />
            </div>
            <div className="message-bubble message-bubble--assistant">
              <div className="typing-indicator">
                <span /><span /><span />
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <ChatInput onSend={handleSend} disabled={isLoading} />
    </div>
  );
};

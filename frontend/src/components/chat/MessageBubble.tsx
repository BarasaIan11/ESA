import React from 'react';
import { Bot, User } from 'lucide-react';
import type { Message } from '../../types';

interface MessageBubbleProps {
  message: Message;
}

export const MessageBubble: React.FC<MessageBubbleProps> = ({ message }) => {
  const isUser = message.role === 'user';

  return (
    <div className={`message-row ${isUser ? 'message-row--user' : 'message-row--assistant'}`}>
      {/* Avatar */}
      <div className={`message-avatar ${isUser ? 'message-avatar--user' : 'message-avatar--assistant'}`}>
        {isUser ? <User size={16} /> : <Bot size={16} />}
      </div>

      {/* Bubble */}
      <div className={`message-bubble ${isUser ? 'message-bubble--user' : 'message-bubble--assistant'}`}>
        <p className="message-content">{message.content}</p>

        {/* Sources */}
        {!isUser && message.sources && message.sources.length > 0 && (
          <div className="message-sources">
            <p className="sources-label">Sources</p>
            <div className="sources-list">
              {message.sources.map((src, i) => (
                <span key={i} className="source-chip">
                  {src.substring(0, 60)}...
                </span>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

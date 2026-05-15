import React, { useState, useRef, useEffect } from 'react';
import { MessageBubble } from './MessageBubble';
import { ChatInput } from './ChatInput';
import { askQuestion } from '../../api/client';
import type { Message } from '../../types';
import { Bot, HelpCircle, FileText, CreditCard } from 'lucide-react';

interface ChatBoxProps {
  messages: Message[];
  backendSessionId: string | undefined;
  onSessionUpdate: (newMessages: Message[], sessionId: string) => void;
}

export const ChatBox: React.FC<ChatBoxProps> = ({ 
  messages, 
  backendSessionId, 
  onSessionUpdate 
}) => {
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
    
    const newMessagesAfterUser = [...messages, userMsg];
    setIsLoading(true);

    try {
      const response = await askQuestion({ 
        question: text, 
        session_id: backendSessionId 
      });

      const assistantMsg: Message = {
        id: crypto.randomUUID(),
        role: 'assistant',
        content: response.answer,
        sources: response.sources,
        timestamp: new Date(),
      };
      
      onSessionUpdate([...newMessagesAfterUser, assistantMsg], response.session_id);
    } catch (err) {
      const errorMsg: Message = {
        id: crypto.randomUUID(),
        role: 'assistant',
        content: 'System error: Communication with the intelligence gateway failed.',
        timestamp: new Date(),
      };
      onSessionUpdate([...newMessagesAfterUser, errorMsg], backendSessionId || 'error-session');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-full bg-white relative">
      {/* Header */}
      <div className="flex items-center justify-between px-8 py-4 border-b border-border-light bg-white/80 backdrop-blur-sm sticky top-0 z-10">
        <h2 className="text-base font-bold text-slate-800">Business Central Assistant</h2>
        <div className="flex items-center gap-2 px-3 py-1 rounded-full bg-slate-50 border border-slate-100 shadow-sm">
          <div className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse" />
          <span className="text-[11px] font-semibold text-slate-600">System Ready</span>
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto px-[15%] py-8">
        {messages.length === 0 && (
          <div className="flex flex-col items-center justify-center min-h-[70%] text-center max-w-2xl mx-auto">
            <div className="w-16 h-16 bg-[#99f6e4] text-[#0d9488] rounded-full flex items-center justify-center mb-6 shadow-sm">
              <Bot size={32} />
            </div>
            <h2 className="text-3xl font-bold text-slate-900 mb-3">How can I help you today?</h2>
            <p className="text-slate-500 text-base mb-10">Ask me anything about Microsoft Dynamics 365 Business Central.</p>
            
            <div className="grid grid-cols-2 gap-4 w-full">
              <div 
                className="bg-white border border-border-medium p-5 rounded-xl text-left cursor-pointer hover:border-accent-primary hover:shadow-md transition-all group" 
                onClick={() => handleSend('How do I set up the Chart of Accounts?')}
              >
                <HelpCircle className="w-6 h-6 text-accent-teal mb-3 group-hover:scale-110 transition-transform" />
                <div className="text-sm font-semibold text-slate-700">How do I set up the Chart of Accounts?</div>
              </div>
              <div 
                className="bg-white border border-border-medium p-5 rounded-xl text-left cursor-pointer hover:border-accent-primary hover:shadow-md transition-all group" 
                onClick={() => handleSend('What are Payment Terms in BC?')}
              >
                <CreditCard className="w-6 h-6 text-accent-teal mb-3 group-hover:scale-110 transition-transform" />
                <div className="text-sm font-semibold text-slate-700">What are Payment Terms in BC?</div>
              </div>
              <div 
                className="bg-white border border-border-medium p-5 rounded-xl text-left cursor-pointer hover:border-accent-primary hover:shadow-md transition-all group col-span-2" 
                onClick={() => handleSend('How do I post a General Journal?')}
              >
                <FileText className="w-6 h-6 text-accent-teal mb-3 group-hover:scale-110 transition-transform" />
                <div className="text-sm font-semibold text-slate-700">How do I post a General Journal?</div>
              </div>
            </div>
          </div>
        )}

        <div className="space-y-6">
          {messages.map((msg) => (
            <MessageBubble key={msg.id} message={msg} />
          ))}

          {isLoading && (
            <div className="flex gap-4 w-full animate-in fade-in slide-in-from-bottom-2 duration-300">
              <div className="w-8 h-8 bg-accent-primary text-white rounded-lg flex items-center justify-center shrink-0 shadow-sm">
                <Bot size={16} />
              </div>
              <div className="flex-1 bg-bg-assistant border border-border-medium p-4 rounded-xl shadow-sm max-w-[85%]">
                <div className="flex gap-1.5 items-center">
                  <span className="w-1.5 h-1.5 bg-accent-primary rounded-full animate-bounce [animation-delay:-0.3s]" />
                  <span className="w-1.5 h-1.5 bg-accent-primary rounded-full animate-bounce [animation-delay:-0.15s]" />
                  <span className="w-1.5 h-1.5 bg-accent-primary rounded-full animate-bounce" />
                </div>
              </div>
            </div>
          )}
        </div>

        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <ChatInput onSend={handleSend} disabled={isLoading} />
    </div>
  );
};

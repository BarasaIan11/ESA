import React from 'react';
import { Bot } from 'lucide-react';
import type { Message } from '../../types';

interface MessageBubbleProps {
  message: Message;
}

export const MessageBubble: React.FC<MessageBubbleProps> = ({ message }) => {
  const isUser = message.role === 'user';

  if (isUser) {
    return (
      <div className="flex justify-end w-full mb-6">
        <div className="max-w-[80%] px-4 py-2 bg-white border border-border-medium rounded-xl text-slate-700 text-[15px] shadow-sm leading-relaxed">
          {message.content}
        </div>
      </div>
    );
  }

  return (
    <div className="flex gap-4 w-full mb-8 animate-in fade-in slide-in-from-bottom-2 duration-300">
      <div className="w-8 h-8 bg-accent-primary text-white rounded-lg flex items-center justify-center shrink-0 shadow-sm mt-1">
        <Bot size={16} />
      </div>
      <div className="flex-1 bg-bg-assistant border border-border-medium p-6 rounded-xl shadow-sm max-w-[85%]">
        <div className="text-[15px] leading-relaxed text-slate-800 space-y-4">
          {message.content}
        </div>

        {message.sources && message.sources.length > 0 && (
          <div className="mt-6 pt-4 border-t border-slate-200/60">
            <p className="text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-2">Sources</p>
            <div className="flex flex-wrap gap-2">
              {message.sources.map((src, i) => (
                <span key={i} className="px-2 py-1 bg-white border border-border-light text-[10px] text-slate-500 rounded font-medium shadow-sm">
                  {src.substring(0, 50)}...
                </span>
              ))}
            </div>
          </div>
        )}
        
        <div className="flex gap-3 mt-6 pt-4 border-t border-slate-200/60">
          <button className="px-4 py-2 bg-white border border-border-medium text-xs font-semibold text-slate-600 rounded-lg hover:bg-slate-50 hover:border-slate-300 hover:text-slate-900 transition-all shadow-sm">
            Apply Customer Template
          </button>
          <button className="px-4 py-2 bg-white border border-border-medium text-xs font-semibold text-slate-600 rounded-lg hover:bg-slate-50 hover:border-slate-300 hover:text-slate-900 transition-all shadow-sm">
            Import Customers from Excel
          </button>
        </div>
      </div>
    </div>
  );
};

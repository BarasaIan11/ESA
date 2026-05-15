import React, { useState, useRef, KeyboardEvent } from 'react';
import { Send, Paperclip, Mic } from 'lucide-react';

interface ChatInputProps {
  onSend: (message: string) => void;
  disabled?: boolean;
}

export const ChatInput: React.FC<ChatInputProps> = ({ onSend, disabled }) => {
  const [value, setValue] = useState('');
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const handleSend = () => {
    const trimmed = value.trim();
    if (!trimmed || disabled) return;
    onSend(trimmed);
    setValue('');
    if (textareaRef.current) textareaRef.current.style.height = 'auto';
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleInput = () => {
    const el = textareaRef.current;
    if (!el) return;
    el.style.height = 'auto';
    el.style.height = `${Math.min(el.scrollHeight, 160)}px`;
  };

  return (
    <div className="px-[15%] pb-8 pt-4 bg-white/80 backdrop-blur-md sticky bottom-0">
      <div className="flex items-center gap-3 bg-white border border-border-medium rounded-[28px] px-5 py-2.5 shadow-sm focus-within:border-accent-primary focus-within:shadow-md transition-all">
        <button className="text-slate-400 hover:text-slate-600 transition-colors p-1" disabled={disabled}>
          <Paperclip size={20} />
        </button>
        <button className="text-slate-400 hover:text-slate-600 transition-colors p-1" disabled={disabled}>
          <Mic size={20} />
        </button>
        
        <textarea
          ref={textareaRef}
          className="flex-1 bg-transparent border-none outline-none text-[15px] text-slate-800 placeholder-slate-400 resize-none py-1.5"
          placeholder="Ask about Business Central..."
          rows={1}
          value={value}
          onChange={(e) => { setValue(e.target.value); handleInput(); }}
          onKeyDown={handleKeyDown}
          disabled={disabled}
        />

        <button
          className={`w-10 h-10 rounded-full flex items-center justify-center transition-all ${
            !value.trim() || disabled 
              ? 'bg-slate-100 text-slate-300' 
              : 'bg-accent-primary text-white hover:bg-accent-hover shadow-sm'
          }`}
          onClick={handleSend}
          disabled={!value.trim() || disabled}
        >
          <Send size={18} fill={value.trim() ? "currentColor" : "none"} />
        </button>
      </div>
      <p className="text-[11px] text-center text-slate-400 mt-4 font-medium">
        AI-generated content may be incorrect. Always verify important information.
      </p>
    </div>
  );
};

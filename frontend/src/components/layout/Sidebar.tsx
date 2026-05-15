import React from 'react';
import { Plus, MessageSquare, Settings, LogOut } from 'lucide-react';
import type { Session } from '../../App';

interface SidebarProps {
  sessions: Session[];
  activeSessionId: string | null;
  onNewChat: () => void;
  onSelectSession: (session: Session) => void;
}

export const Sidebar: React.FC<SidebarProps> = ({ 
  sessions, 
  activeSessionId, 
  onNewChat, 
  onSelectSession 
}) => {
  return (
    <aside className="sidebar">
      <div className="p-6 flex flex-col h-full">
        {/* Brand */}
        <div className="flex items-center gap-3 mb-8">
          <div className="w-10 h-10 rounded-xl bg-indigo-600 flex items-center justify-center shadow-lg shadow-indigo-500/20">
            <span className="text-white font-bold text-xl brand-font">E</span>
          </div>
          <div>
            <h1 className="text-lg font-bold brand-font leading-tight">ESA</h1>
            <p className="text-xs text-slate-500 font-medium">ERP Assistant</p>
          </div>
        </div>

        {/* Action */}
        <button 
          onClick={onNewChat}
          className="btn btn-primary w-full mb-6"
        >
          <Plus size={18} />
          New Thread
        </button>

        {/* History List */}
        <div className="flex-grow overflow-y-auto space-y-2 pr-2">
          <p className="text-[10px] uppercase tracking-wider font-bold text-slate-600 mb-2 px-3">Recent Chats</p>
          
          {sessions.length === 0 ? (
            <p className="px-3 text-xs text-slate-600 italic">No threads yet</p>
          ) : (
            sessions.map((session) => (
              <button 
                key={session.id}
                onClick={() => onSelectSession(session)}
                className={`flex items-center gap-3 w-full p-3 rounded-xl transition-all text-left ${
                  activeSessionId === session.id 
                    ? 'bg-white/10 border border-white/20 text-white shadow-sm' 
                    : 'hover:bg-white/5 text-sm font-medium text-slate-400 hover:text-slate-200'
                }`}
              >
                <MessageSquare size={16} className={activeSessionId === session.id ? 'text-indigo-400' : ''} />
                <span className="truncate">{session.title}</span>
              </button>
            ))
          )}
        </div>

        {/* Footer info */}
        <div className="mt-auto pt-6 space-y-2 border-t border-white/5">
          <button className="flex items-center gap-3 w-full p-3 rounded-xl hover:bg-white/5 text-sm font-medium text-slate-400 hover:text-slate-200 transition-all">
            <Settings size={18} />
            Settings
          </button>
          <button className="flex items-center gap-3 w-full p-3 rounded-xl hover:bg-red-500/10 text-sm font-medium text-slate-400 hover:text-red-400 transition-all">
            <LogOut size={18} />
            Sign Out
          </button>
        </div>
      </div>
    </aside>
  );
};

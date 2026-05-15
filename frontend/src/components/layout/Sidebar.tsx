import React from 'react';
import { Plus, MessageSquare, Settings, LogOut, ChevronLeft } from 'lucide-react';

interface SidebarProps {
  onNewChat: () => void;
}

export const Sidebar: React.FC<SidebarProps> = ({ onNewChat }) => {
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

        {/* History List Placeholder */}
        <div className="flex-grow overflow-y-auto space-y-2 pr-2">
          <p className="text-[10px] uppercase tracking-wider font-bold text-slate-600 mb-2 px-3">Recent Chats</p>
          
          <button className="flex items-center gap-3 w-full p-3 rounded-xl bg-white/5 border border-white/10 text-sm font-medium text-slate-300 hover:text-white transition-all">
            <MessageSquare size={16} className="text-indigo-400" />
            Chart of Accounts Setup
          </button>
          
          <button className="flex items-center gap-3 w-full p-3 rounded-xl hover:bg-white/5 text-sm font-medium text-slate-400 hover:text-slate-200 transition-all">
            <MessageSquare size={16} />
            Payment Terms Info
          </button>
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

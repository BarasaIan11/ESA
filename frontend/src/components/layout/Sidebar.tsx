import React from "react";
import { Plus, MessageSquare, Settings, LogOut, Bot } from "lucide-react";
import type { Session } from "../../App";

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
  onSelectSession,
}) => {
  return (
    <aside className="w-(--sidebar-width) bg-bg-sidebar border-r border-border-light flex flex-col h-full">
      <div className="px-4 py-4 border-b border-border-light">
        <img
          src="/logo.png"
          alt="ESA Logo"
          className="w-full h-auto object-contain"
          style={{ maxHeight: "80px" }}
        />
      </div>

      <div className="px-4 mb-6">
        <button
          onClick={onNewChat}
          className="w-full bg-accent-primary hover:bg-accent-hover text-white py-2.5 px-4 rounded-lg text-sm font-semibold flex items-center justify-center gap-2 transition-colors shadow-sm"
        >
          <Plus size={16} strokeWidth={3} />
          New Thread
        </button>
      </div>

      <nav className="flex-1 px-2 overflow-y-auto">
        <div className="px-3 py-2 text-[10px] font-bold text-slate-400 uppercase tracking-wider">
          RECENT
        </div>
        <div className="space-y-0.5">
          {sessions.length === 0 ? (
            <div className="px-3 py-2 text-xs text-slate-400 italic">
              No history yet
            </div>
          ) : (
            sessions.map((session) => (
              <div
                key={session.id}
                onClick={() => onSelectSession(session)}
                className={`flex items-center gap-3 px-3 py-2 rounded-md cursor-pointer transition-colors ${
                  activeSessionId === session.id
                    ? "bg-white text-accent-primary shadow-sm font-medium"
                    : "text-slate-600 hover:bg-slate-200/50"
                }`}
              >
                <MessageSquare
                  size={16}
                  className={
                    activeSessionId === session.id
                      ? "text-accent-primary"
                      : "text-slate-400"
                  }
                />
                <span className="text-sm truncate">{session.title}</span>
              </div>
            ))
          )}
        </div>
      </nav>

      <div className="p-4 border-t border-border-light space-y-1 mt-auto">
        <div className="flex items-center gap-3 px-3 py-2 text-slate-600 hover:bg-slate-200/50 rounded-md cursor-pointer transition-colors">
          <Settings size={18} />
          <span className="text-sm font-medium">Settings</span>
        </div>
        <div className="flex items-center gap-3 px-3 py-2 text-slate-600 hover:bg-slate-200/50 rounded-md cursor-pointer transition-colors">
          <LogOut size={18} />
          <span className="text-sm font-medium">Sign Out</span>
        </div>
      </div>
    </aside>
  );
};

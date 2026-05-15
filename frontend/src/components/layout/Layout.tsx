import React from 'react';
import { Sidebar } from './Sidebar';
import type { Session } from '../../App';

interface LayoutProps {
  children: React.ReactNode;
  sessions: Session[];
  activeSessionId: string | null;
  onNewChat: () => void;
  onSelectSession: (session: Session) => void;
}

export const Layout: React.FC<LayoutProps> = ({
  children,
  sessions,
  activeSessionId,
  onNewChat,
  onSelectSession,
}) => {
  return (
    <div className="app-layout">
      <Sidebar
        sessions={sessions}
        activeSessionId={activeSessionId}
        onNewChat={onNewChat}
        onSelectSession={onSelectSession}
      />
      <main className="main-content">
        {children}
      </main>
    </div>
  );
};

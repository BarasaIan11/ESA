import React from 'react';
import { Sidebar } from './Sidebar';

interface LayoutProps {
  children: React.ReactNode;
}

export const Layout: React.FC<LayoutProps> = ({ children }) => {
  return (
    <div className="app-layout">
      <Sidebar onNewChat={() => console.log('New Chat')} />
      <main className="main-content">
        {children}
      </main>
    </div>
  );
};

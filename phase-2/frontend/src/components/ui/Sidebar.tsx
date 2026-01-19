'use client';

/**
 * Sidebar component for the dashboard layout.
 * Features user avatar, navigation menu, and logout.
 * Responsive: collapses to hamburger menu on mobile.
 */

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/components/auth/AuthProvider';
import { logout as apiLogout } from '@/lib/api';

// =============================================================================
// Icons as inline SVGs
// =============================================================================

const DashboardIcon = () => (
  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z" />
  </svg>
);

const TaskIcon = () => (
  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
  </svg>
);

const SettingsIcon = () => (
  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
  </svg>
);

const HelpIcon = () => (
  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
  </svg>
);

const LogoutIcon = () => (
  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
  </svg>
);

const MenuIcon = () => (
  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
  </svg>
);

const CloseIcon = () => (
  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
  </svg>
);

// =============================================================================
// Navigation Items
// =============================================================================

interface NavItem {
  id: string;
  name: string;
  icon: React.ReactNode;
  href?: string;
}

const navItems: NavItem[] = [
  { id: 'dashboard', name: 'Dashboard', icon: <DashboardIcon />, href: '/tasks' },
  { id: 'tasks', name: 'My Task', icon: <TaskIcon />, href: '/tasks' },
  { id: 'settings', name: 'Settings', icon: <SettingsIcon />, href: '/settings' },
  { id: 'help', name: 'Help', icon: <HelpIcon /> },
];

// =============================================================================
// Sidebar Component
// =============================================================================

interface SidebarProps {
  activeItem?: string;
}

export function Sidebar({ activeItem: initialActiveItem = 'tasks' }: SidebarProps) {
  const { auth, logout } = useAuth();
  const router = useRouter();
  const [activeItem, setActiveItem] = useState(initialActiveItem);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  // Get user initials for avatar
  const getInitials = (email: string): string => {
    return email.charAt(0).toUpperCase();
  };

  // Handle logout
  const handleLogout = async () => {
    try {
      await apiLogout();
    } catch {
      // Ignore API errors on logout - still clear local state
    }
    logout();
  };

  // Handle nav item click
  const handleNavClick = (item: NavItem) => {
    setActiveItem(item.id);
    setIsMobileMenuOpen(false);
    if (item.href) {
      router.push(item.href);
    }
  };

  const SidebarContent = () => (
    <>
      {/* User Profile Section */}
      <div className="p-6 flex flex-col items-center border-b border-zinc-800">
        {/* Avatar */}
        <div className="w-20 h-20 rounded-full bg-gradient-to-br from-red-400 to-red-600 flex items-center justify-center text-white text-2xl font-bold mb-3 shadow-lg">
          {auth.user ? getInitials(auth.user.email) : 'U'}
        </div>
        {/* User Name/Email */}
        <h3 className="text-white font-semibold text-lg">
          {auth.user?.name || auth.user?.email?.split('@')[0] || 'User'}
        </h3>
        <p className="text-zinc-400 text-sm truncate max-w-full">
          {auth.user?.email || 'user@email.com'}
        </p>
      </div>

      {/* Navigation Menu */}
      <nav className="flex-1 p-4 sidebar-scroll overflow-y-auto">
        <ul className="space-y-1">
          {navItems.map((item) => (
            <li key={item.id}>
              <button
                onClick={() => handleNavClick(item)}
                className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-all duration-200 ${
                  activeItem === item.id
                    ? 'bg-red-500 text-white shadow-md'
                    : 'text-zinc-400 hover:bg-zinc-800 hover:text-white'
                }`}
              >
                {item.icon}
                <span className="font-medium">{item.name}</span>
              </button>
            </li>
          ))}
        </ul>
      </nav>

      {/* Logout Button */}
      <div className="p-4 border-t border-zinc-800">
        <button
          onClick={handleLogout}
          className="w-full flex items-center gap-3 px-4 py-3 rounded-lg text-zinc-400 hover:bg-zinc-800 hover:text-white transition-all duration-200"
        >
          <LogoutIcon />
          <span className="font-medium">Logout</span>
        </button>
      </div>
    </>
  );

  return (
    <>
      {/* Mobile Menu Button */}
      <button
        onClick={() => setIsMobileMenuOpen(true)}
        className="lg:hidden fixed top-4 left-4 z-40 p-2 bg-zinc-900 text-white rounded-lg shadow-lg"
        aria-label="Open menu"
      >
        <MenuIcon />
      </button>

      {/* Mobile Overlay */}
      {isMobileMenuOpen && (
        <div
          className="lg:hidden fixed inset-0 bg-black/50 z-40"
          onClick={() => setIsMobileMenuOpen(false)}
        />
      )}

      {/* Mobile Sidebar */}
      <aside
        className={`lg:hidden fixed inset-y-0 left-0 z-50 w-64 bg-zinc-900 flex flex-col transform transition-transform duration-300 ease-in-out ${
          isMobileMenuOpen ? 'translate-x-0' : '-translate-x-full'
        }`}
      >
        {/* Close Button */}
        <button
          onClick={() => setIsMobileMenuOpen(false)}
          className="absolute top-4 right-4 p-2 text-zinc-400 hover:text-white"
          aria-label="Close menu"
        >
          <CloseIcon />
        </button>
        <SidebarContent />
      </aside>

      {/* Desktop Sidebar */}
      <aside className="hidden lg:flex w-64 bg-zinc-900 min-h-screen flex-col flex-shrink-0">
        <SidebarContent />
      </aside>
    </>
  );
}

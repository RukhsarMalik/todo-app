'use client';

/**
 * TypeScript interfaces for chat components
 */

export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

export interface Conversation {
  id: string;
  userId: string;
  title?: string;
  createdAt: Date;
  updatedAt: Date;
}

export interface ChatInterfaceProps {
  userId: string;
  onSendMessage?: (message: string) => Promise<string>;
  placeholder?: string;
  className?: string;
}

export interface ChatKitProps {
  onSendMessage: (message: string) => Promise<any>;
  placeholder?: string;
  isLoading?: boolean;
  messages?: ChatMessage[];
}

export interface ChatHistoryState {
  conversationId?: string;
  messages: ChatMessage[];
  isLoading: boolean;
  error?: string;
}
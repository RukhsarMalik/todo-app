'use client';

import { useState, useRef, useEffect, FormEvent } from 'react';
import { sendChatMessage } from '../lib/chat-api';
import { ChatMessage } from '../lib/chat-types';

interface ChatInterfaceProps {
  userId: string;
  isCompact?: boolean; // For mini chat window
}

// Icons
const UserIcon = () => (
  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
  </svg>
);

const BotIcon = () => (
  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
  </svg>
);

const SendIcon = () => (
  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
  </svg>
);

export default function ChatInterface({ userId, isCompact = false }: ChatInterfaceProps) {
  const [isLoading, setIsLoading] = useState(false);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [conversationId, setConversationId] = useState<string | undefined>();
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Load conversation history on component mount
  useEffect(() => {
    const loadConversation = async () => {
      try {
        // For now, we'll start with an empty conversation
        // In the future, we could load from local storage or server
        const savedMessages = localStorage.getItem(`chat-${userId}-messages`);
        if (savedMessages) {
          const parsedMessages = JSON.parse(savedMessages).map((msg: any) => ({
            ...msg,
            timestamp: new Date(msg.timestamp)
          }));
          setMessages(parsedMessages);
        }
      } catch (error) {
        console.error('Error loading conversation history:', error);
        // Continue with empty conversation if loading fails
      }
    };

    loadConversation();
  }, [userId]);

  // Save conversation history to local storage when messages change
  useEffect(() => {
    if (messages.length > 0) {
      localStorage.setItem(`chat-${userId}-messages`, JSON.stringify(messages));
    }
  }, [messages, userId]);

  // Scroll to bottom when messages change
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  async function sendMessage(message: string) {
    // Validate message before sending
    if (!message.trim()) {
      console.error('Empty message cannot be sent');
      return '';
    }

    setIsLoading(true);

    try {
      // Add user message to UI immediately
      const userMessage: ChatMessage = {
        id: Date.now().toString(),
        role: 'user',
        content: message,
        timestamp: new Date()
      };

      setMessages(prev => [...prev, userMessage]);

      // Call backend API with conversation ID if available
      const res = await sendChatMessage(userId, message, conversationId);

      // Update conversation ID if new one was returned
      if (res.conversation_id && !conversationId) {
        setConversationId(res.conversation_id);
      }

      // Add assistant response to UI
      const assistantMessage: ChatMessage = {
        id: (Date.now() + 1).toString(), // Simple ID generation
        role: 'assistant',
        content: res.response,
        timestamp: new Date()
      };

      setMessages(prev => [...prev, assistantMessage]);

      return res.response;
    } catch (error) {
      console.error('Error sending message:', error);
      // Add error message to UI
      const errorMessage: ChatMessage = {
        id: Date.now().toString(),
        role: 'assistant',
        content: 'Sorry, I encountered an error processing your request. Please try again.',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);

      // Show user-friendly error notification
      alert('Failed to send message. Please check your connection and try again.');
      return '';
    } finally {
      setIsLoading(false);
    }
  }

  const clearChat = () => {
    setMessages([]);
    setConversationId(undefined);
    localStorage.removeItem(`chat-${userId}-messages`);
  };

  return (
    <div className={`flex flex-col h-full bg-white overflow-hidden ${isCompact ? '' : 'rounded-xl shadow-sm border border-gray-200'}`}>
      {/* Chat Header - hide in compact mode since parent has header */}
      {!isCompact && (
        <div className="px-4 py-3 border-b border-gray-200 bg-gray-50 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <span className="w-8 h-8 bg-red-100 rounded-lg flex items-center justify-center text-red-500">
              <BotIcon />
            </span>
            <div>
              <h3 className="font-semibold text-gray-800 text-sm">Task AI</h3>
              <p className="text-xs text-gray-500">Powered by GPT-4</p>
            </div>
          </div>
          {messages.length > 0 && (
            <button
              onClick={clearChat}
              className="text-xs text-gray-500 hover:text-red-500 transition-colors px-2 py-1 hover:bg-red-50 rounded"
            >
              Clear Chat
            </button>
          )}
        </div>
      )}

      {/* Messages Area */}
      <div className={`flex-1 overflow-y-auto space-y-4 ${isCompact ? 'p-3' : 'p-4'}`} style={{ maxHeight: isCompact ? 'none' : 'calc(100vh - 320px)' }}>
        {messages.length === 0 ? (
          <div className={`flex flex-col items-center justify-center h-full text-center ${isCompact ? 'py-6' : 'py-12'}`}>
            <div className={`bg-red-100 rounded-2xl flex items-center justify-center text-red-500 mb-3 ${isCompact ? 'w-12 h-12' : 'w-16 h-16 mb-4'}`}>
              <svg className={isCompact ? 'w-6 h-6' : 'w-8 h-8'} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
              </svg>
            </div>
            <h3 className={`font-semibold text-gray-800 mb-2 ${isCompact ? 'text-base' : 'text-lg'}`}>Start a Conversation</h3>
            <p className="text-gray-500 text-sm max-w-sm">
              {isCompact ? 'Try saying:' : 'Ask me to manage your tasks. Try saying:'}
            </p>
            <div className={`space-y-2 ${isCompact ? 'mt-3' : 'mt-4'}`}>
              <p className={`text-gray-600 bg-gray-100 px-3 py-1.5 rounded-lg ${isCompact ? 'text-xs' : 'text-sm py-2'}`}>"Add a task to buy groceries"</p>
              <p className={`text-gray-600 bg-gray-100 px-3 py-1.5 rounded-lg ${isCompact ? 'text-xs' : 'text-sm py-2'}`}>"Show me all my tasks"</p>
              {!isCompact && <p className="text-sm text-gray-600 bg-gray-100 px-3 py-2 rounded-lg">"Mark task 1 as complete"</p>}
            </div>
          </div>
        ) : (
          messages.map((msg) => (
            <div
              key={msg.id}
              className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`flex gap-3 max-w-[85%] ${msg.role === 'user' ? 'flex-row-reverse' : 'flex-row'}`}
              >
                {/* Avatar */}
                <div
                  className={`w-8 h-8 rounded-lg flex items-center justify-center flex-shrink-0 ${
                    msg.role === 'user'
                      ? 'bg-red-500 text-white'
                      : 'bg-gray-100 text-gray-600'
                  }`}
                >
                  {msg.role === 'user' ? <UserIcon /> : <BotIcon />}
                </div>

                {/* Message Bubble */}
                <div
                  className={`px-4 py-3 rounded-xl ${
                    msg.role === 'user'
                      ? 'bg-red-500 text-white rounded-tr-none'
                      : 'bg-gray-100 text-gray-800 rounded-tl-none'
                  }`}
                >
                  <p className="text-sm whitespace-pre-wrap">{msg.content}</p>
                  <p className={`text-xs mt-1 ${msg.role === 'user' ? 'text-red-200' : 'text-gray-400'}`}>
                    {msg.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                  </p>
                </div>
              </div>
            </div>
          ))
        )}

        {/* Loading indicator */}
        {isLoading && (
          <div className="flex justify-start">
            <div className="flex gap-3 max-w-[85%]">
              <div className="w-8 h-8 rounded-lg bg-gray-100 flex items-center justify-center text-gray-600 flex-shrink-0">
                <BotIcon />
              </div>
              <div className="bg-gray-100 px-4 py-3 rounded-xl rounded-tl-none">
                <div className="flex items-center gap-1">
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
                </div>
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <ChatInput
        onSendMessage={sendMessage}
        placeholder={isCompact ? "Type a message..." : "Ask me to manage your tasks..."}
        isLoading={isLoading}
        isCompact={isCompact}
        onClearChat={isCompact && messages.length > 0 ? clearChat : undefined}
      />
    </div>
  );
}

// Custom chat input component
interface ChatInputProps {
  onSendMessage: (message: string) => Promise<string>;
  placeholder?: string;
  isLoading?: boolean;
  isCompact?: boolean;
  onClearChat?: () => void;
}

function ChatInput({ onSendMessage, placeholder, isLoading, isCompact, onClearChat }: ChatInputProps) {
  const [inputValue, setInputValue] = useState('');

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    if (!inputValue.trim() || isLoading) return;

    const message = inputValue.trim();
    setInputValue('');
    await onSendMessage(message);
  };

  return (
    <form onSubmit={handleSubmit} className={`border-t border-gray-200 bg-gray-50 ${isCompact ? 'p-3' : 'p-4'}`}>
      {/* Clear chat button for compact mode */}
      {onClearChat && (
        <div className="flex justify-end mb-2">
          <button
            type="button"
            onClick={onClearChat}
            className="text-xs text-gray-500 hover:text-red-500 transition-colors px-2 py-1 hover:bg-red-50 rounded"
          >
            Clear Chat
          </button>
        </div>
      )}
      <div className="flex gap-2">
        <input
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          placeholder={placeholder || "Type a message..."}
          disabled={isLoading}
          className={`flex-1 bg-white border border-gray-200 rounded-xl text-gray-800 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-red-400 focus:border-transparent disabled:bg-gray-100 disabled:cursor-not-allowed transition-all ${isCompact ? 'px-3 py-2 text-sm' : 'px-4 py-3'}`}
        />
        <button
          type="submit"
          disabled={isLoading || !inputValue.trim()}
          className={`bg-red-500 text-white rounded-xl hover:bg-red-600 focus:outline-none focus:ring-2 focus:ring-red-400 focus:ring-offset-2 disabled:bg-gray-300 disabled:cursor-not-allowed transition-all flex items-center justify-center ${isCompact ? 'px-3 py-2' : 'px-5 py-3 gap-2'}`}
        >
          {isLoading ? (
            <svg className={`animate-spin text-white ${isCompact ? 'h-4 w-4' : 'h-5 w-5'}`} xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
          ) : (
            <SendIcon />
          )}
          {!isCompact && <span className="hidden sm:inline">{isLoading ? 'Sending' : 'Send'}</span>}
        </button>
      </div>
    </form>
  );
}

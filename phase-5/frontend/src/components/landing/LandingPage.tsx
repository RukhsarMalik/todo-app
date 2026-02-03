'use client';

import React, { useEffect, useState } from 'react';
import Link from 'next/link';

// Icon components
const CheckIcon = () => (
  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
  </svg>
);

const TaskIcon = () => (
  <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
  </svg>
);

const AIIcon = () => (
  <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
  </svg>
);

const CalendarIcon = () => (
  <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
  </svg>
);

const TagIcon = () => (
  <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
  </svg>
);

const BellIcon = () => (
  <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
  </svg>
);

const RepeatIcon = () => (
  <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
  </svg>
);

const ChatIcon = () => (
  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
  </svg>
);

const SparklesIcon = () => (
  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z" />
  </svg>
);

const features = [
  {
    icon: <TaskIcon />,
    title: 'Smart Task Management',
    description: 'Create, organize, and track tasks with priorities (low, medium, high, urgent) and status tracking.',
    color: 'bg-blue-500',
  },
  {
    icon: <CalendarIcon />,
    title: 'Due Dates & Reminders',
    description: 'Set due dates with customizable reminders so you never miss a deadline again.',
    color: 'bg-teal-500',
  },
  {
    icon: <TagIcon />,
    title: 'Tags & Categories',
    description: 'Organize tasks with custom tags for easy filtering and categorization.',
    color: 'bg-purple-500',
  },
  {
    icon: <RepeatIcon />,
    title: 'Recurring Tasks',
    description: 'Set up daily, weekly, or monthly recurring tasks that auto-generate.',
    color: 'bg-orange-500',
  },
  {
    icon: <BellIcon />,
    title: 'Smart Notifications',
    description: 'Event-driven notifications keep you updated on task changes and deadlines.',
    color: 'bg-pink-500',
  },
  {
    icon: <AIIcon />,
    title: 'AI-Powered Assistant',
    description: 'Chat with AI to manage tasks using natural language - just tell it what you need.',
    color: 'bg-coral-400',
  },
];

const aiChatMessages = [
  { role: 'user', text: 'Add a task to review quarterly report by Friday' },
  { role: 'ai', text: 'Done! I\'ve created "Review quarterly report" with high priority, due Friday. Want me to add a reminder?' },
  { role: 'user', text: 'Yes, remind me 1 day before' },
  { role: 'ai', text: 'Reminder set for Thursday. I\'ve also tagged it as #work. Anything else?' },
];

const stats = [
  { value: '99.9%', label: 'Uptime' },
  { value: '50ms', label: 'Response Time' },
  { value: '10K+', label: 'Tasks Managed' },
  { value: '24/7', label: 'AI Available' },
];

export function LandingPage() {
  const [isVisible, setIsVisible] = useState(false);
  const [currentChatIndex, setCurrentChatIndex] = useState(0);
  const [showNavbar, setShowNavbar] = useState(false);

  useEffect(() => {
    setIsVisible(true);

    const handleScroll = () => {
      setShowNavbar(window.scrollY > 100);
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  useEffect(() => {
    if (currentChatIndex < aiChatMessages.length) {
      const timer = setTimeout(() => {
        setCurrentChatIndex((prev) => prev + 1);
      }, 2000);
      return () => clearTimeout(timer);
    }
  }, [currentChatIndex]);

  return (
    <div className="min-h-screen bg-white overflow-x-hidden">
      {/* Floating Navbar */}
      <nav
        className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${
          showNavbar ? 'bg-white/90 backdrop-blur-md shadow-md' : 'bg-transparent'
        }`}
      >
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            {/* Logo */}
            <div className="flex items-center space-x-2">
              <div className="w-8 h-8 bg-coral-400 rounded-lg flex items-center justify-center">
                <CheckIcon />
              </div>
              <span className="text-xl font-bold">
                <span className="text-coral-400">To</span>
                <span className="text-gray-800">Do</span>
              </span>
            </div>

            {/* Nav Links - Hidden on mobile */}
            <div className="hidden md:flex items-center space-x-8">
              <a href="#features" className="text-gray-600 hover:text-coral-500 transition-colors">
                Features
              </a>
              <a href="#ai" className="text-gray-600 hover:text-coral-500 transition-colors">
                AI Assistant
              </a>
              <a href="#stats" className="text-gray-600 hover:text-coral-500 transition-colors">
                Why Us
              </a>
            </div>

            {/* CTA Buttons */}
            <div className="flex items-center space-x-3">
              <Link
                href="/login"
                className="px-4 py-2 text-gray-700 hover:text-coral-500 font-medium transition-colors"
              >
                Log in
              </Link>
              <Link
                href="/signup"
                className="px-4 py-2 bg-coral-400 hover:bg-coral-500 text-white font-medium rounded-lg transition-all hover:shadow-lg"
              >
                Get Started
              </Link>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="hero-gradient min-h-screen flex items-center pt-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            {/* Left Content */}
            <div className={`space-y-8 ${isVisible ? 'animate-slide-in-left' : 'opacity-0'}`}>
              <div className="inline-flex items-center space-x-2 bg-coral-50 text-coral-600 px-4 py-2 rounded-full text-sm font-medium">
                <SparklesIcon />
                <span>AI-Powered Task Management</span>
              </div>

              <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold text-gray-900 leading-tight">
                Manage Tasks with
                <span className="text-coral-400"> AI Intelligence</span>
              </h1>

              <p className="text-lg sm:text-xl text-gray-600 max-w-lg">
                The smartest way to organize your work. Use natural language to create, manage, and track tasks.
                Let AI handle the complexity while you focus on what matters.
              </p>

              <div className="flex flex-col sm:flex-row gap-4">
                <Link
                  href="/signup"
                  className="inline-flex items-center justify-center px-8 py-4 bg-coral-400 hover:bg-coral-500 text-white font-semibold rounded-xl transition-all hover:shadow-xl hover:scale-105 animate-pulse-glow"
                >
                  Start Free Today
                  <svg className="ml-2 w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
                  </svg>
                </Link>
                <a
                  href="#features"
                  className="inline-flex items-center justify-center px-8 py-4 border-2 border-gray-300 hover:border-coral-400 text-gray-700 hover:text-coral-500 font-semibold rounded-xl transition-all"
                >
                  See Features
                </a>
              </div>

              {/* Trust badges */}
              <div className="flex items-center space-x-6 pt-4">
                <div className="flex -space-x-2">
                  {[1, 2, 3, 4].map((i) => (
                    <div
                      key={i}
                      className="w-10 h-10 rounded-full bg-gradient-to-br from-coral-300 to-teal-300 border-2 border-white"
                    />
                  ))}
                </div>
                <div className="text-sm text-gray-600">
                  <span className="font-semibold text-gray-900">1,000+</span> users already productive
                </div>
              </div>
            </div>

            {/* Right Content - Hero Illustration */}
            <div className={`relative ${isVisible ? 'animate-slide-in-right' : 'opacity-0'}`}>
              {/* Floating Task Cards */}
              <div className="relative w-full h-[500px]">
                {/* Main Card */}
                <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-72 sm:w-80 glass rounded-2xl p-6 shadow-xl animate-float">
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="font-semibold text-gray-800">Today's Tasks</h3>
                    <span className="text-sm text-coral-500 font-medium">3 pending</span>
                  </div>
                  <div className="space-y-3">
                    {[
                      { text: 'Review project proposal', priority: 'high', done: true },
                      { text: 'Team standup meeting', priority: 'medium', done: false },
                      { text: 'Update documentation', priority: 'low', done: false },
                    ].map((task, i) => (
                      <div key={i} className="flex items-center space-x-3 p-3 bg-white rounded-lg">
                        <div
                          className={`w-5 h-5 rounded-full border-2 flex items-center justify-center ${
                            task.done
                              ? 'bg-teal-500 border-teal-500'
                              : 'border-gray-300'
                          }`}
                        >
                          {task.done && (
                            <svg className="w-3 h-3 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" />
                            </svg>
                          )}
                        </div>
                        <span className={`flex-1 text-sm ${task.done ? 'text-gray-400 line-through' : 'text-gray-700'}`}>
                          {task.text}
                        </span>
                        <span
                          className={`px-2 py-1 text-xs rounded-full ${
                            task.priority === 'high'
                              ? 'bg-red-100 text-red-600'
                              : task.priority === 'medium'
                              ? 'bg-yellow-100 text-yellow-600'
                              : 'bg-green-100 text-green-600'
                          }`}
                        >
                          {task.priority}
                        </span>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Floating AI Chat Bubble */}
                <div className="absolute top-8 right-4 sm:right-8 w-56 bg-white rounded-2xl p-4 shadow-lg animate-float delay-200">
                  <div className="flex items-center space-x-2 mb-2">
                    <div className="w-8 h-8 bg-coral-400 rounded-full flex items-center justify-center">
                      <ChatIcon />
                    </div>
                    <span className="text-sm font-medium text-gray-700">AI Assistant</span>
                  </div>
                  <p className="text-sm text-gray-600">
                    "Task added! Due Friday with reminder."
                  </p>
                </div>

                {/* Floating Stats Card */}
                <div className="absolute bottom-8 left-4 sm:left-8 bg-gradient-to-br from-teal-500 to-teal-600 text-white rounded-2xl p-4 shadow-lg animate-float delay-400">
                  <div className="text-2xl font-bold">87%</div>
                  <div className="text-sm text-teal-100">Tasks Completed</div>
                </div>

                {/* Background Decorations */}
                <div className="absolute top-20 left-20 w-20 h-20 bg-coral-200 rounded-full opacity-50 blur-2xl" />
                <div className="absolute bottom-20 right-20 w-32 h-32 bg-teal-200 rounded-full opacity-50 blur-2xl" />
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16 animate-slide-up">
            <h2 className="text-3xl sm:text-4xl font-bold text-gray-900 mb-4">
              Everything You Need to Stay Productive
            </h2>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto">
              Powerful features designed to help you manage tasks efficiently with the help of AI
            </p>
          </div>

          <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-8">
            {features.map((feature, index) => (
              <div
                key={index}
                className="feature-card bg-white rounded-2xl p-6 shadow-card"
                style={{ animationDelay: `${index * 100}ms` }}
              >
                <div className={`w-14 h-14 ${feature.color} text-white rounded-xl flex items-center justify-center mb-4`}>
                  {feature.icon}
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-2">{feature.title}</h3>
                <p className="text-gray-600">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* AI Integration Section */}
      <section id="ai" className="py-20 bg-white overflow-hidden">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            {/* Left - AI Chat Demo */}
            <div className="order-2 lg:order-1">
              <div className="bg-gray-900 rounded-2xl p-6 shadow-2xl max-w-md mx-auto">
                <div className="flex items-center space-x-2 mb-6">
                  <div className="w-3 h-3 rounded-full bg-red-500" />
                  <div className="w-3 h-3 rounded-full bg-yellow-500" />
                  <div className="w-3 h-3 rounded-full bg-green-500" />
                  <span className="ml-4 text-gray-400 text-sm">AI Chat Assistant</span>
                </div>

                <div className="space-y-4 min-h-[300px]">
                  {aiChatMessages.slice(0, currentChatIndex).map((msg, i) => (
                    <div
                      key={i}
                      className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'} animate-chat-bubble`}
                    >
                      <div
                        className={`max-w-[80%] px-4 py-3 rounded-2xl ${
                          msg.role === 'user'
                            ? 'bg-coral-400 text-white rounded-br-none'
                            : 'bg-gray-800 text-gray-100 rounded-bl-none'
                        }`}
                      >
                        {msg.role === 'ai' && (
                          <div className="flex items-center space-x-2 mb-1">
                            <SparklesIcon />
                            <span className="text-xs text-coral-400">AI Assistant</span>
                          </div>
                        )}
                        <p className="text-sm">{msg.text}</p>
                      </div>
                    </div>
                  ))}

                  {currentChatIndex < aiChatMessages.length && (
                    <div className="flex justify-start">
                      <div className="bg-gray-800 px-4 py-3 rounded-2xl rounded-bl-none">
                        <div className="dot-pulse flex space-x-1">
                          <span className="w-2 h-2 bg-gray-400 rounded-full" />
                          <span className="w-2 h-2 bg-gray-400 rounded-full" />
                          <span className="w-2 h-2 bg-gray-400 rounded-full" />
                        </div>
                      </div>
                    </div>
                  )}
                </div>

                <div className="mt-4 flex items-center space-x-2">
                  <input
                    type="text"
                    placeholder="Type a message..."
                    className="flex-1 bg-gray-800 text-white px-4 py-3 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-coral-400"
                    readOnly
                  />
                  <button className="p-3 bg-coral-400 hover:bg-coral-500 text-white rounded-xl transition-colors">
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                    </svg>
                  </button>
                </div>
              </div>
            </div>

            {/* Right - Content */}
            <div className="order-1 lg:order-2 space-y-6">
              <div className="inline-flex items-center space-x-2 bg-teal-50 text-teal-600 px-4 py-2 rounded-full text-sm font-medium">
                <AIIcon />
                <span>AI Integration</span>
              </div>

              <h2 className="text-3xl sm:text-4xl font-bold text-gray-900">
                Chat with AI to Manage Your Tasks
              </h2>

              <p className="text-lg text-gray-600">
                No more clicking through menus. Just tell the AI what you need in plain English.
                Create tasks, set reminders, check your schedule - all through natural conversation.
              </p>

              <ul className="space-y-4">
                {[
                  'Create tasks with natural language commands',
                  'Set priorities and due dates conversationally',
                  'Get smart suggestions and reminders',
                  'Ask questions about your task progress',
                  'Powered by OpenAI with MCP tools',
                ].map((item, i) => (
                  <li key={i} className="flex items-center space-x-3">
                    <div className="w-6 h-6 bg-teal-100 text-teal-600 rounded-full flex items-center justify-center flex-shrink-0">
                      <CheckIcon />
                    </div>
                    <span className="text-gray-700">{item}</span>
                  </li>
                ))}
              </ul>

              <Link
                href="/signup"
                className="inline-flex items-center px-6 py-3 bg-gray-900 hover:bg-gray-800 text-white font-semibold rounded-xl transition-all hover:shadow-lg"
              >
                Try AI Assistant
                <svg className="ml-2 w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
                </svg>
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section id="stats" className="py-20 bg-gradient-to-br from-coral-400 to-coral-500">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl sm:text-4xl font-bold text-white mb-4">
              Built for Performance & Reliability
            </h2>
            <p className="text-coral-100 text-lg max-w-2xl mx-auto">
              Enterprise-grade infrastructure powered by Kubernetes, Kafka, and Dapr
            </p>
          </div>

          <div className="grid grid-cols-2 lg:grid-cols-4 gap-8">
            {stats.map((stat, index) => (
              <div key={index} className="text-center">
                <div className="text-4xl sm:text-5xl font-bold text-white mb-2">{stat.value}</div>
                <div className="text-coral-100">{stat.label}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Technology Stack Section */}
      <section className="py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl sm:text-4xl font-bold text-gray-900 mb-4">
              Powered by Modern Technology
            </h2>
            <p className="text-gray-600 text-lg max-w-2xl mx-auto">
              Built with cutting-edge tools and frameworks for scalability and performance
            </p>
          </div>

          <div className="flex flex-wrap justify-center gap-8 items-center opacity-70">
            {['Next.js', 'FastAPI', 'PostgreSQL', 'Kubernetes', 'Kafka', 'Dapr', 'OpenAI'].map((tech) => (
              <div key={tech} className="px-6 py-3 bg-white rounded-lg shadow-sm text-gray-700 font-medium">
                {tech}
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-white">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl sm:text-4xl font-bold text-gray-900 mb-6">
            Ready to Get More Done?
          </h2>
          <p className="text-lg text-gray-600 mb-8 max-w-2xl mx-auto">
            Join thousands of users who are managing their tasks smarter with AI.
            Start free today and experience the future of productivity.
          </p>

          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              href="/signup"
              className="inline-flex items-center justify-center px-8 py-4 bg-coral-400 hover:bg-coral-500 text-white font-semibold rounded-xl transition-all hover:shadow-xl hover:scale-105"
            >
              Create Free Account
              <svg className="ml-2 w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
              </svg>
            </Link>
            <Link
              href="/login"
              className="inline-flex items-center justify-center px-8 py-4 border-2 border-gray-300 hover:border-coral-400 text-gray-700 hover:text-coral-500 font-semibold rounded-xl transition-all"
            >
              Sign In
            </Link>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-gray-400 py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid md:grid-cols-4 gap-8">
            {/* Brand */}
            <div className="col-span-2 md:col-span-1">
              <div className="flex items-center space-x-2 mb-4">
                <div className="w-8 h-8 bg-coral-400 rounded-lg flex items-center justify-center">
                  <CheckIcon />
                </div>
                <span className="text-xl font-bold text-white">
                  <span className="text-coral-400">To</span>Do
                </span>
              </div>
              <p className="text-sm">
                AI-powered task management for modern teams and individuals.
              </p>
            </div>

            {/* Links */}
            <div>
              <h4 className="text-white font-semibold mb-4">Product</h4>
              <ul className="space-y-2 text-sm">
                <li><a href="#features" className="hover:text-white transition-colors">Features</a></li>
                <li><a href="#ai" className="hover:text-white transition-colors">AI Assistant</a></li>
                <li><a href="#stats" className="hover:text-white transition-colors">Performance</a></li>
              </ul>
            </div>

            <div>
              <h4 className="text-white font-semibold mb-4">Company</h4>
              <ul className="space-y-2 text-sm">
                <li><a href="#" className="hover:text-white transition-colors">About</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Blog</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Careers</a></li>
              </ul>
            </div>

            <div>
              <h4 className="text-white font-semibold mb-4">Legal</h4>
              <ul className="space-y-2 text-sm">
                <li><a href="#" className="hover:text-white transition-colors">Privacy</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Terms</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Security</a></li>
              </ul>
            </div>
          </div>

          <div className="border-t border-gray-800 mt-12 pt-8 text-sm text-center">
            <p>&copy; {new Date().getFullYear()} ToDo App. Built with AI-powered excellence.</p>
          </div>
        </div>
      </footer>
    </div>
  );
}

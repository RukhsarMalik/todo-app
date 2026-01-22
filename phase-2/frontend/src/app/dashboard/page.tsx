'use client';

/**
 * Dashboard page with overview statistics and recent tasks.
 * Features a visually distinct design from the task list.
 */

import { useEffect, useState, useCallback } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/components/auth/AuthProvider';
import { LoadingSpinner } from '@/components/ui/LoadingSpinner';
import { Sidebar } from '@/components/ui/Sidebar';
import { getTasks, ApiError } from '@/lib/api';
import { Task } from '@/lib/types';

// Icons
const TaskIcon = () => (
  <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
  </svg>
);

const CheckCircleIcon = () => (
  <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
  </svg>
);

const ClockIcon = () => (
  <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
  </svg>
);

const TrendingUpIcon = () => (
  <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
  </svg>
);

const ArrowRightIcon = () => (
  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 8l4 4m0 0l-4 4m4-4H3" />
  </svg>
);

interface OverviewCardProps {
  title: string;
  value: number;
  subtitle: string;
  icon: React.ReactNode;
  gradient: string;
}

function OverviewCard({ title, value, subtitle, icon, gradient }: OverviewCardProps) {
  return (
    <div className={`rounded-2xl p-6 text-white ${gradient} shadow-lg`}>
      <div className="flex items-start justify-between">
        <div>
          <p className="text-white/80 text-sm font-medium">{title}</p>
          <p className="text-4xl font-bold mt-2">{value}</p>
          <p className="text-white/70 text-sm mt-1">{subtitle}</p>
        </div>
        <div className="bg-white/20 rounded-xl p-3">
          {icon}
        </div>
      </div>
    </div>
  );
}

interface RecentTaskProps {
  task: Task;
}

function RecentTask({ task }: RecentTaskProps) {
  const createdDate = new Date(task.created_at).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
  });

  return (
    <div className="flex items-center gap-4 p-4 bg-gray-50 rounded-xl hover:bg-gray-100 transition-colors">
      <div className={`w-10 h-10 rounded-full flex items-center justify-center ${
        task.completed ? 'bg-green-100 text-green-600' : 'bg-red-100 text-red-500'
      }`}>
        {task.completed ? (
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
          </svg>
        ) : (
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        )}
      </div>
      <div className="flex-1 min-w-0">
        <p className={`font-medium truncate ${task.completed ? 'text-gray-500 line-through' : 'text-gray-800'}`}>
          {task.title}
        </p>
        <p className="text-sm text-gray-400">{createdDate}</p>
      </div>
      <span className={`px-3 py-1 text-xs font-medium rounded-full ${
        task.completed
          ? 'bg-green-100 text-green-700'
          : 'bg-amber-100 text-amber-700'
      }`}>
        {task.completed ? 'Done' : 'Pending'}
      </span>
    </div>
  );
}

export default function DashboardPage() {
  const router = useRouter();
  const { auth } = useAuth();
  const [tasks, setTasks] = useState<Task[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Get current date
  const currentDate = new Date();
  const greeting = currentDate.getHours() < 12 ? 'Good Morning' : currentDate.getHours() < 18 ? 'Good Afternoon' : 'Good Evening';

  // Fetch tasks
  const fetchTasks = useCallback(async () => {
    if (!auth.user?.userId) return;

    try {
      setIsLoading(true);
      setError(null);
      const fetchedTasks = await getTasks(auth.user.userId);
      setTasks(fetchedTasks);
    } catch (err) {
      if (err instanceof ApiError) {
        setError(err.detail);
      } else {
        setError('Failed to load tasks');
      }
    } finally {
      setIsLoading(false);
    }
  }, [auth.user?.userId]);

  // Redirect to login if not authenticated
  useEffect(() => {
    if (!auth.isLoading && !auth.isAuthenticated) {
      router.replace('/login');
    }
  }, [auth.isLoading, auth.isAuthenticated, router]);

  // Fetch tasks on mount
  useEffect(() => {
    if (auth.isAuthenticated && auth.user?.userId) {
      fetchTasks();
    }
  }, [auth.isAuthenticated, auth.user?.userId, fetchTasks]);

  // Calculate stats
  const totalTasks = tasks.length;
  const completedTasks = tasks.filter(t => t.completed).length;
  const pendingTasks = totalTasks - completedTasks;
  const completionRate = totalTasks > 0 ? Math.round((completedTasks / totalTasks) * 100) : 0;

  // Get recent tasks (last 5)
  const recentTasks = [...tasks]
    .sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime())
    .slice(0, 5);

  // Show loading while checking auth
  if (auth.isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <LoadingSpinner size="lg" />
      </div>
    );
  }

  // Don't render if not authenticated (will redirect)
  if (!auth.isAuthenticated) {
    return null;
  }

  return (
    <div className="min-h-screen flex bg-gradient-to-br from-gray-50 to-gray-100">
      {/* Sidebar */}
      <Sidebar activeItem="dashboard" />

      {/* Main Content */}
      <div className="flex-1 flex flex-col min-h-screen overflow-hidden">
        {/* Header */}
        <header className="bg-white/80 backdrop-blur-sm shadow-sm px-4 lg:px-8 py-6 flex-shrink-0">
          <div className="flex items-center justify-between">
            <div className="ml-12 lg:ml-0">
              <h1 className="text-2xl lg:text-3xl font-bold text-gray-800">
                {greeting}, <span className="text-red-500">{auth.user?.name || auth.user?.email?.split('@')[0] || 'User'}</span>!
              </h1>
              <p className="text-gray-500 mt-1">Here&apos;s your productivity overview</p>
            </div>
            <div className="hidden md:block text-right">
              <p className="text-sm font-semibold text-gray-800">
                {currentDate.toLocaleDateString('en-US', { weekday: 'long', month: 'long', day: 'numeric' })}
              </p>
              <p className="text-sm text-gray-500">
                {currentDate.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' })}
              </p>
            </div>
          </div>
        </header>

        {/* Main content area */}
        <main className="flex-1 p-4 lg:p-8 overflow-auto">
          {isLoading ? (
            <div className="flex items-center justify-center h-64">
              <LoadingSpinner size="lg" />
            </div>
          ) : error ? (
            <div className="bg-red-50 text-red-600 p-4 rounded-xl">
              {error}
            </div>
          ) : (
            <>
              {/* Overview Cards */}
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 lg:gap-6 mb-8">
                <OverviewCard
                  title="Total Tasks"
                  value={totalTasks}
                  subtitle="All time tasks"
                  icon={<TaskIcon />}
                  gradient="bg-gradient-to-br from-blue-500 to-blue-600"
                />
                <OverviewCard
                  title="Completed"
                  value={completedTasks}
                  subtitle="Tasks finished"
                  icon={<CheckCircleIcon />}
                  gradient="bg-gradient-to-br from-green-500 to-green-600"
                />
                <OverviewCard
                  title="Pending"
                  value={pendingTasks}
                  subtitle="Tasks remaining"
                  icon={<ClockIcon />}
                  gradient="bg-gradient-to-br from-amber-500 to-orange-500"
                />
                <OverviewCard
                  title="Completion Rate"
                  value={completionRate}
                  subtitle="% of tasks done"
                  icon={<TrendingUpIcon />}
                  gradient="bg-gradient-to-br from-purple-500 to-purple-600"
                />
              </div>

              {/* Progress Section */}
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
                {/* Progress Bar Card */}
                <div className="bg-white rounded-2xl shadow-lg p-6">
                  <h3 className="text-lg font-bold text-gray-800 mb-4">Overall Progress</h3>
                  <div className="relative pt-1">
                    <div className="flex mb-2 items-center justify-between">
                      <div>
                        <span className="text-xs font-semibold inline-block py-1 px-2 uppercase rounded-full text-green-600 bg-green-100">
                          {completionRate}% Complete
                        </span>
                      </div>
                      <div className="text-right">
                        <span className="text-xs font-semibold inline-block text-gray-600">
                          {completedTasks}/{totalTasks} Tasks
                        </span>
                      </div>
                    </div>
                    <div className="overflow-hidden h-4 text-xs flex rounded-full bg-gray-200">
                      <div
                        style={{ width: `${completionRate}%` }}
                        className="shadow-none flex flex-col text-center whitespace-nowrap text-white justify-center bg-gradient-to-r from-green-400 to-green-600 transition-all duration-500"
                      />
                    </div>
                  </div>

                  {/* Quick Stats */}
                  <div className="mt-6 grid grid-cols-2 gap-4">
                    <div className="bg-gray-50 rounded-xl p-4">
                      <div className="flex items-center gap-2">
                        <div className="w-3 h-3 rounded-full bg-green-500" />
                        <span className="text-sm text-gray-600">Completed</span>
                      </div>
                      <p className="text-2xl font-bold text-gray-800 mt-1">{completedTasks}</p>
                    </div>
                    <div className="bg-gray-50 rounded-xl p-4">
                      <div className="flex items-center gap-2">
                        <div className="w-3 h-3 rounded-full bg-amber-500" />
                        <span className="text-sm text-gray-600">Pending</span>
                      </div>
                      <p className="text-2xl font-bold text-gray-800 mt-1">{pendingTasks}</p>
                    </div>
                  </div>
                </div>

                {/* Recent Tasks Card */}
                <div className="bg-white rounded-2xl shadow-lg p-6">
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="text-lg font-bold text-gray-800">Recent Tasks</h3>
                    <button
                      onClick={() => router.push('/tasks')}
                      className="flex items-center gap-1 text-sm text-red-500 hover:text-red-600 font-medium transition-colors"
                    >
                      View All <ArrowRightIcon />
                    </button>
                  </div>

                  {recentTasks.length === 0 ? (
                    <div className="text-center py-8">
                      <div className="w-16 h-16 mx-auto bg-gray-100 rounded-full flex items-center justify-center mb-3">
                        <TaskIcon />
                      </div>
                      <p className="text-gray-500">No tasks yet</p>
                      <button
                        onClick={() => router.push('/tasks')}
                        className="mt-3 text-red-500 hover:text-red-600 font-medium text-sm"
                      >
                        Create your first task
                      </button>
                    </div>
                  ) : (
                    <div className="space-y-3">
                      {recentTasks.map((task) => (
                        <RecentTask key={task.id} task={task} />
                      ))}
                    </div>
                  )}
                </div>
              </div>

              {/* Quick Actions */}
              <div className="bg-white rounded-2xl shadow-lg p-6">
                <h3 className="text-lg font-bold text-gray-800 mb-4">Quick Actions</h3>
                <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                  <button
                    onClick={() => router.push('/tasks')}
                    className="flex items-center gap-3 p-4 bg-gradient-to-r from-red-500 to-red-600 text-white rounded-xl hover:from-red-600 hover:to-red-700 transition-all shadow-md hover:shadow-lg"
                  >
                    <div className="bg-white/20 rounded-lg p-2">
                      <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                      </svg>
                    </div>
                    <span className="font-medium">Add New Task</span>
                  </button>
                  <button
                    onClick={() => router.push('/tasks')}
                    className="flex items-center gap-3 p-4 bg-gray-100 text-gray-700 rounded-xl hover:bg-gray-200 transition-all"
                  >
                    <div className="bg-white rounded-lg p-2 shadow-sm">
                      <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                      </svg>
                    </div>
                    <span className="font-medium">View All Tasks</span>
                  </button>
                  <button
                    onClick={() => router.push('/settings')}
                    className="flex items-center gap-3 p-4 bg-gray-100 text-gray-700 rounded-xl hover:bg-gray-200 transition-all"
                  >
                    <div className="bg-white rounded-lg p-2 shadow-sm">
                      <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                      </svg>
                    </div>
                    <span className="font-medium">Settings</span>
                  </button>
                </div>
              </div>
            </>
          )}
        </main>
      </div>
    </div>
  );
}

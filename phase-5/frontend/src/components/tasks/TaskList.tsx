'use client';

/**
 * Main task list container with server-side search, filter, and sort.
 */

import React, { useState, useEffect, useCallback, useMemo } from 'react';
import { Task, Tag, Priority, SortField, SortOrder, TaskListParams } from '@/lib/types';
import { getTasks, getTags, toggleTask, deleteTask, ApiError } from '@/lib/api';
import { useAuth } from '@/components/auth/AuthProvider';
import { TaskItem } from './TaskItem';
import { TaskForm } from './TaskForm';
import { LoadingSpinner } from '@/components/ui/LoadingSpinner';
import { ErrorMessage } from '@/components/ui/ErrorMessage';
import { ConfirmDialog } from '@/components/ui/ConfirmDialog';

interface TaskListProps {
  searchQuery?: string;
  onStatsChange?: (stats: { total: number; pending: number; completed: number }) => void;
}

export function TaskList({ searchQuery = '', onStatsChange }: TaskListProps) {
  const { auth } = useAuth();
  const userId = auth.user?.userId;

  const [tasks, setTasks] = useState<Task[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [editingTaskId, setEditingTaskId] = useState<number | null>(null);
  const [deletingTaskId, setDeletingTaskId] = useState<number | null>(null);
  const [isDeleting, setIsDeleting] = useState(false);
  const [showAddForm, setShowAddForm] = useState(false);

  // Filter/sort state
  const [priorityFilter, setPriorityFilter] = useState<Priority | ''>('');
  const [sortField, setSortField] = useState<SortField>('created_at');
  const [sortOrder, setSortOrder] = useState<SortOrder>('desc');
  const [tagFilter, setTagFilter] = useState<string>('');
  const [availableTags, setAvailableTags] = useState<Tag[]>([]);

  // Separate completed and pending
  const pendingTasks = useMemo(() => tasks.filter(t => !t.completed), [tasks]);
  const completedTasks = useMemo(() => tasks.filter(t => t.completed), [tasks]);

  // Update stats
  useEffect(() => {
    if (onStatsChange) {
      onStatsChange({
        total: tasks.length,
        pending: pendingTasks.length,
        completed: completedTasks.length,
      });
    }
  }, [tasks, pendingTasks.length, completedTasks.length, onStatsChange]);

  // Fetch tags
  useEffect(() => {
    if (userId) {
      getTags(userId).then(setAvailableTags).catch(() => {});
    }
  }, [userId]);

  // Fetch tasks with server-side params
  const fetchTasks = useCallback(async () => {
    if (!userId) return;
    setIsLoading(true);
    setError(null);

    try {
      const params: TaskListParams = {
        sort: sortField,
        order: sortOrder,
      };
      if (searchQuery.trim()) params.search = searchQuery.trim();
      if (priorityFilter) params.priority = priorityFilter;
      if (tagFilter) params.tags = tagFilter;

      const data = await getTasks(userId, params);
      setTasks(data);
    } catch (err) {
      if (err instanceof ApiError) {
        setError(err.detail);
      } else {
        setError('Failed to load tasks. Please try again.');
      }
    } finally {
      setIsLoading(false);
    }
  }, [userId, searchQuery, priorityFilter, sortField, sortOrder, tagFilter]);

  useEffect(() => {
    fetchTasks();
  }, [fetchTasks]);

  const handleTaskCreated = (task: Task) => {
    setTasks(prev => [task, ...prev]);
    setShowAddForm(false);
  };

  const handleToggle = async (task: Task) => {
    if (!userId) return;
    const newCompleted = !task.completed;
    setTasks(prev => prev.map(t => (t.id === task.id ? { ...t, completed: newCompleted } : t)));
    try {
      const updated = await toggleTask(userId, task.id, newCompleted);
      // If recurring, the API may return the original task; a new task was created server-side
      setTasks(prev => prev.map(t => (t.id === updated.id ? updated : t)));
      // Refresh to pick up any new recurring task
      if (task.recurrence_rule) fetchTasks();
    } catch (err) {
      setTasks(prev => prev.map(t => (t.id === task.id ? { ...t, completed: task.completed } : t)));
      if (err instanceof ApiError) setError(err.detail);
      else setError('Failed to update task. Please try again.');
    }
  };

  const handleUpdate = (updatedTask: Task) => {
    setTasks(prev => prev.map(t => (t.id === updatedTask.id ? updatedTask : t)));
    setEditingTaskId(null);
  };

  const handleDeleteClick = (taskId: number) => setDeletingTaskId(taskId);

  const handleDeleteConfirm = async () => {
    if (!userId || deletingTaskId === null) return;
    setIsDeleting(true);
    const taskToDelete = tasks.find(t => t.id === deletingTaskId);
    setTasks(prev => prev.filter(t => t.id !== deletingTaskId));
    setDeletingTaskId(null);

    try {
      await deleteTask(userId, deletingTaskId);
    } catch (err) {
      if (taskToDelete) setTasks(prev => [...prev, taskToDelete].sort((a, b) => b.id - a.id));
      if (err instanceof ApiError) setError(err.detail);
      else setError('Failed to delete task. Please try again.');
    } finally {
      setIsDeleting(false);
    }
  };

  const handleDeleteCancel = () => setDeletingTaskId(null);

  if (isLoading) {
    return (
      <div className="flex justify-center py-12">
        <LoadingSpinner size="lg" />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {error && <ErrorMessage message={error} onDismiss={() => setError(null)} />}

      {/* Filters Bar */}
      <div className="bg-white rounded-xl shadow-card p-4">
        <div className="flex flex-wrap gap-3 items-end">
          <div>
            <label className="block text-xs font-medium text-gray-500 mb-1">Priority</label>
            <select
              value={priorityFilter}
              onChange={(e) => setPriorityFilter(e.target.value as Priority | '')}
              className="px-3 py-1.5 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-400"
            >
              <option value="">All</option>
              <option value="urgent">Urgent</option>
              <option value="high">High</option>
              <option value="medium">Medium</option>
              <option value="low">Low</option>
            </select>
          </div>
          <div>
            <label className="block text-xs font-medium text-gray-500 mb-1">Sort by</label>
            <select
              value={sortField}
              onChange={(e) => setSortField(e.target.value as SortField)}
              className="px-3 py-1.5 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-400"
            >
              <option value="created_at">Date Created</option>
              <option value="title">Title</option>
              <option value="priority">Priority</option>
              <option value="due_date">Due Date</option>
            </select>
          </div>
          <div>
            <label className="block text-xs font-medium text-gray-500 mb-1">Order</label>
            <select
              value={sortOrder}
              onChange={(e) => setSortOrder(e.target.value as SortOrder)}
              className="px-3 py-1.5 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-400"
            >
              <option value="desc">Newest first</option>
              <option value="asc">Oldest first</option>
            </select>
          </div>
          {availableTags.length > 0 && (
            <div>
              <label className="block text-xs font-medium text-gray-500 mb-1">Tag</label>
              <select
                value={tagFilter}
                onChange={(e) => setTagFilter(e.target.value)}
                className="px-3 py-1.5 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-400"
              >
                <option value="">All tags</option>
                {availableTags.map(tag => (
                  <option key={tag.id} value={tag.name}>{tag.name}</option>
                ))}
              </select>
            </div>
          )}
        </div>
      </div>

      {/* Add Task Section */}
      <div className="bg-white rounded-xl shadow-card p-4 lg:p-6">
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 mb-4">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-red-100 flex items-center justify-center flex-shrink-0">
              <svg className="w-5 h-5 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
              </svg>
            </div>
            <h3 className="text-lg font-bold text-gray-800">My Tasks</h3>
          </div>
          <button
            onClick={() => setShowAddForm(!showAddForm)}
            className="flex items-center justify-center gap-2 px-4 py-2.5 bg-red-500 text-white rounded-lg hover:bg-red-600 transition-colors font-medium shadow-sm w-full sm:w-auto"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
            </svg>
            Add Task
          </button>
        </div>

        {showAddForm && (
          <div className="mb-6 animate-fade-in">
            <TaskForm onTaskCreated={handleTaskCreated} onCancel={() => setShowAddForm(false)} />
          </div>
        )}

        <p className="text-sm text-gray-500 mb-4">
          {pendingTasks.length} task{pendingTasks.length !== 1 ? 's' : ''} pending
          {searchQuery && ' (filtered)'}
        </p>

        {pendingTasks.length === 0 && !showAddForm ? (
          <div className="text-center py-8">
            <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-gray-100 flex items-center justify-center">
              <svg className="w-8 h-8 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
              </svg>
            </div>
            <p className="text-gray-500">
              {searchQuery ? 'No tasks match your search' : 'No pending tasks. Click "Add Task" to create one!'}
            </p>
          </div>
        ) : (
          <div className="space-y-3">
            {pendingTasks.map(task => (
              <TaskItem
                key={task.id}
                task={task}
                isEditing={editingTaskId === task.id}
                onToggle={handleToggle}
                onUpdate={handleUpdate}
                onDelete={handleDeleteClick}
                onEditStart={setEditingTaskId}
                onEditCancel={() => setEditingTaskId(null)}
              />
            ))}
          </div>
        )}
      </div>

      {/* Completed Tasks */}
      {completedTasks.length > 0 && (
        <div className="bg-white rounded-xl shadow-card p-4 lg:p-6">
          <div className="flex items-center gap-3 mb-4">
            <div className="w-10 h-10 rounded-lg bg-green-100 flex items-center justify-center flex-shrink-0">
              <svg className="w-5 h-5 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
              </svg>
            </div>
            <h3 className="text-lg font-bold text-gray-800">Completed Tasks</h3>
          </div>
          <p className="text-sm text-gray-500 mb-4">
            {completedTasks.length} task{completedTasks.length !== 1 ? 's' : ''} completed
          </p>
          <div className="space-y-3">
            {completedTasks.map(task => (
              <TaskItem
                key={task.id}
                task={task}
                isEditing={editingTaskId === task.id}
                onToggle={handleToggle}
                onUpdate={handleUpdate}
                onDelete={handleDeleteClick}
                onEditStart={setEditingTaskId}
                onEditCancel={() => setEditingTaskId(null)}
              />
            ))}
          </div>
        </div>
      )}

      <ConfirmDialog
        isOpen={deletingTaskId !== null}
        title="Delete Task"
        message="Are you sure you want to delete this task? This action cannot be undone."
        confirmLabel={isDeleting ? 'Deleting...' : 'Delete'}
        onConfirm={handleDeleteConfirm}
        onCancel={handleDeleteCancel}
      />
    </div>
  );
}

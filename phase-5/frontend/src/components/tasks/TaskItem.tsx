'use client';

/**
 * Individual task display component with priority badge, due date, and tags.
 */

import React from 'react';
import { Task, Priority } from '@/lib/types';

interface TaskItemProps {
  task: Task;
  isEditing: boolean;
  onToggle: (task: Task) => void;
  onUpdate: (task: Task) => void;
  onDelete: (taskId: number) => void;
  onEditStart: (taskId: number) => void;
  onEditCancel: () => void;
}

const PRIORITY_STYLES: Record<Priority, { bg: string; text: string; label: string }> = {
  low: { bg: 'bg-gray-100', text: 'text-gray-600', label: 'Low' },
  medium: { bg: 'bg-blue-100', text: 'text-blue-600', label: 'Medium' },
  high: { bg: 'bg-orange-100', text: 'text-orange-600', label: 'High' },
  urgent: { bg: 'bg-red-100', text: 'text-red-600', label: 'Urgent' },
};

const EditIcon = () => (
  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
  </svg>
);

const DeleteIcon = () => (
  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
  </svg>
);

const RecurIcon = () => (
  <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
  </svg>
);

function formatDueDate(dateStr: string): { text: string; className: string } {
  // Handle both ISO timestamp (2025-02-10T14:30:00) and date-only (2025-02-10) formats
  const due = new Date(dateStr);
  if (isNaN(due.getTime())) {
    return { text: 'Invalid date', className: 'text-gray-400' };
  }

  const now = new Date();
  now.setHours(0, 0, 0, 0);
  const dueDay = new Date(due);
  dueDay.setHours(0, 0, 0, 0);
  const diffDays = Math.floor((dueDay.getTime() - now.getTime()) / (1000 * 60 * 60 * 24));

  const formatted = due.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });

  if (diffDays < 0) return { text: `${formatted} (overdue)`, className: 'text-red-600 font-medium' };
  if (diffDays === 0) return { text: 'Today', className: 'text-orange-600 font-medium' };
  if (diffDays === 1) return { text: 'Tomorrow', className: 'text-orange-500' };
  if (diffDays <= 7) return { text: formatted, className: 'text-yellow-600' };
  return { text: formatted, className: 'text-gray-500' };
}

export function TaskItem({
  task,
  isEditing,
  onToggle,
  onUpdate,
  onDelete,
  onEditStart,
  onEditCancel,
}: TaskItemProps) {
  if (isEditing) {
    const TaskEditForm = require('./TaskEditForm').TaskEditForm;
    return <TaskEditForm task={task} onSave={onUpdate} onCancel={onEditCancel} />;
  }

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
  };

  const priorityStyle = PRIORITY_STYLES[task.priority || 'medium'];
  const dueInfo = task.due_date ? formatDueDate(task.due_date) : null;

  return (
    <div className={`task-card p-3 sm:p-4 rounded-lg border bg-white ${task.completed ? 'border-gray-200 bg-gray-50' : 'border-gray-200 hover:border-red-200'}`}>
      <div className="flex items-start gap-3 sm:gap-4">
        {/* Checkbox */}
        <div className="flex-shrink-0 pt-0.5">
          <label className="relative flex items-center cursor-pointer">
            <input
              type="checkbox"
              checked={task.completed}
              onChange={() => onToggle(task)}
              className="sr-only"
              aria-label={`Mark "${task.title}" as ${task.completed ? 'incomplete' : 'complete'}`}
            />
            <div className={`w-5 h-5 rounded-full border-2 flex items-center justify-center transition-colors ${task.completed ? 'bg-green-500 border-green-500' : 'border-gray-300 hover:border-red-400'}`}>
              {task.completed && (
                <svg className="w-3 h-3 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" />
                </svg>
              )}
            </div>
          </label>
        </div>

        {/* Content */}
        <div className="flex-1 min-w-0">
          <div className="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-2">
            <div className="flex-1 min-w-0">
              <div className="flex items-center gap-2 flex-wrap">
                <h4 className={`text-sm sm:text-base font-medium break-words ${task.completed ? 'text-gray-400 line-through' : 'text-gray-900'}`}>
                  {task.title}
                </h4>
                {/* Priority badge */}
                <span className={`px-2 py-0.5 text-xs font-medium rounded-full ${priorityStyle.bg} ${priorityStyle.text}`}>
                  {priorityStyle.label}
                </span>
                {/* Recurrence indicator */}
                {task.recurrence_rule && (
                  <span className="text-gray-400 flex items-center gap-0.5" title={`Repeats ${task.recurrence_rule.type}`}>
                    <RecurIcon />
                    <span className="text-xs">{task.recurrence_rule.type}</span>
                  </span>
                )}
              </div>
              {task.description && (
                <p className={`mt-1 text-xs sm:text-sm break-words ${task.completed ? 'text-gray-400' : 'text-gray-500'}`}>
                  {task.description}
                </p>
              )}
              {/* Tags */}
              {task.tags && task.tags.length > 0 && (
                <div className="flex flex-wrap gap-1 mt-1.5">
                  {task.tags.map(tag => (
                    <span key={tag.id} className="px-2 py-0.5 text-xs bg-gray-100 text-gray-600 rounded-full">
                      {tag.name}
                    </span>
                  ))}
                </div>
              )}
            </div>

            {/* Status badge */}
            <span className={`self-start flex-shrink-0 px-2 py-1 text-xs font-medium rounded-full ${task.completed ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'}`}>
              {task.completed ? 'Completed' : 'Pending'}
            </span>
          </div>

          {/* Meta info */}
          <div className="mt-2 flex items-center justify-between">
            <div className="flex items-center gap-3">
              <span className="text-xs text-gray-400">{formatDate(task.created_at)}</span>
              {dueInfo && (
                <span className={`text-xs ${dueInfo.className}`}>Due: {dueInfo.text}</span>
              )}
            </div>

            {/* Mobile Actions */}
            <div className="flex sm:hidden items-center gap-1">
              <button type="button" onClick={() => onEditStart(task.id)} className="p-1.5 text-gray-400 hover:text-red-500 hover:bg-red-50 rounded-lg transition-colors" aria-label="Edit task">
                <EditIcon />
              </button>
              <button type="button" onClick={() => onDelete(task.id)} className="p-1.5 text-gray-400 hover:text-red-500 hover:bg-red-50 rounded-lg transition-colors" aria-label="Delete task">
                <DeleteIcon />
              </button>
            </div>
          </div>
        </div>

        {/* Desktop Actions */}
        <div className="hidden sm:flex flex-shrink-0 items-center gap-1">
          <button type="button" onClick={() => onEditStart(task.id)} className="p-2 text-gray-400 hover:text-red-500 hover:bg-red-50 rounded-lg transition-colors" aria-label="Edit task">
            <EditIcon />
          </button>
          <button type="button" onClick={() => onDelete(task.id)} className="p-2 text-gray-400 hover:text-red-500 hover:bg-red-50 rounded-lg transition-colors" aria-label="Delete task">
            <DeleteIcon />
          </button>
        </div>
      </div>
    </div>
  );
}

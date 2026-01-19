'use client';

/**
 * Individual task display component with modern card design.
 * Shows task info with checkbox, edit, and delete actions.
 */

import React from 'react';
import { Task } from '@/lib/types';

interface TaskItemProps {
  task: Task;
  isEditing: boolean;
  onToggle: (task: Task) => void;
  onUpdate: (task: Task) => void;
  onDelete: (taskId: number) => void;
  onEditStart: (taskId: number) => void;
  onEditCancel: () => void;
}

// Icons
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

export function TaskItem({
  task,
  isEditing,
  onToggle,
  onUpdate,
  onDelete,
  onEditStart,
  onEditCancel,
}: TaskItemProps) {
  // If in edit mode, render the edit form
  if (isEditing) {
    const TaskEditForm = require('./TaskEditForm').TaskEditForm;
    return (
      <TaskEditForm
        task={task}
        onSave={onUpdate}
        onCancel={onEditCancel}
      />
    );
  }

  // Format date
  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
    });
  };

  return (
    <div className={`
      task-card p-3 sm:p-4 rounded-lg border bg-white
      ${task.completed
        ? 'border-gray-200 bg-gray-50'
        : 'border-gray-200 hover:border-red-200'
      }
    `}>
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
            <div className={`
              w-5 h-5 rounded-full border-2 flex items-center justify-center transition-colors
              ${task.completed
                ? 'bg-green-500 border-green-500'
                : 'border-gray-300 hover:border-red-400'
              }
            `}>
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
              <h4 className={`
                text-sm sm:text-base font-medium break-words
                ${task.completed ? 'text-gray-400 line-through' : 'text-gray-900'}
              `}>
                {task.title}
              </h4>
              {task.description && (
                <p className={`
                  mt-1 text-xs sm:text-sm break-words
                  ${task.completed ? 'text-gray-400' : 'text-gray-500'}
                `}>
                  {task.description}
                </p>
              )}
            </div>

            {/* Status badge */}
            <span className={`
              self-start flex-shrink-0 px-2 py-1 text-xs font-medium rounded-full
              ${task.completed
                ? 'bg-green-100 text-green-700'
                : 'bg-red-100 text-red-700'
              }
            `}>
              {task.completed ? 'Completed' : 'Pending'}
            </span>
          </div>

          {/* Meta info and Actions on mobile */}
          <div className="mt-2 flex items-center justify-between">
            <span className="text-xs text-gray-400">
              {formatDate(task.created_at)}
            </span>

            {/* Mobile Actions */}
            <div className="flex sm:hidden items-center gap-1">
              <button
                type="button"
                onClick={() => onEditStart(task.id)}
                className="p-1.5 text-gray-400 hover:text-red-500 hover:bg-red-50 rounded-lg transition-colors"
                aria-label="Edit task"
              >
                <EditIcon />
              </button>
              <button
                type="button"
                onClick={() => onDelete(task.id)}
                className="p-1.5 text-gray-400 hover:text-red-500 hover:bg-red-50 rounded-lg transition-colors"
                aria-label="Delete task"
              >
                <DeleteIcon />
              </button>
            </div>
          </div>
        </div>

        {/* Desktop Actions */}
        <div className="hidden sm:flex flex-shrink-0 items-center gap-1">
          <button
            type="button"
            onClick={() => onEditStart(task.id)}
            className="p-2 text-gray-400 hover:text-red-500 hover:bg-red-50 rounded-lg transition-colors"
            aria-label="Edit task"
          >
            <EditIcon />
          </button>
          <button
            type="button"
            onClick={() => onDelete(task.id)}
            className="p-2 text-gray-400 hover:text-red-500 hover:bg-red-50 rounded-lg transition-colors"
            aria-label="Delete task"
          >
            <DeleteIcon />
          </button>
        </div>
      </div>
    </div>
  );
}

'use client';

/**
 * Task creation form component with modern inline design.
 */

import React, { useState } from 'react';
import { Task } from '@/lib/types';
import { createTask, ApiError } from '@/lib/api';
import { useAuth } from '@/components/auth/AuthProvider';
import { Button } from '@/components/ui/Button';
import { ErrorMessage } from '@/components/ui/ErrorMessage';
import { VALIDATION } from '@/lib/constants';

interface TaskFormProps {
  onTaskCreated: (task: Task) => void;
  onCancel?: () => void;
}

export function TaskForm({ onTaskCreated, onCancel }: TaskFormProps) {
  const { auth } = useAuth();
  const userId = auth.user?.userId;

  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [errors, setErrors] = useState<{ title?: string; description?: string }>({});
  const [submitError, setSubmitError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  // Validate form
  const validate = (): boolean => {
    const newErrors: { title?: string; description?: string } = {};

    const trimmedTitle = title.trim();
    if (!trimmedTitle) {
      newErrors.title = VALIDATION.taskTitle.messageRequired;
    } else if (trimmedTitle.length > VALIDATION.taskTitle.maxLength) {
      newErrors.title = VALIDATION.taskTitle.messageMaxLength;
    }

    if (description.length > VALIDATION.taskDescription.maxLength) {
      newErrors.description = VALIDATION.taskDescription.message;
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  // Handle form submission
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitError(null);

    if (!validate() || !userId) {
      return;
    }

    setIsSubmitting(true);

    try {
      const task = await createTask(userId, {
        title: title.trim(),
        description: description.trim() || undefined,
      });

      setTitle('');
      setDescription('');
      setErrors({});
      onTaskCreated(task);
    } catch (err) {
      if (err instanceof ApiError) {
        setSubmitError(err.detail);
      } else {
        setSubmitError('Failed to create task. Please try again.');
      }
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="border border-gray-200 rounded-lg p-4 bg-gray-50">
      {submitError && (
        <div className="mb-4">
          <ErrorMessage message={submitError} onDismiss={() => setSubmitError(null)} />
        </div>
      )}

      <div className="space-y-4">
        {/* Title Input */}
        <div>
          <input
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            placeholder="Task title..."
            className={`
              w-full px-4 py-3 border rounded-lg
              placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-red-500
              ${errors.title ? 'border-red-500' : 'border-gray-300'}
            `}
            maxLength={200}
          />
          {errors.title && (
            <p className="mt-1 text-sm text-red-600">{errors.title}</p>
          )}
        </div>

        {/* Description Input */}
        <div>
          <textarea
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            placeholder="Add description (optional)..."
            rows={2}
            maxLength={1000}
            className={`
              w-full px-4 py-3 border rounded-lg resize-none
              placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-red-500
              ${errors.description ? 'border-red-500' : 'border-gray-300'}
            `}
          />
          {errors.description && (
            <p className="mt-1 text-sm text-red-600">{errors.description}</p>
          )}
        </div>

        {/* Actions */}
        <div className="flex justify-end gap-2">
          {onCancel && (
            <Button
              type="button"
              variant="secondary"
              onClick={onCancel}
            >
              Cancel
            </Button>
          )}
          <Button
            type="submit"
            variant="primary"
            isLoading={isSubmitting}
            disabled={isSubmitting}
          >
            Create Task
          </Button>
        </div>
      </div>
    </form>
  );
}

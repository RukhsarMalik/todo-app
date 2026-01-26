'use client';

/**
 * Task edit form component.
 * Allows users to edit existing task title and description.
 */

import React, { useState } from 'react';
import { Task } from '@/lib/types';
import { updateTask, ApiError } from '@/lib/api';
import { useAuth } from '@/components/auth/AuthProvider';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { ErrorMessage } from '@/components/ui/ErrorMessage';
import { VALIDATION } from '@/lib/constants';

interface TaskEditFormProps {
  task: Task;
  onSave: (task: Task) => void;
  onCancel: () => void;
}

export function TaskEditForm({ task, onSave, onCancel }: TaskEditFormProps) {
  const { auth } = useAuth();
  const userId = auth.user?.userId;

  const [title, setTitle] = useState(task.title);
  const [description, setDescription] = useState(task.description || '');
  const [errors, setErrors] = useState<{ title?: string; description?: string }>({});
  const [submitError, setSubmitError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  // Validate form
  const validate = (): boolean => {
    const newErrors: { title?: string; description?: string } = {};

    // Title validation
    const trimmedTitle = title.trim();
    if (!trimmedTitle) {
      newErrors.title = VALIDATION.taskTitle.messageRequired;
    } else if (trimmedTitle.length > VALIDATION.taskTitle.maxLength) {
      newErrors.title = VALIDATION.taskTitle.messageMaxLength;
    }

    // Description validation
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
      const updatedTask = await updateTask(userId, task.id, {
        title: title.trim(),
        description: description.trim() || undefined,
      });

      onSave(updatedTask);
    } catch (err) {
      if (err instanceof ApiError) {
        setSubmitError(err.detail);
      } else {
        setSubmitError('Failed to update task. Please try again.');
      }
    } finally {
      setIsSubmitting(false);
    }
  };

  // Handle cancel - discard changes
  const handleCancel = () => {
    onCancel();
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="bg-white rounded-lg border border-blue-300 p-4 sm:p-6"
    >
      {submitError && (
        <div className="mb-4">
          <ErrorMessage message={submitError} onDismiss={() => setSubmitError(null)} />
        </div>
      )}

      <div className="space-y-4">
        <Input
          label="Title"
          name="title"
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          error={errors.title}
          required
          maxLength={200}
        />

        <div>
          <label
            htmlFor="edit-description"
            className="block text-sm font-medium text-gray-700 mb-1"
          >
            Description (optional)
          </label>
          <textarea
            id="edit-description"
            name="description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            rows={3}
            maxLength={1000}
            className={`
              block w-full px-3 py-2
              border rounded-md shadow-sm
              placeholder-gray-400
              focus:outline-none focus:ring-2 focus:ring-offset-0
              transition-colors duration-200
              ${errors.description
                ? 'border-red-500 focus:border-red-500 focus:ring-red-500'
                : 'border-gray-300 focus:border-blue-500 focus:ring-blue-500'
              }
            `}
          />
          {errors.description && (
            <p className="mt-1 text-sm text-red-600">{errors.description}</p>
          )}
        </div>

        <div className="flex justify-end gap-3">
          <Button
            type="button"
            variant="secondary"
            onClick={handleCancel}
            disabled={isSubmitting}
          >
            Cancel
          </Button>
          <Button
            type="submit"
            variant="primary"
            isLoading={isSubmitting}
            disabled={isSubmitting}
          >
            Save
          </Button>
        </div>
      </div>
    </form>
  );
}

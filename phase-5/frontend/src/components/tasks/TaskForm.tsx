'use client';

/**
 * Task creation form component with priority, due date, tags, and recurrence.
 */

import React, { useState, useEffect } from 'react';
import { Task, Tag, Priority, RecurrenceRule } from '@/lib/types';
import { createTask, getTags, createTag, ApiError } from '@/lib/api';
import { useAuth } from '@/components/auth/AuthProvider';
import { Button } from '@/components/ui/Button';
import { ErrorMessage } from '@/components/ui/ErrorMessage';
import { VALIDATION } from '@/lib/constants';

interface TaskFormProps {
  onTaskCreated: (task: Task) => void;
  onCancel?: () => void;
}

const PRIORITY_OPTIONS: { value: Priority; label: string; color: string }[] = [
  { value: 'low', label: 'Low', color: 'bg-gray-100 text-gray-600' },
  { value: 'medium', label: 'Medium', color: 'bg-blue-100 text-blue-600' },
  { value: 'high', label: 'High', color: 'bg-orange-100 text-orange-600' },
  { value: 'urgent', label: 'Urgent', color: 'bg-red-100 text-red-600' },
];

export function TaskForm({ onTaskCreated, onCancel }: TaskFormProps) {
  const { auth } = useAuth();
  const userId = auth.user?.userId;

  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [priority, setPriority] = useState<Priority>('medium');
  const [dueDate, setDueDate] = useState('');
  const [selectedTagIds, setSelectedTagIds] = useState<number[]>([]);
  const [availableTags, setAvailableTags] = useState<Tag[]>([]);
  const [newTagName, setNewTagName] = useState('');
  const [recurrenceType, setRecurrenceType] = useState<'' | 'daily' | 'weekly' | 'monthly'>('');
  const [showAdvanced, setShowAdvanced] = useState(false);

  const [errors, setErrors] = useState<{ title?: string; description?: string }>({});
  const [submitError, setSubmitError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  // Fetch available tags
  useEffect(() => {
    if (userId) {
      getTags(userId).then(setAvailableTags).catch(() => {});
    }
  }, [userId]);

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

  const handleAddTag = async () => {
    if (!userId || !newTagName.trim()) return;
    try {
      const tag = await createTag(userId, { name: newTagName.trim() });
      setAvailableTags(prev => [...prev, tag]);
      setSelectedTagIds(prev => [...prev, tag.id]);
      setNewTagName('');
    } catch {
      // Tag may already exist
    }
  };

  const toggleTag = (tagId: number) => {
    setSelectedTagIds(prev =>
      prev.includes(tagId) ? prev.filter(id => id !== tagId) : [...prev, tagId]
    );
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitError(null);
    if (!validate() || !userId) return;

    setIsSubmitting(true);
    try {
      const recurrence_rule: RecurrenceRule | undefined = recurrenceType
        ? { type: recurrenceType }
        : undefined;

      const task = await createTask(userId, {
        title: title.trim(),
        description: description.trim() || undefined,
        priority,
        due_date: dueDate || undefined,
        tag_ids: selectedTagIds.length > 0 ? selectedTagIds : undefined,
        recurrence_rule,
      });

      setTitle('');
      setDescription('');
      setPriority('medium');
      setDueDate('');
      setSelectedTagIds([]);
      setRecurrenceType('');
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
        {/* Title */}
        <div>
          <input
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            placeholder="Task title..."
            className={`w-full px-4 py-3 border rounded-lg placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-red-500 ${errors.title ? 'border-red-500' : 'border-gray-300'}`}
            maxLength={200}
          />
          {errors.title && <p className="mt-1 text-sm text-red-600">{errors.title}</p>}
        </div>

        {/* Description */}
        <div>
          <textarea
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            placeholder="Add description (optional)..."
            rows={2}
            maxLength={1000}
            className={`w-full px-4 py-3 border rounded-lg resize-none placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-red-500 ${errors.description ? 'border-red-500' : 'border-gray-300'}`}
          />
          {errors.description && <p className="mt-1 text-sm text-red-600">{errors.description}</p>}
        </div>

        {/* Priority & Due Date row */}
        <div className="flex flex-col sm:flex-row gap-3">
          <div className="flex-1">
            <label className="block text-sm font-medium text-gray-700 mb-1">Priority</label>
            <select
              value={priority}
              onChange={(e) => setPriority(e.target.value as Priority)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500"
            >
              {PRIORITY_OPTIONS.map(opt => (
                <option key={opt.value} value={opt.value}>{opt.label}</option>
              ))}
            </select>
          </div>
          <div className="flex-1">
            <label className="block text-sm font-medium text-gray-700 mb-1">Due Date</label>
            <input
              type="date"
              value={dueDate}
              onChange={(e) => setDueDate(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500"
            />
          </div>
        </div>

        {/* Tags */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Tags</label>
          <div className="flex flex-wrap gap-2 mb-2">
            {availableTags.map(tag => (
              <button
                key={tag.id}
                type="button"
                onClick={() => toggleTag(tag.id)}
                className={`px-3 py-1 text-xs rounded-full border transition-colors ${
                  selectedTagIds.includes(tag.id)
                    ? 'bg-red-500 text-white border-red-500'
                    : 'bg-white text-gray-600 border-gray-300 hover:border-red-300'
                }`}
              >
                {tag.name}
              </button>
            ))}
          </div>
          <div className="flex gap-2">
            <input
              type="text"
              value={newTagName}
              onChange={(e) => setNewTagName(e.target.value)}
              placeholder="New tag..."
              className="flex-1 px-3 py-1.5 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500"
              onKeyDown={(e) => { if (e.key === 'Enter') { e.preventDefault(); handleAddTag(); } }}
            />
            <button
              type="button"
              onClick={handleAddTag}
              className="px-3 py-1.5 text-sm bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300"
            >
              Add
            </button>
          </div>
        </div>

        {/* Advanced toggle */}
        <button
          type="button"
          onClick={() => setShowAdvanced(!showAdvanced)}
          className="text-sm text-gray-500 hover:text-red-500"
        >
          {showAdvanced ? 'Hide advanced options' : 'Show advanced options'}
        </button>

        {showAdvanced && (
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Recurrence</label>
            <select
              value={recurrenceType}
              onChange={(e) => setRecurrenceType(e.target.value as '' | 'daily' | 'weekly' | 'monthly')}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500"
            >
              <option value="">No recurrence</option>
              <option value="daily">Daily</option>
              <option value="weekly">Weekly</option>
              <option value="monthly">Monthly</option>
            </select>
          </div>
        )}

        {/* Actions */}
        <div className="flex justify-end gap-2">
          {onCancel && (
            <Button type="button" variant="secondary" onClick={onCancel}>Cancel</Button>
          )}
          <Button type="submit" variant="primary" isLoading={isSubmitting} disabled={isSubmitting}>
            Create Task
          </Button>
        </div>
      </div>
    </form>
  );
}

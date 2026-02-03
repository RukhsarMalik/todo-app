'use client';

/**
 * Task edit form with priority, due date, tags, and recurrence editing.
 */

import React, { useState, useEffect } from 'react';
import { Task, Tag, Priority, RecurrenceRule } from '@/lib/types';
import { updateTask, getTags, createTag, ApiError } from '@/lib/api';
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

const PRIORITY_OPTIONS: { value: Priority; label: string }[] = [
  { value: 'low', label: 'Low' },
  { value: 'medium', label: 'Medium' },
  { value: 'high', label: 'High' },
  { value: 'urgent', label: 'Urgent' },
];

export function TaskEditForm({ task, onSave, onCancel }: TaskEditFormProps) {
  const { auth } = useAuth();
  const userId = auth.user?.userId;

  const [title, setTitle] = useState(task.title);
  const [description, setDescription] = useState(task.description || '');
  const [priority, setPriority] = useState<Priority>(task.priority || 'medium');
  // Convert ISO timestamp to YYYY-MM-DD for HTML date input
  const [dueDate, setDueDate] = useState(() => {
    if (!task.due_date) return '';
    const date = new Date(task.due_date);
    if (isNaN(date.getTime())) return '';
    return date.toISOString().split('T')[0];
  });
  const [selectedTagIds, setSelectedTagIds] = useState<number[]>(task.tags?.map(t => t.id) || []);
  const [availableTags, setAvailableTags] = useState<Tag[]>([]);
  const [newTagName, setNewTagName] = useState('');
  const [recurrenceType, setRecurrenceType] = useState<'' | 'daily' | 'weekly' | 'monthly'>(
    task.recurrence_rule?.type || ''
  );

  const [errors, setErrors] = useState<{ title?: string; description?: string }>({});
  const [submitError, setSubmitError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

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
      const recurrence_rule: RecurrenceRule | null = recurrenceType
        ? { type: recurrenceType }
        : null;

      const updatedTask = await updateTask(userId, task.id, {
        title: title.trim(),
        description: description.trim() || undefined,
        priority,
        due_date: dueDate || null,
        tag_ids: selectedTagIds,
        recurrence_rule,
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

  return (
    <form onSubmit={handleSubmit} className="bg-white rounded-lg border border-blue-300 p-4 sm:p-6">
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
          <label htmlFor="edit-description" className="block text-sm font-medium text-gray-700 mb-1">
            Description (optional)
          </label>
          <textarea
            id="edit-description"
            name="description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            rows={3}
            maxLength={1000}
            className={`block w-full px-3 py-2 border rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-offset-0 transition-colors duration-200 ${errors.description ? 'border-red-500 focus:border-red-500 focus:ring-red-500' : 'border-gray-300 focus:border-blue-500 focus:ring-blue-500'}`}
          />
          {errors.description && <p className="mt-1 text-sm text-red-600">{errors.description}</p>}
        </div>

        {/* Priority & Due Date */}
        <div className="flex flex-col sm:flex-row gap-3">
          <div className="flex-1">
            <label className="block text-sm font-medium text-gray-700 mb-1">Priority</label>
            <select
              value={priority}
              onChange={(e) => setPriority(e.target.value as Priority)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
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
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
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
                    ? 'bg-blue-500 text-white border-blue-500'
                    : 'bg-white text-gray-600 border-gray-300 hover:border-blue-300'
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
              className="flex-1 px-3 py-1.5 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              onKeyDown={(e) => { if (e.key === 'Enter') { e.preventDefault(); handleAddTag(); } }}
            />
            <button type="button" onClick={handleAddTag} className="px-3 py-1.5 text-sm bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300">
              Add
            </button>
          </div>
        </div>

        {/* Recurrence */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Recurrence</label>
          <select
            value={recurrenceType}
            onChange={(e) => setRecurrenceType(e.target.value as '' | 'daily' | 'weekly' | 'monthly')}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">No recurrence</option>
            <option value="daily">Daily</option>
            <option value="weekly">Weekly</option>
            <option value="monthly">Monthly</option>
          </select>
        </div>

        <div className="flex justify-end gap-3">
          <Button type="button" variant="secondary" onClick={onCancel} disabled={isSubmitting}>Cancel</Button>
          <Button type="submit" variant="primary" isLoading={isSubmitting} disabled={isSubmitting}>Save</Button>
        </div>
      </div>
    </form>
  );
}

import { useState, useCallback } from 'react';

/**
 * Toggle hook - simple boolean state management
 * Use case: Show/hide, open/close, enable/disable states
 */
export function useToggle(initialValue: boolean = false): [boolean, () => void, (value: boolean) => void] {
  const [value, setValue] = useState(initialValue);

  const toggle = useCallback(() => setValue(v => !v), []);
  const set = useCallback((newValue: boolean) => setValue(newValue), []);

  return [value, toggle, set];
}

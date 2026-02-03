import { useState, useCallback } from 'react';

/**
 * Copy to clipboard hook - copy text with feedback
 * Use case: Copy buttons, share links, code snippets
 */
export function useCopyToClipboard(resetDelay: number = 2000): {
  copied: boolean;
  copy: (text: string) => Promise<boolean>;
  reset: () => void;
} {
  const [copied, setCopied] = useState(false);

  const copy = useCallback(async (text: string): Promise<boolean> => {
    if (!navigator?.clipboard) {
      console.warn('Clipboard not supported');
      return false;
    }

    try {
      await navigator.clipboard.writeText(text);
      setCopied(true);

      if (resetDelay > 0) {
        setTimeout(() => setCopied(false), resetDelay);
      }
      return true;
    } catch {
      console.warn('Copy failed');
      setCopied(false);
      return false;
    }
  }, [resetDelay]);

  const reset = useCallback(() => setCopied(false), []);

  return { copied, copy, reset };
}

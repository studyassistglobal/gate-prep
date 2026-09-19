import { useEffect, useState, useCallback } from 'react';

// Theme persistence key. The anti-FOUC script in index.html reads the same key.
const KEY = 'df-theme';

function getInitial() {
  if (typeof window === 'undefined') return 'dark';
  try {
    const saved = window.localStorage.getItem(KEY);
    if (saved === 'light' || saved === 'dark') return saved;
  } catch (e) {
    /* ignore */
  }
  return 'dark';
}

/**
 * Dark/light theme hook. Dark is the design default ("Deep Focus").
 * Toggles the `dark`/`light` class on <html> (the styles.css tokens switch
 * under `html.light`) and persists the choice in localStorage.
 */
export function useTheme() {
  const [theme, setTheme] = useState(getInitial);

  useEffect(() => {
    const root = document.documentElement;
    root.classList.remove('dark', 'light');
    root.classList.add(theme);
    root.style.colorScheme = theme;
    try {
      window.localStorage.setItem(KEY, theme);
    } catch (e) {
      /* ignore */
    }
  }, [theme]);

  const toggle = useCallback(() => {
    setTheme((t) => (t === 'dark' ? 'light' : 'dark'));
  }, []);

  return { theme, toggle, isDark: theme === 'dark' };
}
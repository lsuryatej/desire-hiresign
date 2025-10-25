/**
 * DesignHire Design System
 * Minimalist, low-strain UI theme configuration
 */

export const colors = {
  // Core colors
  bg: '#F6F7F9',
  surface: '#FFFFFF',
  
  // Brand colors
  primary: '#3B82F6',
  accent: '#7C3AED',
  
  // Text
  text: '#0F172A',
  muted: '#475569',
  
  // Status
  success: '#16A34A',
  error: '#DC2626',
  
  // Shadows
  shadow: '0 6px 18px rgba(14, 18, 32, 0.06)',
  
  // Borders
  border: '#E2E8F0',
  
  // Overlays
  overlay: 'rgba(15, 23, 42, 0.6)',
} as const;

export const typography = {
  // Font families
  fontFamily: {
    base: 'Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
    mono: 'ui-monospace, SFMono-Regular, "SF Mono", Menlo, monospace',
  },
  
  // Font sizes
  fontSize: {
    xs: '12px',
    sm: '14px',
    base: '16px',
    lg: '18px',
    xl: '22px',
    '2xl': '28px',
    '3xl': '32px',
  },
  
  // Font weights
  fontWeight: {
    normal: '400',
    medium: '500',
    semibold: '600',
    bold: '700',
  },
  
  // Line heights
  lineHeight: {
    tight: '1.25',
    normal: '1.45',
    relaxed: '1.75',
  },
  
  // Letter spacing
  letterSpacing: {
    tight: '-0.025em',
    normal: '0',
    wide: '0.025em',
    wider: '0.05em',
  },
} as const;

export const spacing = {
  // Base spacing unit: 8px
  xs: '4px',
  sm: '8px',
  md: '16px',
  lg: '24px',
  xl: '32px',
  '2xl': '40px',
  '3xl': '48px',
  '4xl': '64px',
} as const;

export const borderRadius = {
  sm: '6px',
  md: '10px',
  lg: '14px',
  xl: '20px',
  full: '9999px',
} as const;

export const shadows = {
  sm: '0 2px 4px rgba(14, 18, 32, 0.04)',
  md: '0 6px 18px rgba(14, 18, 32, 0.06)',
  lg: '0 12px 32px rgba(14, 18, 32, 0.08)',
  card: colors.shadow,
} as const;

export const breakpoints = {
  sm: '640px',
  md: '768px',
  lg: '1024px',
  xl: '1280px',
} as const;

export const zIndex = {
  base: 0,
  dropdown: 100,
  overlay: 200,
  modal: 300,
  tooltip: 400,
} as const;

export const animation = {
  duration: {
    fast: '120ms',
    normal: '200ms',
    slow: '300ms',
  },
  easing: {
    ease: 'cubic-bezier(0.4, 0.0, 0.2, 1)',
    easeIn: 'cubic-bezier(0.4, 0.0, 1, 1)',
    easeOut: 'cubic-bezier(0.0, 0.0, 0.2, 1)',
    easeInOut: 'cubic-bezier(0.4, 0.0, 0.6, 1)',
  },
} as const;

export const theme = {
  colors,
  typography,
  spacing,
  borderRadius,
  shadows,
  breakpoints,
  zIndex,
  animation,
} as const;

export type Theme = typeof theme;

// Dark mode colors (optional)
export const darkColors = {
  bg: '#0B1020',
  surface: '#0F1724',
  primary: '#60A5FA',
  accent: '#A78BFA',
  text: '#E6EEF6',
  muted: '#94A3B8',
  success: '#4ADE80',
  error: '#F87171',
  border: '#1E293B',
  overlay: 'rgba(230, 238, 246, 0.6)',
} as const;

export const darkTheme = {
  ...theme,
  colors: darkColors,
} as const;

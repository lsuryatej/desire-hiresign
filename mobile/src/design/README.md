# DesignHire Design System

Minimalist, low-strain UI system for the DesignHire marketplace.

## Philosophy

- **Calm & Professional**: Low visual strain, generous whitespace
- **Functional**: Fast, clear interactions without visual noise
- **Accessible**: WCAG AA compliance, reduced motion support
- **Consistent**: Systematic spacing, colors, typography

## Color Palette

### Light Mode (Default)
```typescript
Background:  #F6F7F9  // Very light gray for low strain
Surface:     #FFFFFF  // Cards and panels
Primary:     #3B82F6  // Muted blue - use sparingly
Accent:      #7C3AED  // Muted violet - tags, highlights
Text:        #0F172A  // Almost black
Muted:       #475569  // Secondary text
Success:     #16A34A
Error:       #DC2626
```

### Dark Mode (Optional)
```typescript
Background:  #0B1020
Surface:     #0F1724
Primary:     #60A5FA  // Lighter blue
Text:        #E6EEF6  // Light text
```

## Typography

- **Font**: Inter (fallback to system UI)
- **Scale**: 14 / 16 / 18 / 22 / 28px
- **Weights**: 400 (regular), 600 (semibold)
- **Line height**: 1.45 (body), 1.25 (headings)

## Spacing System

Base unit: **8px**

```
xs:  4px
sm:  8px
md:  16px
lg:  24px
xl:  32px
2xl: 40px
3xl: 48px
```

## Component Guidelines

### 1. Card (Swipe Feed)

**Layout**
- Surface: white, 14px radius
- Shadow: `0 6px 18px rgba(14, 18, 32, 0.06)`
- Padding: 16-20px

**Content Structure**
```
┌─────────────────────┐
│   Thumbnail (55%)   │
│                     │
├─────────────────────┤
│ Headline (semibold) │
│ Skills [chip] [chip]│
│ Bio (1 line)        │
│ Location • Available│
└─────────────────────┘
```

**Interactions**
- Swipe gestures with tilt (max 7deg rotation)
- Scale on drag: `transform: scale(0.95)`
- Pulse animation on like (160ms)
- Optional confetti micro-animation

### 2. Profile Gallery

- Masonry or horizontal carousel
- Lazy load with LQIP (Low Quality Image Placeholder)
- Hover/tap overlay: project title + fade
- Image aspect ratio: 4:3 or 16:9

### 3. Forms

**Fields**
- Floating labels
- Single column layout
- Inline validation (error text: `--error` color)
- Border: 1px solid `--border`
- Focus: 3-4px ring in `--accent`

**Submit Button**
- Background: `--primary`
- Padding: 12px 24px
- Min height: 48px (accessibility)

### 4. Chat Interface

**Messages**
- Left/right alignment
- Border radius: 14px for user, 14px for other
- Timestamp: small, muted color, positioned outside bubble
- Max width: 75% on mobile

**Quick Actions**
- Row of icon buttons below input
- Actions: attach portfolio, schedule interview
- Tappable: 48x48px min

### 5. Search & Filters

**Search Bar**
- Compact, full-width
- Icon on left, clear on right
- Border: 1px solid `--border`

**Filter Chips**
- Background: `--bg`
- Border: 1px solid `--border`
- Padding: 8px 16px
- Active: background `--primary`, text white

**Advanced Filters**
- Collapsible section
- Group related filters
- Apply button at bottom

### 6. Buttons

**Primary**
```tsx
backgroundColor: colors.primary
color: white
padding: '12px 24px'
borderRadius: borderRadius.md
fontWeight: typography.fontWeight.semibold
```

**Secondary**
```tsx
backgroundColor: 'transparent'
borderColor: colors.border
borderWidth: 1
color: colors.text
```

**Ghost**
```tsx
backgroundColor: 'transparent'
color: colors.primary
```

## Micro-interactions

### Timing
- **Fast**: 120ms (hover states)
- **Normal**: 200ms (transitions)
- **Slow**: 300ms (complex animations)

### Easing
```css
ease: cubic-bezier(0.4, 0.0, 0.2, 1)
easeIn: cubic-bezier(0.4, 0.0, 1, 1)
easeOut: cubic-bezier(0.0, 0.0, 0.2, 1)
```

### Optimistic UI
- Immediate visual feedback for swipes
- Toast/snackbar for async success/failure
- Loading: skeleton shapes (not spinners)

## Accessibility

### WCAG Compliance
- Text contrast: ≥ 4.5:1 (body), ≥ 3:1 (large headings)
- Tappable targets: min 48x48px
- Keyboard focus: visible outline (3-4px ring)
- Screen reader: proper ARIA labels

### Reduced Motion
```css
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

### Keyboard Navigation
- Tab order: logical flow
- Focus styles: always visible
- Escape: close modals
- Enter/Space: activate buttons

## Shadows

```typescript
sm:  '0 2px 4px rgba(14, 18, 32, 0.04)'  // Subtle elevation
md:  '0 6px 18px rgba(14, 18, 32, 0.06)' // Cards (default)
lg:  '0 12px 32px rgba(14, 18, 32, 0.08)' // Modals
```

## Dark Mode

When implementing dark mode:
1. Use `useColorScheme()` hook
2. Swap color tokens based on scheme
3. Reduce shadow intensity (or use glow-free borders)
4. Test contrast ratios in both modes

## Usage in Code

```tsx
import { theme } from '../design/theme';

const Card = styled.View`
  background-color: ${theme.colors.surface};
  padding: ${theme.spacing.md};
  border-radius: ${theme.borderRadius.lg};
  box-shadow: ${theme.shadows.card};
`;

const Heading = styled.Text`
  font-size: ${theme.typography.fontSize.xl};
  font-weight: ${theme.typography.fontWeight.semibold};
  color: ${theme.colors.text};
  line-height: ${theme.typography.lineHeight.tight};
`;
```

## Component Checklist

Before implementing any new component:

- [ ] Uses theme tokens (not hardcoded values)
- [ ] Follows spacing system (8px multiples)
- [ ] Includes hover/focus states
- [ ] Supports keyboard navigation
- [ ] Respects `prefers-reduced-motion`
- [ ] Has proper ARIA labels
- [ ] Tested in light & dark mode
- [ ] Contrast ratios meet WCAG AA
- [ ] Tappable areas ≥ 48x48px

## Examples

See implementation examples in:
- `components/Card.tsx` - Swipe card
- `components/Button.tsx` - Buttons
- `components/FormField.tsx` - Form inputs
- `screens/ChatScreen.tsx` - Chat interface

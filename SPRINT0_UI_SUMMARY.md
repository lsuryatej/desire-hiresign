# Sprint 0 - UI Design System Addition

## Overview

In addition to the core infrastructure and API setup, we've added a comprehensive design system for consistent, minimalistic UI across all platforms.

## Design Philosophy

**Minimalist, Low-Strain UI** - Clean, calm, and easy to use
- Calm & Professional: Low visual strain, generous whitespace
- Functional: Fast, clear interactions without visual noise
- Accessible: WCAG AA compliance, reduced motion support
- Consistent: Systematic spacing, colors, typography

## Color Palette

### Light Mode (Default)
```typescript
Background:  #F6F7F9  // Very light gray for low strain
Surface:     #FFFFFF  // Cards and panels
Primary:     #3B82F6  // Muted blue - use sparingly for CTAs
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

- **Font**: Inter (system fallback)
- **Scale**: 14 / 16 / 18 / 22 / 28px
- **Weights**: 400 (regular), 600 (semibold)
- **Line height**: 1.45 (body), 1.25 (headings)

## Spacing System

Base unit: **8px**
- xs: 4px
- sm: 8px
- md: 16px
- lg: 24px
- xl: 32px
- 2xl: 40px
- 3xl: 48px

## Key Components

### 1. Swipe Card (Tinder-style)
- 55% thumbnail + content below
- 14px radius, shadow `0 6px 18px rgba(14, 18, 32, 0.06)`
- Swipe with tilt animation (max 7deg)
- Pulse on like (160ms)

### 2. Forms
- Floating labels
- Inline validation
- 48px min tap targets
- Focus ring: 3-4px accent color

### 3. Chat Interface
- 14px radius bubbles
- Timestamp outside bubble
- Max 75% width
- Quick action row

### 4. Search & Filters
- Compact chips
- Collapsible advanced filters
- Persistent filter pills

## Files Created

### Design System
- `DESIGN_SYSTEM.md` - Main design system documentation
- `mobile/src/design/theme.ts` - Theme tokens for React Native
- `mobile/src/design/README.md` - Component guidelines for mobile

### Integration
- Updated `README.md` with design system reference
- Created component guidelines and checklist

## Implementation Strategy

### Sprint 0-2 (Current)
✅ Design system tokens established
✅ Documentation created
✅ Theme configuration for mobile

### Sprint 3+ (Future)
- Apply to all swipe card components
- Implement form components with design tokens
- Build chat interface with consistent styling
- Create admin panel with matching design

### Sprint 6+ (Optional)
- Dark mode implementation
- High contrast toggle
- Advanced accessibility features

## Micro-interactions

### Timing
- **Fast**: 120ms (hover states)
- **Normal**: 200ms (transitions)
- **Slow**: 300ms (complex animations)

### Easing
```css
ease: cubic-bezier(0.4, 0.0, 0.2, 1)
easeOut: cubic-bezier(0.0, 0.0, 0.2, 1)
```

### Optimistic UI
- Immediate visual feedback for swipes
- Toast/snackbar for async actions
- Loading: skeleton shapes (not spinners)

## Accessibility

✅ **WCAG AA Compliance**
- Text contrast: ≥ 4.5:1 (body), ≥ 3:1 (large headings)
- Tappable targets: min 48x48px
- Keyboard focus: visible outline (3-4px ring)
- Screen reader: proper ARIA labels

✅ **Reduced Motion Support**
```css
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

## Usage Example

```tsx
import { theme } from '../design/theme';

const Card = styled.View`
  background-color: ${theme.colors.surface};
  padding: ${theme.spacing.md};
  border-radius: ${theme.borderRadius.lg};
  box-shadow: ${theme.shadows.card};
`;
```

## Component Checklist

Every component must:
- [ ] Use theme tokens (no hardcoded values)
- [ ] Follow 8px spacing system
- [ ] Include focus/hover states
- [ ] Support keyboard navigation
- [ ] Respect reduced motion preference
- [ ] Meet WCAG contrast ratios
- [ ] Have proper ARIA labels
- [ ] Test in light & dark mode

## Next Steps

From Sprint 3 onward, all new UI components will:

1. Import design tokens from `theme.ts`
2. Follow component guidelines in `README.md`
3. Use spacing system (8px multiples only)
4. Include accessibility features
5. Support reduced motion
6. Be tested in both light/dark modes

## Documentation

- **Main**: `DESIGN_SYSTEM.md` - Quick reference
- **Mobile**: `mobile/src/design/README.md` - Component details
- **Integration**: Updated in main `README.md`

## Acceptance Criteria

✅ Theme tokens defined for colors, typography, spacing
✅ Component guidelines documented
✅ Accessibility requirements specified
✅ Dark mode colors defined
✅ Micro-interaction timing specified
✅ Integration into existing Sprint 0 structure

## Estimated Effort

| Task | Estimated | Actual |
|------|-----------|--------|
| Design system docs | 2h | ~2h |
| Theme tokens | 2h | ~2h |
| Component guidelines | 2h | ~2h |
| **Total** | **6h** | **~6h** |

Total Sprint 0 time: ~24h (18h original + 6h UI)

## Notes

- Design system is platform-agnostic (works for web and mobile)
- Dark mode is optional and will be implemented later
- All components will need to be updated to use design tokens
- Focus on accessibility from the start ensures better UX
- Consistent spacing and colors create a professional, calm experience

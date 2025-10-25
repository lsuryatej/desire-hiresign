# DesignHire Design System

Comprehensive design system for the DesignHire marketplace - applied across mobile app, admin panel, and all future UI work.

## Quick Reference

### Color Palette
- **Background**: `#F6F7F9` - Very light gray for low strain
- **Surface**: `#FFFFFF` - Cards and panels  
- **Primary**: `#3B82F6` - Muted blue (use sparingly for CTAs)
- **Accent**: `#7C3AED` - Muted violet (tags, highlights)
- **Text**: `#0F172A` - Almost black
- **Muted**: `#475569` - Secondary text
- **Success**: `#16A34A`
- **Error**: `#DC2626`

### Spacing
Base unit: **8px** → 4, 8, 16, 24, 32, 40, 48px

### Typography
- **Font**: Inter (system fallback)
- **Sizes**: 14, 16, 18, 22, 28px
- **Weights**: 400 (regular), 600 (semibold)

## Implementation Files

### Mobile (React Native)
📁 `mobile/src/design/`
- `theme.ts` - Color tokens, typography, spacing
- `README.md` - Component guidelines

### Web/Admin (React)
📁 `admin/src/design/` (to be created)
- `theme.ts` - Same tokens, React DOM specific
- `globals.css` - CSS variables

### API (FastAPI Docs)
Update API docs styling to match system colors

## Key Components

### 1. Swipe Card (Mobile)
- 55% thumbnail + content below
- 14px radius, subtle shadow
- Swipe with tilt animation (max 7deg)
- Pulse on like

### 2. Forms
- Floating labels
- Inline validation
- 48px min tap targets
- Focus ring: 3-4px `--accent`

### 3. Chat
- 14px radius bubbles
- Timestamp outside bubble
- Max 75% width
- Quick action row

### 4. Search & Filters
- Compact chips
- Collapsible advanced
- Persistent filter pills

## Accessibility

✅ WCAG AA compliance
- Text contrast ≥ 4.5:1
- Tappable ≥ 48x48px
- Focus: visible outline
- Screen reader: ARIA labels

✅ Reduced motion support
```css
@media (prefers-reduced-motion: reduce) {
  * { animation: none !important; }
}
```

## Dark Mode

Optional implementation with color swap:
- Background: `#0B1020`
- Surface: `#0F1724`
- Primary: `#60A5FA` (lighter)

## Development Workflow

1. **Import theme**: Use design tokens (never hardcode)
2. **Follow spacing**: 8px multiples only
3. **Check accessibility**: Run contrast checker
4. **Test interactions**: Hover, focus, keyboard nav
5. **Verify motion**: Test with reduced motion

## Component Checklist

Every component must:
- [ ] Use theme tokens
- [ ] Follow 8px spacing
- [ ] Include focus states
- [ ] Support keyboard nav
- [ ] Respect reduced motion
- [ ] Meet contrast ratios
- [ ] Have ARIA labels

## Sprint Implementation

**Sprint 0-2**: Theme system established  
**Sprint 3+**: Apply to all components  
**Sprint 6+**: Dark mode (optional)

For implementation details, see:
- Mobile: `mobile/src/design/README.md`
- Admin: `admin/src/design/README.md` (when created)

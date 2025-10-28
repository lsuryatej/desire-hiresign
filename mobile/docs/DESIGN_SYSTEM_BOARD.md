# Design System Board

## Overview
Visual system for DesignHire mobile app following Bumble/Hinge/Apple design principles.

---

## 🎨 Color Swatches

### Primary Palette (Light Mode)
```
Background:      #F6F7F9 (Very light gray)
Surface:         #FFFFFF (White)
Primary:          #3B82F6 (Soft blue)
Accent:           #7C3AED (Muted violet)
Text:             #0F172A (Almost-black)
Muted:            #475569 (Gray-blue)
Success:          #16A34A (Green)
Error:            #DC2626 (Red)
Border:           #E2E8F0 (Light gray)
```

### Dark Mode Palette
```
Background:      #0B1020 (Dark blue-black)
Surface:         #0F1724 (Slightly lighter)
Primary:          #60A5FA (Light blue)
Accent:           #A78BFA (Light violet)
Text:             #E6EEF6 (Almost-white)
Muted:            #94A3B8 (Light gray-blue)
```

---

## 📝 Typography Scale

### Font Family: Inter
```
XS:  12px - Captions, labels
SM:  14px - Body secondary
Base: 16px - Body primary
LG:  18px - Subheading
XL:  22px - Heading 3
2XL: 28px - Heading 2
3XL: 32px - Heading 1
```

### Weights
- Normal: 400 (body)
- Medium: 500 (emphasis)
- Semibold: 600 (headings)
- Bold: 700 (CTA buttons)

---

## 🔲 Component Examples

### Buttons

#### Primary Button
```
Background: #3B82F6
Text: #FFFFFF
Shape: Pill (full radius)
Padding: 12px 24px
```

#### Secondary Button
```
Background: #7C3AED
Text: #FFFFFF
Shape: Pill
```

#### Outline Button
```
Background: Transparent
Border: 2px solid #3B82F6
Text: #3B82F6
```

#### Ghost Button
```
Background: Transparent
Text: #3B82F6
```

### Tags

#### Skill Tag
```
Background: #7C3AED15 (15% opacity)
Text: #7C3AED
Shape: Pill
Padding: 6px 16px
```

#### Filter Tag
```
Active: #3B82F615 + #3B82F6 text
Inactive: Transparent + border
Shape: Pill
```

### Cards

#### Default Card
```
Background: #FFFFFF
Border Radius: 14px
Shadow: 0 6px 18px rgba(14, 18, 32, 0.06)
Padding: 16px
```

#### Elevated Card
```
Background: #FFFFFF
Border Radius: 14px
Shadow: Enhanced (0 12px 32px)
Elevation: 4
```

---

## 📐 Spacing System

Based on 8px unit:
```
XS:  4px
SM:  8px
MD:  16px
LG:  24px
XL:  32px
2XL: 40px
3XL: 48px
4XL: 64px
```

---

## 🎯 Sample Screens

### Onboarding Screen 1 - Value Proposition
```
┌─────────────────────┐
│    [Illustration]   │
│                     │
│   Connect with      │
│   Top Companies     │
│                     │
│   Swipe through     │
│   opportunities     │
│                     │
│  [Secondary CTA]    │
│                     │
│  ● ○ ○ ○ ○         │ (Progress dots)
└─────────────────────┘
```

### Profile Card (Swipe Feed)
```
┌─────────────────────┐
│  [Profile Image]    │
│     Top 55%         │
├─────────────────────┤
│  John Doe           │ ← 22px, semibold
│  UI/UX Designer     │ ← 18px, medium
│                     │
│  🏷️ Figma           │ Tags
│  🏷️ React           │
│  🏷️ Design System   │
│                     │
│  San Francisco, CA  │ ← 14px, muted
│                     │
│  [💬 View Profile] │ Secondary button
│  [💖 Interested]   │ Primary button
└─────────────────────┘
```

### Job Card
```
┌─────────────────────┐
│  [Company Logo]     │
│     Top 55%         │
├─────────────────────┤
│  Senior Designer    │ ← Title (22px)
│  at Tech Corp       │ ← Company (18px)
│                     │
│  🏷️ Remote          │ Tags
│  🏷️ Full-time       │
│  🏷️ Figma, Sketch   │
│                     │
│  💰 $80k-$120k      │ Salary
│  📍 San Francisco   │ Location
│                     │
│  [❌ Skip] [💖 Like]│ Swipe actions
└─────────────────────┘
```

### Chat Preview
```
┌─────────────────────┐
│  [Avatar]           │
│                     │
│  Hey! Interested    │ ← Message bubble
│  in discussing the  │   (background: #3B82F610)
│  role?              │
│                     │
│  Thanks for the     │ ← Your message
│  message. Yes!      │   (background: #3B82F6)
│                     │
│  [Type message...] │ ← Composer (pill)
└─────────────────────┘
```

### Match Celebration
```
┌─────────────────────┐
│                     │
│    🎉 You Matched!  │ ← Confetti animation
│                     │
│   with John Doe     │
│                     │
│   [Start Chat]      │ ← Primary button
│   [Keep Swiping]    │ ← Secondary button
│                     │
└─────────────────────┘
```

---

## 🎭 Motion & Animation

### Transitions
- **Duration**: 120-200ms
- **Easing**: Cubic-bezier(0.4, 0.0, 0.2, 1)
- **Feeling**: Smooth, liquid

### Interactions
- **Button Press**: 0.7 opacity
- **Card Swipe**: ±7° rotation, ≤25px offset
- **Match**: Confetti burst (Lottie)
- **Loading**: Subtle spinner

---

## 📱 Accessibility

### Contrast Ratios
- Body text: 4.5:1 ✅
- Large text: 3:1 ✅
- Interactive elements: 3:1 ✅

### Touch Targets
- Minimum: 44x44px
- Recommended: 48x48px
- Padding: 8-16px

### Text Scaling
- Support dynamic type
- Line height: 1.45-1.75
- Readable on small screens

---

## 🎨 Visual Style Notes

### Inspired By
- **Hinge**: Minimalist layouts, 90% grayscale
- **Bumble**: Warm tone, yellow accents (we use blue)
- **Apple**: Liquid Glass effects, translucency

### Design Principles
- Calm & Low-Strain
- Professional but Friendly
- Authentic & Trustworthy
- Clean & Cohesive

---

This board serves as the visual reference for all UI components and screens.


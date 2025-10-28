# Frontend Development Sprints - Detailed Plan

## 🎯 Overview

Building a complete, polished mobile app and web UI for DesignHire following the provided UX/UI guidelines.

## Sprint Breakdown

### 💜 Sprint 1 — Design System Implementation

**Goal**: Establish the visual foundation across mobile and web.

**Deliverables**:
1. Global Theme Tokens
   - Color palette variables (--bg, --surface, --primary, etc.)
   - Light mode (default) and dark mode placeholder
2. Typography Scale & Components
   - Apply Inter font family
   - Define text sizes, weights, and styles
   - Implement reusable <Text> and <Heading> components in RN
3. Spacing & Grid System
   - Global spacing units (8px scale)
   - Container widths and card paddings
4. Shape & Elevation
   - Uniform border radii (8–14px)
   - Soft shadows
   - Translucent glass backgrounds
5. Button + Tag Components
   - Primary (filled) and secondary (outline) buttons
   - Pill tags for skills/filters

**Design Focus**: Minimalist + calm. 60–30–10 color balance; contrast ratio ≥ 4.5:1.

**Acceptance Criteria**:
- Theme tokens loaded globally in RN theme context
- Light theme visually matches spec
- Dark mode toggles successfully
- Buttons, tags, and typography render correctly on all screens

**Estimate**: 16–20 hours

---

### 🎨 Sprint 2 — Figma Mockups & Style Guide Validation

**Goal**: Create and validate visual mockups to lock design direction.

**Deliverables**:
1. Figma/Design System Board
   - All tokens, color swatches, components
   - UI examples (buttons, tags, modals)
2. Sample Screens:
   - Onboarding
   - Profile card
   - Job card
   - Chat preview
3. UI Review + Feedback Loop
   - Export image assets
   - Motion examples
   - Confirm with real devices

**Design Focus**: Ensure calm and low-strain interface — neutral tones, gentle gradients, rounded buttons.

**Acceptance Criteria**:
- Stakeholder review → visual approval
- Components imported into RN storybook for parity check

**Estimate**: 20 hours

---

### 🪄 Sprint 3 — Onboarding & Auth Flow (Guided UX)

**Goal**: Design and implement high-quality onboarding experience + authentication.

**Deliverables**:
1. Onboarding Carousel: 3–5 slides
   - Value prop
   - How it works
   - Signup CTA
2. Auth Screens
   - Signup/Login (email)
   - Google OAuth (if configured)
   - Password reset
3. Profile Setup Wizard: Guided step-by-step form
   - Personal info
   - Skills
   - Upload portfolio
4. Progress Bar Component

**Design Focus**: Smooth transitions, slight motion (120–200 ms fade/slide). Guided, friendly copy tone.

**Acceptance Criteria**:
- Onboarding sequence runs seamlessly with progress indicators
- Authentication integrated with backend
- Tokens stored securely
- UX validated on both iOS/Android simulators

**Estimate**: 22–26 hours

---

### 🧭 Sprint 4 — Swipe Feed UI + Interaction Engine

**Goal**: Build the "Bumble-like" card feed for designers and job postings.

**Deliverables**:
1. CardStack Component
   - 3-card preload
   - Swipe left/right/up actions (Reanimated + GestureHandler)
   - Customizable card types: DesignerCard, JobCard
2. Card States: idle, dragging, liked, skipped
3. Interaction API Integration: POST /interactions, fetch new cards
4. Empty & Loading States

**Design Focus**: Cards styled like Hinge: subtle gradients, drop shadow, profile photo or logo top half. Rounded corners (radius = 14px), soft entry/exit transitions, minimal jitter.

**Acceptance Criteria**:
- Smooth < 60 fps swipe on test devices
- "Like" and "Skip" events recorded via API
- Card rotation ± 7°, offset ≤ 25 px
- Velocity threshold tuned to feel natural

**Estimate**: 28–34 hours

---

### 💬 Sprint 5 — Match Celebration & Messaging UX

**Goal**: Complete user-to-user connection flow.

**Deliverables**:
1. Match Modal + Confetti Animation
   - Triggered on mutual interest
   - Includes CTA ("Start Chat")
2. Matches List Screen
   - Thumbnail, last message preview, unread count
3. Chat Screen
   - Bubble layout
   - Timestamps
   - Scroll persistence
   - Composer bar
4. Typing Indicator + Read Receipts (polling initially)

**Design Focus**: Very slight, high-quality animation; celebratory yet elegant. Chat layout airy and low strain.

**Acceptance Criteria**:
- Confetti triggers correctly (Lottie or RN animation)
- Chat stable across refreshes
- Messages load within < 200 ms latency
- Message composer accessible (keyboard overlay properly handled)

**Estimate**: 24–28 hours

---

### 🧑‍💻 Sprint 6 — Job Posting & Profile Detail Views

**Goal**: Build detailed views for job postings and designer portfolios.

**Deliverables**:
1. Job Detail Screen
   - Job description
   - Tags
   - Apply button
2. Designer Profile Screen
   - Photo/banner
   - Skills grid
   - About text
   - Behance integration (display first project via API)
3. Resume/Portfolio Link Openers
4. Share/Save Actions

**Design Focus**: "Glass-effect" modals for expanded views; polished transitions between cards and detail screens.

**Acceptance Criteria**:
- Behance preview card loads live data via Behance API
- Detail view scroll smoothness verified
- Links open in in-app browser or modal

**Estimate**: 20–24 hours

---

### 🧱 Sprint 7 — Search, Filters & Tag System

**Goal**: Enable discovery and control.

**Deliverables**:
1. Filter Modal: role, skills, location, availability
2. Tag Chips Component: reusable for filters and skills
3. Search Bar + Suggestion List
4. Save Search Preferences

**Design Focus**: Simple, collapsible filters (inspired by Apple Music filter modals). Light animation on open/close; persistent preferences.

**Acceptance Criteria**:
- Filters update feed dynamically
- Preferences persist locally
- Chips visually consistent with design system

**Estimate**: 16–20 hours

---

### ⚙️ Sprint 8 — Admin Web UI (Moderation & Analytics)

**Goal**: Create a simple browser interface for internal management.

**Deliverables**:
1. Web Dashboard: user list, job list, reports
2. Toggle Actions: ban/unpublish buttons
3. Metrics Section: matches/day, active users, reported content

**Design Focus**: Flat, professional web look with your color system; responsive layout.

**Acceptance Criteria**:
- Admin CRUD operations hit existing API
- Dashboard loads under 2 s
- Responsive ≥ 1024 px width

**Estimate**: 20 hours

---

### 🧩 Sprint 9 — Polish, Accessibility & QA

**Goal**: Ensure performance, accessibility, and final visual consistency.

**Deliverables**:
1. Accessibility Pass: color contrast, font scaling, focus outlines
2. Performance Optimization: image lazy-loading, reduced motion toggle
3. Handoff Docs: updated Figma + dev documentation (UI_GUIDE.md)
4. Beta QA & Bug Bash

**Design Focus**: User comfort: ensure visual calmness, remove flicker/jank, refine transitions.

**Acceptance Criteria**:
- All text passes contrast checks
- FPS stable > 55 on low-end device
- All screens accessible with VoiceOver/TalkBack

**Estimate**: 18–22 hours

---

### 🧠 Sprint 10 — Delight & Expansion

**Goal**: Add finishing touches that create emotional connection.

**Deliverables**:
1. Streak & Rewards Micro-Feature: daily login streak, gentle Duolingo-style icon
2. Push Notifications (new match, new job)
3. Dark Mode Theme
4. Launch Screen + Tagline Animation

**Design Focus**: Subtle gamification and emotional design. Maintain professionalism—no heavy gamified clutter.

**Acceptance Criteria**:
- Streak logic updates daily; animation smooth
- Push notifications delivered (tested on iOS/Android)
- Dark mode parity verified

**Estimate**: 20–26 hours

---

## 📊 Total Estimated Effort

**Sprint 1**: 16–20 hours  
**Sprint 2**: 20 hours  
**Sprint 3**: 22–26 hours  
**Sprint 4**: 28–34 hours  
**Sprint 5**: 24–28 hours  
**Sprint 6**: 20–24 hours  
**Sprint 7**: 16–20 hours  
**Sprint 8**: 20 hours  
**Sprint 9**: 18–22 hours  
**Sprint 10**: 20–26 hours  

**Total**: 204–250 hours (~5–6 weeks full-time)

---

## 🎨 Key Design Principles

### Visual Identity
- **Calm & Clean**: Neutral base with gentle accents
- **Grayscale First**: ~90% neutral, ≤10% accent
- **60-30-10 Rule**: 60% primary neutral, 30% secondary, 10% accent
- **Accessibility**: WCAG 4.5:1 contrast ratio minimum

### Typography
- **Font**: Inter (designed for screens)
- **Weights**: Bold/medium for headings, regular for body
- **Sizing**: Consistent hierarchy

### UI Shapes
- **Rounded Corners**: All cards, buttons, containers
- **Pill Buttons**: Nearly spherical
- **Soft Edges**: Friendly, approachable

### Color & Branding
- **Inspired By**: Bumble (warm tone), Hinge (minimalist), Apple (Liquid Glass effects)
- **Accents**: Soft blue or green (calming, trustworthy)
- **Effects**: Subtle translucency/blur for depth

### Animations
- **Speed**: 120–200ms transitions
- **Feeling**: Smooth, liquid, responsive
- **Quality**: High-quality, not gimmicky
- **Confetti**: Tasteful celebration on match

---

## ❓ Questions for You

Before I start, please clarify:

1. **Design Assets**: Do you have Figma files, mockups, or reference images? (Sprint 2 assumes creating mockups from scratch)

2. **Behance Integration**: Do you have Behance API credentials for portfolio integration? (Sprint 6)

3. **OAuth**: Which OAuth providers should I implement? Google, Apple, LinkedIn? (Sprint 3)

4. **Platform Priority**: iOS and Android, or focus on one first?

5. **Testing**: Simulator/emulator testing sufficient, or need physical devices?

6. **Admin UI Stack**: React? Next.js? Plain HTML/CSS/JS?

**Or should I proceed with Sprint 1 now and handle these decisions as they come?**


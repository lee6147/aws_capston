# StudyBot v3 — Plan Document

## Executive Summary

| Perspective | Description |
|-------------|-------------|
| **Problem** | v2 had 50 features but looked cheap — design was an afterthought, features added without visual cohesion |
| **Solution** | Design-first rebuild: premium design system → core architecture → features layered on top |
| **Function UX Effect** | Users feel they're using a polished, professional study app comparable to ChatGPT/Claude |
| **Core Value** | Document-grounded AI tutor that students trust, enjoy using, and come back to daily |

---

## 1. Project Overview

- **Feature**: StudyBot v3 — Complete rebuild of document-grounded AI chatbot
- **Type**: Single HTML file, zero dependencies, works offline
- **Target**: AWS capstone project evaluation
- **Constraint**: One file, no CDN, no npm, file:// protocol compatible

## 2. Design-First Philosophy (v2 Lesson)

> v2 failed because features came before design. v3 inverts this:
> **Design System → Architecture → Features**

### Phase 1: Premium Design System (CSS)
- Modern dark theme with glassmorphism as default
- Design tokens: spacing scale (4/8/12/16/24px), type scale, color palette
- Component library: buttons, cards, badges, inputs, overlays
- Animations: cubic-bezier springs, staggered reveals, micro-interactions
- Mobile-first responsive breakpoints

### Phase 2: Core Architecture (JS)
- Clean IIFE with module pattern
- State management: conversations, settings, achievements
- Event system: delegation over per-element listeners
- Render pipeline: data → template → DOM

### Phase 3: Features (built on Phase 1+2)
All 50 features from v2, but designed cohesively from day one.

## 3. Feature Spec (Carried from v2)

### Tier 1: Core Chat (must have)
1. Message streaming with typing indicator
2. 6 domains (bio, cook, sport, music, biz, travel) with RAG simulation
3. Conversation management (create, switch, delete, pin, time grouping)
4. Confidence indicator + hallucination guard
5. Source citations (collapsible)
6. Follow-up chips + cross-domain suggestions

### Tier 2: Study Tools (differentiators)
7. Interactive SVG mind map with text analysis
8. Mind map zoom/pan/drag + PNG export
9. Voice input (STT) + Read aloud (TTS)
10. Comprehension quiz on bot messages
11. Smart summary (/summary-chat)
12. Quick notes pad (auto-save)
13. Keyboard shortcuts (Ctrl+K, Ctrl+/, Alt+1-6, Alt+Z)
14. YouTube/book recommendations per domain

### Tier 3: Gamification
15. Achievement badges (6) with confetti
16. Study streak counter
17. Activity heatmap
18. Daily study tips
19. Time-based personalized greeting

### Tier 4: Export & Share
20. Ctrl+K conversation search
21. /export-md (Markdown + file download)
22. /share (standalone HTML export)
23. /stats (domain statistics)
24. /heatmap (35-day activity grid)
25. Clickable bookmarks with jump navigation
26. Print-friendly CSS

### Tier 5: Visual Polish
27. 3 themes (dark/light/high contrast)
28. Ambient background gradient
29. Message slide-in animations
30. Skeleton shimmer loading
31. Toast notification system
32. Glassmorphism on hover
33. Gradient text on headers
34. Focus mode (Alt+Z)
35. Page load animation + favicon
36. Resizable sidebar with drag handle
37. Mobile responsive with toggle panels

## 4. Design Tokens

```css
/* Spacing */
--space-1: 4px;  --space-2: 8px;  --space-3: 12px;
--space-4: 16px; --space-5: 24px; --space-6: 32px;

/* Typography */
--font-xs: .65rem; --font-sm: .78rem; --font-base: .88rem;
--font-lg: 1rem;   --font-xl: 1.2rem; --font-2xl: 1.5rem;

/* Radius */
--radius-sm: 6px; --radius-md: 12px; --radius-lg: 16px; --radius-full: 9999px;

/* Shadows */
--shadow-sm: 0 1px 2px rgba(0,0,0,.2);
--shadow-md: 0 4px 12px rgba(0,0,0,.25);
--shadow-lg: 0 8px 32px rgba(0,0,0,.3);
--shadow-glow: 0 0 16px rgba(59,130,246,.3);
```

## 5. Architecture

```
studybot-v3.html
├── <head> — meta, CSP, favicon, <style>
│   └── CSS: design tokens → layout → components → themes → animations → print
├── <body>
│   ├── HTML: search overlay, toast container
│   ├── .app (3-panel flex)
│   │   ├── aside.panel-left (domains, convos, streak)
│   │   ├── main.panel-center (topbar, messages, input)
│   │   └── aside.panel-right (mind map, notes, bookmarks)
│   └── <script> IIFE
│       ├── Utils (DOM, escape, sanitize, toast, copy)
│       ├── State (store, conversations, settings)
│       ├── Render (convos, domains, messages, mind map)
│       ├── Features (TTS, STT, search, achievements, etc.)
│       └── Init (load, bind events, greet)
```

## 6. Quality Gates

- [ ] Design review: does it look premium? (before adding features)
- [ ] All HTML IDs verified before JS references
- [ ] Mobile responsive at 768px and 1024px breakpoints
- [ ] All 3 themes tested
- [ ] Print layout verified
- [ ] Keyboard navigation complete
- [ ] No console errors on load

## 7. Timeline

| Phase | What | Priority |
|-------|------|----------|
| Design | CSS design system + layout + components | First |
| Plan | This document | Done |
| Do-1 | Core architecture + design system + layout | High |
| Do-2 | Chat engine + 6 domains + streaming | High |
| Do-3 | Study tools (mind map, voice, quiz) | Medium |
| Do-4 | Gamification + export + polish | Medium |
| Check | Gap analysis + stability audit | Required |
| Report | Completion report | Final |

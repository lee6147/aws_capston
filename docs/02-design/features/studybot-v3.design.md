# StudyBot v3 — Design Document

> Reference: [Plan Document](../../01-plan/features/studybot-v3.plan.md)

---

## 1. Design Philosophy

**Inspiration**: Linear.app + Claude.ai + Vercel Dashboard

> "Premium means restraint. Less decoration, more precision.
> Every pixel earns its place. Motion has purpose. Color has meaning."

### Principles
1. **Depth through subtlety** — glassmorphism, not gradients everywhere
2. **Typography hierarchy** — font weight + size + opacity, not color
3. **Purposeful motion** — animations guide attention, never distract
4. **Spatial rhythm** — consistent 4px baseline grid
5. **Dark-first** — designed for dark theme, adapted for light

---

## 2. Color System

### Dark Theme (Default)
```css
:root {
  /* Backgrounds — layered depth */
  --bg-0: #09090b;        /* deepest — page background */
  --bg-1: #0f0f12;        /* surface — panels */
  --bg-2: #18181b;        /* elevated — cards, inputs */
  --bg-3: #27272a;        /* hover states */

  /* Text — 4-level hierarchy */
  --text-1: #fafafa;      /* primary — headings */
  --text-2: #a1a1aa;      /* secondary — body */
  --text-3: #71717a;      /* tertiary — hints, timestamps */
  --text-4: #52525b;      /* quaternary — disabled */

  /* Borders */
  --border: #27272a;      /* default */
  --border-hover: #3f3f46; /* interactive */

  /* Accents — semantic */
  --accent: #3b82f6;      /* primary action — blue */
  --accent-hover: #2563eb;
  --accent-soft: rgba(59,130,246,.12);
  --purple: #8b5cf6;      /* secondary — purple */
  --green: #22c55e;       /* success */
  --orange: #f59e0b;      /* warning */
  --red: #ef4444;         /* error/danger */
  --cyan: #06b6d4;        /* info/citations */
}
```

### Light Theme
```css
[data-theme="light"] {
  --bg-0: #ffffff;
  --bg-1: #f4f4f5;
  --bg-2: #e4e4e7;
  --bg-3: #d4d4d8;
  --text-1: #09090b;
  --text-2: #52525b;
  --text-3: #a1a1aa;
  --border: #e4e4e7;
  --border-hover: #d4d4d8;
}
```

### High Contrast
```css
[data-theme="highcontrast"] {
  --bg-0: #000000;
  --bg-1: #0a0a0a;
  --bg-2: #171717;
  --text-1: #ffffff;
  --text-2: #e5e5e5;
  --border: #ffffff;
  --accent: #60a5fa;
}
```

---

## 3. Typography

```css
/* Font Stack — optimized for Korean + English */
--font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI',
  'Apple SD Gothic Neo', 'Noto Sans KR', 'Malgun Gothic', sans-serif;

/* Type Scale (1.2 ratio) */
--text-xs: 0.694rem;    /* 11.1px — badges, hints */
--text-sm: 0.833rem;    /* 13.3px — captions, timestamps */
--text-base: 1rem;      /* 16px — body text */
--text-lg: 1.2rem;      /* 19.2px — subheadings */
--text-xl: 1.44rem;     /* 23px — section titles */
--text-2xl: 1.728rem;   /* 27.6px — page titles */

/* Line Heights */
--leading-tight: 1.25;
--leading-normal: 1.5;
--leading-relaxed: 1.75;  /* for message body — Korean readability */

/* Font Weights */
--weight-normal: 400;
--weight-medium: 500;
--weight-semibold: 600;
--weight-bold: 700;
```

---

## 4. Spacing System (4px Grid)

```css
--space-0: 0;
--space-1: 4px;    /* micro — icon gaps */
--space-2: 8px;    /* tight — inline elements */
--space-3: 12px;   /* default — component padding */
--space-4: 16px;   /* comfortable — section gaps */
--space-5: 20px;   /* relaxed — card padding */
--space-6: 24px;   /* spacious — section margins */
--space-8: 32px;   /* large — panel padding */
--space-10: 40px;  /* extra — page margins */
```

---

## 5. Component Library

### 5.1 Buttons
```
Primary:  bg=accent, text=white, radius=8px, h=36px, px=16px
          hover: bg=accent-hover, shadow=glow
Secondary: bg=transparent, border=border, text=text-2
          hover: bg=bg-3, border=border-hover
Ghost:    bg=transparent, text=text-3
          hover: bg=bg-3, text=text-1
Icon:     w=32px, h=32px, radius=8px, same as ghost
Chip:     h=28px, px=12px, radius=full, border=border, text-sm
```

### 5.2 Input Fields
```
bg=bg-2, border=border, radius=8px, h=40px, px=12px
placeholder=text-4
focus: border=accent, ring=accent-soft (0 0 0 3px)
```

### 5.3 Cards (Messages)
```
Flat design (NO bubbles — modern chatbots use flat)
border-bottom=border (1px)
padding=16px 0
hover: bg=bg-2 (very subtle)
```

### 5.4 Overlays
```
Backdrop: bg=black/50%, backdrop-filter=blur(8px)
Card: bg=bg-1, border=border, radius=16px, shadow=lg
      max-width=480px, animation=slideUp 0.2s
```

### 5.5 Toast Notifications
```
Fixed bottom-right, bg=bg-1, border-left=3px solid accent
backdrop-filter=blur(12px)
slide-in from right, auto-dismiss 3s
```

---

## 6. Layout Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    .app (flex row)                       │
├──────────┬──────────────────────────┬───────────────────┤
│          │       .panel-center      │                   │
│ .panel-  │  ┌──────────────────┐   │  .panel-right     │
│  left    │  │  .topbar         │   │                   │
│ (260px)  │  ├──────────────────┤   │  (320px)          │
│          │  │                  │   │  ┌─────────────┐  │
│ ┌──────┐ │  │  .messages       │   │  │ Mind Map    │  │
│ │domain│ │  │  (scrollable)    │   │  │ (SVG)       │  │
│ │chips │ │  │                  │   │  ├─────────────┤  │
│ ├──────┤ │  │  msg ────────    │   │  │ Text Input  │  │
│ │convo │ │  │  msg ────────    │   │  ├─────────────┤  │
│ │list  │ │  │  msg ────────    │   │  │ Bookmarks   │  │
│ │(time │ │  │                  │   │  ├─────────────┤  │
│ │group)│ │  ├──────────────────┤   │  │ Quick Notes │  │
│ ├──────┤ │  │ .suggest-bar     │   │  └─────────────┘  │
│ │streak│ │  │ .input-area      │   │                   │
│ └──────┘ │  └──────────────────┘   │                   │
├──────────┴──────────────────────────┴───────────────────┤
│ Responsive: <1024px hide right, <768px overlay left     │
└─────────────────────────────────────────────────────────┘
```

---

## 7. Animation System

### Keyframes
```css
/* Entry — elements appearing */
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(8px); }
  to { opacity: 1; transform: translateY(0); }
}

/* Message — bot messages slide up with spring */
@keyframes msgIn {
  from { opacity: 0; transform: translateY(16px) scale(0.98); }
  to { opacity: 1; transform: translateY(0) scale(1); }
}

/* User message — slide from right */
@keyframes msgUser {
  from { opacity: 0; transform: translateX(8px); }
  to { opacity: 1; transform: translateX(0); }
}

/* Pop — achievements, badges */
@keyframes pop {
  from { opacity: 0; transform: scale(0.5); }
  to { opacity: 1; transform: scale(1); }
}

/* Shimmer — skeleton loading */
@keyframes shimmer {
  0% { background-position: -600px 0; }
  100% { background-position: 600px 0; }
}

/* Ambient — background gradient shift */
@keyframes ambient {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

/* Draw — SVG line animation */
@keyframes draw {
  to { stroke-dashoffset: 0; }
}
```

### Timing
```css
--ease-out: cubic-bezier(0.16, 1, 0.3, 1);     /* smooth deceleration */
--ease-spring: cubic-bezier(0.34, 1.56, 0.64, 1); /* playful overshoot */
--duration-fast: 150ms;   /* hover, toggle */
--duration-normal: 250ms; /* transitions */
--duration-slow: 400ms;   /* entry animations */
```

---

## 8. JS Architecture

```javascript
(function() {
  'use strict';

  // ═══ UTILS ═══
  // $(id), escHtml(s), sanitizeHtml(h), showToast(msg,type)
  // copyText(t), scrollToBottom()

  // ═══ STATE ═══
  // var STORE, convos, activeId, curDomain, theme, busy
  // loadStore(), saveStore(), getActive()

  // ═══ DOMAIN DATA ═══
  // var domains = { bio, cook, sport, music, biz, travel }
  // var recs = { ... } (YouTube recommendations)
  // var mmData = { ... } (mind map trees)

  // ═══ RENDER ═══
  // renderConvos(), renderDomainBar(), renderDocs()
  // renderWelcome(), renderMindmap(), renderSuggestions()
  // renderBookmarks(), updateSummaryBtn()

  // ═══ MESSAGES ═══
  // addUser(t), addBot(t,s,c,doStream,conf)
  // stream(el,html,done), showTyp(), hideTyp()

  // ═══ INPUT ═══
  // resolve(t), handle(t), doSlash(t), send()

  // ═══ FEATURES ═══
  // generateSummary(), analyzeText(), showConfetti()
  // checkAchievements(), unlockAchievement(id)

  // ═══ INIT ═══
  // Event delegation on containers (not per-element)
  // Load state, render, bind shortcuts
})();
```

### Key Architecture Decisions (v2 Lessons)

1. **Event delegation** — `convoList.addEventListener('click', handler)` once, not per-item
2. **HTML before `<script>`** — all overlay/toast containers in DOM before JS runs
3. **Null guards everywhere** — `var el=$('id'); if(!el) return;`
4. **No `done()` in stream cancel** — prevents data corruption on convo switch
5. **Single `pushMsg` call site** — centralized word count, summary button, save

---

## 9. Implementation Order

| Step | What | Dependencies |
|------|------|-------------|
| 1 | `<head>` + CSS design system (tokens, reset, layout) | None |
| 2 | HTML structure (3-panel layout, all containers) | Step 1 |
| 3 | CSS components (buttons, inputs, cards, badges) | Step 1 |
| 4 | JS core (state, utils, IIFE skeleton) | Step 2 |
| 5 | Domain data (6 domains, recs, mind map data) | Step 4 |
| 6 | Chat engine (addUser, addBot, stream, resolve) | Step 4,5 |
| 7 | Slash commands (15 commands) | Step 6 |
| 8 | Mind map (SVG render, zoom, pan, export) | Step 4 |
| 9 | Voice (STT+TTS), search (Ctrl+K) | Step 6 |
| 10 | Gamification (achievements, streak, heatmap) | Step 6 |
| 11 | Polish (animations, themes, print, mobile) | All |
| 12 | Stability audit (ID verification, null checks) | All |

---

## 10. File Size Budget

| Section | Target Lines |
|---------|-------------|
| CSS (design system + components + themes + animations) | ~250 |
| HTML (structure + overlays) | ~120 |
| JS (domain data — 6 domains + recs + mind map) | ~200 |
| JS (core engine — state, render, chat, slash) | ~250 |
| JS (features — mind map, voice, search, achievements) | ~250 |
| JS (init + event binding) | ~80 |
| **Total target** | **~1150 lines** |

---

## 11. Quality Checklist

- [ ] Design system looks premium before any features
- [ ] Color contrast meets WCAG AA (4.5:1 minimum)
- [ ] All 3 themes verified (dark, light, high contrast)
- [ ] Mobile responsive at 768px and 1024px
- [ ] All HTML IDs exist before JS references them
- [ ] No `addEventListener` on null elements
- [ ] Print CSS hides UI, shows only messages
- [ ] Keyboard: Ctrl+K, Ctrl+/, Alt+1-6, Alt+Z, Enter, Shift+Enter, Esc
- [ ] No console errors on fresh load
- [ ] localStorage save/load cycle verified

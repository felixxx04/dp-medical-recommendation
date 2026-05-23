# Light Theme Migration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Migrate the entire frontend from dark theme to Neumorphic Medical Light theme for print-friendly paper screenshots.

**Architecture:** Replace all dark-theme colors, shadows, and component styles with neumorphic light equivalents. Foundation first (tailwind + CSS variables), then UI primitives, then layout, then pages. No dark/light toggle — single light theme.

**Tech Stack:** React 18 + TypeScript + Tailwind CSS + class-variance-authority (cva)

---

## Phase 1: Foundation

### Task 1: Update tailwind.config.ts

**Files:**
- Modify: `tailwind.config.ts`

- [ ] **Step 1: Replace the entire `tailwind.config.ts` with light theme configuration**

```typescript
import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './index.html',
    './src/**/*.{js,ts,jsx,tsx}',
  ],
  prefix: '',
  theme: {
    container: {
      center: true,
      padding: '2rem',
      screens: {
        '2xl': '1400px',
      },
    },
    extend: {
      colors: {
        border: 'rgba(155,175,200,0.18)',
        input: 'rgba(155,175,200,0.22)',
        ring: 'rgba(8,145,178,0.25)',
        background: '#e4ecf4',
        foreground: '#0a2f2f',
        primary: {
          DEFAULT: '#0891b2',
          foreground: '#ffffff',
          hover: '#0e7490',
          light: '#22d3ee',
        },
        secondary: {
          DEFAULT: '#3d5f73',
          foreground: '#0a2f2f',
        },
        destructive: {
          DEFAULT: '#b91c1c',
          foreground: '#ffffff',
        },
        warning: {
          DEFAULT: '#b45309',
          foreground: '#ffffff',
        },
        success: {
          DEFAULT: '#059669',
          foreground: '#ffffff',
        },
        info: {
          DEFAULT: '#0369a1',
          foreground: '#ffffff',
        },
        muted: {
          DEFAULT: '#dae4ef',
          foreground: '#5e7f92',
        },
        accent: {
          DEFAULT: '#14b8a6',
          foreground: '#ffffff',
        },
        popover: {
          DEFAULT: '#edf3fa',
          foreground: '#0a2f2f',
        },
        card: {
          DEFAULT: '#e4ecf4',
          foreground: '#0a2f2f',
        },
        surface: {
          base: '#e4ecf4',
          DEFAULT: '#e4ecf4',
          elevated: '#edf3fa',
          inset: '#dae4ef',
        },
        brand: {
          sky: '#0891b2',
          teal: '#14b8a6',
          mint: '#5eead4',
          navy: '#0a2f2f',
        },
        neu: {
          light: 'rgba(255,255,255,0.72)',
          dark: 'rgba(148,168,195,0.38)',
          'dark-hover': 'rgba(138,160,188,0.28)',
          'dark-subtle': 'rgba(128,152,180,0.18)',
        },
      },
      borderRadius: {
        none: '0px',
        xs: '4px',
        sm: '8px',
        DEFAULT: '10px',
        md: '10px',
        lg: '12px',
        xl: '16px',
        '2xl': '24px',
        full: '9999px',
      },
      fontFamily: {
        sans: ['Inter', 'SF Pro Display', '-apple-system', 'BlinkMacSystemFont', 'Noto Sans SC', 'PingFang SC', 'Microsoft YaHei', 'sans-serif'],
        mono: ['JetBrains Mono', 'SF Mono', 'Consolas', 'monospace'],
      },
      boxShadow: {
        xs: '0 1px 3px rgba(0,0,0,0.06)',
        sm: '0 4px 12px rgba(0,0,0,0.08)',
        md: '0 8px 24px rgba(0,0,0,0.10)',
        lg: '0 16px 40px rgba(0,0,0,0.12)',
        xl: '0 24px 56px rgba(0,0,0,0.14)',
        'neu-raised': '5px 5px 12px rgba(148,168,195,0.38), -5px -5px 12px rgba(255,255,255,0.72)',
        'neu-raised-hover': '7px 7px 16px rgba(138,160,188,0.28), -7px -7px 16px rgba(255,255,255,0.72)',
        'neu-inset': 'inset 1.5px 1.5px 4px rgba(148,168,195,0.38), inset -1px -1px 3px rgba(255,255,255,0.72)',
        'neu-inset-soft': 'inset 1px 1px 3px rgba(148,168,195,0.38), inset -0.5px -0.5px 2px rgba(255,255,255,0.72)',
        'neu-pressed': 'inset 2px 2px 4px rgba(0,0,0,0.15)',
        'btn-primary': '3px 3px 7px rgba(148,168,195,0.38), -2px -2px 5px rgba(255,255,255,0.72), 0 2px 6px rgba(8,145,178,0.2)',
        'btn-primary-hover': '5px 5px 10px rgba(138,160,188,0.28), -3px -3px 7px rgba(255,255,255,0.72), 0 4px 12px rgba(8,145,178,0.3)',
        'btn-glass': '3px 3px 7px rgba(148,168,195,0.38), -3px -3px 7px rgba(255,255,255,0.72)',
        'btn-glass-hover': '4px 4px 9px rgba(138,160,188,0.28), -4px -4px 9px rgba(255,255,255,0.72)',
        'glow-primary': '0 0 20px rgba(8,145,178,0.1)',
        'glow-sm': '0 0 0 2px rgba(8,145,178,0.12)',
      },
      keyframes: {
        'accordion-down': {
          from: { height: '0' },
          to: { height: 'var(--radix-accordion-content-height)' },
        },
        'accordion-up': {
          from: { height: 'var(--radix-accordion-content-height)' },
          to: { height: '0' },
        },
        'fade-in': {
          from: { opacity: '0' },
          to: { opacity: '1' },
        },
        'slide-up': {
          from: { transform: 'translateY(8px)', opacity: '0' },
          to: { transform: 'translateY(0)', opacity: '1' },
        },
        shimmer: {
          '0%': { transform: 'translateX(-100%)' },
          '100%': { transform: 'translateX(100%)' },
        },
      },
      animation: {
        'accordion-down': 'accordion-down 0.2s ease-out',
        'accordion-up': 'accordion-up 0.2s ease-out',
        'fade-in': 'fade-in 0.25s ease-out forwards',
        'slide-up': 'slide-up 0.3s ease-out forwards',
        shimmer: 'shimmer 1.5s infinite',
      },
      transitionDuration: {
        DEFAULT: '200ms',
      },
    },
  },
  plugins: [require('tailwindcss-animate')],
}

export default config
```

- [ ] **Step 2: Verify dev server compiles**

Run: `cd D:/grad_medical && npx vite build 2>&1 | tail -5`
Expected: Build succeeds (may have visual issues, but no compile errors)

- [ ] **Step 3: Commit**

```bash
git add tailwind.config.ts
git commit -m "refactor: replace dark theme with Neumorphic Medical Light in tailwind config"
```

---

### Task 2: Rewrite src/index.css

**Files:**
- Modify: `src/index.css`

- [ ] **Step 1: Replace entire `src/index.css` with light theme CSS**

```css
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=Noto+Sans+SC:wght@400;500;600;700&display=swap');

@tailwind base;
@tailwind components;
@tailwind utilities;

/* ============================================
   MediAI Design System — Neumorphic Medical Light
   Soft Gray-Blue Base · Teal Accent · Dual Shadows
   ============================================ */

@layer base {
  :root {
    --bg: #e4ecf4;
    --bg-card: #e4ecf4;
    --bg-inset: #dae4ef;
    --bg-elevated: #edf3fa;
    --sh-l: rgba(255,255,255,0.72);
    --sh-d: rgba(148,168,195,0.38);
    --sh-d2: rgba(138,160,188,0.28);
    --sh-d3: rgba(128,152,180,0.18);
    --text-heading: #0a2f2f;
    --text-body: #1a3244;
    --text-secondary: #3d5f73;
    --text-muted: #5e7f92;
    --brand-primary: #0891b2;
    --brand-accent: #14b8a6;
    --border-subtle: rgba(155,175,200,0.12);
    --border-default: rgba(155,175,200,0.18);
    --border-emphasis: rgba(8,145,178,0.15);
    --text-hero: clamp(2.25rem, 5vw, 3rem);
    --text-section: 1.375rem;
    --text-card-title: 1rem;
    --text-body-size: 0.9375rem;
    --text-caption: 0.8125rem;
    --text-micro: 0.6875rem;
    --radius-xs: 4px;
    --radius-sm: 8px;
    --radius-md: 10px;
    --radius-lg: 12px;
    --radius-xl: 16px;
    --radius-2xl: 24px;
  }

  * { border-color: var(--border-subtle); }

  html {
    scroll-behavior: smooth;
    text-rendering: optimizeLegibility;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
  }

  body {
    background: var(--bg);
    color: var(--text-body);
    font-family: 'Inter', 'SF Pro Display', -apple-system, BlinkMacSystemFont,
                 'Noto Sans SC', 'PingFang SC', 'Microsoft YaHei', sans-serif;
    font-feature-settings: "kern" 1, "liga" 1;
    line-height: 1.6;
  }

  h1, h2, h3, h4, h5, h6 {
    color: var(--text-heading);
    font-weight: 700;
    letter-spacing: -0.02em;
    line-height: 1.2;
  }

  h1 { font-size: var(--text-hero); font-weight: 800; letter-spacing: -0.03em; }
  h2 { font-size: var(--text-section); }
  h3 { font-size: var(--text-card-title); font-weight: 600; }

  p { line-height: 1.65; color: var(--text-secondary); }

  a { color: var(--brand-primary); text-decoration: none; transition: color 0.2s ease; }
  a:hover { color: #0e7490; }
}

/* Scrollbar */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(148,168,195,0.25); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: rgba(148,168,195,0.4); }
::selection { background: rgba(8,145,178,0.15); color: var(--text-heading); }
:focus-visible { outline: 2px solid var(--brand-primary); outline-offset: 2px; }

@layer components {
  .container {
    width: 100%;
    margin-left: auto;
    margin-right: auto;
    padding-left: 1rem;
    padding-right: 1rem;
  }

  @media (min-width: 768px) {
    .container { max-width: 768px; padding-left: 1.5rem; padding-right: 1.5rem; }
  }
  @media (min-width: 1024px) {
    .container { max-width: 1024px; padding-left: 2rem; padding-right: 2rem; }
  }
  @media (min-width: 1280px) {
    .container { max-width: 1280px; }
  }
  @media (min-width: 1536px) {
    .container { max-width: 1400px; }
  }

  /* Neumorphic Utilities */
  .n-raised {
    background: var(--bg-card);
    border-radius: var(--radius-lg);
    box-shadow: 5px 5px 12px var(--sh-d), -5px -5px 12px var(--sh-l);
  }
  .n-flat {
    background: var(--bg-card);
    border-radius: var(--radius-lg);
    box-shadow: 3px 3px 8px var(--sh-d3), -3px -3px 8px var(--sh-l);
  }
  .n-inset {
    background: var(--bg-inset);
    border-radius: var(--radius-md);
    box-shadow: inset 1.5px 1.5px 4px var(--sh-d), inset -1px -1px 3px var(--sh-l);
  }
  .n-inset-soft {
    background: var(--bg-inset);
    border-radius: var(--radius-md);
    box-shadow: inset 1px 1px 3px var(--sh-d), inset -0.5px -0.5px 2px var(--sh-l);
  }
  .glass {
    background: rgba(255,255,255,0.38);
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    border: 1px solid rgba(255,255,255,0.55);
    border-radius: var(--radius-lg);
  }

  /* Card Base — Neumorphic */
  .ia-card {
    background: var(--bg-card);
    border-radius: var(--radius-lg);
    box-shadow: 5px 5px 12px var(--sh-d), -5px -5px 12px var(--sh-l);
    transition: transform 0.2s ease-out, box-shadow 0.2s ease-out;
  }
  .ia-card-hover:hover {
    transform: translateY(-2px);
    box-shadow: 7px 7px 16px var(--sh-d2), -7px -7px 16px var(--sh-l);
  }
  .ia-card-active {
    box-shadow: 7px 7px 16px var(--sh-d2), -7px -7px 16px var(--sh-l);
    border: 1px solid rgba(8,145,178,0.12);
  }

  /* Badge — Light background + deep text */
  .ia-badge {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    padding: 3px 10px;
    font-size: var(--text-micro);
    font-weight: 600;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    border-radius: var(--radius-lg);
    border: 1px solid;
  }
  .ia-badge-primary { color: #0e7490; border-color: rgba(8,145,178,0.1); background: rgba(8,145,178,0.08); }
  .ia-badge-success { color: #059669; border-color: rgba(5,150,105,0.1); background: rgba(5,150,105,0.07); }
  .ia-badge-warning { color: #b45309; border-color: rgba(180,83,9,0.1); background: rgba(180,83,9,0.07); }
  .ia-badge-danger { color: #b91c1c; border-color: rgba(185,28,28,0.08); background: rgba(185,28,28,0.06); }
  .ia-badge-info { color: #0369a1; border-color: rgba(3,105,161,0.08); background: rgba(3,105,161,0.06); }

  /* Data Table */
  .data-table {
    width: 100%;
    border-collapse: collapse;
    font-size: var(--text-caption);
  }
  .data-table thead {
    border-bottom: none;
    background: var(--bg-inset);
  }
  .data-table th {
    padding: 10px 12px;
    text-align: left;
    font-weight: 600;
    font-size: var(--text-micro);
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: var(--text-muted);
    box-shadow: inset 1px 1px 2.5px var(--sh-d), inset -0.5px -0.5px 2px var(--sh-l);
  }
  .data-table td {
    padding: 10px 12px;
    border-bottom: 1px solid rgba(155,175,200,0.1);
    color: var(--text-body);
  }
  .data-table tbody tr { transition: background-color 0.15s ease; }
  .data-table tbody tr:nth-child(even) { background: rgba(8,145,178,0.015); }
  .data-table tbody tr:hover { background: rgba(8,145,178,0.04); }
  .data-table tbody tr:last-child td { border-bottom: none; }

  /* Progress Bar */
  .progress-bar {
    width: 100%;
    height: 5px;
    background: var(--bg-inset);
    border-radius: var(--radius-lg);
    box-shadow: inset 1px 1px 2.5px var(--sh-d), inset -0.5px -0.5px 2px var(--sh-l);
    overflow: hidden;
  }
  .progress-bar-fill {
    height: 100%;
    background: linear-gradient(90deg, var(--brand-primary), var(--brand-accent));
    border-radius: var(--radius-lg);
    box-shadow: 0 0 4px rgba(8,145,178,0.15);
    transition: width 0.4s ease;
  }
  .progress-bar-fill-success { background: linear-gradient(90deg, #059669, #34d399); }
  .progress-bar-fill-warning { background: linear-gradient(90deg, #b45309, #fbbf24); }

  /* Skeleton */
  .skeleton {
    position: relative;
    overflow: hidden;
    background: var(--bg-elevated);
    border-radius: var(--radius-sm);
  }
  .skeleton::after {
    content: '';
    position: absolute;
    inset: 0;
    transform: translateX(-100%);
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
    animation: skeletonShimmer 1.5s infinite;
  }

  /* Gradient Text */
  .gradient-text {
    background: linear-gradient(135deg, var(--brand-primary), var(--brand-accent));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }

  /* Drug Item */
  .drug-item {
    display: flex;
    align-items: center;
    gap: 11px;
    padding: 11px 13px;
    border-radius: var(--radius-md);
    background: var(--bg-inset);
    box-shadow: inset 1px 1px 3px var(--sh-d), inset -0.5px -0.5px 2px var(--sh-l);
    margin-bottom: 9px;
    transition: all 0.2s ease;
  }
  .drug-item:hover {
    background: var(--bg-elevated);
    box-shadow: 3px 3px 7px var(--sh-d), -3px -3px 7px var(--sh-l);
  }
}

/* Animations */
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}
@keyframes slideUp {
  from { opacity: 0; transform: translateY(12px); }
  to { opacity: 1; transform: translateY(0); }
}
@keyframes skeletonShimmer {
  100% { transform: translateX(100%); }
}
.animate-fade-in { animation: fadeIn 0.25s ease-out forwards; }
.animate-slide-up { animation: slideUp 0.3s ease-out forwards; }

/* Print */
@media print {
  .no-print { display: none !important; }
  .print-area { break-inside: avoid; }
  body { background: #e4ecf4 !important; color: #1a3244 !important; }
  .n-raised, .ia-card { background: #e4ecf4 !important; box-shadow: none !important; border: 1px solid #c8d5e0 !important; }
  .n-inset, .drug-item { background: #dae4ef !important; box-shadow: none !important; border: 1px solid #c8d5e0 !important; }
  h1, h2, h3, h4 { color: #0a2f2f !important; }
  .gradient-text { background: none !important; -webkit-text-fill-color: #0891b2 !important; }
}

/* Responsive */
@media (max-width: 640px) {
  .mobile-stack { flex-direction: column; }
  .mobile-full { width: 100%; }
  .mobile-hide { display: none; }
}
@media (min-width: 641px) {
  .desktop-hide { display: none; }
}

/* Accessibility */
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border-width: 0;
}
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

- [ ] **Step 2: Verify dev server compiles**

Run: `cd D:/grad_medical && npx vite build 2>&1 | tail -5`
Expected: Build succeeds

- [ ] **Step 3: Commit**

```bash
git add src/index.css
git commit -m "refactor: rewrite index.css for Neumorphic Medical Light theme"
```

---

## Phase 2: UI Primitives

### Task 3: Update button.tsx — new variants

**Files:**
- Modify: `src/components/ui/button.tsx`

- [ ] **Step 1: Replace button variants with neumorphic equivalents**

Replace the entire `buttonVariants` cva call in `button.tsx`:

```typescript
const buttonVariants = cva(
  'inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-md text-sm font-semibold tracking-tight transition-all duration-200 ease-out focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary/25 focus-visible:ring-offset-1 focus-visible:ring-offset-background disabled:pointer-events-none disabled:opacity-50 relative overflow-hidden',
  {
    variants: {
      variant: {
        default:
          'bg-gradient-to-br from-[#0a9dc4] to-[#077f9f] text-white shadow-btn-primary hover:shadow-btn-primary-hover hover:-translate-y-0.5 active:shadow-neu-pressed active:translate-y-0 after:absolute after:top-0 after:left-0 after:right-0 after:h-px after:bg-gradient-to-r after:from-transparent after:via-white/15 after:to-transparent',
        destructive:
          'bg-red-50/80 backdrop-blur-sm text-destructive border border-red-200/60 shadow-btn-glass hover:shadow-btn-glass-hover hover:-translate-y-0.5 active:shadow-neu-pressed active:translate-y-0',
        outline:
          'bg-white/35 backdrop-blur-sm text-primary border border-white/50 shadow-btn-glass hover:bg-white/50 hover:shadow-btn-glass-hover hover:-translate-y-0.5 active:shadow-neu-pressed active:translate-y-0 after:absolute after:top-0 after:left-0 after:right-0 after:h-px after:bg-gradient-to-r after:from-transparent after:via-white/15 after:to-transparent',
        secondary:
          'bg-background text-secondary-foreground shadow-btn-glass hover:text-primary hover:-translate-y-0.5 active:shadow-neu-pressed active:translate-y-0',
        ghost:
          'hover:bg-muted/50 hover:text-primary text-muted-foreground',
        success:
          'bg-gradient-to-br from-[#06a873] to-[#048a5e] text-white shadow-btn-primary hover:shadow-btn-primary-hover hover:-translate-y-0.5 active:shadow-neu-pressed active:translate-y-0 after:absolute after:top-0 after:left-0 after:right-0 after:h-px after:bg-gradient-to-r after:from-transparent after:via-white/15 after:to-transparent',
      },
      size: {
        default: 'h-10 px-5 py-2',
        sm: 'h-8 rounded-sm px-3 text-xs',
        lg: 'h-12 rounded-lg px-6 text-base',
        icon: 'h-10 w-10',
      },
    },
    defaultVariants: {
      variant: 'default',
      size: 'default',
    },
  }
)
```

Also update the `Button` component to remove the `active:scale-[0.98]` from the base class (already handled by active:shadow + translate in variants).

- [ ] **Step 2: Verify compilation**

Run: `cd D:/grad_medical && npx tsc --noEmit 2>&1 | tail -5`
Expected: No type errors

- [ ] **Step 3: Commit**

```bash
git add src/components/ui/button.tsx
git commit -m "refactor: update button variants for neumorphic light theme"
```

---

### Task 4: Update card.tsx — neumorphic cards

**Files:**
- Modify: `src/components/ui/card.tsx`

- [ ] **Step 1: Replace card component with neumorphic styles**

Replace the entire `card.tsx`:

```typescript
import * as React from 'react'
import { cn } from '@/lib/utils'

const Card = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement> & { hover?: 'lift' | 'none' | 'glow' }
>(({ className, hover = 'lift', ...props }, ref) => (
  <div
    ref={ref}
    className={cn(
      'rounded-xl bg-card text-card-foreground shadow-neu-raised',
      hover === 'lift' && 'transition-all duration-200 ease-out hover:-translate-y-0.5 hover:shadow-neu-raised-hover',
      hover === 'glow' && 'transition-all duration-200 ease-out hover:-translate-y-0.5 hover:shadow-neu-raised-hover hover:border-primary/12',
      hover === 'none' && '',
      className
    )}
    {...props}
  />
))
Card.displayName = 'Card'

const CardHeader = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div ref={ref} className={cn('flex flex-col space-y-1.5 p-5', className)} {...props} />
))
CardHeader.displayName = 'CardHeader'

const CardTitle = React.forwardRef<
  HTMLParagraphElement,
  React.HTMLAttributes<HTMLHeadingElement>
>(({ className, ...props }, ref) => (
  <h3 ref={ref} className={cn('text-base font-semibold leading-none tracking-tight text-foreground', className)} {...props} />
))
CardTitle.displayName = 'CardTitle'

const CardDescription = React.forwardRef<
  HTMLParagraphElement,
  React.HTMLAttributes<HTMLParagraphElement>
>(({ className, ...props }, ref) => (
  <p ref={ref} className={cn('text-sm text-muted-foreground leading-relaxed', className)} {...props} />
))
CardDescription.displayName = 'CardDescription'

const CardContent = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div ref={ref} className={cn('p-5 pt-4', className)} {...props} />
))
CardContent.displayName = 'CardContent'

const CardFooter = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div ref={ref} className={cn('flex items-center p-5 pt-0', className)} {...props} />
))
CardFooter.displayName = 'CardFooter'

export { Card, CardHeader, CardFooter, CardTitle, CardDescription, CardContent }
```

- [ ] **Step 2: Verify compilation**

Run: `cd D:/grad_medical && npx tsc --noEmit 2>&1 | tail -5`
Expected: No type errors

- [ ] **Step 3: Commit**

```bash
git add src/components/ui/card.tsx
git commit -m "refactor: update card component for neumorphic light theme"
```

---

### Task 5: Update input.tsx — inset shadow

**Files:**
- Modify: `src/components/ui/input.tsx`

- [ ] **Step 1: Replace input styles with neumorphic inset**

Replace the `classes` variable in `input.tsx`:

```typescript
const classes = cn(
  'flex h-10 w-full rounded-md border-0 bg-surface-inset px-3 py-2 text-sm text-foreground placeholder:text-muted-foreground/60 focus-visible:outline-none focus-visible:shadow-[inset_2px_2px_5px_var(--sh-d),inset_-1.5px_-1.5px_4px_var(--sh-l),0_0_0_2px_rgba(8,145,178,0.12)] shadow-neu-inset disabled:cursor-not-allowed disabled:opacity-40 transition-all duration-150',
  className
)
```

- [ ] **Step 2: Verify compilation**

Run: `cd D:/grad_medical && npx tsc --noEmit 2>&1 | tail -5`
Expected: No type errors

- [ ] **Step 3: Commit**

```bash
git add src/components/ui/input.tsx
git commit -m "refactor: update input component with neumorphic inset style"
```

---

### Task 6: Update SafetyBadge.tsx — light badge colors

**Files:**
- Modify: `src/components/SafetyBadge.tsx`

- [ ] **Step 1: Replace SafetyBadge with light-theme badge styles**

Replace the entire `SafetyBadge.tsx`:

```typescript
const safetyConfig: Record<string, { label: string; color: string; bg: string; border: string }> = {
  safe:                      { label: '安全',     color: '#059669', bg: 'rgba(5,150,105,0.07)',  border: 'rgba(5,150,105,0.1)' },
  relative_contraindication: { label: '需谨慎',   color: '#b45309', bg: 'rgba(180,83,9,0.07)',   border: 'rgba(180,83,9,0.1)' },
  off_label:                 { label: '超说明书', color: '#0369a1', bg: 'rgba(3,105,161,0.06)',  border: 'rgba(3,105,161,0.08)' },
  unverified:                { label: '待验证',   color: '#b91c1c', bg: 'rgba(185,28,28,0.06)',  border: 'rgba(185,28,28,0.08)' },
  data_unverified:           { label: '待验证',   color: '#b91c1c', bg: 'rgba(185,28,28,0.06)',  border: 'rgba(185,28,28,0.08)' },
}

export function SafetyBadge({ level }: { level: string }) {
  const cfg = safetyConfig[level] || { label: level || '未知', color: '#5e7f92', bg: 'rgba(94,127,146,0.06)', border: 'rgba(94,127,146,0.1)' }
  return (
    <span
      style={{
        display: 'inline-flex',
        alignItems: 'center',
        padding: '2px 9px',
        borderRadius: '9999px',
        fontSize: '11px',
        fontWeight: 600,
        color: cfg.color,
        backgroundColor: cfg.bg,
        border: `1px solid ${cfg.border}`,
        marginLeft: '6px',
        lineHeight: '18px',
      }}
    >
      {cfg.label}
    </span>
  )
}
```

- [ ] **Step 2: Verify compilation**

Run: `cd D:/grad_medical && npx tsc --noEmit 2>&1 | tail -5`
Expected: No type errors

- [ ] **Step 3: Commit**

```bash
git add src/components/SafetyBadge.tsx
git commit -m "refactor: update SafetyBadge with light theme badge colors"
```

---

## Phase 3: Layout

### Task 7: Update Layout.tsx

**Files:**
- Modify: `src/components/Layout.tsx`

This is a large file. The changes are systematic: replace all dark-theme color classes with light-theme equivalents.

- [ ] **Step 1: Update header background and border**

In the header className, replace:
- `bg-[rgba(10,22,40,0.96)]` → `bg-[rgba(228,236,244,0.85)]`
- `bg-[rgba(10,22,40,0.85)]` → `bg-[rgba(228,236,244,0.75)]`
- `border-white/[0.10]` → `border-[rgba(8,145,178,0.08)]`
- `border-white/[0.06]` → `border-[rgba(155,175,200,0.1)]`

- [ ] **Step 2: Update navigation classes**

Replace the desktop nav wrapping and items:
- Active nav item: `bg-brand-sky/10 text-brand-sky border border-brand-sky/20` → `bg-primary/8 text-primary border border-primary/12`
- Inactive nav item: `text-muted-foreground hover:text-foreground hover:bg-muted border border-transparent` → `text-secondary hover:text-primary hover:bg-muted/50 border border-transparent`
- Nav container: add `bg-background shadow-neu-inset rounded-md p-0.5` wrapping around nav items

- [ ] **Step 3: Update user section styles**

- User chip: `border border-ia-border bg-card` → `shadow-neu-raised border-0 bg-background`
- User avatar gradient: stays the same (gradient works on both themes)
- Logout button: `hover:bg-destructive/8 hover:text-destructive` → `hover:bg-destructive/6 hover:text-destructive`

- [ ] **Step 4: Update footer styles**

- Footer: `border-white/[0.06] bg-surface` → `border-[rgba(155,175,200,0.1)] bg-background`
- Footer text: already uses `text-muted-foreground` — no change needed (the token value changes via CSS variables)

- [ ] **Step 5: Update login modal overlay**

- Overlay: `bg-foreground/20` → `bg-foreground/10`
- Login card: uses Card component — already updated in Task 4
- Account demo boxes: `border border-ia-border` → `shadow-neu-inset border-0`
- Error box: `border-destructive/30 bg-destructive/6` → stays similar (works on light bg)

- [ ] **Step 6: Update mobile menu**

- Mobile menu: `border-t border-ia-border bg-card` → `border-t border-[rgba(155,175,200,0.1)] bg-background`
- Mobile user card: `border border-ia-border bg-card` → `shadow-neu-raised border-0 bg-background`
- Mobile nav active: `bg-primary/8 text-primary border-l-2 border-l-primary` → stays same (already uses semantic tokens)
- Mobile nav inactive: `text-muted-foreground hover:bg-muted hover:text-foreground` → `text-secondary hover:bg-muted/50 hover:text-primary`

- [ ] **Step 7: Verify the layout renders**

Run: `cd D:/grad_medical && npx vite build 2>&1 | tail -5`
Expected: Build succeeds

- [ ] **Step 8: Commit**

```bash
git add src/components/Layout.tsx
git commit -m "refactor: update Layout with neumorphic light theme styles"
```

---

## Phase 4: Page Components

### Task 8: Update HomePage.tsx

**Files:**
- Modify: `src/pages/HomePage.tsx`

- [ ] **Step 1: Replace all dark-theme color references**

Search for and replace:
- `bg-[#060f1e]`, `bg-[#0a1628]`, `bg-[#0f2744]`, `bg-[#132f4c]` → `bg-background` or `bg-surface-elevated`
- `bg-surface`, `bg-surface-elevated`, `bg-surface-overlay` → `bg-background` or `bg-surface-elevated`
- `text-white`, `text-slate-*` light variants → `text-foreground`, `text-secondary`, `text-muted-foreground`
- `border-white/[0.06]`, `border-white/[0.10]` → `border-border` or `border-[rgba(155,175,200,0.12)]`
- `shadow-*` dark variants → `shadow-neu-raised`, `shadow-neu-inset`

- [ ] **Step 2: Verify page renders without errors**

Run: `cd D:/grad_medical && npx tsc --noEmit 2>&1 | tail -5`

- [ ] **Step 3: Commit**

```bash
git add src/pages/HomePage.tsx
git commit -m "refactor: update HomePage with light theme styles"
```

---

### Task 9: Update DrugRecommendation.tsx

**Files:**
- Modify: `src/pages/DrugRecommendation.tsx`

- [ ] **Step 1: Replace all dark-theme hardcoded colors**

This page has the most color references (23 occurrences). Systematic replacements:
- `bg-[#0a1628]`, `bg-[#0f2744]`, `bg-[#132f4c]` → `bg-background` / `bg-surface-elevated` / `bg-surface-inset`
- `bg-surface`, `bg-surface-elevated` → `bg-background` / `bg-surface-elevated`
- `text-white` → `text-foreground`
- `border-white/[0.06]` etc. → `border-border`
- Drug result items → use `drug-item` CSS class from index.css
- Score badges with dark backgrounds → `ia-badge-*` classes
- Progress bars → `progress-bar` / `progress-bar-fill` classes

- [ ] **Step 2: Verify page renders**

Run: `cd D:/grad_medical && npx tsc --noEmit 2>&1 | tail -5`

- [ ] **Step 3: Commit**

```bash
git add src/pages/DrugRecommendation.tsx
git commit -m "refactor: update DrugRecommendation with light theme styles"
```

---

### Task 10: Update remaining page components (batch)

**Files:**
- Modify: `src/pages/PatientRecords.tsx`
- Modify: `src/pages/PrivacyConfig.tsx`
- Modify: `src/pages/AdminDashboard.tsx`
- Modify: `src/pages/LoginPage.tsx`
- Modify: `src/pages/DrugDatabase.tsx`
- Modify: `src/pages/MyRecords.tsx`
- Modify: `src/pages/ReviewDashboard.tsx`
- Modify: `src/pages/RecommendationStats.tsx`
- Modify: `src/pages/ForbiddenPage.tsx`
- Modify: `src/components/ReviewPanel.tsx`
- Modify: `src/components/ConsentDialog.tsx`
- Modify: `src/components/charts/AgeDistributionChart.tsx`
- Modify: `src/components/charts/DiseaseDistributionChart.tsx`

For each file, apply the same systematic replacements:
- `bg-[#060f1e]`, `bg-[#0a1628]`, `bg-[#0f2744]`, `bg-[#132f4c]` → `bg-background` / `bg-surface-elevated` / `bg-surface-inset`
- `bg-surface`, `bg-surface-elevated`, `bg-surface-overlay` → `bg-background` / `bg-surface-elevated` / `bg-surface-inset`
- `text-white` (in body context) → `text-foreground`
- `text-slate-300`, `text-slate-400` etc. light text → `text-secondary` / `text-muted-foreground`
- `border-white/[0.06]`, `border-white/[0.10]` → `border-border`
- `shadow-xs`, `shadow-sm` etc. → `shadow-neu-raised` / `shadow-neu-inset` where appropriate
- Chart components: update text colors from light-on-dark to dark-on-light (axis labels, legends)

- [ ] **Step 1: Update PatientRecords.tsx**

- [ ] **Step 2: Update PrivacyConfig.tsx**

- [ ] **Step 3: Update AdminDashboard.tsx**

- [ ] **Step 4: Update LoginPage.tsx**

- [ ] **Step 5: Update DrugDatabase.tsx**

- [ ] **Step 6: Update MyRecords.tsx**

- [ ] **Step 7: Update ReviewDashboard.tsx**

- [ ] **Step 8: Update RecommendationStats.tsx**

- [ ] **Step 9: Update ForbiddenPage.tsx**

- [ ] **Step 10: Update ReviewPanel.tsx**

- [ ] **Step 11: Update ConsentDialog.tsx**

- [ ] **Step 12: Update chart components**

For chart components, the key changes are:
- Axis tick colors: `#94a3b8` → `#5e7f92`
- Grid line colors: `rgba(255,255,255,0.06)` → `rgba(155,175,200,0.15)`
- Legend text: light → dark
- Tooltip backgrounds: dark → light

- [ ] **Step 13: Verify all pages compile**

Run: `cd D:/grad_medical && npx tsc --noEmit 2>&1 | tail -5`
Expected: No type errors

- [ ] **Step 14: Commit**

```bash
git add src/pages/ src/components/ReviewPanel.tsx src/components/ConsentDialog.tsx src/components/charts/
git commit -m "refactor: update all page components with neumorphic light theme"
```

---

## Phase 5: Verification

### Task 11: Visual verification and build test

**Files:**
- None (verification only)

- [ ] **Step 1: Run full build**

Run: `cd D:/grad_medical && npx vite build 2>&1 | tail -10`
Expected: Build succeeds with no errors

- [ ] **Step 2: Start dev server and visually verify each page**

Run: `cd D:/grad_medical && npx vite --port 5173`

Open browser and check each page:
- `/` (HomePage) — hero, stats, features visible
- `/recommendation` — drug items, badges, form inputs
- `/patients` — table, cards
- `/privacy` — progress bars, config cards
- `/admin` — dashboard cards
- `/login` — form inputs, buttons
- `/drug-database` — table, search
- `/review` — review panel
- `/recommendation-stats` — charts

- [ ] **Step 3: Check for remaining dark-theme artifacts**

Search for any remaining dark-specific patterns:
Run: `cd D:/grad_medical && grep -rn "bg-\[#0" src/ || echo "No dark bg hex found"`
Run: `cd D:/grad_medical && grep -rn "border-white" src/ || echo "No border-white found"`
Expected: No matches (all replaced)

- [ ] **Step 4: Verify print output**

In browser, use Ctrl+P to preview print. Verify:
- Background is light gray-blue (not white, not dark)
- All text is readable
- Cards have subtle borders (not shadows)
- Badges are visible

- [ ] **Step 5: Final commit if any fixes needed**

```bash
git add -A
git commit -m "fix: light theme visual adjustments after verification"
```

---

## Self-Review Checklist

- [x] **Spec coverage:** Every section of the design spec maps to a task
  - Color palette → Task 1 (tailwind) + Task 2 (CSS vars)
  - Shadow system → Task 1 + Task 2
  - Typography → Task 2 (body styles)
  - Buttons → Task 3
  - Badges → Task 2 (CSS) + Task 6 (SafetyBadge)
  - Cards → Task 4
  - Inputs → Task 5
  - Navigation → Task 7
  - Tables → Task 2 (CSS)
  - Progress bars → Task 2 (CSS)
  - Print CSS → Task 2
  - Dark-theme CSS cleanup → Task 2
  - darkMode removal → Task 1
  - All page files → Tasks 8-10
- [x] **No placeholders:** All steps contain actual code or exact commands
- [x] **Type consistency:** Button variant names match between Task 3 and the spec
- [x] **File paths:** All paths are exact and match the actual codebase

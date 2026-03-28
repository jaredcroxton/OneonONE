# PerformOS Design System
## Complete Style Guide for Building Family Apps

**Source:** PulseCheck 360  
**Purpose:** Use this to create consistent PerformOS family apps  
**Last Updated:** March 2026

---

## 🎨 COLOR PALETTE

### Foundation Colors
```css
--bg: #0B1220;                    /* Primary dark background */
--bg-2: #0E1A2B;                  /* Secondary dark background */
--surface-dark: #0F2138;          /* Dark surface (cards on dark bg) */
--surface-dark-2: #102844;        /* Secondary dark surface */
--surface-light: #FFFFFF;         /* White surface (cards on light bg) */
--surface-light-2: #F6F8FC;       /* Light gray surface */
```

### Text Colors
```css
--text-on-dark: #EAF0FF;                    /* Primary text on dark bg */
--text-on-dark-muted: rgba(234, 240, 255, 0.72);  /* Muted text on dark */
--text-on-light: #0B1220;                   /* Primary text on light bg */
--text-on-light-muted: rgba(11, 18, 32, 0.62);    /* Muted text on light */
```

### Border Colors
```css
--border-dark: rgba(255, 255, 255, 0.10);   /* Borders on dark bg */
--border-light: rgba(11, 18, 32, 0.10);     /* Borders on light bg */
```

### Accent Colors (Brand)
```css
--accent-blue: #3B82F6;     /* Primary interactive */
--accent-teal: #14B8A6;     /* Success / confirmation */
--accent-green: #22C55E;    /* Positive / growth */
```

### Status Colors
```css
--caution-amber: #F59E0B;                  /* Warning state */
--caution-amber-bg: rgba(245, 158, 11, 0.12);  /* Warning background */
--risk-red: #F87171;                       /* Error / danger */
--risk-red-bg: rgba(248, 113, 113, 0.12);  /* Error background */
```

### Functional
```css
--focus-ring: rgba(20, 184, 166, 0.45);    /* Focus state ring */
--shadow-soft: 0 10px 30px rgba(2, 6, 23, 0.35);   /* Soft shadow */
--shadow-card: 0 8px 24px rgba(2, 6, 23, 0.18);    /* Card shadow */
```

### Border Radius
```css
--radius-card: 16px;      /* Cards, panels */
--radius-control: 12px;   /* Buttons, inputs, form controls */
```

---

## 📝 TYPOGRAPHY

### Font Families
```css
/* Import these fonts */
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700&family=DM+Sans:wght@400;500;600;700&display=swap');

--font-sans: 'DM Sans', ui-sans-serif, system-ui;      /* Body text, UI */
--font-display: 'Outfit', ui-sans-serif, system-ui;    /* Headings, titles */
```

### Type Scale

**Display / Hero Text:**
```css
font-size: 3rem;        /* 48px - Login product name */
font-weight: 700;
font-family: var(--font-display);
letter-spacing: -0.03em;
line-height: 1;
```

**H1 - Page Titles:**
```css
font-size: 2.5rem;      /* 40px */
font-weight: 600;
font-family: var(--font-display);
letter-spacing: -0.02em;
line-height: 1.2;
```

**H2 - Section Titles:**
```css
font-size: 1.5rem;      /* 24px */
font-weight: 600;
font-family: var(--font-display);
line-height: 1.3;
```

**H3 - Subsection Headings:**
```css
font-size: 1.125rem;    /* 18px */
font-weight: 600;
font-family: var(--font-sans);
line-height: 1.4;
```

**H4 - Card Titles:**
```css
font-size: 1rem;        /* 16px */
font-weight: 600;
font-family: var(--font-sans);
line-height: 1.4;
```

**Body - Default Text:**
```css
font-size: 0.9375rem;   /* 15px */
font-weight: 400;
font-family: var(--font-sans);
line-height: 1.6;
```

**Small - Secondary Text:**
```css
font-size: 0.875rem;    /* 14px */
font-weight: 400;
font-family: var(--font-sans);
line-height: 1.5;
color: var(--text-on-dark-muted);
```

**Tiny - Labels, Captions:**
```css
font-size: 0.8125rem;   /* 13px */
font-weight: 500;
font-family: var(--font-sans);
letter-spacing: 0.01em;
```

**Micro - Overlines, Tags:**
```css
font-size: 0.75rem;     /* 12px */
font-weight: 600;
font-family: var(--font-sans);
text-transform: uppercase;
letter-spacing: 0.05em;
```

---

## 📐 SPACING SYSTEM

Use consistent spacing multipliers based on 0.25rem (4px):

```css
/* Spacing scale (multiply by 4px) */
0.25rem  =  4px   /* Tiny gaps */
0.5rem   =  8px   /* Small gaps */
0.75rem  = 12px   /* Default gaps */
1rem     = 16px   /* Standard spacing */
1.5rem   = 24px   /* Medium spacing */
2rem     = 32px   /* Large spacing */
3rem     = 48px   /* XL spacing */
4rem     = 64px   /* Section spacing */
```

**Common Patterns:**
- Card padding: `1.5rem` (24px)
- Section gaps: `2rem` (32px)
- Button padding: `0.75rem 1.5rem` (12px 24px)
- Form field spacing: `1rem` (16px)
- Container max-width: `1280px`
- Page padding: `2rem` (32px left/right)

---

## 🎯 LAYOUT PATTERNS

### App Shell Structure
```
┌─────────────────────────────────────┐
│  Header (sticky)                    │  80px height
│  max-width: 1280px, padding: 1rem  │
├─────────────────────────────────────┤
│                                     │
│  Main Content                       │
│  max-width: 1280px                  │
│  padding: 2rem                      │
│                                     │
│                                     │
└─────────────────────────────────────┘
```

### Header
```css
.app-header {
  background: var(--bg);
  border-bottom: 1px solid var(--border-dark);
  position: sticky;
  top: 0;
  z-index: 100;
  backdrop-filter: blur(12px);
  background: rgba(11, 18, 32, 0.8);  /* Semi-transparent */
}

.header-content {
  max-width: 1280px;
  margin: 0 auto;
  padding: 1rem 2rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
```

### Main Content Container
```css
.main-content {
  max-width: 1280px;
  margin: 0 auto;
  padding: 2rem;
}

.content-section {
  background: var(--surface-dark);
  border: 1px solid var(--border-dark);
  border-radius: var(--radius-card);
  padding: 2rem;
  margin-bottom: 2rem;
}
```

### Grid Layouts
```css
/* 2-column responsive grid */
.grid-2col {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 1.5rem;
}

/* 3-column responsive grid */
.grid-3col {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.5rem;
}

/* Stats grid (4 columns) */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}
```

---

## 🔘 BUTTON STYLES

### Primary Button
```css
.btn-primary {
  background: linear-gradient(135deg, #3B82F6, #06B6D4, #10B981);
  background-size: 200% 200%;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: var(--radius-control);
  font-size: 0.9375rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 24px rgba(59, 130, 246, 0.35);
  background-position: 100% 50%;
}

.btn-primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
}
```

### Secondary Button
```css
.btn-secondary {
  background: var(--surface-dark-2);
  color: var(--text-on-dark);
  border: 1px solid var(--border-dark);
  padding: 0.75rem 1.5rem;
  border-radius: var(--radius-control);
  font-size: 0.9375rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-secondary:hover {
  background: var(--surface-dark);
  border-color: var(--accent-teal);
}
```

### Ghost Button
```css
.btn-ghost {
  background: transparent;
  color: var(--text-on-dark-muted);
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: var(--radius-control);
  font-size: 0.9375rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-ghost:hover {
  background: rgba(255, 255, 255, 0.05);
  color: var(--text-on-dark);
}
```

---

## 📝 FORM CONTROLS

### Input Fields
```css
.form-input {
  background: var(--surface-dark-2);
  border: 1px solid var(--border-dark);
  border-radius: var(--radius-control);
  padding: 0.75rem 1rem;
  font-size: 0.9375rem;
  color: var(--text-on-dark);
  font-family: var(--font-sans);
  width: 100%;
  transition: all 0.2s;
}

.form-input:focus {
  outline: none;
  border-color: var(--accent-teal);
  box-shadow: 0 0 0 3px var(--focus-ring);
}

.form-input::placeholder {
  color: var(--text-on-dark-muted);
}
```

### Textarea
```css
.form-textarea {
  background: var(--surface-dark-2);
  border: 1px solid var(--border-dark);
  border-radius: var(--radius-control);
  padding: 0.75rem 1rem;
  font-size: 0.9375rem;
  color: var(--text-on-dark);
  font-family: var(--font-sans);
  width: 100%;
  min-height: 120px;
  resize: vertical;
  transition: all 0.2s;
}

.form-textarea:focus {
  outline: none;
  border-color: var(--accent-teal);
  box-shadow: 0 0 0 3px var(--focus-ring);
}
```

### Form Labels
```css
.form-label {
  display: block;
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--text-on-dark);
  margin-bottom: 0.5rem;
}
```

### Form Groups
```css
.form-group {
  margin-bottom: 1.5rem;
}

.form-group:last-child {
  margin-bottom: 0;
}
```

---

## 🃏 CARD COMPONENTS

### Standard Card
```css
.card {
  background: var(--surface-dark);
  border: 1px solid var(--border-dark);
  border-radius: var(--radius-card);
  padding: 1.5rem;
  transition: all 0.2s;
}

.card:hover {
  border-color: var(--accent-teal);
  transform: translateY(-2px);
  box-shadow: var(--shadow-card);
}
```

### Card with Header/Body
```css
.card-header {
  padding-bottom: 1rem;
  margin-bottom: 1rem;
  border-bottom: 1px solid var(--border-dark);
}

.card-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--text-on-dark);
}

.card-body {
  font-size: 0.9375rem;
  color: var(--text-on-dark-muted);
  line-height: 1.6;
}
```

### Stat Card
```css
.stat-card {
  background: var(--surface-dark);
  border: 1px solid var(--border-dark);
  border-radius: var(--radius-card);
  padding: 1.5rem;
  text-align: center;
}

.stat-value {
  font-size: 2.5rem;
  font-weight: 700;
  font-family: var(--font-display);
  color: var(--accent-teal);
  line-height: 1;
}

.stat-label {
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--text-on-dark-muted);
  margin-top: 0.5rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}
```

---

## 🏷️ BADGES & TAGS

### Status Badge
```css
.badge {
  display: inline-flex;
  align-items: center;
  padding: 0.375rem 0.75rem;
  border-radius: 999px;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.badge-success {
  background: rgba(34, 197, 94, 0.15);
  color: var(--accent-green);
}

.badge-warning {
  background: rgba(245, 158, 11, 0.15);
  color: var(--caution-amber);
}

.badge-danger {
  background: rgba(248, 113, 113, 0.15);
  color: var(--risk-red);
}

.badge-info {
  background: rgba(59, 130, 246, 0.15);
  color: var(--accent-blue);
}
```

---

## 📊 TABLE STYLES

### Standard Table
```css
.data-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  font-size: 0.875rem;
}

.data-table thead {
  background: var(--surface-dark-2);
  border-bottom: 1px solid var(--border-dark);
}

.data-table th {
  padding: 0.75rem 1rem;
  text-align: left;
  font-weight: 600;
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--text-on-dark-muted);
}

.data-table td {
  padding: 1rem;
  border-bottom: 1px solid var(--border-dark);
  color: var(--text-on-dark);
}

.data-table tbody tr {
  transition: background 0.2s;
}

.data-table tbody tr:hover {
  background: rgba(255, 255, 255, 0.02);
}
```

---

## 🎭 ANIMATIONS

### Transitions (Default)
```css
/* Use these timing functions */
transition: all 0.2s ease;      /* Standard UI transitions */
transition: all 0.3s ease;      /* Larger movements */
transition: transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);  /* Bounce effect */
```

### Hover Effects
```css
/* Standard hover lift */
.hover-lift:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-card);
}

/* Button hover */
.btn:hover {
  transform: translateY(-2px);
}
```

### Fade In Animation
```css
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.fade-in {
  animation: fadeIn 0.3s ease-out;
}
```

---

## 🖼️ LOGIN SCREEN PATTERN

### Split-Screen Layout
```css
.login-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  min-height: 100vh;
}

/* Left Panel - Brand */
.login-brand-panel {
  background: linear-gradient(135deg, #0B1220 0%, #0F2138 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 4rem;
}

.brand-content {
  max-width: 480px;
  text-align: center;
}

.brand-logo-image {
  width: 200px;
  margin-bottom: 2rem;
}

.brand-tagline {
  font-size: 0.75rem;
  font-weight: 600;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: var(--accent-teal);
  margin-bottom: 1.5rem;
}

.product-name {
  font-size: 2.5rem;
  font-weight: 700;
  color: var(--text-on-dark);
  margin-bottom: 1rem;
  font-family: var(--font-display);
}

.brand-description {
  font-size: 1.125rem;
  color: var(--text-on-dark-muted);
  line-height: 1.6;
}

/* Right Panel - Form */
.login-form-panel {
  background: var(--surface-light);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 4rem;
}

.login-form {
  width: 100%;
  max-width: 400px;
}

.login-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--text-on-light);
  margin-bottom: 2rem;
}
```

---

## 🎨 DASHBOARD HEADER PATTERN

### Role Header with Branding
```html
<header class="app-header">
  <div class="header-content">
    <h1 class="header-title">PerformOS · [Product Name]</h1>
    <div class="header-right">
      <div class="user-info">
        <span class="user-name">{user.name}</span>
        <span class="user-role">{user.role}</span>
      </div>
      <button class="btn-ghost">Sign out</button>
    </div>
  </div>
</header>
```

---

## 📱 RESPONSIVE BREAKPOINTS

```css
/* Mobile First Approach */

/* Mobile: 320px - 767px (default) */

/* Tablet: 768px and up */
@media (min-width: 768px) {
  .main-content {
    padding: 2rem;
  }
}

/* Desktop: 1024px and up */
@media (min-width: 1024px) {
  .main-content {
    padding: 3rem 2rem;
  }
}

/* Large Desktop: 1280px and up */
@media (min-width: 1280px) {
  .main-content {
    max-width: 1280px;
  }
}
```

---

## 🎯 TWO-ROLE AUTHENTICATION PATTERN

### For Manager + Executive Apps

**Login Screen:**
```jsx
// Role detection based on email domain or explicit selection
const roles = ['Manager', 'Executive'];

// Login form submits to single endpoint
// Backend returns user role in JWT token
```

**Route Protection:**
```jsx
// Protect routes based on role
if (user.role === 'manager') {
  // Show manager dashboard
} else if (user.role === 'executive') {
  // Show executive dashboard
}
```

**Dashboard Variants:**
- **Manager Dashboard**: Team-level data, individual reports, action items
- **Executive Dashboard**: Org-level metrics, trends, heatmaps, aggregates

---

## 🧩 COMMON PATTERNS

### Section Header
```css
.section-header {
  margin-bottom: 2rem;
}

.section-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--text-on-dark);
  margin-bottom: 0.5rem;
}

.section-description {
  font-size: 0.9375rem;
  color: var(--text-on-dark-muted);
}
```

### Empty State
```css
.empty-state {
  text-align: center;
  padding: 4rem 2rem;
  color: var(--text-on-dark-muted);
}

.empty-state-icon {
  font-size: 3rem;
  opacity: 0.3;
  margin-bottom: 1rem;
}

.empty-state-text {
  font-size: 1rem;
  margin-bottom: 1.5rem;
}
```

### Loading State
```css
.loading-spinner {
  border: 3px solid rgba(255, 255, 255, 0.1);
  border-top-color: var(--accent-teal);
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
```

---

## ✅ IMPLEMENTATION CHECKLIST

When building a new PerformOS family app:

**Setup:**
- [ ] Import Outfit & DM Sans fonts
- [ ] Copy all CSS variables to :root
- [ ] Set up app shell structure (header + main)
- [ ] Implement split-screen login
- [ ] Add PerformOS logo + product branding

**Components:**
- [ ] Create button variants (primary, secondary, ghost)
- [ ] Build form controls (input, textarea, labels)
- [ ] Design cards (standard, stat, with header)
- [ ] Add badges (success, warning, danger, info)
- [ ] Implement table styles
- [ ] Create empty/loading states

**Pages:**
- [ ] Manager dashboard layout
- [ ] Executive dashboard layout
- [ ] Use consistent section headers
- [ ] Apply proper spacing (2rem sections)
- [ ] Add hover effects and transitions

**Brand:**
- [ ] "PerformOS · [Product]" in header
- [ ] "by PerformOS" credit on login
- [ ] "POWERING HIGH PERFORMANCE" tagline
- [ ] Consistent accent colors (teal, blue, green)

---

## 📦 QUICK START TEMPLATE

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>[Product Name] by PerformOS</title>
  <link rel="stylesheet" href="performos-styles.css">
</head>
<body>
  <div class="app-shell">
    <!-- Header -->
    <header class="app-header">
      <div class="header-content">
        <h1 class="header-title">PerformOS · [Product]</h1>
        <div class="header-right">
          <div class="user-info">
            <span class="user-name">User Name</span>
            <span class="user-role">Manager</span>
          </div>
          <button class="btn-ghost">Sign out</button>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="main-content">
      <section class="content-section">
        <div class="section-header">
          <h2 class="section-title">Section Title</h2>
          <p class="section-description">Brief description</p>
        </div>
        
        <!-- Your content here -->
        <div class="grid-2col">
          <div class="card">
            <div class="card-header">
              <h3 class="card-title">Card Title</h3>
            </div>
            <div class="card-body">
              <p>Card content...</p>
            </div>
          </div>
        </div>
      </section>
    </main>
  </div>
</body>
</html>
```

---

**Need more specifics?** Check the source: `/app/frontend/src/App.css` for complete styles.

**Questions?** This design system ensures visual consistency across all PerformOS family products.

# PerformOS Brand Design System
## Use this as a prefix for all PerformOS applications

---

## 🎨 BRAND IDENTITY

**Brand Name:** PerformOS  
**Design Personality:**
- Executive-ready and professional
- Calm, trustworthy, premium SaaS (Stripe/Linear-level restraint)
- Sensitive-data respectful
- High-clarity, low-noise
- Modern corporate without being stiff

**Design Philosophy:**
Make business-critical applications feel structured, private, and actionable—without looking like generic enterprise software.

---

## 🎯 LOGIN PAGE (MANDATORY PATTERN)

**Layout:** Split-screen design (50/50 on desktop)

### Left Panel (Dark - Brand Side):
- **Background:** Deep navy (`#0B1220`)
- **Content:**
  - Large PerformOS brand title (3rem, Outfit font, weight 700)
  - Descriptive tagline (1.5rem, muted color, line-height 1.4)
  - Application-specific value proposition (3-4 words describing what this specific app does)
- **Style:** Centered vertically, generous padding (4rem)
- **Optional:** Subtle background image with dark overlay (10-20% opacity)

### Right Panel (Light - Form Side):
- **Background:** Pure white (`#FFFFFF`)
- **Content:**
  - Login form title (1.875rem, "Sign in to PerformOS [App Name]")
  - Email and password inputs
  - Primary action button (full-width teal)
  - Demo credentials block (small, muted, in light gray box)
- **Style:** Centered both ways, max-width 400px

### Mobile Behavior:
- Stack vertically
- Hide left panel on mobile
- Show compact brand logo at top of form

**Example Structure:**
```
┌─────────────────────┬─────────────────────┐
│                     │                     │
│   [Dark Navy]       │    [White]          │
│                     │                     │
│   PerformOS         │   Sign in to        │
│   [App Name]        │   PerformOS         │
│                     │                     │
│   [Tagline about    │   [Email input]     │
│    this specific    │   [Password input]  │
│    app's value]     │   [Sign In Button]  │
│                     │                     │
│                     │   [Demo logins]     │
│                     │                     │
└─────────────────────┴─────────────────────┘
```

---

## 🎨 COLOR SYSTEM (EXACT VALUES)

### Core Backgrounds:
```css
--bg: #0B1220;                    /* Primary dark background */
--bg-2: #0E1A2B;                  /* Slightly lighter dark */
--surface-dark: #0F2138;          /* Dark cards */
--surface-dark-2: #102844;        /* Darker cards */
--surface-light: #FFFFFF;         /* Light sections */
--surface-light-2: #F6F8FC;       /* Light secondary */
```

### Text Colors:
```css
--text-on-dark: #EAF0FF;                    /* Primary text on dark */
--text-on-dark-muted: rgba(234,240,255,0.72); /* Muted text on dark */
--text-on-light: #0B1220;                   /* Primary text on light */
--text-on-light-muted: rgba(11,18,32,0.62);   /* Muted text on light */
```

### Accent Colors (Blue → Teal → Green gradient):
```css
--accent-blue: #3B82F6;
--accent-teal: #14B8A6;          /* PRIMARY ACTION COLOR */
--accent-green: #22C55E;
```

### Status Colors:
```css
--caution-amber: #F59E0B;
--caution-amber-bg: rgba(245,158,11,0.12);
--risk-red: #F87171;             /* Muted red, never aggressive */
--risk-red-bg: rgba(248,113,113,0.12);
```

### Functional:
```css
--border-dark: rgba(255,255,255,0.10);
--border-light: rgba(11,18,32,0.10);
--focus-ring: rgba(20,184,166,0.45);
--shadow-soft: 0 10px 30px rgba(2,6,23,0.35);
--shadow-card: 0 8px 24px rgba(2,6,23,0.18);
--radius-card: 16px;
--radius-control: 12px;
```

### Gradient (Decorative Accent Only - Max 20% Viewport):
```css
linear-gradient(90deg, 
  rgba(59,130,246,0.95) 0%, 
  rgba(20,184,166,0.95) 45%, 
  rgba(34,197,94,0.95) 100%
)
```

**Usage:** Thin top border on hero cards, progress bars, 2-4px divider lines, chart highlights only

**PROHIBITED:** Never use purple, never use dark purple-to-pink gradients, never exceed 20% viewport coverage

---

## 📝 TYPOGRAPHY

### Font Families:
```css
--font-sans: 'DM Sans', ui-sans-serif, system-ui;     /* Body text */
--font-display: 'Outfit', ui-sans-serif, system-ui;    /* Headings */
```

### Google Fonts Import:
```html
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700&family=DM+Sans:wght@400;500;600;700&display=swap');
```

### Typography Scale:
- **H1/Hero:** 3rem (mobile) to 5rem (desktop), Outfit, weight 600-700
- **H2/Section Title:** 1.5rem to 2rem, Outfit, weight 600
- **Card Title:** 0.875rem to 1rem, Outfit, weight 600
- **Body Text:** 0.875rem to 1rem, DM Sans, weight 400
- **Small/Meta:** 0.75rem, DM Sans, weight 400, muted color

---

## 🏗️ LAYOUT PATTERNS

### App Shell:
- **Background:** Deep navy (`#0B1220`)
- **Pattern:** Alternating dark and light sections
  - Dark sections: Overview, KPIs, dashboards
  - Light sections: Tables, forms, long text reading areas
- **Max Width:** 1280px (dashboards), 1024px (content pages)
- **Padding:** 2rem horizontal, 3rem vertical between sections

### Header (Sticky):
- **Background:** Semi-transparent navy with backdrop blur
- **Border:** Bottom border (`1px solid var(--border-dark)`)
- **Height:** Auto (padding-based)
- **Content:** Logo/app name left, user info + nav right

### Cards:
- **Dark Cards:**
  - Background: `var(--surface-dark)`
  - Border: `1px solid var(--border-dark)`
  - Radius: `16px`
  - Padding: `1.5rem`
  - Shadow: `var(--shadow-card)`

- **Light Cards:**
  - Background: `#FFFFFF`
  - Border: `1px solid var(--border-light)`
  - Radius: `16px`
  - Padding: `1.5rem`
  - Shadow: `0 2px 8px rgba(0,0,0,0.04)`

### Grid Systems:
```css
/* KPI Grid */
grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
gap: 1.5rem;

/* Dashboard 2-Column */
grid-template-columns: 1fr 1fr;
gap: 1.5rem;

/* 3-Column */
grid-template-columns: repeat(3, 1fr);
gap: 1.5rem;
```

---

## 🎨 COMPONENT PATTERNS

### Buttons:

**Primary (Teal):**
```css
background: var(--accent-teal);
color: #0B1220;
padding: 0.75rem 1.5rem;
border-radius: var(--radius-control);
font-weight: 500;
hover: brightness(1.05);
transition: all 200ms;
```

**Secondary (Ghost on Dark):**
```css
background: rgba(255,255,255,0.10);
color: var(--text-on-dark);
border: 1px solid var(--border-dark);
hover: background rgba(255,255,255,0.15);
```

**Danger (Soft Red):**
```css
background: var(--risk-red-bg);
color: var(--risk-red);
border: 1px solid rgba(248,113,113,0.20);
```

### Form Inputs:

**On Dark Backgrounds:**
```css
background: rgba(255,255,255,0.05);
border: 1px solid var(--border-dark);
color: var(--text-on-dark);
padding: 0.75rem;
border-radius: var(--radius-control);
focus: outline 2px solid var(--focus-ring);
```

**On Light Backgrounds:**
```css
background: #FFFFFF;
border: 1px solid var(--border-light);
color: var(--text-on-light);
focus: border-color var(--accent-teal);
focus: outline 2px solid var(--focus-ring);
```

### Badges/Status:

**Success/On Track:**
```css
background: rgba(34,197,94,0.10);
color: #22C55E;
border: 1px solid rgba(34,197,94,0.20);
```

**Caution:**
```css
background: rgba(245,158,11,0.10);
color: #F59E0B;
border: 1px solid rgba(245,158,11,0.20);
```

**Risk/Error:**
```css
background: rgba(248,113,113,0.10);
color: #F87171;
border: 1px solid rgba(248,113,113,0.20);
```

### Tables (Always on Light Background):
- Use white background sections for all data tables
- Header: Subtle gray background, bold text
- Row hover: `hover:bg-slate-50`
- Borders: 1px solid `var(--border-light)`

---

## ✨ MOTION & INTERACTIONS

### Principles:
- Calm and deliberate (no bouncy overshoot)
- Motion clarifies state changes
- Respect `prefers-reduced-motion`

### Standard Transitions:
```css
/* Card Hover */
hover: transform translateY(-2px);
hover: shadow var(--shadow-soft);
transition: all 200ms ease;

/* Button Press */
active: transform scale(0.98);

/* Page Enter */
opacity: 0 → 1;
translateY: 8px → 0;
duration: 250ms;
```

---

## 📐 SPACING SYSTEM

Use consistent spacing multiples:
- **0.25rem** (4px) - Tiny gaps
- **0.5rem** (8px) - Small gaps, icon margins
- **1rem** (16px) - Standard element spacing
- **1.5rem** (24px) - Card padding, form groups
- **2rem** (32px) - Section padding horizontal
- **3rem** (48px) - Section padding vertical
- **4rem** (64px) - Hero padding, login panels

---

## ♿ ACCESSIBILITY REQUIREMENTS

- **Contrast:** WCAG AA minimum for all text
- **Focus Rings:** Always visible using `var(--focus-ring)`
- **Color Independence:** Never rely on color alone for status (include icons + labels)
- **Keyboard Navigation:** All interactive elements must be keyboard accessible
- **Motion:** Respect `prefers-reduced-motion`
- **ARIA:** Proper labels for forms, dialogs, tables

---

## 🚫 NEVER DO

1. **Never use purple** anywhere in PerformOS applications
2. **Never use dark gradients** (purple-to-pink, blue-to-purple)
3. **Never center-align the app container** globally
4. **Never use `transition: all`** (breaks transforms)
5. **Never use emoji icons** (🤖💡🎯) - use Lucide React or FontAwesome only
6. **Never exceed 20% viewport** with gradients
7. **Never use aggressive/bright red** for errors (use muted `#F87171`)
8. **Never use default HTML form elements** without styling
9. **Never hardcode colors** - always use CSS variables
10. **Never skip focus states** on interactive elements

---

## ✅ ALWAYS DO

1. **Always use the split-screen login** pattern (left dark, right white)
2. **Always include PerformOS branding** on the left panel
3. **Always use alternating dark/light sections** for content hierarchy
4. **Always use Outfit** for headings, **DM Sans** for body
5. **Always use teal (`#14B8A6`)** for primary actions
6. **Always add subtle shadows** to elevated cards
7. **Always make forms full-width** with proper spacing
8. **Always include hover states** with smooth transitions
9. **Always use 16px border radius** for cards, 12px for controls
10. **Always test on mobile** - the split login becomes stacked

---

## 📦 TECH STACK PREFERENCES

### Recommended Libraries:
- **UI Components:** Shadcn/UI (already configured)
- **Icons:** Lucide React (already installed)
- **Charts:** Recharts (for data visualization)
- **Motion:** Framer Motion (for smooth animations)
- **Toasts:** Sonner (already configured)

### Component Path:
```
/app/frontend/src/components/ui/
```

Use these pre-built components: Button, Card, Input, Tabs, Badge, Table, Dialog, Form, Select, etc.

---

## 📋 BRAND CHECKLIST FOR NEW APPS

When starting a new PerformOS app, ensure:

- [ ] Split-screen login with PerformOS branding on dark left panel
- [ ] Deep navy background (`#0B1220`) as primary background
- [ ] Outfit font for all headings
- [ ] DM Sans font for all body text
- [ ] Teal (`#14B8A6`) primary action buttons
- [ ] Blue → Teal → Green accent gradient (decorative only)
- [ ] Alternating dark and light content sections
- [ ] White background for all data tables
- [ ] 16px border radius on cards
- [ ] Subtle shadows on elevated elements
- [ ] Focus rings on all interactive elements
- [ ] Responsive mobile design (stacked login on mobile)
- [ ] No purple anywhere
- [ ] No emoji icons
- [ ] All CSS variables defined in `:root`
- [ ] Smooth hover states on all buttons/cards

---

## 🎯 HOW TO USE THIS PROMPT

When creating a new PerformOS application in Emergent:

1. **Start your prompt with:**
   > "This is a PerformOS application. Follow the PerformOS Brand Design System exactly as defined in the brand guidelines. This includes the split-screen login pattern, deep navy color scheme, Outfit/DM Sans typography, and teal accent color. The app is called '[Your App Name]' and it [describe functionality]."

2. **Provide app-specific details:**
   - What the app does
   - User roles
   - Key features
   - Data models

3. **Emergent will automatically apply:**
   - PerformOS login page design
   - Color system
   - Typography
   - Layout patterns
   - Component styling

4. **Result:** Consistent PerformOS look and feel across all applications in your suite

---

## 📸 VISUAL REFERENCE

**Login Page Structure:**
- Left: Dark navy (`#0B1220`) with PerformOS branding, large tagline
- Right: White (`#FFFFFF`) with centered login form, demo credentials at bottom
- Mobile: Vertical stack, hide left panel

**Dashboard Structure:**
- Dark navy header (sticky)
- Alternating sections: Dark (KPIs, overview) → Light (tables, forms) → Dark (charts)
- Cards with 16px radius, subtle shadows
- Teal primary buttons

**Typography Hierarchy:**
- Large Outfit headings (2.5-3rem)
- DM Sans body text (0.875-1rem)
- Muted secondary text (72% opacity on dark, 62% on light)

---

## 🔗 FILE REFERENCES

When Emergent builds your app, reference these files for exact implementation:
- **Design Guidelines:** `/app/design_guidelines.md`
- **CSS Variables:** `/app/frontend/src/App.css` (lines 4-40)
- **Login Pattern:** `.login-container`, `.login-left`, `.login-right` classes

---

**VERSION:** 1.0  
**LAST UPDATED:** March 2026  
**MAINTAINED BY:** PerformOS Product Team

---

## ⚡ QUICK START TEMPLATE

Copy this when starting a new PerformOS app:

```
I'm building a new PerformOS application called "[App Name]".

BRAND REQUIREMENTS:
- Follow PerformOS Brand Design System exactly
- Use split-screen login: left panel dark navy (#0B1220) with PerformOS branding, right panel white with login form
- Color scheme: Deep navy backgrounds, teal primary actions (#14B8A6), blue-teal-green accents
- Typography: Outfit for headings, DM Sans for body
- Layout: Alternating dark and light sections for content
- Cards: 16px radius, subtle shadows, 1.5rem padding
- Never use purple, never use emoji icons, never exceed 20% viewport with gradients

APP DETAILS:
[Describe your specific application here - what it does, user roles, features, etc.]

Please build this with the exact PerformOS look and feel.
```


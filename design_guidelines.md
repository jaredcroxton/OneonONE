{
  "product": {
    "name": "PerformOS One-on-One Builder",
    "design_personality": [
      "executive-ready",
      "calm + trustworthy",
      "premium SaaS (Stripe/Linear-level restraint)",
      "sensitive-data respectful",
      "high-clarity, low-noise"
    ],
    "north_star": "Make psychologically-safe performance conversations feel structured, private, and actionable—without looking like a generic HR tool."
  },

  "global_rules": {
    "must_match_reference_component": "Match the provided performos-one-on-one.jsx styling: deep navy app shell with alternating dark/white sections, premium cards, and blue→teal→green accent.",
    "file_type": "Project uses .js (not .tsx). Write components accordingly.",
    "testing": {
      "data_testid_required": "All interactive and key informational elements MUST include data-testid in kebab-case (role-based, not appearance-based).",
      "examples": [
        "data-testid=\"login-form-submit-button\"",
        "data-testid=\"manager-dashboard-team-health-tab\"",
        "data-testid=\"risk-flag-acknowledge-button\"",
        "data-testid=\"session-reflection-submit-button\""
      ]
    },
    "content_tone": {
      "voice": "neutral, supportive, non-judgmental",
      "avoid": [
        "alarmist language",
        "shaming phrasing",
        "overly playful copy"
      ],
      "preferred_terms": [
        "Signal",
        "Caution",
        "Needs attention",
        "Follow-up suggested",
        "Resolved"
      ]
    }
  },

  "typography": {
    "font_pairing": {
      "headings": {
        "family": "Outfit",
        "weights": [600, 700],
        "usage": "H1/H2, card titles, KPI numbers"
      },
      "body": {
        "family": "DM Sans",
        "weights": [400, 500, 600],
        "usage": "body, labels, helper text, table text"
      }
    },
    "implementation": {
      "google_fonts": [
        "https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700&family=DM+Sans:wght@400;500;600;700&display=swap"
      ],
      "css_vars": {
        "--font-sans": "'DM Sans', ui-sans-serif, system-ui",
        "--font-display": "'Outfit', ui-sans-serif, system-ui"
      }
    },
    "type_scale_tailwind": {
      "h1": "text-4xl sm:text-5xl lg:text-6xl font-semibold tracking-tight",
      "h2": "text-base md:text-lg font-medium text-slate-200/90",
      "section_title": "text-xl md:text-2xl font-semibold",
      "card_title": "text-sm font-semibold tracking-tight",
      "kpi_value": "text-2xl md:text-3xl font-semibold tabular-nums",
      "body": "text-sm md:text-base leading-relaxed",
      "small": "text-xs text-slate-500"
    }
  },

  "color_system": {
    "notes": [
      "Primary shell is deep navy; content cards alternate between dark-surface and white-surface sections.",
      "Use blue→teal→green accent for highlights, progress, and positive trends.",
      "Use amber for caution and muted red for high risk (never aggressive neon red).",
      "Gradients are decorative accents only; keep under 20% viewport."
    ],
    "tokens_css": {
      ":root": {
        "--bg": "#0B1220",
        "--bg-2": "#0E1A2B",
        "--surface-dark": "#0F2138",
        "--surface-dark-2": "#102844",
        "--surface-light": "#FFFFFF",
        "--surface-light-2": "#F6F8FC",
        "--text-on-dark": "#EAF0FF",
        "--text-on-dark-muted": "rgba(234,240,255,0.72)",
        "--text-on-light": "#0B1220",
        "--text-on-light-muted": "rgba(11,18,32,0.62)",

        "--border-dark": "rgba(255,255,255,0.10)",
        "--border-light": "rgba(11,18,32,0.10)",

        "--accent-blue": "#3B82F6",
        "--accent-teal": "#14B8A6",
        "--accent-green": "#22C55E",

        "--caution-amber": "#F59E0B",
        "--caution-amber-bg": "rgba(245,158,11,0.12)",
        "--risk-red": "#F87171",
        "--risk-red-bg": "rgba(248,113,113,0.12)",

        "--focus-ring": "rgba(20,184,166,0.45)",

        "--shadow-soft": "0 10px 30px rgba(2,6,23,0.35)",
        "--shadow-card": "0 8px 24px rgba(2,6,23,0.18)",
        "--radius-card": "16px",
        "--radius-control": "12px"
      },
      ".dark": {
        "--background": "220 45% 8%",
        "--foreground": "210 40% 98%",
        "--card": "220 45% 10%",
        "--card-foreground": "210 40% 98%",
        "--border": "215 25% 20%",
        "--ring": "173 80% 40%"
      }
    },
    "accent_gradient": {
      "allowed": "linear-gradient(90deg, rgba(59,130,246,0.95) 0%, rgba(20,184,166,0.95) 45%, rgba(34,197,94,0.95) 100%)",
      "usage": [
        "thin top border on hero card",
        "progress indicator fill",
        "small 2-4px divider lines",
        "chart line highlight"
      ]
    }
  },

  "layout_and_grid": {
    "app_shell": {
      "pattern": "Dark navy background with alternating white sections for dense reading areas (tables, forms, long notes).",
      "max_width": "max-w-6xl (content), max-w-7xl (dashboards)",
      "padding": "px-4 sm:px-6 lg:px-8",
      "section_spacing": "py-10 sm:py-14",
      "card_padding": "p-5 sm:p-6",
      "card_radius": "rounded-[var(--radius-card)]",
      "card_border": "border border-white/10 on dark; border-slate-200 on light"
    },
    "dashboard_grid": {
      "kpi_row": "grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-6",
      "content_row": "grid grid-cols-1 lg:grid-cols-3 gap-4 sm:gap-6",
      "table_area": "col-span-1 lg:col-span-2"
    },
    "navigation": {
      "top_nav": "sticky top-0 z-40 backdrop-blur supports-[backdrop-filter]:bg-[#0B1220]/70 border-b border-white/10",
      "tabs": "Use shadcn Tabs with pill-like triggers; active state uses subtle teal ring + dark fill"
    }
  },

  "components": {
    "component_path": {
      "shadcn_primary": "/app/frontend/src/components/ui/",
      "use_these": {
        "Button": "button.jsx",
        "Card": "card.jsx",
        "Tabs": "tabs.jsx",
        "Badge": "badge.jsx",
        "Table": "table.jsx",
        "Dialog": "dialog.jsx",
        "Drawer": "drawer.jsx (mobile session notes)",
        "Form": "form.jsx",
        "Input": "input.jsx",
        "Textarea": "textarea.jsx",
        "Select": "select.jsx",
        "Calendar": "calendar.jsx (schedule date picking)",
        "Progress": "progress.jsx",
        "Tooltip": "tooltip.jsx",
        "HoverCard": "hover-card.jsx (risk explanation)",
        "Separator": "separator.jsx",
        "Skeleton": "skeleton.jsx",
        "SonnerToast": "sonner.jsx"
      }
    },
    "card_recipes": {
      "dark_card": {
        "classes": "rounded-[var(--radius-card)] border border-white/10 bg-[color:var(--surface-dark)] shadow-[var(--shadow-card)]",
        "header": "flex items-start justify-between gap-4",
        "title": "font-display text-sm text-[color:var(--text-on-dark)]",
        "meta": "text-xs text-[color:var(--text-on-dark-muted)]"
      },
      "light_card": {
        "classes": "rounded-[var(--radius-card)] border border-slate-200 bg-white shadow-sm",
        "title": "font-display text-sm text-slate-900",
        "meta": "text-xs text-slate-500"
      }
    },
    "badges_and_status": {
      "health_ok": {
        "label": "On track",
        "classes": "bg-emerald-500/10 text-emerald-200 border border-emerald-500/20"
      },
      "health_caution": {
        "label": "Caution",
        "classes": "bg-amber-500/10 text-amber-200 border border-amber-500/20"
      },
      "health_risk": {
        "label": "High risk",
        "classes": "bg-rose-500/10 text-rose-200 border border-rose-500/20"
      },
      "flag_chip": {
        "pattern": "Use Badge with icon + short label; never rely on color alone."
      }
    },
    "buttons": {
      "shape": "Professional / Corporate: medium radius 10–12px (use --radius-control)",
      "variants": {
        "primary": {
          "usage": "Main actions: Start session, Submit reflection, Acknowledge flag",
          "classes": "bg-[color:var(--accent-teal)] text-slate-950 hover:bg-[color:rgba(20,184,166,0.92)] focus-visible:ring-2 focus-visible:ring-[color:var(--focus-ring)]",
          "motion": "transition-colors duration-200"
        },
        "secondary": {
          "usage": "Less prominent actions: View details, Export",
          "classes": "bg-white/10 text-[color:var(--text-on-dark)] hover:bg-white/15 border border-white/10",
          "motion": "transition-colors duration-200"
        },
        "ghost": {
          "usage": "Inline actions in tables",
          "classes": "bg-transparent hover:bg-white/10 text-[color:var(--text-on-dark)]",
          "motion": "transition-colors duration-200"
        },
        "danger_soft": {
          "usage": "Resolve/Remove flag (confirm in dialog)",
          "classes": "bg-rose-500/10 text-rose-200 hover:bg-rose-500/15 border border-rose-500/20",
          "motion": "transition-colors duration-200"
        }
      },
      "press_state": "active:scale-[0.98] (only on buttons, not globally)"
    },
    "forms": {
      "pattern": "Use shadcn Form + Input/Textarea. Labels always visible; helper text below. For sensitive prompts, add a short privacy note.",
      "input_classes": "bg-white/5 border-white/10 text-[color:var(--text-on-dark)] placeholder:text-white/35 focus-visible:ring-2 focus-visible:ring-[color:var(--focus-ring)]",
      "textarea": "Prefer 6–10 rows for reflection; autosize optional."
    },
    "tables": {
      "pattern": "Use shadcn Table inside a light section for readability. Sticky header optional.",
      "row_hover": "hover:bg-slate-50",
      "actions": "Use ghost buttons with tooltips; keep actions right-aligned."
    },
    "charts": {
      "library": "Recharts",
      "usage": [
        "Team Health score trend line",
        "Confidence trend line",
        "Action completion rate bar"
      ],
      "style": {
        "grid": "stroke: rgba(255,255,255,0.08) on dark; rgba(15,23,42,0.08) on light",
        "line": "stroke: var(--accent-teal)",
        "secondary_line": "stroke: var(--accent-blue)",
        "danger": "stroke: rgba(248,113,113,0.9)",
        "tooltip": "Use shadcn Tooltip/HoverCard styling; avoid heavy shadows"
      }
    }
  },

  "page_blueprints": {
    "login": {
      "layout": "Split layout: left = brand + trust copy on dark; right = white card form.",
      "must_include": [
        "Demo credentials block (small, muted)",
        "Password visibility toggle",
        "Privacy reassurance line"
      ],
      "key_testids": [
        "login-form-email-input",
        "login-form-password-input",
        "login-form-submit-button"
      ]
    },
    "home_role_select": {
      "layout": "Two premium cards (Manager / Team Member) with short description + CTA.",
      "interaction": "Card hover lifts 2px + border brightens; CTA button appears stronger.",
      "key_testids": [
        "role-select-manager-card",
        "role-select-team-member-card",
        "role-select-manager-continue-button",
        "role-select-team-member-continue-button"
      ]
    },
    "manager_dashboard": {
      "top_kpis": [
        "Upcoming 1:1s",
        "Completed this month",
        "Team health score",
        "Active flags"
      ],
      "tabs": [
        "Schedule",
        "Team Health",
        "Performance Trends"
      ],
      "key_testids": [
        "manager-dashboard-tabs",
        "manager-dashboard-schedule-tab",
        "manager-dashboard-team-health-tab",
        "manager-dashboard-performance-trends-tab"
      ]
    },
    "schedule_tab": {
      "layout": "Light section table for team list; right rail (on desktop) for selected member details.",
      "table_columns": [
        "Team member",
        "Health status",
        "Last session",
        "Next session",
        "Actions"
      ],
      "actions": [
        "Schedule",
        "Start session",
        "View history"
      ]
    },
    "team_health_tab": {
      "layout": "Top: flags summary + trend chart. Below: member health cards grid.",
      "flag_management": "Each flag row has: severity badge, short label, source, created date, actions (Acknowledge/Resolve) with confirmation dialog.",
      "safety_copy": "Use calm language: 'Signal detected' not 'Problem found'."
    },
    "performance_trends_tab": {
      "layout": "Two charts + one table: confidence trend, action completion, recent commitments.",
      "empty_state": "If no data, show a light card with 'Run your first 1:1' CTA."
    },
    "team_member_dashboard": {
      "layout": "Top: pending reflection card (primary). Below: recent sessions + personal trend.",
      "privacy": "Add a small note: 'Only you can view your reflections unless you choose to share in-session.'"
    },
    "session_flow": {
      "steps": [
        "Pre-meeting reflection (team member)",
        "Conversation notes (manager)",
        "AI summary + follow-ups"
      ],
      "ui_pattern": "Use a stepper-like header (can be Tabs or custom) with subtle gradient underline.",
      "notes_entry": "On desktop: Dialog; on mobile: Drawer.",
      "ai_summary": "Show summary in a light card with sections: Themes, Risks (if any), Suggested follow-ups, Commitments."
    }
  },

  "motion_and_microinteractions": {
    "principles": [
      "Motion should feel calm and deliberate (no bouncy overshoot).",
      "Use motion to clarify state changes: selection, success, caution.",
      "Respect prefers-reduced-motion."
    ],
    "recommended_library": {
      "name": "framer-motion",
      "install": "npm i framer-motion",
      "use_cases": [
        "Card hover lift",
        "Tab content fade/slide",
        "Flag acknowledge -> row collapse",
        "Session step transitions"
      ]
    },
    "motion_recipes": {
      "card_hover": "hover:-translate-y-0.5 hover:shadow-[0_14px_40px_rgba(2,6,23,0.35)] transition-[box-shadow,transform,border-color] duration-200",
      "section_enter": "initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.25 }}",
      "button_press": "whileTap={{ scale: 0.98 }}"
    }
  },

  "accessibility": {
    "requirements": [
      "WCAG AA contrast for all text on dark and light surfaces.",
      "Visible focus rings using --focus-ring.",
      "Never rely on color alone for risk states; include icon + label.",
      "Keyboard navigable tabs, dialogs, menus (shadcn defaults).",
      "Respect prefers-reduced-motion for animations."
    ],
    "aria": {
      "dialogs": "Dialog titles required; describe risk flags with aria-labels.",
      "tables": "Use proper table semantics; add captions for screen readers when needed."
    }
  },

  "images": {
    "image_urls": [
      {
        "category": "login-left-panel",
        "description": "Subtle executive office / meeting image with dark overlay (10–20% opacity). Use as decorative background only.",
        "url": "https://images.unsplash.com/photo-1637665662134-db459c1bbb46?crop=entropy&cs=srgb&fm=jpg&ixid=M3w4NTYxODh8MHwxfHNlYXJjaHwxfHxleGVjdXRpdmUlMjB0ZWFtJTIwbWVldGluZyUyMG1vZGVybiUyMG9mZmljZSUyMGNhbmRpZHxlbnwwfHx8Ymx1ZXwxNzc0MDczNTY0fDA&ixlib=rb-4.1.0&q=85"
      },
      {
        "category": "home-role-select-hero",
        "description": "Warm, human, modern office collaboration image for the role selection page header (optional).",
        "url": "https://images.pexels.com/photos/7580644/pexels-photo-7580644.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940"
      },
      {
        "category": "empty-state-illustration",
        "description": "Use as a subtle empty-state visual (blurred + desaturated). Keep it small; do not dominate the viewport.",
        "url": "https://images.pexels.com/photos/7580751/pexels-photo-7580751.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940"
      }
    ]
  },

  "implementation_notes": {
    "instructions_to_main_agent": [
      "Replace CRA default App.css centering patterns; do NOT center the app container globally.",
      "Update index.css tokens to match the deep navy + premium accent system above; keep shadcn variable structure but override values.",
      "Use alternating sections: dark shell sections for overview + KPIs; white sections for tables/forms/long text.",
      "Cards: 12–16px radius, 20–24px padding, subtle shadows; consistent across dashboards.",
      "Use shadcn Tabs for Manager dashboard sections; ensure each tab trigger has data-testid.",
      "Use Sonner for toasts (success: teal, caution: amber, risk: soft red).",
      "Charts: use Recharts with restrained styling; avoid heavy fills; prefer lines + subtle area fill at 8–12% opacity.",
      "Risk flags: show severity badge + short label + 'Why this matters' hover card; actions require confirmation dialog.",
      "Do not use purple anywhere (especially not in gradients)."
    ],
    "extra_libraries": [
      {
        "name": "recharts",
        "install": "npm i recharts",
        "usage": "Trends charts in Team Health and Performance Trends tabs."
      },
      {
        "name": "framer-motion",
        "install": "npm i framer-motion",
        "usage": "Micro-interactions and calm transitions."
      }
    ]
  },

  "appendix_general_ui_ux_design_guidelines": "<General UI UX Design Guidelines>  \n    - You must **not** apply universal transition. Eg: `transition: all`. This results in breaking transforms. Always add transitions for specific interactive elements like button, input excluding transforms\n    - You must **not** center align the app container, ie do not add `.App { text-align: center; }` in the css file. This disrupts the human natural reading flow of text\n   - NEVER: use AI assistant Emoji characters like`🤖🧠💭💡🔮🎯📚🎭🎬🎪🎉🎊🎁🎀🎂🍰🎈🎨🎰💰💵💳🏦💎🪙💸🤑📊📈📉💹🔢🏆🥇 etc for icons. Always use **FontAwesome cdn** or **lucid-react** library already installed in the package.json\n\n **GRADIENT RESTRICTION RULE**\nNEVER use dark/saturated gradient combos (e.g., purple/pink) on any UI element.  Prohibited gradients: blue-500 to purple 600, purple 500 to pink-500, green-500 to blue-500, red to pink etc\nNEVER use dark gradients for logo, testimonial, footer etc\nNEVER let gradients cover more than 20% of the viewport.\nNEVER apply gradients to text-heavy content or reading areas.\nNEVER use gradients on small UI elements (<100px width).\nNEVER stack multiple gradient layers in the same viewport.\n\n**ENFORCEMENT RULE:**\n    • Id gradient area exceeds 20% of viewport OR affects readability, **THEN** use solid colors\n\n**How and where to use:**\n   • Section backgrounds (not content backgrounds)\n   • Hero section header content. Eg: dark to light to dark color\n   • Decorative overlays and accent elements only\n   • Hero section with 2-3 mild color\n   • Gradients creation can be done for any angle say horizontal, vertical or diagonal\n\n- For AI chat, voice application, **do not use purple color. Use color like light green, ocean blue, peach orange etc**\n\n</Font Guidelines>\n\n- Every interaction needs micro-animations - hover states, transitions, parallax effects, and entrance animations. Static = dead. \n   \n- Use 2-3x more spacing than feels comfortable. Cramped designs look cheap.\n\n- Subtle grain textures, noise overlays, custom cursors, selection states, and loading animations: separates good from extraordinary.\n   \n- Before generating UI, infer the visual style from the problem statement (palette, contrast, mood, motion) and immediately instantiate it by setting global design tokens (primary, secondary/accent, background, foreground, ring, state colors), rather than relying on any library defaults. Don't make the background dark as a default step, always understand problem first and define colors accordingly\n    Eg: - if it implies playful/energetic, choose a colorful scheme\n           - if it implies monochrome/minimal, choose a black–white/neutral scheme\n\n**Component Reuse:**\n\t- Prioritize using pre-existing components from src/components/ui when applicable\n\t- Create new components that match the style and conventions of existing components when needed\n\t- Examine existing components to understand the project's component patterns before creating new ones\n\n**IMPORTANT**: Do not use HTML based component like dropdown, calendar, toast etc. You **MUST** always use `/app/frontend/src/components/ui/ ` only as a primary components as these are modern and stylish component\n\n**Best Practices:**\n\t- Use Shadcn/UI as the primary component library for consistency and accessibility\n\t- Import path: ./components/[component-name]\n\n**Export Conventions:**\n\t- Components MUST use named exports (export const ComponentName = ...)\n\t- Pages MUST use default exports (export default function PageName() {...})\n\n**Toasts:**\n  - Use `sonner` for toasts\"\n  - Sonner component are located in `/app/src/components/ui/sonner.tsx`\n\nUse 2–4 color gradients, subtle textures/noise overlays, or CSS-based noise to avoid flat visuals.\n</General UI UX Design Guidelines>"
}

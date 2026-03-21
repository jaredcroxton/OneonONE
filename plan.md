# PerformOS One-on-One Builder — plan.md

## 1) Objectives
- Deliver a working MVP for structured one-on-ones (pre-reflection → manager notes → summary) with **AI-powered psychological safety risk detection** as the core differentiator.
- Prove XAI Grok integration reliably returns **(a) risk analysis**, **(b) conversation starters**, **(c) session summaries** in predictable JSON.
- Implement manager + team member experiences that match the provided premium design system and leverage the supplied React reference UI.
- Provide dashboards: Manager metrics + Team Health flags + Performance Trends; Senior-leader-ready aggregated view (MVP-level).

## 2) Implementation Steps

### Phase 1 — Core AI POC (Isolation, must pass before app build)
**User stories**
1. As a developer, I can send sample reflection text to Grok and receive a structured JSON risk assessment.
2. As a manager, I can get 2–3 grounded conversation starters based on a reflection + active flags.
3. As a manager, I can paste meeting notes/actions and get a concise JSON session summary.
4. As a system, I can enforce “JSON-only” responses and recover from malformed outputs.
5. As a system, I can map AI outputs into our flag categories/severity without ambiguity.

**Steps**
- Web research: confirm current **xAI Grok chat completions** endpoint, auth header format, model names, JSON mode (if available), and rate limits.
- Create `poc_grok.py` (standalone) that runs 3 calls:
  - `risk_analysis(reflection_payload, previous_sessions_summary)` → `{flags:[{category,severity,signal}], sentiment, key_quotes}`
  - `conversation_starters(reflection_payload, active_flags)` → `{starters:[...]}`
  - `session_summary(manager_notes, actions)` → `{summary, key_actions, follow_ups}`
- Implement strict parsing:
  - request JSON-only; strip code fences; retry once with “repair JSON” prompt if parsing fails.
- Validate with seed scenarios (Priya safety, James burnout, Marcus workload, Sarah healthy).
- **Do not proceed** until: 10/10 runs produce valid JSON and correct category/severity mappings.

### Phase 2 — V1 App Development (FastAPI + MongoDB + React, minimal auth)
**User stories**
1. As a team member, I can complete a pre-meeting reflection for my next 1:1.
2. As a manager, I can open a team member’s next session, review the reflection, and take structured notes.
3. As a manager, I can add actions with owner/status and save the session.
4. As a manager, I can see detected flags (rules + AI) in Team Health, and drill into a member.
5. As a leader, I can see an aggregated team health score and active flag counts.

**Backend (FastAPI)**
- Data models/collections: `users`, `members`, `sessions`, `flags` (MongoDB).
- Seed loader on startup (dev-only): manager + 6 members + session history + initial flags.
- Core endpoints (no OAuth; keep minimal):
  - Users/members: `GET /me`, `GET /members`, `GET /members/{id}`
  - Sessions: `GET /sessions?memberId=`, `POST /sessions` (create/update), `POST /reflections` (submit pre-meeting)
  - Flags: `GET /flags?status=open`, `PATCH /flags/{id}` (ack/resolve)
  - AI: `POST /ai/risk`, `POST /ai/starters`, `POST /ai/summary` (server calls Grok using provided key)
- Flag engine (deterministic + AI):
  - Rule flags: low scores (1–2), drop ≥2, persistent ≤3 for 3 sessions, withdrawal/blank changes, missed reflections, manager gap.
  - AI text analysis: map to categories/severity; dedupe with rule flags; persist flags with links to session.

**Frontend (React)**
- Start from provided `performos-one-on-one.jsx` UI:
  - Replace in-component Anthropic calls with backend calls (`/ai/*`).
  - Replace seed state with API fetch + optimistic updates.
  - Keep styling tokens/colors/layout intact (dark/white alternation + gradient accent).
- Implement core flows:
  - Login-lite for dev (email/password) OR temporary user switcher (to avoid auth blocking testing).
  - Team Member view: pending reflection form + recent sessions read-only.
  - Manager view: schedule list → start 1:1 modal → save notes/actions → summary display → flags updated.

**Phase 2 testing (1 full E2E pass)**
- Validate main flow: reflection submit → manager session → AI summary → flag creation → team health updates.
- Validate drilldowns: open flag → acknowledge/resolve → UI state updates.

### Phase 3 — Add Features + Hardening (still MVP scope)
**User stories**
1. As a manager, I can see trend charts per metric across sessions for each direct report.
2. As a manager, I can mark actions complete and track completion rate.
3. As a manager, I can filter Team Health by severity/category.
4. As a leader, I can view aggregated insights without seeing private notes.
5. As a team member, I can view my trends without seeing manager private notes.

**Steps**
- Improve trend computations and sparklines; ensure consistent ordering/time windows.
- Add flag lifecycle: open → acknowledged → resolved; audit fields.
- Add data validation and error states (network, partial saves, retries for AI).
- Refactor frontend into modular components/files (post-V1).
- Run E2E tests again after refactor.

### Phase 4 — Authentication + Role-based Access (ask before implementing)
**User stories**
1. As a user, I can securely log in and stay signed in.
2. As a manager, I can only see my direct reports.
3. As a team member, I can only see my own reflections/sessions.
4. As a leader, I can view aggregate metrics across teams without personal details.
5. As an admin, I can seed/reset demo data for demos.

**Steps**
- Add JWT auth (email/password) + role middleware; lock down endpoints.
- Add leader role + aggregated endpoints.
- Final E2E regression.

## 3) Next Actions (immediate)
1. Do web research + confirm xAI Grok API endpoint/model/headers + JSON-mode options.
2. Implement and run `poc_grok.py` for the 3 AI capabilities using the provided key.
3. Freeze prompts + JSON schemas + parsing/retry strategy once stable.
4. Stand up FastAPI + Mongo with seed loader and `/ai/*` endpoints.
5. Wire the reference React UI to backend APIs; complete Phase 2 E2E flow.

## 4) Success Criteria
- POC: Grok returns valid JSON for risk/starters/summary consistently; flags map correctly to categories/severity.
- V1: Users can complete the full workflow end-to-end; flags appear on dashboards; actions persist.
- UX: Premium styling preserved from reference UI; no broken states; loading/error states handled.
- Reliability: AI failures degrade gracefully (fallback starters/summary; rule-based flags still run).

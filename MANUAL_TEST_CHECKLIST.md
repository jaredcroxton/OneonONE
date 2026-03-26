# Manual Testing Checklist for Flag Action Tracking

## Test URL
**Preview**: https://team-health-hub-2.preview.emergentagent.com
**Production**: https://performos.digital

## Test Credentials
- **Manager**: alex@performos.io / demo

## Problem 1: Clickable Flags & Modal

### Test Steps:
1. Login as manager (alex@performos.io / demo)
2. Click "Team Health" tab
3. **Verify**: 7 active flags showing
4. **Verify**: James Rodriguez flag shows "1 action" badge (teal)
5. **Verify**: Marcus Thompson flag should show "2 actions" badge
6. **Click** on James Rodriguez flag card (anywhere on the card)
7. **Check browser console** for:
   - "Flag clicked: flag_001"
   - "Modal render check - selectedFlag:" (should show flag object)
8. **Verify**: Modal opens with:
   - James Rodriguez name and avatar
   - Wellbeing category
   - 1 existing action: "Removed James from on-call rotation..."
   - Timestamp: Mar 22, 2026 at [time]
   - Add New Action form (NO date picker - only textarea + checkbox)
9. **Fill form**:
   - Action note: "Had follow-up 1:1 to check energy levels"
   - Check: "I confirm this action has been completed"
10. **Click**: "Save Action"
11. **Verify**: 
    - Success toast appears
    - Action appears in history with SERVER-GENERATED timestamp
    - Action count badge updates to "2 actions"

## Problem 2: Tamper-Proof Timestamps

### Test Steps:
1. In the modal form, **verify**: NO date picker exists
2. When saving action, **verify**: Timestamp appears automatically
3. Try to edit existing action: **verify**: Cannot be edited or deleted
4. **Check format**: "Mar 26, 2026 at 2:45 PM" (server-generated)

## Problem 3: Weekly Action History

### Test Steps:
1. Scroll down below Active Signals
2. **Verify**: "My Action History" section exists
3. **Verify**: 8 week cards showing:
   - "This Week" - should show 3 actions (from seed data)
   - "Last Week" - should show 0 actions
   - Etc.
4. **Verify**: Weeks with actions have GREEN left border
5. **Verify**: Weeks with 0 actions have GRAY left border
6. **Click**: "This Week" card
7. **Verify**: Panel expands showing:
   - All actions from this week
   - Grouped by member
   - Shows: category icon, member name, severity, action note, timestamp
   - Each has green checkmark "Confirmed"
8. **Click**: Week card again to collapse

## Expected Seed Data Actions

### This Week (Mar 22-26, 2026):
1. **James Rodriguez** - Wellbeing - "Removed from on-call rotation..." (Mar 22)
2. **Marcus Thompson** - Workload - "Identified Sarah as DevOps..." (Mar 18) - WAIT, this is 2 weeks ago!
3. **Marcus Thompson** - Workload - "Reassigned 2 tickets..." (Mar 20)

## Console Debugging

If modal doesn't appear:
1. Open browser DevTools (F12)
2. Go to Console tab
3. Click a flag card
4. Look for:
   - "Flag clicked: [flag_id]" 
   - "Modal render check - selectedFlag: [object]"
5. If selectedFlag is null, there's a state issue
6. If selectedFlag has data but modal doesn't show, there's a CSS/z-index issue

## Browser Console Commands

```javascript
// Check if modal exists in DOM
document.querySelector('[data-testid="flag-modal"]')

// Check if overlay exists
document.querySelector('[data-testid="flag-modal-overlay"]')

// Check z-index
window.getComputedStyle(document.querySelector('.modal-overlay')).zIndex
```

## Success Criteria

✅ All 7 flags visible with correct action count badges
✅ Flag cards clickable everywhere
✅ Modal opens on click
✅ NO date picker in form
✅ Server generates timestamp on save
✅ Weekly history shows 8 weeks
✅ Week cards show correct action counts
✅ Clicking week card expands action list
✅ All actions show with proper formatting

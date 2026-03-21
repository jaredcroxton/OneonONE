from datetime import datetime
from database import users_collection, members_collection, submissions_collection, flags_collection
from auth import get_password_hash

# Generate Monday dates from Feb 23 to June 29, 2026
def generate_mondays():
    from datetime import datetime, timedelta
    mondays = []
    d = datetime(2026, 2, 23)  # Start from Feb 23
    end = datetime(2026, 6, 29)
    while d <= end:
        mondays.append(d.strftime("%Y-%m-%d"))
        d += timedelta(days=7)
    return mondays

MONDAY_DATES = generate_mondays()
CURRENT_WEEK = "2026-03-23"

# Helper function
def mk(r, c):
    return {"rating": r, "comment": c}

SEED_DATA = {
    "users": [
        {"_id": "manager_001", "name": "Alex Chen", "email": "alex@performos.io", "hashed_password": None, "role": "manager", "title": "Engineering Manager", "created_at": datetime(2026, 1, 1)},
        {"_id": "user_001", "name": "Sarah Mitchell", "email": "sarah@performos.io", "hashed_password": None, "role": "team_member", "title": "Senior Frontend Engineer", "created_at": datetime(2026, 1, 1)},
        {"_id": "user_002", "name": "James Rodriguez", "email": "james@performos.io", "hashed_password": None, "role": "team_member", "title": "Backend Engineer", "created_at": datetime(2026, 1, 1)},
        {"_id": "user_003", "name": "Priya Sharma", "email": "priya@performos.io", "hashed_password": None, "role": "team_member", "title": "Full Stack Engineer", "created_at": datetime(2026, 1, 1)},
        {"_id": "user_004", "name": "Marcus Thompson", "email": "marcus@performos.io", "hashed_password": None, "role": "team_member", "title": "DevOps Engineer", "created_at": datetime(2026, 1, 1)},
        {"_id": "user_005", "name": "Emily Nakamura", "email": "emily@performos.io", "hashed_password": None, "role": "team_member", "title": "Junior Engineer", "created_at": datetime(2026, 1, 1)},
        {"_id": "user_006", "name": "David O'Brien", "email": "david@performos.io", "hashed_password": None, "role": "team_member", "title": "QA Engineer", "created_at": datetime(2026, 1, 1)}
    ],
    "members": [
        {"_id": "member_001", "user_id": "user_001", "name": "Sarah Mitchell", "email": "sarah@performos.io", "title": "Senior Frontend Engineer", "manager_id": "manager_001"},
        {"_id": "member_002", "user_id": "user_002", "name": "James Rodriguez", "email": "james@performos.io", "title": "Backend Engineer", "manager_id": "manager_001"},
        {"_id": "member_003", "user_id": "user_003", "name": "Priya Sharma", "email": "priya@performos.io", "title": "Full Stack Engineer", "manager_id": "manager_001"},
        {"_id": "member_004", "user_id": "user_004", "name": "Marcus Thompson", "email": "marcus@performos.io", "title": "DevOps Engineer", "manager_id": "manager_001"},
        {"_id": "member_005", "user_id": "user_005", "name": "Emily Nakamura", "email": "emily@performos.io", "title": "Junior Engineer", "manager_id": "manager_001"},
        {"_id": "member_006", "user_id": "user_006", "name": "David O'Brien", "email": "david@performos.io", "title": "QA Engineer", "manager_id": "manager_001"}
    ],
    "submissions": [
        # SARAH - Week 1
        {"_id": "sub_001", "member_id": "member_001", "date": "2026-02-23", "submitted_at": "2026-02-22T09:00:00", "locked": "2026-02-22T09:00:00", "responses": {"proud_of": mk(4,"Closed a tricky refactor on the auth module"), "stuck_on": mk(2,"Waiting on design review for the settings page"), "need_from_manager": mk(2,"Need a quick sign-off on the component approach"), "target_confidence": mk(4,"Solid progress this sprint"), "feeling_about_work": mk(4,"Good week. Focused and productive"), "safe_to_raise_concerns": mk(5,"Always comfortable speaking up"), "feel_supported": mk(4,"Good team energy"), "workload_manageable": mk(4,"Balanced nicely"), "anything_affecting": mk(1,"")}, "flags_detected": []},
        # SARAH - Week 2
        {"_id": "sub_002", "member_id": "member_001", "date": "2026-03-02", "submitted_at": "2026-03-01T10:00:00", "locked": "2026-03-01T10:00:00", "responses": {"proud_of": mk(5,"Shipped the new search feature ahead of schedule"), "stuck_on": mk(1,"Nothing blocking me"), "need_from_manager": mk(2,"Help prioritising backlog"), "target_confidence": mk(5,"Ahead of targets"), "feeling_about_work": mk(5,"Great week. Energised"), "safe_to_raise_concerns": mk(5,"Spoke up in retro, felt heard"), "feel_supported": mk(5,"Excellent collaboration"), "workload_manageable": mk(4,"Slightly heavier but enjoyable"), "anything_affecting": mk(1,"")}, "flags_detected": []},
        # SARAH - Week 3
        {"_id": "sub_003", "member_id": "member_001", "date": "2026-03-09", "submitted_at": "2026-03-08T09:30:00", "locked": "2026-03-08T09:30:00", "responses": {"proud_of": mk(4,"Mentored Emily on the component library"), "stuck_on": mk(2,"Flaky tests in CI slowing PRs"), "need_from_manager": mk(2,"Second pair of eyes on architecture proposal"), "target_confidence": mk(4,"On track, clear priorities"), "feeling_about_work": mk(4,"Enjoying mentoring alongside delivery"), "safe_to_raise_concerns": mk(5,"Raised concern about deploy schedule, addressed same day"), "feel_supported": mk(5,"Strong team dynamic"), "workload_manageable": mk(4,"Good balance"), "anything_affecting": mk(1,"")}, "flags_detected": []},
        # SARAH - Week 4
        {"_id": "sub_004", "member_id": "member_001", "date": "2026-03-16", "submitted_at": "2026-03-15T08:45:00", "locked": "2026-03-15T08:45:00", "responses": {"proud_of": mk(5,"Led component library migration — finished 2 days early, zero regressions"), "stuck_on": mk(1,"Waiting on design specs, no blockers"), "need_from_manager": mk(1,"Just the architecture review when you have time"), "target_confidence": mk(5,"Smashing it this quarter"), "feeling_about_work": mk(5,"Best week in a while. Everything clicked"), "safe_to_raise_concerns": mk(5,"Love that I can disagree in planning and it's welcomed"), "feel_supported": mk(5,"Team firing on all cylinders"), "workload_manageable": mk(4,"Protected deep work time well"), "anything_affecting": mk(1,"")}, "flags_detected": []},
        # SARAH - Week 5
        {"_id": "sub_005", "member_id": "member_001", "date": "2026-03-23", "submitted_at": "2026-03-22T09:00:00", "locked": "2026-03-22T09:00:00", "responses": {"proud_of": mk(5,"Architecture proposal approved. Starting implementation next sprint"), "stuck_on": mk(1,"Nothing major. Smooth sailing"), "need_from_manager": mk(2,"A quick chat about the tech lead path would be great"), "target_confidence": mk(5,"Well ahead of Q2 targets"), "feeling_about_work": mk(5,"Really enjoying the work. New projects are exciting"), "safe_to_raise_concerns": mk(5,"Always feel comfortable speaking up in our team"), "feel_supported": mk(5,"Great collaboration this sprint"), "workload_manageable": mk(4,"Slightly busy but manageable"), "anything_affecting": mk(1,"")}, "flags_detected": []},
        
        # JAMES - Week 1
        {"_id": "sub_006", "member_id": "member_002", "date": "2026-02-23", "submitted_at": "2026-02-22T11:00:00", "locked": "2026-02-22T11:00:00", "responses": {"proud_of": mk(4,"Shipped the new payment integration"), "stuck_on": mk(2,"Some tech debt slowing things down"), "need_from_manager": mk(2,"Time to address tech debt in Q2"), "target_confidence": mk(4,"Hitting targets"), "feeling_about_work": mk(4,"Positive week. Motivated"), "safe_to_raise_concerns": mk(5,"Great team culture"), "feel_supported": mk(4,"Good support"), "workload_manageable": mk(3,"A bit more than usual but manageable"), "anything_affecting": mk(1,"")}, "flags_detected": []},
        # JAMES - Week 2
        {"_id": "sub_007", "member_id": "member_002", "date": "2026-03-02", "submitted_at": "2026-03-01T14:00:00", "locked": "2026-03-01T14:00:00", "responses": {"proud_of": mk(4,"Closed out database migration tickets"), "stuck_on": mk(3,"On-call interruptions affecting focus"), "need_from_manager": mk(3,"Can we look at the on-call schedule?"), "target_confidence": mk(4,"Still on track but slower"), "feeling_about_work": mk(3,"On-call was disruptive"), "safe_to_raise_concerns": mk(4,"Comfortable raising issues"), "feel_supported": mk(4,"Supportive team"), "workload_manageable": mk(3,"On-call adding up. Two incidents last week"), "anything_affecting": mk(2,"On-call has been rough. Starting to feel it")}, "flags_detected": []},
        # JAMES - Week 3
        {"_id": "sub_008", "member_id": "member_002", "date": "2026-03-09", "submitted_at": "2026-03-08T15:00:00", "locked": "2026-03-08T15:00:00", "responses": {"proud_of": mk(3,"Got through the sprint but it was a grind"), "stuck_on": mk(4,"On-call killed my deep work time again"), "need_from_manager": mk(4,"Seriously need the on-call rotation fixed. Asked twice"), "target_confidence": mk(3,"Falling behind. Hard to focus"), "feeling_about_work": mk(3,"Not great. Tired most of the time"), "safe_to_raise_concerns": mk(4,"Still okay to raise issues"), "feel_supported": mk(3,"Team is heads down on their own stuff"), "workload_manageable": mk(2,"On-call load is unsustainable. I raised this last week"), "anything_affecting": mk(3,"Sleep is suffering because of late-night pages")}, "flags_detected": []},
        # JAMES - Week 4
        {"_id": "sub_009", "member_id": "member_002", "date": "2026-03-16", "submitted_at": "2026-03-15T16:00:00", "locked": "2026-03-15T16:00:00", "responses": {"proud_of": mk(3,"Pushed through API refactor. Took longer than it should"), "stuck_on": mk(4,"Everything takes twice as long. Making careless mistakes"), "need_from_manager": mk(5,"Need breathing room. Workload hasn't changed despite raising it"), "target_confidence": mk(2,"Won't hit sprint goals"), "feeling_about_work": mk(2,"Feeling drained. Struggling to stay motivated"), "safe_to_raise_concerns": mk(3,"Starting to wonder if raising issues makes me look like I can't cope"), "feel_supported": mk(3,"Everyone's too busy to help"), "workload_manageable": mk(1,"I'm drowning. On-call from last month destroyed me"), "anything_affecting": mk(4,"Sleeping badly. Context-switching is exhausting. Something has to change")}, "flags_detected": []},
        # JAMES - Week 5
        {"_id": "sub_010", "member_id": "member_002", "date": "2026-03-23", "submitted_at": "2026-03-22T14:00:00", "locked": "2026-03-22T14:00:00", "responses": {"proud_of": mk(3,"Got the API refactor through code review. That's about it"), "stuck_on": mk(5,"Everything feels like it's taking twice as long. Making silly mistakes"), "need_from_manager": mk(5,"Honestly I don't know. Maybe just some breathing room"), "target_confidence": mk(2,"Really struggling to keep pace"), "feeling_about_work": mk(2,"Not great. Feeling drained and unmotivated"), "safe_to_raise_concerns": mk(3,"Sometimes I wonder if raising issues makes me look weak"), "feel_supported": mk(3,"Team is fine but everyone's heads down"), "workload_manageable": mk(1,"I'm drowning. The on-call rotation really took it out of me"), "anything_affecting": mk(4,"Been sleeping badly. Constant context-switching is exhausting")}, "flags_detected": []},
        
        # PRIYA - Week 1
        {"_id": "sub_011", "member_id": "member_003", "date": "2026-02-23", "submitted_at": "2026-02-22T10:00:00", "locked": "2026-02-22T10:00:00", "responses": {"proud_of": mk(4,"Finished API integration ahead of schedule"), "stuck_on": mk(2,"Waiting on overdue stakeholder feedback"), "need_from_manager": mk(2,"Chase stakeholder feedback"), "target_confidence": mk(4,"On track"), "feeling_about_work": mk(4,"Good week"), "safe_to_raise_concerns": mk(4,"Comfortable speaking up"), "feel_supported": mk(4,"Collaborative team"), "workload_manageable": mk(4,"Balanced"), "anything_affecting": mk(1,"")}, "flags_detected": []},
        # PRIYA - Week 2
        {"_id": "sub_012", "member_id": "member_003", "date": "2026-03-02", "submitted_at": "2026-03-01T11:00:00", "locked": "2026-03-01T11:00:00", "responses": {"proud_of": mk(4,"Delivered the reporting module"), "stuck_on": mk(3,"Late requirement changes caused rework"), "need_from_manager": mk(3,"Earlier visibility on requirement changes"), "target_confidence": mk(4,"On track despite rework"), "feeling_about_work": mk(4,"Frustrating but manageable"), "safe_to_raise_concerns": mk(4,"Generally comfortable"), "feel_supported": mk(3,"Less collaboration this sprint"), "workload_manageable": mk(3,"Rework added extra hours"), "anything_affecting": mk(2,"Noticing decisions being made without team input")}, "flags_detected": []},
        # PRIYA - Week 3
        {"_id": "sub_013", "member_id": "member_003", "date": "2026-03-09", "submitted_at": "2026-03-08T10:30:00", "locked": "2026-03-08T10:30:00", "responses": {"proud_of": mk(4,"Shipped analytics dashboard despite shifting requirements"), "stuck_on": mk(3,"Requirements changed mid-sprint again. Third time in a row"), "need_from_manager": mk(4,"Need to understand how project direction decisions are made"), "target_confidence": mk(3,"Hard to be confident when target keeps moving"), "feeling_about_work": mk(3,"Work is fine but process is frustrating"), "safe_to_raise_concerns": mk(3,"Raised concern about planning process — noted but nothing changed"), "feel_supported": mk(3,"Disconnected from decision-making"), "workload_manageable": mk(3,"Workload okay but rework adds up"), "anything_affecting": mk(2,"ICs aren't consulted before direction changes. It's demoralising")}, "flags_detected": []},
        # PRIYA - Week 4
        {"_id": "sub_014", "member_id": "member_003", "date": "2026-03-16", "submitted_at": "2026-03-15T10:00:00", "locked": "2026-03-15T10:00:00", "responses": {"proud_of": mk(4,"Delivered analytics dashboard despite late changes"), "stuck_on": mk(4,"Built something that got changed last minute. Again"), "need_from_manager": mk(4,"Want to understand how decisions are made. Feels opaque"), "target_confidence": mk(3,"Hard to be confident with constant shifts"), "feeling_about_work": mk(3,"Work is fine but process is really frustrating"), "safe_to_raise_concerns": mk(2,"Raised concern in team meeting and felt dismissed. Not sure my input is valued"), "feel_supported": mk(2,"Feeling isolated. Building things in a vacuum"), "workload_manageable": mk(3,"Workload okay but rework adds up"), "anything_affecting": mk(3,"Team meeting incident really shook me. Need to know my voice matters")}, "flags_detected": []},
        # PRIYA - Week 5
        {"_id": "sub_015", "member_id": "member_003", "date": "2026-03-23", "submitted_at": "2026-03-22T11:30:00", "locked": "2026-03-22T11:30:00", "responses": {"proud_of": mk(4,"Delivered user analytics dashboard on time despite late changes"), "stuck_on": mk(4,"Decisions still being made without consulting the team"), "need_from_manager": mk(4,"Want to understand how decisions are being made. It feels opaque"), "target_confidence": mk(3,"Hard to be confident when requirements keep shifting"), "feeling_about_work": mk(3,"Mixed. Work is fine but process is frustrating"), "safe_to_raise_concerns": mk(2,"Raised a concern last week and felt dismissed"), "feel_supported": mk(2,"Feeling isolated. Building in a vacuum"), "workload_manageable": mk(3,"Workload okay but rework adds up"), "anything_affecting": mk(3,"Team meeting incident shook me. Need to know my voice matters")}, "flags_detected": []},
        
        # MARCUS - Week 1
        {"_id": "sub_016", "member_id": "member_004", "date": "2026-02-23", "submitted_at": "2026-02-22T12:00:00", "locked": "2026-02-22T12:00:00", "responses": {"proud_of": mk(4,"Migrated staging environment to new infrastructure"), "stuck_on": mk(2,"Legacy scripts need updating"), "need_from_manager": mk(2,"Budget approval for monitoring upgrade"), "target_confidence": mk(4,"On track with infra goals"), "feeling_about_work": mk(4,"Good week. Productive"), "safe_to_raise_concerns": mk(4,"Comfortable raising technical concerns"), "feel_supported": mk(4,"Team respects DevOps work"), "workload_manageable": mk(3,"Slightly heavy but manageable"), "anything_affecting": mk(1,"")}, "flags_detected": []},
        # MARCUS - Week 2
        {"_id": "sub_017", "member_id": "member_004", "date": "2026-03-02", "submitted_at": "2026-03-01T13:00:00", "locked": "2026-03-01T13:00:00", "responses": {"proud_of": mk(4,"Production stayed stable through migration"), "stuck_on": mk(3,"I'm the only one who knows the deployment pipeline"), "need_from_manager": mk(3,"Need to start cross-training someone on DevOps"), "target_confidence": mk(4,"On track"), "feeling_about_work": mk(3,"Good technically but noticing bus factor risk"), "safe_to_raise_concerns": mk(4,"Can raise issues"), "feel_supported": mk(3,"Team relies on me but can't help"), "workload_manageable": mk(3,"Getting busier. More incidents"), "anything_affecting": mk(2,"Starting to feel like single point of failure")}, "flags_detected": []},
        # MARCUS - Week 3
        {"_id": "sub_018", "member_id": "member_004", "date": "2026-03-09", "submitted_at": "2026-03-08T14:00:00", "locked": "2026-03-08T14:00:00", "responses": {"proud_of": mk(4,"Handled 3 production incidents and delivered monitoring upgrade"), "stuck_on": mk(4,"Context-switching between incidents and projects killing productivity"), "need_from_manager": mk(4,"Cross-training is urgent. I literally cannot take a day off"), "target_confidence": mk(3,"Delivering but at personal cost"), "feeling_about_work": mk(3,"Pace isn't sustainable"), "safe_to_raise_concerns": mk(4,"Can raise issues but not sure changes happen fast enough"), "feel_supported": mk(3,"Team respects what I do but nobody can back me up"), "workload_manageable": mk(2,"Context-switching is exhausting"), "anything_affecting": mk(3,"Seriously thinking about whether this pace is sustainable")}, "flags_detected": []},
        # MARCUS - Week 4
        {"_id": "sub_019", "member_id": "member_004", "date": "2026-03-16", "submitted_at": "2026-03-15T12:00:00", "locked": "2026-03-15T12:00:00", "responses": {"proud_of": mk(4,"Kept systems running through infrastructure migration"), "stuck_on": mk(5,"Only one who can handle deployment pipeline issues. No backup"), "need_from_manager": mk(5,"Need to cross-train someone NOW. Can't be single point of failure"), "target_confidence": mk(3,"Can deliver if incidents slow down"), "feeling_about_work": mk(3,"Love technical work but firefighting is wearing me down"), "safe_to_raise_concerns": mk(4,"Comfortable raising issues but nothing changes fast enough"), "feel_supported": mk(3,"Nobody can help because they don't know the systems"), "workload_manageable": mk(2,"Context-switching between incidents and projects is exhausting"), "anything_affecting": mk(3,"Starting to think about whether this pace is sustainable long-term")}, "flags_detected": []},
        # MARCUS - Week 5
        {"_id": "sub_020", "member_id": "member_004", "date": "2026-03-23", "submitted_at": "2026-03-22T13:00:00", "locked": "2026-03-22T13:00:00", "responses": {"proud_of": mk(4,"Kept systems running through infrastructure migration"), "stuck_on": mk(5,"Only one who can handle deployment pipeline issues. No backup"), "need_from_manager": mk(5,"Need to cross-train someone NOW. Can't be single point of failure"), "target_confidence": mk(3,"Can deliver if incidents slow down"), "feeling_about_work": mk(3,"Love technical work but firefighting is wearing me down"), "safe_to_raise_concerns": mk(4,"Comfortable raising issues but nothing changes fast enough"), "feel_supported": mk(3,"Nobody can help because they don't know the systems"), "workload_manageable": mk(2,"Context-switching between incidents and projects is exhausting"), "anything_affecting": mk(3,"Starting to think about whether this pace is sustainable long-term")}, "flags_detected": []},
        
        # EMILY - Week 2
        {"_id": "sub_021", "member_id": "member_005", "date": "2026-03-02", "submitted_at": "2026-03-01T09:00:00", "locked": "2026-03-01T09:00:00", "responses": {"proud_of": mk(3,"Completed first code review. Learning the standards"), "stuck_on": mk(3,"Codebase is enormous. Hard to know where things live"), "need_from_manager": mk(3,"More documentation on codebase structure"), "target_confidence": mk(3,"Early days. Building confidence"), "feeling_about_work": mk(3,"Week one done. Overwhelming but exciting"), "safe_to_raise_concerns": mk(4,"Everyone welcoming. No issues"), "feel_supported": mk(4,"Great onboarding"), "workload_manageable": mk(4,"Good pace for new starter"), "anything_affecting": mk(1,"")}, "flags_detected": []},
        # EMILY - Week 3
        {"_id": "sub_022", "member_id": "member_005", "date": "2026-03-09", "submitted_at": "2026-03-08T09:00:00", "locked": "2026-03-08T09:00:00", "responses": {"proud_of": mk(4,"Submitted first PR! Approved with minor comments"), "stuck_on": mk(3,"Still getting used to testing framework"), "need_from_manager": mk(3,"Pairing sessions with seniors would accelerate learning"), "target_confidence": mk(3,"Getting there. More confident each week"), "feeling_about_work": mk(4,"Enjoying the team. Good energy"), "safe_to_raise_concerns": mk(4,"Comfortable asking questions"), "feel_supported": mk(4,"Sarah has been amazing mentor"), "workload_manageable": mk(4,"Good balance"), "anything_affecting": mk(1,"")}, "flags_detected": []},
        # EMILY - Week 4
        {"_id": "sub_023", "member_id": "member_005", "date": "2026-03-16", "submitted_at": "2026-03-15T09:00:00", "locked": "2026-03-15T09:00:00", "responses": {"proud_of": mk(4,"First feature PR merged with minor review comments"), "stuck_on": mk(2,"Getting better at navigating codebase"), "need_from_manager": mk(2,"Weekly pairing with Sarah is incredibly helpful"), "target_confidence": mk(4,"Finding my rhythm"), "feeling_about_work": mk(4,"Enjoying the work. Learning heaps"), "safe_to_raise_concerns": mk(4,"Comfortable asking anything"), "feel_supported": mk(5,"Sarah is a fantastic mentor. Team is very supportive"), "workload_manageable": mk(4,"Good workload for where I'm at"), "anything_affecting": mk(1,"")}, "flags_detected": []},
        # EMILY - Week 5
        {"_id": "sub_024", "member_id": "member_005", "date": "2026-03-23", "submitted_at": "2026-03-23T08:00:00", "locked": "2026-03-23T08:00:00", "responses": {"proud_of": mk(4,"Completed first feature PR! Approved with minor comments"), "stuck_on": mk(3,"Still getting used to the codebase"), "need_from_manager": mk(3,"More pairing sessions would help a lot"), "target_confidence": mk(3,"Still building speed but good trajectory"), "feeling_about_work": mk(4,"Enjoying it! Everyone welcoming"), "safe_to_raise_concerns": mk(4,"Comfortable asking questions. Everyone's patient"), "feel_supported": mk(4,"Great onboarding. Sarah amazing mentor"), "workload_manageable": mk(4,"Good balance"), "anything_affecting": mk(1,"")}, "flags_detected": []},
        
        # DAVID - Week 1
        {"_id": "sub_025", "member_id": "member_006", "date": "2026-02-23", "submitted_at": "2026-02-22T14:00:00", "locked": "2026-02-22T14:00:00", "responses": {"proud_of": mk(4,"Cleared the QA backlog for the release"), "stuck_on": mk(2,"Flaky automated tests need attention"), "need_from_manager": mk(2,"Clarity on QA priorities for next quarter"), "target_confidence": mk(4,"On track"), "feeling_about_work": mk(4,"Fine week"), "safe_to_raise_concerns": mk(4,"No issues"), "feel_supported": mk(4,"Team is fine"), "workload_manageable": mk(4,"Manageable"), "anything_affecting": mk(1,"")}, "flags_detected": []},
        # DAVID - Week 2
        {"_id": "sub_026", "member_id": "member_006", "date": "2026-03-02", "submitted_at": "2026-03-01T16:00:00", "locked": "2026-03-01T16:00:00", "responses": {"proud_of": mk(3,"Ran regression testing for release"), "stuck_on": mk(3,"Automation framework needs upgrade but no one has time"), "need_from_manager": mk(3,"Want to discuss future of QA in team"), "target_confidence": mk(3,"Okay"), "feeling_about_work": mk(3,"Average week"), "safe_to_raise_concerns": mk(3,"Fine"), "feel_supported": mk(3,"Okay"), "workload_manageable": mk(3,"Manageable"), "anything_affecting": mk(1,"")}, "flags_detected": []},
        # DAVID - Week 5
        {"_id": "sub_027", "member_id": "member_006", "date": "2026-03-23", "submitted_at": "2026-03-22T17:00:00", "locked": "2026-03-22T17:00:00", "responses": {"proud_of": mk(2,"Got through the testing queue"), "stuck_on": mk(3,"Same issues as always"), "need_from_manager": mk(2,"Not sure it matters"), "target_confidence": mk(2,"Not confident"), "feeling_about_work": mk(2,"It's fine"), "safe_to_raise_concerns": mk(3,"I guess"), "feel_supported": mk(2,"Don't feel like part of the team lately"), "workload_manageable": mk(3,"It's fine"), "anything_affecting": mk(2,"Don't see the point in raising things that never change")}, "flags_detected": []}
    ],
    "flags": [
        {"_id": "flag_001", "member_id": "member_002", "submission_id": "sub_010", "date": "2026-03-23", "category": "wellbeing", "severity": "action_required", "signal": "Wellbeing score at 2/5 for two consecutive weeks. Reports feeling drained and unmotivated.", "comment_snippet": "Not great. Feeling drained and unmotivated.", "status": "open"},
        {"_id": "flag_002", "member_id": "member_002", "submission_id": "sub_010", "date": "2026-03-23", "category": "workload", "severity": "action_required", "signal": "Workload score at 1/5 (Overwhelmed). Declining from 3→2→1 over four weeks.", "comment_snippet": "I'm drowning. The on-call rotation really took it out of me.", "status": "open"},
        {"_id": "flag_003", "member_id": "member_003", "submission_id": "sub_015", "date": "2026-03-23", "category": "psychological_safety", "severity": "action_required", "signal": "Safe to raise concerns dropped from 4→3→2 over four weeks. Reports feeling dismissed.", "comment_snippet": "Raised a concern last week and felt dismissed.", "status": "open"},
        {"_id": "flag_004", "member_id": "member_003", "submission_id": "sub_014", "date": "2026-03-16", "category": "team_dynamics", "severity": "concern", "signal": "Feel supported dropped to 2/5. Reports feeling isolated and excluded from decisions.", "comment_snippet": "Feeling isolated. Building things in a vacuum.", "status": "open"},
        {"_id": "flag_005", "member_id": "member_004", "submission_id": "sub_020", "date": "2026-03-23", "category": "workload", "severity": "concern", "signal": "Workload score at 2/5 for three consecutive weeks. Single point of failure.", "comment_snippet": "Context-switching between incidents and projects is exhausting.", "status": "open"},
        {"_id": "flag_006", "member_id": "member_006", "submission_id": None, "date": "2026-03-16", "category": "manager_gap", "severity": "action_required", "signal": "Missed 2 consecutive reflections (Mar 9, Mar 16). Potential disengagement.", "comment_snippet": None, "status": "open"},
        {"_id": "flag_007", "member_id": "member_006", "submission_id": "sub_027", "date": "2026-03-23", "category": "engagement", "severity": "concern", "signal": "Responses minimal and declining. 'Don't see the point in raising things.' Withdrawal pattern.", "comment_snippet": "Don't see the point in raising things that never change.", "status": "open"}
    ]
}

async def seed_database():
    """Seed the database with V3 data"""
    print("🌱 Seeding database V3...")
    
    await users_collection.delete_many({})
    await members_collection.delete_many({})
    await submissions_collection.delete_many({})
    await flags_collection.delete_many({})
    print("✅ Cleared existing data")
    
    password_hash = get_password_hash("demo")
    for user in SEED_DATA["users"]:
        user["hashed_password"] = password_hash
    
    if SEED_DATA["users"]:
        await users_collection.insert_many(SEED_DATA["users"])
        print(f"✅ Inserted {len(SEED_DATA['users'])} users")
    
    if SEED_DATA["members"]:
        await members_collection.insert_many(SEED_DATA["members"])
        print(f"✅ Inserted {len(SEED_DATA['members'])} team members")
    
    if SEED_DATA["submissions"]:
        await submissions_collection.insert_many(SEED_DATA["submissions"])
        print(f"✅ Inserted {len(SEED_DATA['submissions'])} weekly submissions (5 weeks per member)")
    
    if SEED_DATA["flags"]:
        await flags_collection.insert_many(SEED_DATA["flags"])
        print(f"✅ Inserted {len(SEED_DATA['flags'])} flags")
    
    print("🎉 Database seeding V3 complete!")
    print(f"📅 Weekly schedule: {len(MONDAY_DATES)} Mondays from Feb 23 to June 29, 2026")
    print(f"📍 Current week: {CURRENT_WEEK}")
    print("\n📧 Demo credentials:")
    print("   Manager: alex@performos.io / demo")
    print("   Team members: sarah@performos.io, james@performos.io, priya@performos.io, marcus@performos.io, emily@performos.io, david@performos.io")
    print("   Password for all: demo\n")

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

# Helper for wellness check-in (updated to use target_confidence)
def wc(mood, energy, target_conf, comments=""):
    mood_scores = {"great": 5, "good": 4, "okay": 3, "stressed": 2, "exhausted": 1}
    return {
        "mood": mood,
        "mood_score": mood_scores[mood],
        "energy_level": energy,
        "target_confidence": target_conf,
        "comments": comments
    }

SEED_DATA = {
    "users": [
        {"_id": "exec_001", "name": "Rachel Kim", "email": "rachel@performos.io", "hashed_password": None, "role": "executive", "title": "VP of Operations", "created_at": datetime(2026, 1, 1)},
        {"_id": "manager_001", "name": "Alex Chen", "email": "alex@performos.io", "hashed_password": None, "role": "manager", "title": "Area Manager", "created_at": datetime(2026, 1, 1)},
        {"_id": "user_001", "name": "Ashley Mitchell", "email": "ashley@performos.io", "hashed_password": None, "role": "team_member", "title": "Loyalty Sales Consultant", "created_at": datetime(2026, 1, 1)},
        {"_id": "user_002", "name": "James Rodriguez", "email": "james@performos.io", "hashed_password": None, "role": "team_member", "title": "Loyalty Sales Consultant", "created_at": datetime(2026, 1, 1)},
        {"_id": "user_003", "name": "Priya Sharma", "email": "priya@performos.io", "hashed_password": None, "role": "team_member", "title": "Loyalty Sales Consultant", "created_at": datetime(2026, 1, 1)},
        {"_id": "user_004", "name": "Marcus Thompson", "email": "marcus@performos.io", "hashed_password": None, "role": "team_member", "title": "Loyalty Sales Consultant", "created_at": datetime(2026, 1, 1)},
        {"_id": "user_005", "name": "Emily Nakamura", "email": "emily@performos.io", "hashed_password": None, "role": "team_member", "title": "Loyalty Sales Consultant", "created_at": datetime(2026, 1, 1)},
        {"_id": "user_006", "name": "David O'Brien", "email": "david@performos.io", "hashed_password": None, "role": "team_member", "title": "Loyalty Sales Consultant", "created_at": datetime(2026, 1, 1)}
    ],
    "members": [
        {"_id": "member_001", "user_id": "user_001", "name": "Ashley Mitchell", "email": "ashley@performos.io", "title": "Loyalty Sales Consultant", "manager_id": "manager_001"},
        {"_id": "member_002", "user_id": "user_002", "name": "James Rodriguez", "email": "james@performos.io", "title": "Loyalty Sales Consultant", "manager_id": "manager_001"},
        {"_id": "member_003", "user_id": "user_003", "name": "Priya Sharma", "email": "priya@performos.io", "title": "Loyalty Sales Consultant", "manager_id": "manager_001"},
        {"_id": "member_004", "user_id": "user_004", "name": "Marcus Thompson", "email": "marcus@performos.io", "title": "Loyalty Sales Consultant", "manager_id": "manager_001"},
        {"_id": "member_005", "user_id": "user_005", "name": "Emily Nakamura", "email": "emily@performos.io", "title": "Loyalty Sales Consultant", "manager_id": "manager_001"},
        {"_id": "member_006", "user_id": "user_006", "name": "David O'Brien", "email": "david@performos.io", "title": "Loyalty Sales Consultant", "manager_id": "manager_001"}
    ],
    "submissions": [
        # ASHLEY - Week 1
        {"_id": "sub_001", "member_id": "member_001", "date": "2026-02-23", "submitted_at": "2026-02-22T09:00:00", "locked": "2026-02-22T09:00:00", "responses": {"proud_of": mk(4,"Closed a tricky refactor on the auth module"), "stuck_on": mk(2,"Waiting on design review for the settings page"), "need_from_manager": mk(2,"Need a quick sign-off on the component approach"), "feeling_about_work": mk(4,"Good week. Focused and productive"), "safe_to_raise_concerns": mk(5,"Always comfortable speaking up")}, "wellness_checkin": wc("great", 8, 5, "Feeling energized and excited about the project!"), "flags_detected": []},
        # ASHLEY - Week 2
        {"_id": "sub_002", "member_id": "member_001", "date": "2026-03-02", "submitted_at": "2026-03-01T10:00:00", "locked": "2026-03-01T10:00:00", "responses": {"proud_of": mk(5,"Shipped the new search feature ahead of schedule"), "stuck_on": mk(1,"Nothing blocking me"), "need_from_manager": mk(2,"Help prioritising backlog"), "feeling_about_work": mk(5,"Great week. Energised"), "safe_to_raise_concerns": mk(5,"Spoke up in retro, felt heard")}, "wellness_checkin": wc("great", 8, 5, "Really proud of shipping early - team collaboration was awesome"), "flags_detected": []},
        # ASHLEY - Week 3
        {"_id": "sub_003", "member_id": "member_001", "date": "2026-03-09", "submitted_at": "2026-03-08T09:30:00", "locked": "2026-03-08T09:30:00", "responses": {"proud_of": mk(4,"Mentored Emily on the component library"), "stuck_on": mk(2,"Flaky tests in CI slowing PRs"), "need_from_manager": mk(2,"Second pair of eyes on architecture proposal"), "feeling_about_work": mk(4,"Enjoying mentoring alongside delivery"), "safe_to_raise_concerns": mk(5,"Raised concern about deploy schedule, addressed same day")}, "wellness_checkin": wc("great", 8, 5, "Loving the mentoring aspect - Emily is doing great!"), "flags_detected": []},
        # ASHLEY - Week 4
        {"_id": "sub_004", "member_id": "member_001", "date": "2026-03-16", "submitted_at": "2026-03-15T08:45:00", "locked": "2026-03-15T08:45:00", "responses": {"proud_of": mk(5,"Led component library migration — finished 2 days early, zero regressions"), "stuck_on": mk(1,"Waiting on design specs, no blockers"), "need_from_manager": mk(1,"Just the architecture review when you have time"), "feeling_about_work": mk(5,"Best week in a while. Everything clicked"), "safe_to_raise_concerns": mk(5,"Love that I can disagree in planning and it's welcomed")}, "wellness_checkin": wc("great", 8, 5, "Everything is clicking - in the zone!"), "flags_detected": []},
        # ASHLEY - Week 5
        {"_id": "sub_005", "member_id": "member_001", "date": "2026-03-23", "submitted_at": "2026-03-22T09:00:00", "locked": "2026-03-22T09:00:00", "responses": {"proud_of": mk(5,"Architecture proposal approved. Starting implementation next sprint"), "stuck_on": mk(1,"Nothing major. Smooth sailing"), "need_from_manager": mk(2,"A quick chat about the tech lead path would be great"), "feeling_about_work": mk(5,"Really enjoying the work. New projects are exciting"), "safe_to_raise_concerns": mk(5,"Always feel comfortable speaking up in our team")}, "wellness_checkin": wc("great", 8, 5, "Excited about the tech lead conversation!"), "flags_detected": []},
        
        # JAMES - Week 1
        {"_id": "sub_006", "member_id": "member_002", "date": "2026-02-23", "submitted_at": "2026-02-22T11:00:00", "locked": "2026-02-22T11:00:00", "responses": {"proud_of": mk(4,"Shipped the new payment integration"), "stuck_on": mk(2,"Some tech debt slowing things down"), "need_from_manager": mk(2,"Time to address tech debt in Q2"), "feeling_about_work": mk(4,"Positive week. Motivated"), "safe_to_raise_concerns": mk(5,"Great team culture")}, "wellness_checkin": wc("good", 7, 4, "Good week overall, workload picking up"), "flags_detected": []},
        # JAMES - Week 2
        {"_id": "sub_007", "member_id": "member_002", "date": "2026-03-02", "submitted_at": "2026-03-01T14:00:00", "locked": "2026-03-01T14:00:00", "responses": {"proud_of": mk(4,"Closed out database migration tickets"), "stuck_on": mk(3,"On-call interruptions affecting focus"), "need_from_manager": mk(3,"Can we look at the on-call schedule?"), "feeling_about_work": mk(3,"On-call was disruptive"), "safe_to_raise_concerns": mk(4,"Comfortable raising issues")}, "wellness_checkin": wc("okay", 5, 3, "On-call is starting to wear on me"), "flags_detected": []},
        # JAMES - Week 3
        {"_id": "sub_008", "member_id": "member_002", "date": "2026-03-09", "submitted_at": "2026-03-08T15:00:00", "locked": "2026-03-08T15:00:00", "responses": {"proud_of": mk(3,"Got through the sprint but it was a grind"), "stuck_on": mk(4,"On-call killed my deep work time again"), "need_from_manager": mk(4,"Seriously need the on-call rotation fixed. Asked twice"), "feeling_about_work": mk(3,"Not great. Tired most of the time"), "safe_to_raise_concerns": mk(4,"Still okay to raise issues")}, "wellness_checkin": wc("stressed", 4, 3, "Really struggling with on-call load"), "flags_detected": []},
        # JAMES - Week 4
        {"_id": "sub_009", "member_id": "member_002", "date": "2026-03-16", "submitted_at": "2026-03-15T16:00:00", "locked": "2026-03-15T16:00:00", "responses": {"proud_of": mk(3,"Pushed through API refactor. Took longer than it should"), "stuck_on": mk(4,"Everything takes twice as long. Making careless mistakes"), "need_from_manager": mk(5,"Need breathing room. Workload hasn't changed despite raising it"), "feeling_about_work": mk(2,"Feeling drained. Struggling to stay motivated"), "safe_to_raise_concerns": mk(3,"Starting to wonder if raising issues makes me look like I can't cope")}, "wellness_checkin": wc("stressed", 3, 2, "Feeling drained, making mistakes"), "flags_detected": []},
        # JAMES - Week 5
        {"_id": "sub_010", "member_id": "member_002", "date": "2026-03-23", "submitted_at": "2026-03-22T14:00:00", "locked": "2026-03-22T14:00:00", "responses": {"proud_of": mk(3,"Got the API refactor through code review. That's about it"), "stuck_on": mk(5,"Everything feels like it's taking twice as long. Making silly mistakes"), "need_from_manager": mk(5,"Honestly I don't know. Maybe just some breathing room"), "feeling_about_work": mk(2,"Not great. Feeling drained and unmotivated"), "safe_to_raise_concerns": mk(3,"Sometimes I wonder if raising issues makes me look weak")}, "wellness_checkin": wc("exhausted", 2, 1, "Completely burned out, need a break"), "flags_detected": []},
        
        # PRIYA - Week 1
        {"_id": "sub_011", "member_id": "member_003", "date": "2026-02-23", "submitted_at": "2026-02-22T10:00:00", "locked": "2026-02-22T10:00:00", "responses": {"proud_of": mk(4,"Finished API integration ahead of schedule"), "stuck_on": mk(2,"Waiting on overdue stakeholder feedback"), "need_from_manager": mk(2,"Chase stakeholder feedback"), "feeling_about_work": mk(4,"Good week"), "safe_to_raise_concerns": mk(4,"Comfortable speaking up")}, "wellness_checkin": wc("okay", 5, 3), "flags_detected": []},
        # PRIYA - Week 2
        {"_id": "sub_012", "member_id": "member_003", "date": "2026-03-02", "submitted_at": "2026-03-01T11:00:00", "locked": "2026-03-01T11:00:00", "responses": {"proud_of": mk(4,"Delivered the reporting module"), "stuck_on": mk(3,"Late requirement changes caused rework"), "need_from_manager": mk(3,"Earlier visibility on requirement changes"), "feeling_about_work": mk(4,"Frustrating but manageable"), "safe_to_raise_concerns": mk(4,"Generally comfortable")}, "wellness_checkin": wc("okay", 5, 3, "Process is frustrating"), "flags_detected": []},
        # PRIYA - Week 3
        {"_id": "sub_013", "member_id": "member_003", "date": "2026-03-09", "submitted_at": "2026-03-08T10:30:00", "locked": "2026-03-08T10:30:00", "responses": {"proud_of": mk(4,"Shipped analytics dashboard despite shifting requirements"), "stuck_on": mk(3,"Requirements changed mid-sprint again. Third time in a row"), "need_from_manager": mk(4,"Need to understand how project direction decisions are made"), "feeling_about_work": mk(3,"Work is fine but process is frustrating"), "safe_to_raise_concerns": mk(3,"Raised concern about planning process — noted but nothing changed")}, "wellness_checkin": wc("okay", 5, 3), "flags_detected": []},
        # PRIYA - Week 4
        {"_id": "sub_014", "member_id": "member_003", "date": "2026-03-16", "submitted_at": "2026-03-15T10:00:00", "locked": "2026-03-15T10:00:00", "responses": {"proud_of": mk(4,"Delivered analytics dashboard despite late changes"), "stuck_on": mk(4,"Built something that got changed last minute. Again"), "need_from_manager": mk(4,"Want to understand how decisions are made. Feels opaque"), "feeling_about_work": mk(3,"Work is fine but process is really frustrating"), "safe_to_raise_concerns": mk(2,"Raised concern in team meeting and felt dismissed. Not sure my input is valued")}, "wellness_checkin": wc("okay", 5, 3, "Feeling dismissed"), "flags_detected": []},
        # PRIYA - Week 5
        {"_id": "sub_015", "member_id": "member_003", "date": "2026-03-23", "submitted_at": "2026-03-22T11:30:00", "locked": "2026-03-22T11:30:00", "responses": {"proud_of": mk(4,"Delivered user analytics dashboard on time despite late changes"), "stuck_on": mk(4,"Decisions still being made without consulting the team"), "need_from_manager": mk(4,"Want to understand how decisions are being made. It feels opaque"), "feeling_about_work": mk(3,"Mixed. Work is fine but process is frustrating"), "safe_to_raise_concerns": mk(2,"Raised a concern last week and felt dismissed")}, "wellness_checkin": wc("okay", 5, 3), "flags_detected": []},
        
        # MARCUS - Week 1
        {"_id": "sub_016", "member_id": "member_004", "date": "2026-02-23", "submitted_at": "2026-02-22T12:00:00", "locked": "2026-02-22T12:00:00", "responses": {"proud_of": mk(4,"Migrated staging environment to new infrastructure"), "stuck_on": mk(2,"Legacy scripts need updating"), "need_from_manager": mk(2,"Budget approval for monitoring upgrade"), "feeling_about_work": mk(4,"Good week. Productive"), "safe_to_raise_concerns": mk(4,"Comfortable raising technical concerns")}, "wellness_checkin": wc("stressed", 4, 2, "Lot of infrastructure work piling up"), "flags_detected": []},
        # MARCUS - Week 2
        {"_id": "sub_017", "member_id": "member_004", "date": "2026-03-02", "submitted_at": "2026-03-01T13:00:00", "locked": "2026-03-01T13:00:00", "responses": {"proud_of": mk(4,"Production stayed stable through migration"), "stuck_on": mk(3,"I'm the only one who knows the deployment pipeline"), "need_from_manager": mk(3,"Need to start cross-training someone on DevOps"), "feeling_about_work": mk(3,"Good technically but noticing bus factor risk"), "safe_to_raise_concerns": mk(4,"Can raise issues")}, "wellness_checkin": wc("stressed", 4, 2, "Too many hats to wear"), "flags_detected": []},
        # MARCUS - Week 3
        {"_id": "sub_018", "member_id": "member_004", "date": "2026-03-09", "submitted_at": "2026-03-08T14:00:00", "locked": "2026-03-08T14:00:00", "responses": {"proud_of": mk(4,"Handled 3 production incidents and delivered monitoring upgrade"), "stuck_on": mk(4,"Context-switching between incidents and projects killing productivity"), "need_from_manager": mk(4,"Cross-training is urgent. I literally cannot take a day off"), "feeling_about_work": mk(3,"Pace isn't sustainable"), "safe_to_raise_concerns": mk(4,"Can raise issues but not sure changes happen fast enough")}, "wellness_checkin": wc("stressed", 4, 2, "Single point of failure"), "flags_detected": []},
        # MARCUS - Week 4
        {"_id": "sub_019", "member_id": "member_004", "date": "2026-03-16", "submitted_at": "2026-03-15T12:00:00", "locked": "2026-03-15T12:00:00", "responses": {"proud_of": mk(4,"Kept systems running through infrastructure migration"), "stuck_on": mk(5,"Only one who can handle deployment pipeline issues. No backup"), "need_from_manager": mk(5,"Need to cross-train someone NOW. Can't be single point of failure"), "feeling_about_work": mk(3,"Love technical work but firefighting is wearing me down"), "safe_to_raise_concerns": mk(4,"Comfortable raising issues but nothing changes fast enough")}, "wellness_checkin": wc("stressed", 4, 2, "Firefighting constantly"), "flags_detected": []},
        # MARCUS - Week 5
        {"_id": "sub_020", "member_id": "member_004", "date": "2026-03-23", "submitted_at": "2026-03-22T13:00:00", "locked": "2026-03-22T13:00:00", "responses": {"proud_of": mk(4,"Kept systems running through infrastructure migration"), "stuck_on": mk(5,"Only one who can handle deployment pipeline issues. No backup"), "need_from_manager": mk(5,"Need to cross-train someone NOW. Can't be single point of failure"), "feeling_about_work": mk(3,"Love technical work but firefighting is wearing me down"), "safe_to_raise_concerns": mk(4,"Comfortable raising issues but nothing changes fast enough")}, "wellness_checkin": wc("stressed", 4, 2, "Need backup urgently"), "flags_detected": []},
        
        # EMILY - Week 2
        {"_id": "sub_021", "member_id": "member_005", "date": "2026-03-02", "submitted_at": "2026-03-01T09:00:00", "locked": "2026-03-01T09:00:00", "responses": {"proud_of": mk(3,"Completed first code review. Learning the standards"), "stuck_on": mk(3,"Codebase is enormous. Hard to know where things live"), "need_from_manager": mk(3,"More documentation on codebase structure"), "feeling_about_work": mk(3,"Week one done. Exciting but challenging"), "safe_to_raise_concerns": mk(4,"Everyone welcoming. No issues")}, "wellness_checkin": wc("okay", 5, 3, "Excited but challenged"), "flags_detected": []},
        # EMILY - Week 3
        {"_id": "sub_022", "member_id": "member_005", "date": "2026-03-09", "submitted_at": "2026-03-08T09:00:00", "locked": "2026-03-08T09:00:00", "responses": {"proud_of": mk(4,"Submitted first PR! Approved with minor comments"), "stuck_on": mk(3,"Still getting used to testing framework"), "need_from_manager": mk(3,"Pairing sessions with seniors would accelerate learning"), "feeling_about_work": mk(4,"Enjoying the team. Good energy"), "safe_to_raise_concerns": mk(4,"Comfortable asking questions")}, "wellness_checkin": wc("okay", 5, 3, "Getting the hang of it"), "flags_detected": []},
        # EMILY - Week 4
        {"_id": "sub_023", "member_id": "member_005", "date": "2026-03-16", "submitted_at": "2026-03-15T09:00:00", "locked": "2026-03-15T09:00:00", "responses": {"proud_of": mk(4,"First feature PR merged with minor review comments"), "stuck_on": mk(2,"Getting better at navigating codebase"), "need_from_manager": mk(2,"Weekly pairing with Sarah is incredibly helpful"), "feeling_about_work": mk(4,"Enjoying the work. Learning heaps"), "safe_to_raise_concerns": mk(4,"Comfortable asking anything")}, "wellness_checkin": wc("good", 6, 4, "Really clicking now!"), "flags_detected": []},
        # EMILY - Week 5
        {"_id": "sub_024", "member_id": "member_005", "date": "2026-03-23", "submitted_at": "2026-03-23T08:00:00", "locked": "2026-03-23T08:00:00", "responses": {"proud_of": mk(4,"Completed first feature PR! Approved with minor comments"), "stuck_on": mk(3,"Still getting used to the codebase"), "need_from_manager": mk(3,"More pairing sessions would help a lot"), "feeling_about_work": mk(4,"Enjoying it! Everyone welcoming"), "safe_to_raise_concerns": mk(4,"Comfortable asking questions. Everyone's patient")}, "wellness_checkin": wc("good", 7, 4, "Loving the team!"), "flags_detected": []},
        
        # DAVID - Week 1
        {"_id": "sub_025", "member_id": "member_006", "date": "2026-02-23", "submitted_at": "2026-02-22T14:00:00", "locked": "2026-02-22T14:00:00", "responses": {"proud_of": mk(4,"Cleared the QA backlog for the release"), "stuck_on": mk(2,"Flaky automated tests need attention"), "need_from_manager": mk(2,"Clarity on QA priorities for next quarter"), "feeling_about_work": mk(4,"Fine week"), "safe_to_raise_concerns": mk(4,"No issues")}, "wellness_checkin": wc("okay", 4, 3), "flags_detected": []},
        # DAVID - Week 2
        {"_id": "sub_026", "member_id": "member_006", "date": "2026-03-02", "submitted_at": "2026-03-01T16:00:00", "locked": "2026-03-01T16:00:00", "responses": {"proud_of": mk(3,"Ran regression testing for release"), "stuck_on": mk(3,"Automation framework needs upgrade but no one has time"), "need_from_manager": mk(3,"Want to discuss future of QA in team"), "feeling_about_work": mk(3,"Average week"), "safe_to_raise_concerns": mk(3,"Fine")}, "wellness_checkin": wc("okay", 4, 3), "flags_detected": []},
        # DAVID - Week 5
        {"_id": "sub_027", "member_id": "member_006", "date": "2026-03-23", "submitted_at": "2026-03-22T17:00:00", "locked": "2026-03-22T17:00:00", "responses": {"proud_of": mk(2,"Got through the testing queue"), "stuck_on": mk(3,"Same issues as always"), "need_from_manager": mk(2,"Not sure it matters"), "feeling_about_work": mk(2,"It's fine"), "safe_to_raise_concerns": mk(3,"I guess")}, "wellness_checkin": wc("okay", 4, 2, "Don't see the point in raising things that never change"), "flags_detected": []}
    ],
    "flags": [
        {"_id": "flag_001", "member_id": "member_002", "submission_id": "sub_010", "date": "2026-03-23", "category": "wellbeing", "severity": "action_required", "signal": "Wellbeing score at 2/5 for two consecutive weeks. Reports feeling drained and unmotivated.", "comment_snippet": "Not great. Feeling drained and unmotivated.", "status": "in_progress", "actions": [
            {
                "id": "action_001",
                "note": "Removed James from on-call rotation for 4 weeks. Communicated to team.",
                "savedAt": "2026-03-22T14:30:00Z",
                "confirmed": True
            }
        ]},
        {"_id": "flag_002", "member_id": "member_002", "submission_id": "sub_010", "date": "2026-03-23", "category": "performance", "severity": "action_required", "signal": "Target confidence at 1/5 (behind on targets). Declining from 4→3→2→1 over five weeks.", "comment_snippet": "Completely burned out, need a break", "status": "open", "actions": []},
        {"_id": "flag_003", "member_id": "member_003", "submission_id": "sub_015", "date": "2026-03-23", "category": "psychological_safety", "severity": "action_required", "signal": "Speaking up score dropped from 4→3→2 over four weeks. Reports feeling dismissed.", "comment_snippet": "Raised a concern last week and felt dismissed.", "status": "open", "actions": []},
        {"_id": "flag_005", "member_id": "member_004", "submission_id": "sub_020", "date": "2026-03-23", "category": "performance", "severity": "concern", "signal": "Target confidence at 2/5 for four consecutive weeks. Single point of failure.", "comment_snippet": "Need backup urgently", "status": "in_progress", "actions": [
            {
                "id": "action_002",
                "note": "Identified Sarah as DevOps cross-training candidate. Starting next sprint.",
                "savedAt": "2026-03-18T10:00:00Z",
                "confirmed": True
            },
            {
                "id": "action_003",
                "note": "Reassigned 2 non-urgent infrastructure tickets to reduce queue.",
                "savedAt": "2026-03-20T14:30:00Z",
                "confirmed": True
            }
        ]},
        {"_id": "flag_006", "member_id": "member_006", "submission_id": None, "date": "2026-03-16", "category": "manager_gap", "severity": "action_required", "signal": "Missed 2 consecutive reflections (Mar 9, Mar 16). Potential disengagement.", "comment_snippet": None, "status": "open", "actions": []},
        {"_id": "flag_007", "member_id": "member_006", "submission_id": "sub_027", "date": "2026-03-23", "category": "engagement", "severity": "concern", "signal": "Responses minimal and declining. 'Don't see the point in raising things.' Withdrawal pattern.", "comment_snippet": "Don't see the point in raising things that never change.", "status": "open", "actions": []}
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
    print("   Executive: rachel@performos.io / demo")
    print("   Manager: alex@performos.io / demo")
    print("   Team members: ashley@performos.io, james@performos.io, priya@performos.io, marcus@performos.io, emily@performos.io, david@performos.io")
    print("   Password for all: demo\n")

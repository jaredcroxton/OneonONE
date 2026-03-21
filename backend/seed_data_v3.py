from datetime import datetime
from database import users_collection, members_collection, submissions_collection, flags_collection
from auth import get_password_hash

# Generate Monday dates from Feb 23 to June 29, 2026
def generate_mondays():
    from datetime import datetime, timedelta
    mondays = []
    d = datetime(2026, 2, 23)  # Start from Feb 23 instead of March 23
    end = datetime(2026, 6, 29)
    while d <= end:
        mondays.append(d.strftime("%Y-%m-%d"))
        d += timedelta(days=7)
    return mondays

MONDAY_DATES = generate_mondays()
CURRENT_WEEK = "2026-03-23"  # Current week for demo

# Helper to create response object
def mk_response(rating, comment):
    return {"rating": rating, "comment": comment}

# Seed data with 5 weeks of submissions for each team member
SEED_DATA = {
    "users": [
        {
            "_id": "manager_001",
            "name": "Alex Chen",
            "email": "alex@performos.io",
            "hashed_password": None,
            "role": "manager",
            "title": "Engineering Manager",
            "created_at": datetime(2026, 1, 1)
        },
        {
            "_id": "user_001",
            "name": "Sarah Mitchell",
            "email": "sarah@performos.io",
            "hashed_password": None,
            "role": "team_member",
            "title": "Senior Frontend Engineer",
            "created_at": datetime(2026, 1, 1)
        },
        {
            "_id": "user_002",
            "name": "James Rodriguez",
            "email": "james@performos.io",
            "hashed_password": None,
            "role": "team_member",
            "title": "Backend Engineer",
            "created_at": datetime(2026, 1, 1)
        },
        {
            "_id": "user_003",
            "name": "Priya Sharma",
            "email": "priya@performos.io",
            "hashed_password": None,
            "role": "team_member",
            "title": "Full Stack Engineer",
            "created_at": datetime(2026, 1, 1)
        },
        {
            "_id": "user_004",
            "name": "Marcus Thompson",
            "email": "marcus@performos.io",
            "hashed_password": None,
            "role": "team_member",
            "title": "DevOps Engineer",
            "created_at": datetime(2026, 1, 1)
        },
        {
            "_id": "user_005",
            "name": "Emily Nakamura",
            "email": "emily@performos.io",
            "hashed_password": None,
            "role": "team_member",
            "title": "Junior Engineer",
            "created_at": datetime(2026, 1, 1)
        },
        {
            "_id": "user_006",
            "name": "David O'Brien",
            "email": "david@performos.io",
            "hashed_password": None,
            "role": "team_member",
            "title": "QA Engineer",
            "created_at": datetime(2026, 1, 1)
        }
    ],
    "members": [
        {
            "_id": "member_001",
            "user_id": "user_001",
            "name": "Sarah Mitchell",
            "email": "sarah@performos.io",
            "title": "Senior Frontend Engineer",
            "manager_id": "manager_001"
        },
        {
            "_id": "member_002",
            "user_id": "user_002",
            "name": "James Rodriguez",
            "email": "james@performos.io",
            "title": "Backend Engineer",
            "manager_id": "manager_001"
        },
        {
            "_id": "member_003",
            "user_id": "user_003",
            "name": "Priya Sharma",
            "email": "priya@performos.io",
            "title": "Full Stack Engineer",
            "manager_id": "manager_001"
        },
        {
            "_id": "member_004",
            "user_id": "user_004",
            "name": "Marcus Thompson",
            "email": "marcus@performos.io",
            "title": "DevOps Engineer",
            "manager_id": "manager_001"
        },
        {
            "_id": "member_005",
            "user_id": "user_005",
            "name": "Emily Nakamura",
            "email": "emily@performos.io",
            "title": "Junior Engineer",
            "manager_id": "manager_001"
        },
        {
            "_id": "member_006",
            "user_id": "user_006",
            "name": "David O'Brien",
            "email": "david@performos.io",
            "title": "QA Engineer",
            "manager_id": "manager_001"
        }
    ],
    "submissions": []  # Will be populated below
}

# SARAH MITCHELL - Consistently strong (4s and 5s), no flags
sarah_submissions = [
    # Week 1: Feb 23
    {
        "_id": "sub_sarah_1",
        "member_id": "member_001",
        "date": "2026-02-23",
        "submitted_at": "2026-02-22T09:00:00",
        "responses": {
            "proud_of": mk_response(4, "Closed a tricky refactor on the auth module."),
            "stuck_on": mk_response(2, "Waiting on design review for the settings page."),
            "need_from_manager": mk_response(2, "Need a quick sign-off on the component approach."),
            "target_confidence": mk_response(4, "Solid progress this sprint. On track."),
            "feeling_about_work": mk_response(4, "Good week. Focused and productive."),
            "safe_to_raise_concerns": mk_response(5, "Always comfortable speaking up here."),
            "feel_supported": mk_response(4, "Good team energy this sprint."),
            "workload_manageable": mk_response(4, "Balanced nicely between deep work and meetings."),
            "anything_affecting": mk_response(1, "")
        },
        "flags_detected": []
    },
    # Week 2: Mar 2
    {
        "_id": "sub_sarah_2",
        "member_id": "member_001",
        "date": "2026-03-02",
        "submitted_at": "2026-03-01T10:00:00",
        "responses": {
            "proud_of": mk_response(5, "Shipped the new search feature ahead of schedule. Really proud of this one."),
            "stuck_on": mk_response(1, "Nothing blocking me right now."),
            "need_from_manager": mk_response(2, "Help prioritising the backlog — a few competing requests."),
            "target_confidence": mk_response(5, "Ahead of targets. Feeling confident."),
            "feeling_about_work": mk_response(5, "Great week. Energised by the new projects."),
            "safe_to_raise_concerns": mk_response(5, "Spoke up in retro about process issues, felt heard."),
            "feel_supported": mk_response(5, "Team collaboration was excellent this sprint."),
            "workload_manageable": mk_response(4, "Slightly heavier week but I enjoyed it."),
            "anything_affecting": mk_response(1, "")
        },
        "flags_detected": []
    },
    # Week 3: Mar 9
    {
        "_id": "sub_sarah_3",
        "member_id": "member_001",
        "date": "2026-03-09",
        "submitted_at": "2026-03-08T09:30:00",
        "responses": {
            "proud_of": mk_response(4, "Mentored Emily on the component library. She's picking it up fast."),
            "stuck_on": mk_response(2, "Some flaky tests in the CI pipeline slowing down PRs."),
            "need_from_manager": mk_response(2, "Could use a second pair of eyes on the architecture proposal."),
            "target_confidence": mk_response(4, "On track. Clear priorities this sprint."),
            "feeling_about_work": mk_response(4, "Enjoying the mentoring work alongside feature delivery."),
            "safe_to_raise_concerns": mk_response(5, "Raised a concern about the deploy schedule and it was addressed same day."),
            "feel_supported": mk_response(5, "Strong team dynamic right now."),
            "workload_manageable": mk_response(4, "Good balance this week."),
            "anything_affecting": mk_response(1, "")
        },
        "flags_detected": []
    },
    # Week 4: Mar 16
    {
        "_id": "sub_sarah_4",
        "member_id": "member_001",
        "date": "2026-03-16",
        "submitted_at": "2026-03-15T08:45:00",
        "responses": {
            "proud_of": mk_response(5, "Led the component library migration — finished 2 days early with zero regressions."),
            "stuck_on": mk_response(1, "Waiting on design specs for the dashboard refresh. No blockers though."),
            "need_from_manager": mk_response(1, "All good. Just the architecture review when you have time."),
            "target_confidence": mk_response(5, "Smashing it this quarter. Very confident in Q2 targets."),
            "feeling_about_work": mk_response(5, "Best week in a while. Everything clicked."),
            "safe_to_raise_concerns": mk_response(5, "Love that I can disagree in planning and it's welcomed."),
            "feel_supported": mk_response(5, "Team is firing on all cylinders."),
            "workload_manageable": mk_response(4, "Managed to protect deep work time well."),
            "anything_affecting": mk_response(1, "")
        },
        "flags_detected": []
    },
    # Week 5: Mar 23 (CURRENT)
    {
        "_id": "sub_sarah_5",
        "member_id": "member_001",
        "date": "2026-03-23",
        "submitted_at": "2026-03-22T09:00:00",
        "responses": {
            "proud_of": mk_response(5, "Architecture proposal approved. Starting implementation next sprint."),
            "stuck_on": mk_response(1, "Nothing major. Smooth sailing."),
            "need_from_manager": mk_response(2, "A quick chat about the tech lead path would be great."),
            "target_confidence": mk_response(5, "Well ahead of Q2 targets."),
            "feeling_about_work": mk_response(5, "Really enjoying the work. New projects are exciting."),
            "safe_to_raise_concerns": mk_response(5, "Always feel comfortable speaking up in our team."),
            "feel_supported": mk_response(5, "Great collaboration with the team this sprint."),
            "workload_manageable": mk_response(4, "Slightly busy but manageable. Good balance."),
            "anything_affecting": mk_response(1, "")
        },
        "flags_detected": []
    }
]

# JAM

ES RODRIGUEZ - Declining burnout arc (4→3→2→1)
james_submissions = [
    # Week 1: Feb 23
    {
        "_id": "sub_james_1",
        "member_id": "member_002",
        "date": "2026-02-23",
        "submitted_at": "2026-02-22T11:00:00",
        "responses": {
            "proud_of": mk_response(4, "Shipped the new payment integration. Clean implementation."),
            "stuck_on": mk_response(2, "Some tech debt in the codebase slowing things down."),
            "need_from_manager": mk_response(2, "Time to address tech debt in Q2 planning."),
            "target_confidence": mk_response(4, "Good progress. Hitting targets."),
            "feeling_about_work": mk_response(4, "Positive week. Motivated and focused."),
            "safe_to_raise_concerns": mk_response(5, "No issues at all. Great team culture."),
            "feel_supported": mk_response(4, "Good support from the team."),
            "workload_manageable": mk_response(3, "A bit more than usual but nothing I can't handle."),
            "anything_affecting": mk_response(1, "")
        },
        "flags_detected": []
    },
    # Week 2: Mar 2 (starting to decline)
    {
        "_id": "sub_james_2",
        "member_id": "member_002",
        "date": "2026-03-02",
        "submitted_at": "2026-03-01T14:00:00",
        "responses": {
            "proud_of": mk_response(4, "Closed out the database migration tickets."),
            "stuck_on": mk_response(3, "The on-call interruptions are starting to affect my focus time."),
            "need_from_manager": mk_response(3, "Can we look at the on-call schedule? It's getting heavy."),
            "target_confidence": mk_response(4, "Still on track but pace is slower."),
            "feeling_about_work": mk_response(3, "Okay week. On-call was disruptive though."),
            "safe_to_raise_concerns": mk_response(4, "Comfortable raising issues."),
            "feel_supported": mk_response(4, "Team is supportive."),
            "workload_manageable": mk_response(3, "On-call is adding up. Two incidents last week."),
            "anything_affecting": mk_response(2, "On-call has been rough. Starting to feel it.")
        },
        "flags_detected": []
    },
    # Week 3: Mar 9 (decline continues)
    {
        "_id": "sub_james_3",
        "member_id": "member_002",
        "date": "2026-03-09",
        "submitted_at": "2026-03-08T15:00:00",
        "responses": {
            "proud_of": mk_response(3, "Got through the sprint but it was a grind."),
            "stuck_on": mk_response(4, "On-call interruptions killed my deep work time again."),
            "need_from_manager": mk_response(4, "Seriously need the on-call rotation fixed. I've asked twice."),
            "target_confidence": mk_response(3, "Falling behind. Hard to focus."),
            "feeling_about_work": mk_response(3, "Not great. Tired most of the time."),
            "safe_to_raise_concerns": mk_response(4, "Still okay to raise issues."),
            "feel_supported": mk_response(3, "Team is heads down on their own stuff. Less collaboration."),
            "workload_manageable": mk_response(2, "The on-call load is unsustainable. I raised this last week."),
            "anything_affecting": mk_response(3, "Sleep is suffering because of the late-night pages.")
        },
        "flags_detected": []
    },
    # Week 4: Mar 16 (serious decline)
    {
        "_id": "sub_james_4",
        "member_id": "member_002",
        "date": "2026-03-16",
        "submitted_at": "2026-03-15T16:00:00",
        "responses": {
            "proud_of": mk_response(3, "Pushed through the API refactor. Took longer than it should have."),
            "stuck_on": mk_response(4, "Everything takes twice as long now. Making careless mistakes."),
            "need_from_manager": mk_response(5, "I need breathing room. The workload hasn't changed despite me raising it."),
            "target_confidence": mk_response(2, "Don't think I'll hit sprint goals."),
            "feeling_about_work": mk_response(2, "Feeling drained. Struggling to stay motivated."),
            "safe_to_raise_concerns": mk_response(3, "Starting to wonder if raising issues makes me look like I can't cope."),
            "feel_supported": mk_response(3, "Everyone's too busy to help."),
            "workload_manageable": mk_response(1, "I'm drowning. The on-call from last month destroyed me and I haven't recovered."),
            "anything_affecting": mk_response(4, "Sleeping badly. Constant context-switching is exhausting. Something has to change.")
        },
        "flags_detected": []
    },
    # Week 5: Mar 23 (CURRENT - crisis)
    {
        "_id": "sub_james_5",
        "member_id": "member_002",
        "date": "2026-03-23",
        "submitted_at": "2026-03-22T14:00:00",
        "responses": {
            "proud_of": mk_response(3, "Got the API refactor through code review. That's about it."),
            "stuck_on": mk_response(5, "Everything feels like it's taking twice as long. I'm making silly mistakes."),
            "need_from_manager": mk_response(5, "Honestly, I don't know. Maybe just some breathing room."),
            "target_confidence": mk_response(2, "Really struggling to keep pace."),
            "feeling_about_work": mk_response(2, "Not great. Feeling drained and unmotivated."),
            "safe_to_raise_concerns": mk_response(3, "Sometimes I wonder if raising issues just makes me look weak."),
            "feel_supported": mk_response(3, "Team is fine but everyone's heads down on their own stuff."),
            "workload_manageable": mk_response(1, "I'm drowning. The on-call rotation last month really took it out of me."),
            "anything_affecting": mk_response(4, "I've been sleeping badly and it's catching up with me. The constant context-switching is exhausting.")
        },
        "flags_detected": []
    }
]

# Add all submissions
SEED_DATA["submissions"].extend(sarah_submissions)
SEED_DATA["submissions"].extend(james_submissions)

# FLAGS
SEED_DATA["flags"] = [
    {
        "_id": "flag_001",
        "member_id": "member_002",
        "submission_id": "sub_james_5",
        "date": "2026-03-23",
        "category": "wellbeing",
        "severity": "action_required",
        "signal": "Wellbeing score at 2/5 for two consecutive weeks. Reports feeling drained and unmotivated.",
        "comment_snippet": "Not great. Feeling drained and unmotivated.",
        "status": "open"
    },
    {
        "_id": "flag_002",
        "member_id": "member_002",
        "submission_id": "sub_james_5",
        "date": "2026-03-23",
        "category": "workload",
        "severity": "action_required",
        "signal": "Workload score at 1/5 (Overwhelmed). Declining from 3→2→1 over three weeks.",
        "comment_snippet": "I'm drowning. The on-call rotation last month really took it out of me.",
        "status": "open"
    }
]


async def seed_database():
    """Seed the database with initial data"""
    print("🌱 Seeding database V3...")
    
    # Clear existing data
    await users_collection.delete_many({})
    await members_collection.delete_many({})
    await submissions_collection.delete_many({})
    await flags_collection.delete_many({})
    print("✅ Cleared existing data")
    
    # Hash passwords for all users
    password_hash = get_password_hash("demo")
    for user in SEED_DATA["users"]:
        user["hashed_password"] = password_hash
    
    # Insert users
    if SEED_DATA["users"]:
        await users_collection.insert_many(SEED_DATA["users"])
        print(f"✅ Inserted {len(SEED_DATA['users'])} users")
    
    # Insert members
    if SEED_DATA["members"]:
        await members_collection.insert_many(SEED_DATA["members"])
        print(f"✅ Inserted {len(SEED_DATA['members'])} team members")
    
    # Insert submissions
    if SEED_DATA["submissions"]:
        await submissions_collection.insert_many(SEED_DATA["submissions"])
        print(f"✅ Inserted {len(SEED_DATA['submissions'])} weekly submissions (5 weeks per member)")
    
    # Insert flags
    if SEED_DATA["flags"]:
        await flags_collection.insert_many(SEED_DATA["flags"])
        print(f"✅ Inserted {len(SEED_DATA['flags'])} flags")
    
    print("🎉 Database seeding V3 complete!")
    print(f"📅 Weekly schedule: {len(MONDAY_DATES)} Mondays from Feb 23 to June 29, 2026")
    print(f"📍 Current week: {CURRENT_WEEK}")
    print("\n📧 Demo credentials:")
    print("   Manager: alex@performos.io / demo")
    print("   Team members: sarah@performos.io, james@performos.io (all: demo)\n")

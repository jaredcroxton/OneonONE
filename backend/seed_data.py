from datetime import datetime
from database import users_collection, members_collection, submissions_collection, flags_collection
from auth import get_password_hash

# Generate Monday dates from March 23 to June 29, 2026
def generate_mondays():
    from datetime import datetime, timedelta
    mondays = []
    d = datetime(2026, 3, 23)
    end = datetime(2026, 6, 29)
    while d <= end:
        mondays.append(d.strftime("%Y-%m-%d"))
        d += timedelta(days=7)
    return mondays

MONDAY_DATES = generate_mondays()

# Seed data with new structure
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
    "submissions": [
        # Sarah - Week of March 23 (THIS WEEK) - Good submission
        {
            "_id": "sub_001",
            "member_id": "member_001",
            "date": "2026-03-23",
            "submitted_at": "2026-03-22T09:00:00",
            "responses": {
                "proud_of": {"rating": 5, "comment": "Led the migration to the new component library — finished 2 days early with zero regressions."},
                "stuck_on": {"rating": 1, "comment": "Nothing major. Waiting on design specs for the dashboard refresh."},
                "need_from_manager": {"rating": 2, "comment": "Just a quick review of my architecture proposal when you get a chance."},
                "target_confidence": {"rating": 5, "comment": "Feeling great about Q2 targets. We're ahead of schedule."},
                "feeling_about_work": {"rating": 5, "comment": "Really enjoying the work right now. The new projects are exciting."},
                "safe_to_raise_concerns": {"rating": 5, "comment": "Always feel comfortable speaking up in our team."},
                "feel_supported": {"rating": 5, "comment": "Great collaboration with the team this sprint."},
                "workload_manageable": {"rating": 4, "comment": "Slightly busy but manageable. Good balance."},
                "anything_affecting": {"rating": 1, "comment": ""}
            },
            "flags_detected": []
        },
        # James - Week of March 23 (THIS WEEK) - Burnout signals
        {
            "_id": "sub_002",
            "member_id": "member_002",
            "date": "2026-03-23",
            "submitted_at": "2026-03-22T14:00:00",
            "responses": {
                "proud_of": {"rating": 3, "comment": "Got the API refactor through code review."},
                "stuck_on": {"rating": 5, "comment": "Everything feels like it's taking twice as long. I'm making silly mistakes."},
                "need_from_manager": {"rating": 5, "comment": "Honestly, I don't know. Maybe just some breathing room."},
                "target_confidence": {"rating": 2, "comment": "Really struggling to keep pace. Don't think I'll hit the sprint goals."},
                "feeling_about_work": {"rating": 2, "comment": "Not great. Feeling drained and unmotivated."},
                "safe_to_raise_concerns": {"rating": 3, "comment": "Sometimes I wonder if raising issues just makes me look like I can't cope."},
                "feel_supported": {"rating": 3, "comment": "Team is fine but everyone's heads down on their own stuff."},
                "workload_manageable": {"rating": 1, "comment": "I'm drowning. The on-call rotation last month really took it out of me and I haven't recovered."},
                "anything_affecting": {"rating": 4, "comment": "I've been sleeping badly and it's catching up with me. The constant context-switching is exhausting."}
            },
            "flags_detected": []
        },
        # Priya - Week of March 23 (THIS WEEK) - Psych safety concerns
        {
            "_id": "sub_003",
            "member_id": "member_003",
            "date": "2026-03-23",
            "submitted_at": "2026-03-22T11:30:00",
            "responses": {
                "proud_of": {"rating": 4, "comment": "Delivered the user analytics dashboard on time."},
                "stuck_on": {"rating": 4, "comment": "Some decisions are being made without consulting the team. I built something that got changed last minute."},
                "need_from_manager": {"rating": 4, "comment": "I'd like to understand how decisions are being made about project direction. It feels opaque."},
                "target_confidence": {"rating": 3, "comment": "Hard to be confident when requirements keep shifting."},
                "feeling_about_work": {"rating": 3, "comment": "Mixed. The work itself is fine but the process is frustrating."},
                "safe_to_raise_concerns": {"rating": 2, "comment": "I raised a concern in the team meeting last week and felt like it was dismissed. Not sure my input is valued."},
                "feel_supported": {"rating": 2, "comment": "Feeling a bit isolated. Like I'm building things in a vacuum."},
                "workload_manageable": {"rating": 3, "comment": "Workload is okay but the rework from changing requirements adds up."},
                "anything_affecting": {"rating": 3, "comment": "The team meeting incident really shook me. I need to know my voice matters."}
            },
            "flags_detected": []
        },
        # Marcus - Week of March 23 (THIS WEEK) - Workload issues
        {
            "_id": "sub_004",
            "member_id": "member_004",
            "date": "2026-03-23",
            "submitted_at": "2026-03-22T16:00:00",
            "responses": {
                "proud_of": {"rating": 4, "comment": "Kept all systems running through the infrastructure migration."},
                "stuck_on": {"rating": 5, "comment": "I'm the only one who can handle the deployment pipeline issues. There's no backup."},
                "need_from_manager": {"rating": 5, "comment": "We need to cross-train someone on the deployment pipeline. I can't be the single point of failure."},
                "target_confidence": {"rating": 3, "comment": "Can deliver if the incidents slow down, but that's not in my control."},
                "feeling_about_work": {"rating": 3, "comment": "I love the technical work but the constant firefighting is wearing me down."},
                "safe_to_raise_concerns": {"rating": 4, "comment": "Feel comfortable raising issues, just not sure anything changes fast enough."},
                "feel_supported": {"rating": 3, "comment": "Team respects what I do but nobody can help because they don't know the systems."},
                "workload_manageable": {"rating": 2, "comment": "The constant context-switching between incidents and project work is exhausting. I can't do either well."},
                "anything_affecting": {"rating": 3, "comment": "Starting to think about whether this pace is sustainable long-term."}
            },
            "flags_detected": []
        },
        # Emily - Week of March 23 (THIS WEEK) - New, positive
        {
            "_id": "sub_005",
            "member_id": "member_005",
            "date": "2026-03-23",
            "submitted_at": "2026-03-23T08:00:00",
            "responses": {
                "proud_of": {"rating": 4, "comment": "Completed my first feature PR! It got approved with minor comments."},
                "stuck_on": {"rating": 3, "comment": "Still getting used to the codebase. It's big and I don't always know where to look."},
                "need_from_manager": {"rating": 3, "comment": "More pairing sessions with senior devs would help a lot."},
                "target_confidence": {"rating": 3, "comment": "Getting there. Still building up speed but feeling good about the trajectory."},
                "feeling_about_work": {"rating": 4, "comment": "Enjoying it! Everyone has been really welcoming."},
                "safe_to_raise_concerns": {"rating": 4, "comment": "Feel comfortable asking questions. Everyone's been patient."},
                "feel_supported": {"rating": 4, "comment": "Great onboarding experience. Sarah has been an amazing mentor."},
                "workload_manageable": {"rating": 4, "comment": "Good balance for now. Not overwhelmed."},
                "anything_affecting": {"rating": 1, "comment": ""}
            },
            "flags_detected": []
        }
        # David - NO SUBMISSION for March 23 (manager gap flag)
    ],
    "flags": [
        {
            "_id": "flag_001",
            "member_id": "member_002",
            "submission_id": "sub_002",
            "date": "2026-03-23",
            "category": "wellbeing",
            "severity": "action_required",
            "signal": "Wellbeing score at 2/5. Reports feeling drained and unmotivated.",
            "comment_snippet": "Not great. Feeling drained and unmotivated.",
            "status": "open"
        },
        {
            "_id": "flag_002",
            "member_id": "member_002",
            "submission_id": "sub_002",
            "date": "2026-03-23",
            "category": "workload",
            "severity": "action_required",
            "signal": "Workload score at 1/5 (Overwhelmed). Reports drowning and poor sleep.",
            "comment_snippet": "I'm drowning. The on-call rotation last month really took it out of me and I haven't recovered.",
            "status": "open"
        },
        {
            "_id": "flag_003",
            "member_id": "member_003",
            "submission_id": "sub_003",
            "date": "2026-03-23",
            "category": "psychological_safety",
            "severity": "action_required",
            "signal": "Safe to raise concerns score at 2/5. Reports feeling dismissed in team meetings.",
            "comment_snippet": "I raised a concern in the team meeting last week and felt like it was dismissed. Not sure my input is valued.",
            "status": "open"
        },
        {
            "_id": "flag_004",
            "member_id": "member_003",
            "submission_id": "sub_003",
            "date": "2026-03-23",
            "category": "team_dynamics",
            "severity": "concern",
            "signal": "Feel supported score at 2/5. Reports feeling isolated.",
            "comment_snippet": "Feeling a bit isolated. Like I'm building things in a vacuum.",
            "status": "open"
        },
        {
            "_id": "flag_005",
            "member_id": "member_004",
            "submission_id": "sub_004",
            "date": "2026-03-23",
            "category": "workload",
            "severity": "concern",
            "signal": "Workload score at 2/5. Single point of failure on deployment pipeline.",
            "comment_snippet": "The constant context-switching between incidents and project work is exhausting. I can't do either well.",
            "status": "open"
        },
        {
            "_id": "flag_006",
            "member_id": "member_006",
            "submission_id": None,
            "date": "2026-03-23",
            "category": "manager_gap",
            "severity": "action_required",
            "signal": "No submission received for this week. Potential disengagement.",
            "comment_snippet": None,
            "status": "open"
        }
    ]
}


async def seed_database():
    """Seed the database with initial data"""
    print("🌱 Seeding database...")
    
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
        print(f"✅ Inserted {len(SEED_DATA['submissions'])} weekly submissions")
    
    # Insert flags
    if SEED_DATA["flags"]:
        await flags_collection.insert_many(SEED_DATA["flags"])
        print(f"✅ Inserted {len(SEED_DATA['flags'])} flags")
    
    print("🎉 Database seeding complete!")
    print(f"📅 Weekly schedule: {len(MONDAY_DATES)} Mondays from March 23 to June 29, 2026")
    print("\n📧 Demo credentials:")
    print("   Manager: alex@performos.io / demo")
    print("   Team members: sarah@performos.io, james@performos.io, priya@performos.io (all: demo)\n")

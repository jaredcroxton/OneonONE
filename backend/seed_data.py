from datetime import datetime
from database import users_collection, members_collection, sessions_collection, flags_collection
from auth import get_password_hash

# Seed data matching the reference component
SEED_DATA = {
    "users": [
        {
            "_id": "manager_001",
            "name": "Alex Chen",
            "email": "alex@performos.io",
            "hashed_password": None,  # Will be set to hash of "demo"
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
            "manager_id": "manager_001",
            "cadence": "fortnightly",
            "next_session": "2026-04-02",
            "last_session": "2026-03-19",
            "avatar": "SM"
        },
        {
            "_id": "member_002",
            "user_id": "user_002",
            "name": "James Rodriguez",
            "email": "james@performos.io",
            "title": "Backend Engineer",
            "manager_id": "manager_001",
            "cadence": "weekly",
            "next_session": "2026-03-28",
            "last_session": "2026-03-21",
            "avatar": "JR"
        },
        {
            "_id": "member_003",
            "user_id": "user_003",
            "name": "Priya Sharma",
            "email": "priya@performos.io",
            "title": "Full Stack Engineer",
            "manager_id": "manager_001",
            "cadence": "fortnightly",
            "next_session": "2026-03-28",
            "last_session": "2026-03-14",
            "avatar": "PS"
        },
        {
            "_id": "member_004",
            "user_id": "user_004",
            "name": "Marcus Thompson",
            "email": "marcus@performos.io",
            "title": "DevOps Engineer",
            "manager_id": "manager_001",
            "cadence": "weekly",
            "next_session": "2026-03-28",
            "last_session": "2026-03-14",
            "avatar": "MT"
        },
        {
            "_id": "member_005",
            "user_id": "user_005",
            "name": "Emily Nakamura",
            "email": "emily@performos.io",
            "title": "Junior Engineer",
            "manager_id": "manager_001",
            "cadence": "weekly",
            "next_session": "2026-03-28",
            "last_session": "2026-03-21",
            "avatar": "EN"
        },
        {
            "_id": "member_006",
            "user_id": "user_006",
            "name": "David O'Brien",
            "email": "david@performos.io",
            "title": "QA Engineer",
            "manager_id": "manager_001",
            "cadence": "fortnightly",
            "next_session": "2026-03-07",
            "last_session": "2026-02-21",
            "avatar": "DO"
        }
    ],
    "sessions": [
        # Sarah - performing well
        {
            "_id": "sess_001",
            "manager_id": "manager_001",
            "member_id": "member_001",
            "date": "2026-03-19",
            "status": "completed",
            "pre_meeting": {
                "proud_of": "Led the migration to the new component library — finished 2 days early with zero regressions.",
                "stuck_on": "Nothing major. Waiting on design specs for the dashboard refresh.",
                "need_from_manager": "Just a quick review of my architecture proposal when you get a chance.",
                "target_confidence": 5,
                "feeling_about_work": 5,
                "safe_to_raise_concerns": 5,
                "anything_affecting": "",
                "feel_supported": 5,
                "workload_manageable": 4
            },
            "manager_notes": {
                "check_in": "Sarah is in great form. Energised and confident.",
                "results_review": "Component library migration was excellent — clean execution.",
                "goal_alignment": "On track for Q2 goals. Discussed taking on mentoring Emily.",
                "support_development": "Interested in tech lead path. Will connect her with VP Eng.",
                "wellbeing": "No concerns. Strong energy.",
                "private_note": "Sarah is ready for promotion discussion next quarter."
            },
            "actions": [
                {"action": "Review architecture proposal", "owner": "manager", "status": "completed"},
                {"action": "Draft mentoring plan for Emily", "owner": "member", "status": "pending"}
            ],
            "follow_ups": ["Check on design specs delivery", "Discuss tech lead path"],
            "flags_detected": [],
            "created_at": datetime(2026, 3, 19)
        },
        # James - burnout
        {
            "_id": "sess_003",
            "manager_id": "manager_001",
            "member_id": "member_002",
            "date": "2026-03-21",
            "status": "completed",
            "pre_meeting": {
                "proud_of": "Got the API refactor through code review.",
                "stuck_on": "Everything feels like it's taking twice as long. I'm making silly mistakes.",
                "need_from_manager": "Honestly, I don't know. Maybe just some breathing room.",
                "target_confidence": 2,
                "feeling_about_work": 2,
                "safe_to_raise_concerns": 3,
                "anything_affecting": "I've been sleeping badly and it's catching up with me. The on-call rotation last month really took it out of me.",
                "feel_supported": 3,
                "workload_manageable": 1
            },
            "manager_notes": {
                "check_in": "James looked tired. Less engaged than usual.",
                "results_review": "API refactor done but took longer than expected. Not his usual quality.",
                "goal_alignment": "Paused stretch goals for now. Focus on core deliverables only.",
                "support_development": "Not the right time to push. Let him stabilise.",
                "wellbeing": "Raised sleep issues and burnout from on-call. Need to address workload.",
                "private_note": "Third session in a row with declining scores. Need to seriously reduce his load."
            },
            "actions": [
                {"action": "Remove James from on-call rotation for 4 weeks", "owner": "manager", "status": "pending"},
                {"action": "Reassign 2 backlog items to reduce load", "owner": "manager", "status": "pending"}
            ],
            "follow_ups": ["Check sleep/energy levels", "Review workload after changes"],
            "flags_detected": [],
            "created_at": datetime(2026, 3, 21)
        },
        {
            "_id": "sess_004",
            "manager_id": "manager_001",
            "member_id": "member_002",
            "date": "2026-03-07",
            "status": "completed",
            "pre_meeting": {
                "proud_of": "Closed out the database migration tickets.",
                "stuck_on": "The on-call interruptions are killing my focus time.",
                "need_from_manager": "Can we look at the on-call schedule? It's really draining.",
                "target_confidence": 3,
                "feeling_about_work": 3,
                "safe_to_raise_concerns": 4,
                "anything_affecting": "On-call has been rough. Two incidents last week.",
                "feel_supported": 3,
                "workload_manageable": 2
            },
            "manager_notes": {
                "check_in": "Seemed frustrated but engaged.",
                "results_review": "Migration done well despite on-call load.",
                "goal_alignment": "Adjusted timelines to account for on-call impact.",
                "support_development": "On hold while we sort workload.",
                "wellbeing": "On-call is clearly the issue. Need to address.",
                "private_note": "Scores are declining. Watch this closely."
            },
            "actions": [
                {"action": "Review on-call rotation fairness", "owner": "manager", "status": "completed"}
            ],
            "follow_ups": ["On-call rotation changes"],
            "flags_detected": [],
            "created_at": datetime(2026, 3, 7)
        },
        {
            "_id": "sess_005",
            "manager_id": "manager_001",
            "member_id": "member_002",
            "date": "2026-02-21",
            "status": "completed",
            "pre_meeting": {
                "proud_of": "Shipped the new payment integration.",
                "stuck_on": "Some tech debt in the codebase slowing things down.",
                "need_from_manager": "Time to address tech debt in Q2 planning.",
                "target_confidence": 4,
                "feeling_about_work": 4,
                "safe_to_raise_concerns": 5,
                "anything_affecting": "",
                "feel_supported": 4,
                "workload_manageable": 3
            },
            "manager_notes": {
                "check_in": "Positive, motivated.",
                "results_review": "Payment integration was solid.",
                "goal_alignment": "On track.",
                "support_development": "Interested in system design training.",
                "wellbeing": "No concerns.",
                "private_note": ""
            },
            "actions": [
                {"action": "Add tech debt sprint to Q2 plan", "owner": "manager", "status": "completed"}
            ],
            "follow_ups": ["System design course options"],
            "flags_detected": [],
            "created_at": datetime(2026, 2, 21)
        },
        # Priya - psychological safety
        {
            "_id": "sess_006",
            "manager_id": "manager_001",
            "member_id": "member_003",
            "date": "2026-03-14",
            "status": "completed",
            "pre_meeting": {
                "proud_of": "Delivered the user analytics dashboard.",
                "stuck_on": "Some decisions are being made without consulting the team. I built something that got changed last minute.",
                "need_from_manager": "I'd like to understand how decisions are being made about project direction.",
                "target_confidence": 3,
                "feeling_about_work": 3,
                "safe_to_raise_concerns": 2,
                "anything_affecting": "I raised a concern in the team meeting last week and felt like it was dismissed. I'm not sure my input is valued.",
                "feel_supported": 2,
                "workload_manageable": 3
            },
            "manager_notes": {
                "check_in": "Priya seemed guarded. Less open than usual.",
                "results_review": "Dashboard was good but she's frustrated by late requirement changes.",
                "goal_alignment": "Need to improve how we communicate direction changes.",
                "support_development": "She wants more involvement in planning.",
                "wellbeing": "Concerned about her psychological safety score. She doesn't feel heard.",
                "private_note": "I need to investigate the team meeting incident."
            },
            "actions": [
                {"action": "Set up monthly planning sessions including ICs", "owner": "manager", "status": "pending"},
                {"action": "Follow up on team meeting incident privately", "owner": "manager", "status": "pending"}
            ],
            "follow_ups": ["Check if Priya feels more included in decisions"],
            "flags_detected": [],
            "created_at": datetime(2026, 3, 14)
        },
        # Marcus - workload
        {
            "_id": "sess_008",
            "manager_id": "manager_001",
            "member_id": "member_004",
            "date": "2026-03-14",
            "status": "completed",
            "pre_meeting": {
                "proud_of": "Kept all systems running through the infrastructure migration.",
                "stuck_on": "I'm the only one who can handle the deployment pipeline issues. There's no backup.",
                "need_from_manager": "We need to cross-train someone on the deployment pipeline. I can't be the single point of failure.",
                "target_confidence": 3,
                "feeling_about_work": 3,
                "safe_to_raise_concerns": 4,
                "anything_affecting": "The constant context-switching between incidents and project work is exhausting. I feel like I can't do either well.",
                "feel_supported": 3,
                "workload_manageable": 2
            },
            "manager_notes": {
                "check_in": "Marcus is stretched thin. Acknowledged it openly.",
                "results_review": "Infrastructure migration was well-handled but at personal cost.",
                "goal_alignment": "Need to adjust expectations while we solve the bus factor.",
                "support_development": "Wants to mentor someone on DevOps — good sign.",
                "wellbeing": "Workload is the primary concern. Not sustainable.",
                "private_note": "Marcus is a flight risk if we don't fix the workload."
            },
            "actions": [
                {"action": "Identify DevOps cross-training candidate", "owner": "manager", "status": "pending"},
                {"action": "Document deployment pipeline runbooks", "owner": "member", "status": "pending"}
            ],
            "follow_ups": ["Cross-training plan timeline"],
            "flags_detected": [],
            "created_at": datetime(2026, 3, 14)
        },
        # Emily - new
        {
            "_id": "sess_009",
            "manager_id": "manager_001",
            "member_id": "member_005",
            "date": "2026-03-21",
            "status": "completed",
            "pre_meeting": {
                "proud_of": "Completed my first feature PR! It got approved with minor comments.",
                "stuck_on": "Still getting used to the codebase. It's big and I don't always know where to look.",
                "need_from_manager": "More pairing sessions with senior devs would help a lot.",
                "target_confidence": 3,
                "feeling_about_work": 4,
                "safe_to_raise_concerns": 4,
                "anything_affecting": "",
                "feel_supported": 4,
                "workload_manageable": 4
            },
            "manager_notes": {
                "check_in": "Emily is settling in well. Positive attitude.",
                "results_review": "First PR was clean. Good instincts.",
                "goal_alignment": "Set 30/60/90 day goals together.",
                "support_development": "Pairing with Sarah on component library. Good mentor match.",
                "wellbeing": "No concerns. Good onboarding experience so far.",
                "private_note": ""
            },
            "actions": [
                {"action": "Set up weekly pairing with Sarah", "owner": "manager", "status": "completed"},
                {"action": "Complete codebase walkthrough doc", "owner": "member", "status": "pending"}
            ],
            "follow_ups": ["30-day check-in on onboarding goals"],
            "flags_detected": [],
            "created_at": datetime(2026, 3, 21)
        }
    ],
    "flags": [
        {
            "_id": "flag_001",
            "member_id": "member_002",
            "session_id": "sess_003",
            "category": "wellbeing",
            "severity": "action_required",
            "signal": "Wellbeing score dropped from 4 to 2 over three consecutive sessions. Reports poor sleep and burnout from on-call.",
            "status": "open",
            "created_at": "2026-03-21",
            "resolved_at": None,
            "manager_note": None
        },
        {
            "_id": "flag_002",
            "member_id": "member_002",
            "session_id": "sess_003",
            "category": "workload",
            "severity": "action_required",
            "signal": "Workload score at 1 (Overwhelmed). Declining from 3 → 2 → 1 over three sessions.",
            "status": "open",
            "created_at": "2026-03-21",
            "resolved_at": None,
            "manager_note": None
        },
        {
            "_id": "flag_003",
            "member_id": "member_003",
            "session_id": "sess_006",
            "category": "psychological_safety",
            "severity": "action_required",
            "signal": "Safe to raise concerns score at 2. Reports feeling dismissed in team meetings and excluded from decisions.",
            "status": "open",
            "created_at": "2026-03-14",
            "resolved_at": None,
            "manager_note": None
        },
        {
            "_id": "flag_004",
            "member_id": "member_003",
            "session_id": "sess_006",
            "category": "team_dynamics",
            "severity": "concern",
            "signal": "Reports decisions being made without team consultation. Feels input is not valued.",
            "status": "open",
            "created_at": "2026-03-14",
            "resolved_at": None,
            "manager_note": None
        },
        {
            "_id": "flag_005",
            "member_id": "member_004",
            "session_id": "sess_008",
            "category": "workload",
            "severity": "concern",
            "signal": "Workload score at 2. Single point of failure on deployment pipeline. Context-switching fatigue.",
            "status": "open",
            "created_at": "2026-03-14",
            "resolved_at": None,
            "manager_note": None
        },
        {
            "_id": "flag_006",
            "member_id": "member_006",
            "session_id": None,
            "category": "manager_gap",
            "severity": "action_required",
            "signal": "No one-on-one conducted for 4+ weeks. Last session was Feb 21. Two scheduled sessions missed.",
            "status": "open",
            "created_at": "2026-03-14",
            "resolved_at": None,
            "manager_note": None
        }
    ]
}


async def seed_database():
    """Seed the database with initial data"""
    print("🌱 Seeding database...")
    
    # Clear existing data
    await users_collection.delete_many({})
    await members_collection.delete_many({})
    await sessions_collection.delete_many({})
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
    
    # Insert sessions
    if SEED_DATA["sessions"]:
        await sessions_collection.insert_many(SEED_DATA["sessions"])
        print(f"✅ Inserted {len(SEED_DATA['sessions'])} sessions")
    
    # Insert flags
    if SEED_DATA["flags"]:
        await flags_collection.insert_many(SEED_DATA["flags"])
        print(f"✅ Inserted {len(SEED_DATA['flags'])} flags")
    
    print("🎉 Database seeding complete!")
    print("\n📧 Demo credentials:")
    print("   Manager: alex@performos.io / demo")
    print("   Team members: sarah@performos.io, james@performos.io, priya@performos.io (all: demo)\n")

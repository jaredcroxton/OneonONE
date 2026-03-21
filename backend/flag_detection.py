from datetime import datetime
from typing import List, Dict, Any
from models import Flag, Session, PreMeetingReflection
from database import sessions_collection, flags_collection
from ai_service import analyze_risk
import json


async def detect_flags_for_session(session: Session, previous_sessions: List[Session],
                                   member_name: str, member_title: str) -> List[Dict]:
    """Detect flags from a session using rule-based and AI analysis"""
    flags = []
    
    if not session.pre_meeting:
        return flags
    
    pm = session.pre_meeting
    
    # Rule-based flag detection
    # 1. Low scores (1-2) trigger immediate flags
    if pm.feeling_about_work and pm.feeling_about_work <= 2:
        flags.append({
            "category": "wellbeing",
            "severity": "action_required",
            "signal": f"Feeling about work score at {pm.feeling_about_work}/5 — significant concern",
            "member_id": session.member_id,
            "session_id": session.id,
            "status": "open"
        })
    
    if pm.safe_to_raise_concerns and pm.safe_to_raise_concerns <= 2:
        flags.append({
            "category": "psychological_safety",
            "severity": "action_required",
            "signal": f"Safe to raise concerns score at {pm.safe_to_raise_concerns}/5 — psychological safety at risk",
            "member_id": session.member_id,
            "session_id": session.id,
            "status": "open"
        })
    
    if pm.feel_supported and pm.feel_supported <= 2:
        flags.append({
            "category": "team_dynamics",
            "severity": "action_required",
            "signal": f"Feel supported score at {pm.feel_supported}/5 — lacks team support",
            "member_id": session.member_id,
            "session_id": session.id,
            "status": "open"
        })
    
    if pm.workload_manageable and pm.workload_manageable <= 2:
        flags.append({
            "category": "workload",
            "severity": "action_required" if pm.workload_manageable == 1 else "concern",
            "signal": f"Workload manageable score at {pm.workload_manageable}/5 — {'overwhelmed' if pm.workload_manageable == 1 else 'workload concern'}",
            "member_id": session.member_id,
            "session_id": session.id,
            "status": "open"
        })
    
    if pm.target_confidence and pm.target_confidence <= 2:
        flags.append({
            "category": "performance_confidence",
            "severity": "action_required",
            "signal": f"Target confidence score at {pm.target_confidence}/5 — low performance confidence",
            "member_id": session.member_id,
            "session_id": session.id,
            "status": "open"
        })
    
    # 2. Declining trends (score drops by 2+ points)
    if len(previous_sessions) > 0:
        prev = previous_sessions[0].pre_meeting
        if prev:
            # Check for declining trends
            if pm.feeling_about_work and prev.feeling_about_work:
                if prev.feeling_about_work - pm.feeling_about_work >= 2:
                    flags.append({
                        "category": "wellbeing",
                        "severity": "concern",
                        "signal": f"Feeling about work declining: {prev.feeling_about_work} → {pm.feeling_about_work}",
                        "member_id": session.member_id,
                        "session_id": session.id,
                        "status": "open"
                    })
            
            if pm.safe_to_raise_concerns and prev.safe_to_raise_concerns:
                if prev.safe_to_raise_concerns - pm.safe_to_raise_concerns >= 2:
                    flags.append({
                        "category": "psychological_safety",
                        "severity": "action_required",
                        "signal": f"Safe to raise concerns declining: {prev.safe_to_raise_concerns} → {pm.safe_to_raise_concerns} — psychological safety erosion",
                        "member_id": session.member_id,
                        "session_id": session.id,
                        "status": "open"
                    })
            
            if pm.workload_manageable and prev.workload_manageable:
                if prev.workload_manageable - pm.workload_manageable >= 2:
                    flags.append({
                        "category": "workload",
                        "severity": "concern",
                        "signal": f"Workload manageable declining: {prev.workload_manageable} → {pm.workload_manageable}",
                        "member_id": session.member_id,
                        "session_id": session.id,
                        "status": "open"
                    })
    
    # 3. Persistent low scores (3 or below for 3+ consecutive sessions)
    if len(previous_sessions) >= 2:
        persistent_checks = [
            ("feeling_about_work", "wellbeing"),
            ("safe_to_raise_concerns", "psychological_safety"),
            ("workload_manageable", "workload"),
            ("target_confidence", "performance_confidence")
        ]
        
        for field, category in persistent_checks:
            current_val = getattr(pm, field, None)
            if current_val and current_val <= 3:
                # Check if previous 2 sessions also had low scores
                all_low = True
                for prev_sess in previous_sessions[:2]:
                    if prev_sess.pre_meeting:
                        prev_val = getattr(prev_sess.pre_meeting, field, None)
                        if not prev_val or prev_val > 3:
                            all_low = False
                            break
                
                if all_low:
                    flags.append({
                        "category": category,
                        "severity": "concern",
                        "signal": f"Persistent low {field.replace('_', ' ')} score (≤ 3) for 3+ consecutive sessions",
                        "member_id": session.member_id,
                        "session_id": session.id,
                        "status": "open"
                    })
    
    # 4. AI text analysis
    try:
        # Prepare previous session summaries for AI
        prev_sessions_summary = []
        for i, prev_sess in enumerate(previous_sessions[:3]):
            if prev_sess.pre_meeting:
                prev_sessions_summary.append({
                    "date": prev_sess.date,
                    "feeling": prev_sess.pre_meeting.feeling_about_work,
                    "safety": prev_sess.pre_meeting.safe_to_raise_concerns,
                    "workload": prev_sess.pre_meeting.workload_manageable
                })
        
        # Get existing flags to provide context to AI
        existing_flags_cursor = flags_collection.find({
            "member_id": session.member_id,
            "status": "open"
        })
        existing_flags = await existing_flags_cursor.to_list(length=100)
        active_flags = [{"category": f.get("category"), "signal": f.get("signal")} for f in existing_flags]
        
        # Call AI for text analysis
        ai_result = await analyze_risk(
            member_name=member_name,
            member_title=member_title,
            reflection=pm.model_dump(),
            previous_sessions=prev_sessions_summary,
            active_flags=active_flags
        )
        
        # Add AI-detected flags
        for ai_flag in ai_result.get("flags", []):
            # Check if similar flag already exists from rule-based detection
            is_duplicate = False
            for existing_flag in flags:
                if existing_flag["category"] == ai_flag["category"]:
                    is_duplicate = True
                    # Update with AI signal if more detailed
                    if len(ai_flag["signal"]) > len(existing_flag["signal"]):
                        existing_flag["signal"] = ai_flag["signal"]
                    break
            
            if not is_duplicate:
                flags.append({
                    "category": ai_flag["category"],
                    "severity": ai_flag["severity"],
                    "signal": ai_flag["signal"],
                    "member_id": session.member_id,
                    "session_id": session.id,
                    "status": "open"
                })
    
    except Exception as e:
        print(f"⚠️  AI flag detection failed: {str(e)}")
        # Continue with rule-based flags even if AI fails
    
    return flags


async def check_manager_gap_flags(manager_id: str):
    """Check for manager gap flags (no one-on-one for 3+ weeks)"""
    from database import members_collection
    from datetime import datetime, timedelta
    
    # Get all team members for this manager
    members_cursor = members_collection.find({"manager_id": manager_id})
    members = await members_cursor.to_list(length=1000)
    
    current_date = datetime(2026, 3, 21)  # Current date in our seed data
    gap_threshold = timedelta(weeks=3)
    
    for member in members:
        last_session_date_str = member.get("last_session")
        if not last_session_date_str:
            # No sessions ever - create gap flag
            existing = await flags_collection.find_one({
                "member_id": member["_id"],
                "category": "manager_gap",
                "status": "open"
            })
            if not existing:
                await flags_collection.insert_one({
                    "member_id": member["_id"],
                    "session_id": None,
                    "category": "manager_gap",
                    "severity": "action_required",
                    "signal": "No one-on-one sessions recorded",
                    "status": "open",
                    "created_at": current_date.strftime("%Y-%m-%d"),
                    "resolved_at": None,
                    "manager_note": None
                })
        else:
            try:
                last_session_date = datetime.strptime(last_session_date_str, "%Y-%m-%d")
                days_since = (current_date - last_session_date).days
                
                if days_since >= 21:  # 3 weeks
                    # Check if gap flag already exists
                    existing = await flags_collection.find_one({
                        "member_id": member["_id"],
                        "category": "manager_gap",
                        "status": "open"
                    })
                    if not existing:
                        await flags_collection.insert_one({
                            "member_id": member["_id"],
                            "session_id": None,
                            "category": "manager_gap",
                            "severity": "action_required",
                            "signal": f"No one-on-one conducted for {days_since} days. Last session: {last_session_date_str}",
                            "status": "open",
                            "created_at": current_date.strftime("%Y-%m-%d"),
                            "resolved_at": None,
                            "manager_note": None
                        })
            except Exception as e:
                print(f"⚠️  Error checking manager gap for member {member['_id']}: {str(e)}")
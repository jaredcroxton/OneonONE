from datetime import datetime
from typing import List, Dict, Any
from database import submissions_collection, flags_collection


async def detect_flags_for_submission(submission_id: str, member_id: str, member_name: str, 
                                      date: str, responses: Dict[str, Dict[str, Any]]) -> List[Dict]:
    """Detect flags from a submission using rule-based analysis on rating+comment pairs"""
    flags = []
    
    # Define the rules for flag detection
    flag_rules = [
        {
            "field": "feeling_about_work",
            "threshold": 2,
            "category": "wellbeing",
            "severity": "action_required",
            "signal_template": "Wellbeing score at {rating}/5. {comment_snippet}"
        },
        {
            "field": "safe_to_raise_concerns",
            "threshold": 2,
            "category": "psychological_safety",
            "severity": "action_required",
            "signal_template": "Safe to raise concerns score at {rating}/5. {comment_snippet}"
        },
        {
            "field": "feel_supported",
            "threshold": 2,
            "category": "team_dynamics",
            "severity": "action_required" if "field_rating" == 1 else "concern",
            "signal_template": "Feel supported score at {rating}/5. {comment_snippet}"
        },
        {
            "field": "workload_manageable",
            "threshold": 2,
            "category": "workload",
            "severity": "action_required",
            "signal_template": "Workload score at {rating}/5. {comment_snippet}"
        },
        {
            "field": "target_confidence",
            "threshold": 2,
            "category": "performance_confidence",
            "severity": "action_required",
            "signal_template": "Performance confidence at {rating}/5. {comment_snippet}"
        }
    ]
    
    # Check each rule
    for rule in flag_rules:
        field = rule["field"]
        response_item = responses.get(field)
        
        if response_item and isinstance(response_item, dict):
            rating = response_item.get("rating", 0)
            comment = response_item.get("comment", "").strip()
            
            if rating <= rule["threshold"]:
                # Determine severity based on rating
                if rating == 1:
                    severity = "action_required"
                elif rating == 2:
                    severity = "action_required"
                else:
                    severity = "concern"
                
                # Create comment snippet (first 150 chars)
                comment_snippet = comment[:150] + "..." if len(comment) > 150 else comment
                if not comment_snippet:
                    comment_snippet = f"Reports {field.replace('_', ' ')} at {rating}/5"
                
                # Build signal
                signal = rule["signal_template"].format(
                    rating=rating,
                    comment_snippet=comment_snippet if comment_snippet else f"No additional context provided"
                )
                
                flags.append({
                    "member_id": member_id,
                    "submission_id": submission_id,
                    "date": date,
                    "category": rule["category"],
                    "severity": severity,
                    "signal": signal,
                    "comment_snippet": comment if comment else None,
                    "status": "open"
                })
    
    # Check for concerning keywords in text comments
    concerning_patterns = {
        "burnout": ["burned out", "burnout", "exhausted", "drained", "can't keep up", "drowning"],
        "isolation": ["alone", "isolated", "no one", "nobody", "by myself", "vacuum"],
        "conflict": ["toxic", "hostile", "bullying", "unfair", "dismissed", "ignored"],
        "disengagement": ["don't care", "doesn't matter", "giving up", "checking out", "pointless"]
    }
    
    all_comments = []
    for field, response_item in responses.items():
        if isinstance(response_item, dict):
            comment = response_item.get("comment", "").lower()
            if comment:
                all_comments.append((field, comment, response_item.get("rating", 0)))
    
    for field, comment, rating in all_comments:
        for pattern_type, patterns in concerning_patterns.items():
            if any(pattern in comment for pattern in patterns):
                # Found concerning pattern
                comment_snippet = responses[field]["comment"][:150]
                if len(responses[field]["comment"]) > 150:
                    comment_snippet += "..."
                
                # Determine category based on pattern type
                category_map = {
                    "burnout": "wellbeing",
                    "isolation": "team_dynamics",
                    "conflict": "psychological_safety",
                    "disengagement": "engagement"
                }
                
                category = category_map.get(pattern_type, "wellbeing")
                
                # Check if we already have a flag for this category to avoid duplicates
                has_flag = any(f["category"] == category for f in flags)
                if not has_flag:
                    flags.append({
                        "member_id": member_id,
                        "submission_id": submission_id,
                        "date": date,
                        "category": category,
                        "severity": "concern" if rating > 2 else "action_required",
                        "signal": f"Concerning language detected in {field.replace('_', ' ')}: \"{pattern_type}\" pattern",
                        "comment_snippet": comment_snippet,
                        "status": "open"
                    })
                break
    
    return flags


async def check_missing_submissions(manager_id: str, current_date: str):
    """Check for team members who haven't submitted for the current week"""
    from database import members_collection
    
    # Get all team members for this manager
    members_cursor = members_collection.find({"manager_id": manager_id})
    members = await members_cursor.to_list(length=1000)
    
    flags = []
    
    for member in members:
        # Check if there's a submission for current_date
        submission = await submissions_collection.find_one({
            "member_id": member["_id"],
            "date": current_date
        })
        
        if not submission:
            # Check if manager gap flag already exists
            existing_flag = await flags_collection.find_one({
                "member_id": member["_id"],
                "date": current_date,
                "category": "manager_gap",
                "status": "open"
            })
            
            if not existing_flag:
                flag = {
                    "member_id": member["_id"],
                    "submission_id": None,
                    "date": current_date,
                    "category": "manager_gap",
                    "severity": "action_required",
                    "signal": f"No submission received for week of {current_date}. Potential disengagement.",
                    "comment_snippet": None,
                    "status": "open"
                }
                await flags_collection.insert_one(flag)
                flags.append(flag)
    
    return flags

from datetime import datetime
from typing import List, Dict, Any
from database import submissions_collection, flags_collection


async def detect_flags_for_submission(submission_id: str, member_id: str, member_name: str, 
                                      date: str, responses: Dict[str, Dict[str, Any]], 
                                      wellness_checkin: Dict[str, Any] = None) -> List[Dict]:
    """Detect flags from a submission using rule-based analysis on rating+comment pairs"""
    flags = []
    
    # Define the rules for flag detection
    flag_rules = [
        {
            "field": "feeling_about_work",
            "threshold": 2,
            "operator": "<=",
            "category": "wellbeing",
            "severity": "action_required",
            "signal_template": "Feeling about work at {rating}/5. {comment_snippet}"
        },
        {
            "field": "safe_to_raise_concerns",
            "threshold": 2,
            "operator": "<=",
            "category": "psychological_safety",
            "severity": "action_required",
            "signal_template": "Speaking up score at {rating}/5 (holding back). {comment_snippet}"
        },
        {
            "field": "stuck_on",
            "threshold": 4,
            "operator": ">=",
            "category": "performance",
            "severity": "concern",
            "signal_template": "Blocked rating at {rating}/5 (completely stuck). {comment_snippet}"
        }
    ]
    
    # Check each rule
    for rule in flag_rules:
        field = rule["field"]
        response_item = responses.get(field)
        
        if response_item and isinstance(response_item, dict):
            rating = response_item.get("rating", 0)
            comment = response_item.get("comment", "").strip()
            
            # Check threshold based on operator
            operator = rule.get("operator", "<=")
            trigger = False
            if operator == "<=" and rating <= rule["threshold"]:
                trigger = True
            elif operator == ">=" and rating >= rule["threshold"]:
                trigger = True
            
            if trigger:
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
    
    # WELLNESS CHECK-IN FLAG DETECTION
    if wellness_checkin:
        mood = wellness_checkin.get("mood", "")
        mood_score = wellness_checkin.get("mood_score", 3)
        energy_level = wellness_checkin.get("energy_level", 5)
        workload_level = wellness_checkin.get("workload_level", 5)
        wellness_comments = wellness_checkin.get("comments", "")
        
        # Rule 1: Mood is "Stressed" or "Exhausted" triggers wellbeing flag
        if mood in ["stressed", "exhausted"]:
            severity = "action_required" if mood == "exhausted" else "concern"
            
            # Upgrade to action_required if mood is exhausted AND energy <= 3
            if mood == "exhausted" and energy_level <= 3:
                severity = "action_required"
            
            signal = f"Mood selected: {mood.capitalize()} ({mood_score}/5)"
            if energy_level <= 3:
                signal += f", Energy at {energy_level}/10"
            if wellness_comments:
                signal += f" - {wellness_comments[:100]}"
            
            # Check if we already have a wellbeing flag to avoid duplicates
            has_wellbeing_flag = any(f["category"] == "wellbeing" for f in flags)
            if not has_wellbeing_flag:
                flags.append({
                    "member_id": member_id,
                    "submission_id": submission_id,
                    "date": date,
                    "category": "wellbeing",
                    "severity": severity,
                    "signal": signal,
                    "comment_snippet": wellness_comments[:150] if wellness_comments else None,
                    "status": "open"
                })
        
        # Rule 2: Energy <= 3 triggers wellbeing flag
        if energy_level <= 3:
            has_wellbeing_flag = any(f["category"] == "wellbeing" for f in flags)
            if not has_wellbeing_flag:
                signal = f"Energy level at {energy_level}/10 (Low)"
                if mood:
                    signal += f", Mood: {mood.capitalize()}"
                
                flags.append({
                    "member_id": member_id,
                    "submission_id": submission_id,
                    "date": date,
                    "category": "wellbeing",
                    "severity": "concern",
                    "signal": signal,
                    "comment_snippet": wellness_comments[:150] if wellness_comments else None,
                    "status": "open"
                })
        
        # Rule 3: Target confidence <= 2 triggers performance flag
        target_confidence = wellness_checkin.get("target_confidence", 3)
        if target_confidence <= 2:
            has_performance_flag = any(f["category"] == "performance" for f in flags)
            if not has_performance_flag:
                severity = "action_required" if target_confidence == 1 and energy_level <= 2 else "concern"
                signal = f"Target confidence at {target_confidence}/5 (behind on targets)"
                if energy_level <= 2:
                    signal += f", Energy at {energy_level}/5"
                if wellness_comments:
                    signal += f" - {wellness_comments[:100]}"
                
                flags.append({
                    "member_id": member_id,
                    "submission_id": submission_id,
                    "date": date,
                    "category": "performance",
                    "severity": severity,
                    "signal": signal,
                    "comment_snippet": wellness_comments[:150] if wellness_comments else None,
                    "status": "open"
                })
    
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

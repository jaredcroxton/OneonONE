"""
PerformOS One-on-One Builder - XAI Grok API POC
Tests three critical AI features:
1. Risk analysis for psychological safety detection
2. Conversation starters generation
3. Session summary generation
"""

import asyncio
import json
import re
from typing import Dict, List, Any

# XAI Grok API configuration
XAI_API_KEY = "xai-eYSXFxTrChwZoExc0oEZjBsmKgUpAvK6rlquAQpYn2LfVgNVnDzap4iMQAMUUbewtQW8hYfNdNEcD90A"
XAI_API_URL = "https://api.x.ai/v1/chat/completions"
MODEL = "grok-4-1-fast-non-reasoning"  # Latest fast model from xAI

# Sample test data representing different scenarios
TEST_SCENARIOS = {
    "sarah_healthy": {
        "name": "Sarah Mitchell",
        "title": "Senior Frontend Engineer",
        "reflection": {
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
        "previous_sessions": [
            {"date": "2026-03-05", "feeling": 4, "safety": 5, "workload": 4}
        ],
        "active_flags": []
    },
    "james_burnout": {
        "name": "James Rodriguez",
        "title": "Backend Engineer",
        "reflection": {
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
        "previous_sessions": [
            {"date": "2026-03-07", "feeling": 3, "safety": 4, "workload": 2},
            {"date": "2026-02-21", "feeling": 4, "safety": 5, "workload": 3}
        ],
        "active_flags": []
    },
    "priya_safety": {
        "name": "Priya Sharma",
        "title": "Full Stack Engineer",
        "reflection": {
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
        "previous_sessions": [
            {"date": "2026-02-28", "feeling": 4, "safety": 3, "workload": 4}
        ],
        "active_flags": []
    },
    "marcus_workload": {
        "name": "Marcus Thompson",
        "title": "DevOps Engineer",
        "reflection": {
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
        "previous_sessions": [
            {"date": "2026-02-28", "feeling": 4, "safety": 4, "workload": 3}
        ],
        "active_flags": []
    }
}

# Manager notes sample for session summary testing
SAMPLE_MANAGER_NOTES = {
    "check_in": "James looked tired. Less engaged than usual.",
    "results_review": "API refactor done but took longer than expected. Not his usual quality.",
    "goal_alignment": "Paused stretch goals for now. Focus on core deliverables only.",
    "support_development": "Not the right time to push. Let him stabilise.",
    "wellbeing": "Raised sleep issues and burnout from on-call. Need to address workload."
}

SAMPLE_ACTIONS = [
    {"action": "Remove James from on-call rotation for 4 weeks", "owner": "manager"},
    {"action": "Reassign 2 backlog items to reduce load", "owner": "manager"}
]


def clean_json_response(text: str) -> str:
    """Clean JSON from markdown code blocks and extra whitespace"""
    # Remove markdown code blocks
    text = re.sub(r'```json\n?', '', text)
    text = re.sub(r'```\n?', '', text)
    # Strip whitespace
    text = text.strip()
    return text


async def call_grok_api(prompt: str, json_schema: Dict = None, max_retries: int = 2) -> Dict:
    """Call Grok API with retry logic and JSON parsing"""
    import aiohttp
    
    headers = {
        "Authorization": f"Bearer {XAI_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 2000
    }
    
    # Add JSON schema if provided (Grok supports structured outputs)
    if json_schema:
        payload["response_format"] = {
            "type": "json_schema",
            "json_schema": {
                "name": "response_schema",
                "strict": True,
                "schema": json_schema
            }
        }
    
    for attempt in range(max_retries):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(XAI_API_URL, json=payload, headers=headers) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        print(f"❌ API Error (status {response.status}): {error_text}")
                        if attempt < max_retries - 1:
                            print(f"🔄 Retrying... (attempt {attempt + 2}/{max_retries})")
                            await asyncio.sleep(1)
                            continue
                        raise Exception(f"API call failed: {error_text}")
                    
                    data = await response.json()
                    content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
                    
                    # Clean and parse JSON
                    cleaned = clean_json_response(content)
                    try:
                        parsed = json.loads(cleaned)
                        return parsed
                    except json.JSONDecodeError as e:
                        print(f"❌ JSON parsing error: {e}")
                        print(f"Raw response: {content[:200]}...")
                        if attempt < max_retries - 1:
                            print(f"🔄 Retrying with repair prompt...")
                            # Retry with explicit JSON repair instruction
                            payload["messages"].append({
                                "role": "user",
                                "content": f"The previous response was not valid JSON. Please provide ONLY valid JSON, no markdown, no explanations: {content}"
                            })
                            continue
                        raise
        except Exception as e:
            print(f"❌ Error on attempt {attempt + 1}: {str(e)}")
            if attempt < max_retries - 1:
                await asyncio.sleep(1)
                continue
            raise
    
    raise Exception("All retry attempts failed")


async def test_risk_analysis():
    """Test 1: Risk analysis for psychological safety detection"""
    print("\n" + "="*80)
    print("TEST 1: RISK ANALYSIS FOR PSYCHOLOGICAL SAFETY DETECTION")
    print("="*80)
    
    json_schema = {
        "type": "object",
        "properties": {
            "flags": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "category": {
                            "type": "string",
                            "enum": ["wellbeing", "psychological_safety", "workload", "engagement", "team_dynamics"]
                        },
                        "severity": {
                            "type": "string",
                            "enum": ["watch", "concern", "action_required"]
                        },
                        "signal": {"type": "string"},
                        "quote_trigger": {"type": "string"}
                    },
                    "required": ["category", "severity", "signal", "quote_trigger"],
                    "additionalProperties": False
                }
            },
            "overall_sentiment": {
                "type": "string",
                "enum": ["positive", "neutral", "mixed", "concerning"]
            },
            "summary": {"type": "string"}
        },
        "required": ["flags", "overall_sentiment", "summary"],
        "additionalProperties": False
    }
    
    results = {}
    
    for scenario_name, scenario_data in TEST_SCENARIOS.items():
        print(f"\n🧪 Testing scenario: {scenario_name} ({scenario_data['name']})")
        
        reflection = scenario_data['reflection']
        prev_sessions = scenario_data.get('previous_sessions', [])
        
        # Build prompt
        prompt = f"""You are a workplace psychological safety analyst. Analyse the following responses from a team member's one-on-one reflection. Your job is to detect early warning signs of psychological safety risks, wellbeing concerns, burnout, disengagement, isolation, or team conflict.

Do NOT over-flag. Only flag when there is a genuine signal. Normal work frustration is not a flag. A bad day is not a flag. Look for patterns that suggest something deeper.

Team member: {scenario_data['name']} ({scenario_data['title']})

Current reflection:
- Most proud of: {reflection['proud_of']}
- Where stuck: {reflection['stuck_on']}
- Need from manager: {reflection['need_from_manager']}
- Target confidence: {reflection['target_confidence']}/5
- Feeling about work: {reflection['feeling_about_work']}/5
- Safe to raise concerns: {reflection['safe_to_raise_concerns']}/5
- Feel supported: {reflection['feel_supported']}/5
- Workload manageable: {reflection['workload_manageable']}/5
- Anything affecting work: {reflection['anything_affecting'] or 'Not provided'}

Previous session scores:
{json.dumps(prev_sessions, indent=2) if prev_sessions else 'No previous sessions'}

Respond in JSON only (the response will be automatically parsed):
- flags: array of detected flags with category, severity, signal, and quote_trigger
- overall_sentiment: positive, neutral, mixed, or concerning
- summary: one sentence summary of the overall tone

Remember:
- Category must be one of: wellbeing, psychological_safety, workload, engagement, team_dynamics
- Severity must be one of: watch, concern, action_required
- Use action_required for scores of 1-2 or significant concerns
- Use concern for declining trends or scores of 3
- Use watch for potential issues worth monitoring"""

        try:
            result = await call_grok_api(prompt, json_schema)
            results[scenario_name] = result
            
            print(f"✅ Response received")
            print(f"   Sentiment: {result.get('overall_sentiment')}")
            print(f"   Flags detected: {len(result.get('flags', []))}")
            for flag in result.get('flags', []):
                print(f"      • [{flag['severity'].upper()}] {flag['category']}: {flag['signal'][:80]}...")
            
            # Validate response structure
            assert 'flags' in result, "Missing 'flags' field"
            assert 'overall_sentiment' in result, "Missing 'overall_sentiment' field"
            assert 'summary' in result, "Missing 'summary' field"
            assert isinstance(result['flags'], list), "'flags' must be an array"
            
            # Validate flag structure
            for flag in result['flags']:
                assert 'category' in flag, "Flag missing 'category'"
                assert 'severity' in flag, "Flag missing 'severity'"
                assert 'signal' in flag, "Flag missing 'signal'"
                assert flag['category'] in ['wellbeing', 'psychological_safety', 'workload', 'engagement', 'team_dynamics'], f"Invalid category: {flag['category']}"
                assert flag['severity'] in ['watch', 'concern', 'action_required'], f"Invalid severity: {flag['severity']}"
            
            print(f"✅ Validation passed for {scenario_name}")
            
        except Exception as e:
            print(f"❌ Test failed for {scenario_name}: {str(e)}")
            results[scenario_name] = {"error": str(e)}
    
    # Summary
    print(f"\n{'='*80}")
    print(f"RISK ANALYSIS TEST SUMMARY")
    print(f"{'='*80}")
    passed = sum(1 for r in results.values() if 'error' not in r)
    total = len(results)
    print(f"✅ Passed: {passed}/{total}")
    if passed < total:
        print(f"❌ Failed: {total - passed}/{total}")
        return False
    return True


async def test_conversation_starters():
    """Test 2: Conversation starters generation"""
    print("\n" + "="*80)
    print("TEST 2: CONVERSATION STARTERS GENERATION")
    print("="*80)
    
    json_schema = {
        "type": "object",
        "properties": {
            "starters": {
                "type": "array",
                "items": {"type": "string"},
                "minItems": 2,
                "maxItems": 3
            }
        },
        "required": ["starters"],
        "additionalProperties": False
    }
    
    results = {}
    
    # Test with scenarios that have flags or concerns
    test_cases = ["james_burnout", "priya_safety", "marcus_workload"]
    
    for scenario_name in test_cases:
        scenario_data = TEST_SCENARIOS[scenario_name]
        print(f"\n🧪 Testing scenario: {scenario_name} ({scenario_data['name']})")
        
        reflection = scenario_data['reflection']
        
        prompt = f"""You are a leadership coach helping a manager prepare for a one-on-one conversation. Based on the team member's pre-meeting reflection below, suggest 2-3 natural conversation starters the manager could use. These should feel human and genuine, not scripted or clinical. Focus on opening dialogue, not interrogating.

If there are concerning responses, suggest a gentle way to open that topic without making the team member feel investigated.

Team member: {scenario_data['name']} ({scenario_data['title']})

Pre-meeting reflection:
- Most proud of: {reflection['proud_of']}
- Where stuck: {reflection['stuck_on']}
- Need from manager: {reflection['need_from_manager']}
- Target confidence: {reflection['target_confidence']}/5
- Feeling about work: {reflection['feeling_about_work']}/5
- Safe to raise concerns: {reflection['safe_to_raise_concerns']}/5
- Feel supported: {reflection['feel_supported']}/5
- Workload manageable: {reflection['workload_manageable']}/5
{f"- Anything affecting work: {reflection['anything_affecting']}" if reflection['anything_affecting'] else ""}

Respond in JSON only with 2-3 conversation starters."""

        try:
            result = await call_grok_api(prompt, json_schema)
            results[scenario_name] = result
            
            print(f"✅ Response received")
            print(f"   Starters generated: {len(result.get('starters', []))}")
            for i, starter in enumerate(result.get('starters', []), 1):
                print(f"      {i}. \"{starter}\"")
            
            # Validate response structure
            assert 'starters' in result, "Missing 'starters' field"
            assert isinstance(result['starters'], list), "'starters' must be an array"
            assert 2 <= len(result['starters']) <= 3, f"Expected 2-3 starters, got {len(result['starters'])}"
            
            for starter in result['starters']:
                assert isinstance(starter, str), "Each starter must be a string"
                assert len(starter) > 10, "Starters should be meaningful (>10 chars)"
            
            print(f"✅ Validation passed for {scenario_name}")
            
        except Exception as e:
            print(f"❌ Test failed for {scenario_name}: {str(e)}")
            results[scenario_name] = {"error": str(e)}
    
    # Summary
    print(f"\n{'='*80}")
    print(f"CONVERSATION STARTERS TEST SUMMARY")
    print(f"{'='*80}")
    passed = sum(1 for r in results.values() if 'error' not in r)
    total = len(results)
    print(f"✅ Passed: {passed}/{total}")
    if passed < total:
        print(f"❌ Failed: {total - passed}/{total}")
        return False
    return True


async def test_session_summary():
    """Test 3: Session summary generation"""
    print("\n" + "="*80)
    print("TEST 3: SESSION SUMMARY GENERATION")
    print("="*80)
    
    json_schema = {
        "type": "object",
        "properties": {
            "summary": {"type": "string"},
            "key_actions": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "action": {"type": "string"},
                        "owner": {
                            "type": "string",
                            "enum": ["manager", "team_member"]
                        },
                        "due": {"type": "string"}
                    },
                    "required": ["action", "owner", "due"],
                    "additionalProperties": False
                }
            },
            "follow_ups": {
                "type": "array",
                "items": {"type": "string"}
            }
        },
        "required": ["summary", "key_actions", "follow_ups"],
        "additionalProperties": False
    }
    
    print(f"\n🧪 Testing session summary generation")
    
    prompt = f"""You are a workplace assistant. Summarise the following one-on-one session notes into a clean, professional summary. Include: key discussion points, agreed actions with owners, follow-up items, and overall tone of the conversation.

Keep it concise — 4-6 sentences maximum. Do not editorialize. Do not add opinions. Just summarise what was discussed and agreed.

Manager notes:
- Check-in: {SAMPLE_MANAGER_NOTES['check_in']}
- Results review: {SAMPLE_MANAGER_NOTES['results_review']}
- Goal alignment: {SAMPLE_MANAGER_NOTES['goal_alignment']}
- Support & development: {SAMPLE_MANAGER_NOTES['support_development']}
- Wellbeing: {SAMPLE_MANAGER_NOTES['wellbeing']}

Actions agreed:
{json.dumps(SAMPLE_ACTIONS, indent=2)}

Respond in JSON only."""

    try:
        result = await call_grok_api(prompt, json_schema)
        
        print(f"✅ Response received")
        print(f"\n📝 Summary:")
        print(f"   {result.get('summary')}")
        print(f"\n✓ Key Actions ({len(result.get('key_actions', []))}):")
        for action in result.get('key_actions', []):
            print(f"      • {action['action']} ({action['owner']}) - Due: {action['due']}")
        print(f"\n→ Follow-ups ({len(result.get('follow_ups', []))}):")
        for followup in result.get('follow_ups', []):
            print(f"      • {followup}")
        
        # Validate response structure
        assert 'summary' in result, "Missing 'summary' field"
        assert 'key_actions' in result, "Missing 'key_actions' field"
        assert 'follow_ups' in result, "Missing 'follow_ups' field"
        assert isinstance(result['summary'], str), "'summary' must be a string"
        assert isinstance(result['key_actions'], list), "'key_actions' must be an array"
        assert isinstance(result['follow_ups'], list), "'follow_ups' must be an array"
        
        # Validate key actions structure
        for action in result['key_actions']:
            assert 'action' in action, "Action missing 'action' field"
            assert 'owner' in action, "Action missing 'owner' field"
            assert 'due' in action, "Action missing 'due' field"
            assert action['owner'] in ['manager', 'team_member'], f"Invalid owner: {action['owner']}"
        
        print(f"\n✅ Validation passed")
        
        # Summary
        print(f"\n{'='*80}")
        print(f"SESSION SUMMARY TEST SUMMARY")
        print(f"{'='*80}")
        print(f"✅ Passed: 1/1")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        print(f"\n{'='*80}")
        print(f"SESSION SUMMARY TEST SUMMARY")
        print(f"{'='*80}")
        print(f"❌ Failed: 1/1")
        return False


async def main():
    """Run all POC tests"""
    print("="*80)
    print("PerformOS One-on-One Builder - XAI Grok API POC")
    print("="*80)
    print(f"Model: {MODEL}")
    print(f"API Endpoint: {XAI_API_URL}")
    print("="*80)
    
    results = {
        "risk_analysis": await test_risk_analysis(),
        "conversation_starters": await test_conversation_starters(),
        "session_summary": await test_session_summary()
    }
    
    # Final summary
    print("\n" + "="*80)
    print("FINAL POC RESULTS")
    print("="*80)
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, passed_status in results.items():
        status = "✅ PASSED" if passed_status else "❌ FAILED"
        print(f"{status}: {test_name.replace('_', ' ').title()}")
    
    print(f"\n{'='*80}")
    if passed == total:
        print(f"🎉 ALL TESTS PASSED ({passed}/{total})")
        print("✅ Grok API integration is working correctly!")
        print("✅ Ready to proceed with Phase 2: Full app development")
    else:
        print(f"⚠️  SOME TESTS FAILED ({passed}/{total} passed)")
        print("❌ Need to fix issues before proceeding to Phase 2")
    print(f"{'='*80}\n")
    
    return passed == total


if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1)

import os
import json
import re
from typing import Dict, List, Any
import aiohttp
from dotenv import load_dotenv

load_dotenv()

XAI_API_KEY = os.getenv("XAI_API_KEY")
XAI_API_URL = os.getenv("XAI_API_URL")
XAI_MODEL = os.getenv("XAI_MODEL", "grok-4-1-fast-non-reasoning")


def clean_json_response(text: str) -> str:
    """Clean JSON from markdown code blocks and extra whitespace"""
    text = re.sub(r'```json\n?', '', text)
    text = re.sub(r'```\n?', '', text)
    return text.strip()


async def call_grok_api(prompt: str, json_schema: Dict = None, max_retries: int = 2) -> Dict:
    """Call Grok API with retry logic and JSON parsing"""
    headers = {
        "Authorization": f"Bearer {XAI_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": XAI_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": 2000
    }
    
    # Add JSON schema if provided
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
                        print(f"❌ Grok API Error (status {response.status}): {error_text}")
                        if attempt < max_retries - 1:
                            continue
                        raise Exception(f"Grok API call failed: {error_text}")
                    
                    data = await response.json()
                    content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
                    
                    # Clean and parse JSON
                    cleaned = clean_json_response(content)
                    try:
                        parsed = json.loads(cleaned)
                        return parsed
                    except json.JSONDecodeError as e:
                        print(f"❌ JSON parsing error: {e}")
                        if attempt < max_retries - 1:
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
                continue
            raise
    
    raise Exception("All retry attempts failed")


async def analyze_risk(member_name: str, member_title: str, reflection: Dict,
                       previous_sessions: List[Dict] = None, active_flags: List[Dict] = None) -> Dict:
    """Analyze psychological safety risks from team member's reflection"""
    prev_sessions = previous_sessions or []
    flags = active_flags or []
    
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
    
    prompt = f"""You are a workplace psychological safety analyst. Analyse the following responses from a team member's one-on-one reflection. Your job is to detect early warning signs of psychological safety risks, wellbeing concerns, burnout, disengagement, isolation, or team conflict.

Do NOT over-flag. Only flag when there is a genuine signal. Normal work frustration is not a flag. A bad day is not a flag. Look for patterns that suggest something deeper.

Team member: {member_name} ({member_title})

Current reflection:
- Most proud of: {reflection.get('proud_of', 'Not provided')}
- Where stuck: {reflection.get('stuck_on', 'Not provided')}
- Need from manager: {reflection.get('need_from_manager', 'Not provided')}
- Target confidence: {reflection.get('target_confidence', 'N/A')}/5
- Feeling about work: {reflection.get('feeling_about_work', 'N/A')}/5
- Safe to raise concerns: {reflection.get('safe_to_raise_concerns', 'N/A')}/5
- Feel supported: {reflection.get('feel_supported', 'N/A')}/5
- Workload manageable: {reflection.get('workload_manageable', 'N/A')}/5
- Anything affecting work: {reflection.get('anything_affecting', 'Not provided')}

Previous session scores:
{json.dumps(prev_sessions, indent=2) if prev_sessions else 'No previous sessions'}

Active flags: {json.dumps([f"{f['category']}: {f['signal']}" for f in flags]) if flags else 'None'}

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
    
    return await call_grok_api(prompt, json_schema)


async def generate_conversation_starters(member_name: str, member_title: str,
                                        reflection: Dict, active_flags: List[Dict] = None) -> Dict:
    """Generate conversation starters for manager"""
    flags = active_flags or []
    
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
    
    prompt = f"""You are a leadership coach helping a manager prepare for a one-on-one conversation. Based on the team member's pre-meeting reflection below, suggest 2-3 natural conversation starters the manager could use. These should feel human and genuine, not scripted or clinical. Focus on opening dialogue, not interrogating.

If there are concerning responses, suggest a gentle way to open that topic without making the team member feel investigated.

Team member: {member_name} ({member_title})

Pre-meeting reflection:
- Most proud of: {reflection.get('proud_of', 'Not provided')}
- Where stuck: {reflection.get('stuck_on', 'Not provided')}
- Need from manager: {reflection.get('need_from_manager', 'Not provided')}
- Target confidence: {reflection.get('target_confidence', 'N/A')}/5
- Feeling about work: {reflection.get('feeling_about_work', 'N/A')}/5
- Safe to raise concerns: {reflection.get('safe_to_raise_concerns', 'N/A')}/5
- Feel supported: {reflection.get('feel_supported', 'N/A')}/5
- Workload manageable: {reflection.get('workload_manageable', 'N/A')}/5
{f"- Anything affecting work: {reflection.get('anything_affecting', '')}" if reflection.get('anything_affecting') else ''}

Active flags: {json.dumps([f"{f['category']}: {f['signal']}" for f in flags]) if flags else 'None'}

Respond in JSON only with 2-3 conversation starters."""
    
    return await call_grok_api(prompt, json_schema)


async def generate_session_summary(manager_notes: Dict, actions: List[Dict]) -> Dict:
    """Generate session summary from manager's notes"""
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
    
    prompt = f"""You are a workplace assistant. Summarise the following one-on-one session notes into a clean, professional summary. Include: key discussion points, agreed actions with owners, follow-up items, and overall tone of the conversation.

Keep it concise — 4-6 sentences maximum. Do not editorialize. Do not add opinions. Just summarise what was discussed and agreed.

Manager notes:
- Check-in: {manager_notes.get('check_in', 'No notes')}
- Results review: {manager_notes.get('results_review', 'No notes')}
- Goal alignment: {manager_notes.get('goal_alignment', 'No notes')}
- Support & development: {manager_notes.get('support_development', 'No notes')}
- Wellbeing: {manager_notes.get('wellbeing', 'No notes')}

Actions agreed:
{json.dumps([f"{a['action']} ({a['owner']})" for a in actions]) if actions else 'None'}

Respond in JSON only."""
    
    return await call_grok_api(prompt, json_schema)
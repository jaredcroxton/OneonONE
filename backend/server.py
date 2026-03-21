from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import List, Optional
from datetime import datetime, timedelta
from jose import JWTError, jwt
import os
from dotenv import load_dotenv

from database import init_db, users_collection, members_collection, sessions_collection, flags_collection
from models import (
    User, UserLogin, Token, TeamMember, Session, SessionCreate, Flag, FlagCreate,
    PreMeetingReflection, ManagerNotes, Action,
    RiskAnalysisRequest, ConversationStartersRequest, SessionSummaryRequest
)
from auth import authenticate_user, create_access_token, get_password_hash
from ai_service import analyze_risk, generate_conversation_starters, generate_session_summary
from flag_detection import detect_flags_for_session, check_manager_gap_flags
from seed_data import seed_database

load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET", "performos_jwt_secret_key")
ALGORITHM = "HS256"

app = FastAPI(title="PerformOS One-on-One Builder API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBearer()


def serialize_doc(doc):
    """Convert MongoDB document to serializable dict"""
    if not doc:
        return None
    if isinstance(doc, list):
        return [serialize_doc(d) for d in doc]
    if "_id" in doc:
        doc["_id"] = str(doc["_id"])
    if "created_at" in doc and isinstance(doc["created_at"], datetime):
        doc["created_at"] = doc["created_at"].isoformat()
    return doc


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify JWT token and return current user"""
    token = credentials.credentials
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials"
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
    
    user = await users_collection.find_one({"_id": user_id})
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    return serialize_doc(user)


@app.on_event("startup")
async def startup_event():
    """Initialize database and seed data"""
    await init_db()
    # Check if database is empty and seed if needed
    user_count = await users_collection.count_documents({})
    if user_count == 0:
        await seed_database()


@app.get("/")
async def root():
    return {"message": "PerformOS One-on-One Builder API", "status": "running"}


# ============================================================
# AUTHENTICATION ROUTES
# ============================================================

@app.post("/api/auth/login", response_model=Token)
async def login(user_login: UserLogin):
    """Login user and return JWT token"""
    user = await authenticate_user(user_login.email, user_login.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    access_token = create_access_token(data={"sub": user["_id"]})
    user_data = serialize_doc(user)
    user_data.pop("hashed_password", None)
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user_data
    }


@app.get("/api/auth/me")
async def get_me(current_user: dict = Depends(get_current_user)):
    """Get current user"""
    current_user.pop("hashed_password", None)
    return current_user


# ============================================================
# TEAM MEMBERS ROUTES
# ============================================================

@app.get("/api/members")
async def get_members(current_user: dict = Depends(get_current_user)):
    """Get team members for current user"""
    if current_user["role"] == "manager":
        # Get all team members managed by this manager
        members_cursor = members_collection.find({"manager_id": current_user["_id"]})
        members = await members_cursor.to_list(length=1000)
        return serialize_doc(members)
    else:
        # Team member can only see their own record
        member = await members_collection.find_one({"user_id": current_user["_id"]})
        return serialize_doc([member] if member else [])


@app.get("/api/members/{member_id}")
async def get_member(member_id: str, current_user: dict = Depends(get_current_user)):
    """Get specific team member"""
    member = await members_collection.find_one({"_id": member_id})
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    
    # Check permissions
    if current_user["role"] == "manager" and member["manager_id"] != current_user["_id"]:
        raise HTTPException(status_code=403, detail="Not authorized")
    elif current_user["role"] == "team_member" and member["user_id"] != current_user["_id"]:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    return serialize_doc(member)


# ============================================================
# SESSIONS ROUTES
# ============================================================

@app.get("/api/sessions")
async def get_sessions(member_id: Optional[str] = None, current_user: dict = Depends(get_current_user)):
    """Get sessions"""
    query = {}
    
    if current_user["role"] == "manager":
        query["manager_id"] = current_user["_id"]
        if member_id:
            query["member_id"] = member_id
    else:
        # Team member can only see their own sessions
        member = await members_collection.find_one({"user_id": current_user["_id"]})
        if member:
            query["member_id"] = member["_id"]
        else:
            return []
    
    sessions_cursor = sessions_collection.find(query).sort("date", -1)
    sessions = await sessions_cursor.to_list(length=1000)
    return serialize_doc(sessions)


@app.get("/api/sessions/{session_id}")
async def get_session(session_id: str, current_user: dict = Depends(get_current_user)):
    """Get specific session"""
    session = await sessions_collection.find_one({"_id": session_id})
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Check permissions
    if current_user["role"] == "manager" and session["manager_id"] != current_user["_id"]:
        raise HTTPException(status_code=403, detail="Not authorized")
    elif current_user["role"] == "team_member":
        member = await members_collection.find_one({"user_id": current_user["_id"]})
        if not member or session["member_id"] != member["_id"]:
            raise HTTPException(status_code=403, detail="Not authorized")
    
    return serialize_doc(session)


@app.post("/api/sessions")
async def create_session(session_data: SessionCreate, current_user: dict = Depends(get_current_user)):
    """Create or update a session"""
    # Only managers can create sessions
    if current_user["role"] != "manager":
        raise HTTPException(status_code=403, detail="Only managers can create sessions")
    
    session_dict = session_data.model_dump()
    session_dict["created_at"] = datetime.utcnow()
    
    # If session has a pre_meeting reflection and manager_notes, it's complete - detect flags
    if session_dict.get("pre_meeting") and session_dict.get("manager_notes") and session_dict.get("status") == "completed":
        # Get member info
        member = await members_collection.find_one({"_id": session_dict["member_id"]})
        if member:
            # Get previous sessions for this member
            prev_sessions_cursor = sessions_collection.find({
                "member_id": session_dict["member_id"],
                "status": "completed"
            }).sort("date", -1).limit(5)
            prev_sessions_raw = await prev_sessions_cursor.to_list(length=5)
            prev_sessions = [serialize_doc(s) for s in prev_sessions_raw]
            
            # Create a temporary session object for flag detection
            from models import Session as SessionModel, PreMeetingReflection as PreMeetingModel
            temp_session = SessionModel(
                _id="temp",
                manager_id=session_dict["manager_id"],
                member_id=session_dict["member_id"],
                date=session_dict["date"],
                status=session_dict["status"],
                pre_meeting=PreMeetingModel(**session_dict["pre_meeting"]) if session_dict.get("pre_meeting") else None,
                manager_notes=session_dict.get("manager_notes"),
                actions=session_dict.get("actions", []),
                follow_ups=session_dict.get("follow_ups", [])
            )
            
            # Convert prev sessions to Session objects
            prev_session_objs = []
            for ps in prev_sessions:
                if ps.get("pre_meeting"):
                    try:
                        prev_session_objs.append(SessionModel(
                            _id=ps["_id"],
                            manager_id=ps["manager_id"],
                            member_id=ps["member_id"],
                            date=ps["date"],
                            status=ps["status"],
                            pre_meeting=PreMeetingModel(**ps["pre_meeting"]) if ps.get("pre_meeting") else None
                        ))
                    except Exception as e:
                        print(f"Warning: Could not parse previous session {ps['_id']}: {e}")
            
            # Detect flags
            try:
                detected_flags = await detect_flags_for_session(
                    temp_session,
                    prev_session_objs,
                    member["name"],
                    member["title"]
                )
                
                # Insert detected flags
                flag_ids = []
                for flag_data in detected_flags:
                    flag_data["created_at"] = datetime.utcnow().strftime("%Y-%m-%d")
                    result = await flags_collection.insert_one(flag_data)
                    flag_ids.append(str(result.inserted_id))
                
                session_dict["flags_detected"] = flag_ids
            except Exception as e:
                print(f"Warning: Flag detection failed: {e}")
                session_dict["flags_detected"] = []
            
            # Update member's last session date
            await members_collection.update_one(
                {"_id": session_dict["member_id"]},
                {"$set": {"last_session": session_dict["date"]}}
            )
    
    result = await sessions_collection.insert_one(session_dict)
    session_dict["_id"] = str(result.inserted_id)
    return serialize_doc(session_dict)


@app.post("/api/sessions/{session_id}/reflection")
async def submit_reflection(session_id: str, reflection: PreMeetingReflection, current_user: dict = Depends(get_current_user)):
    """Submit pre-meeting reflection for a session"""
    # Only team members can submit reflections
    if current_user["role"] != "team_member":
        raise HTTPException(status_code=403, detail="Only team members can submit reflections")
    
    # Get member record
    member = await members_collection.find_one({"user_id": current_user["_id"]})
    if not member:
        raise HTTPException(status_code=404, detail="Member record not found")
    
    session = await sessions_collection.find_one({"_id": session_id})
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    if session["member_id"] != member["_id"]:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Update session with pre_meeting data
    await sessions_collection.update_one(
        {"_id": session_id},
        {"$set": {"pre_meeting": reflection.model_dump()}}
    )
    
    updated_session = await sessions_collection.find_one({"_id": session_id})
    return serialize_doc(updated_session)


# ============================================================
# FLAGS ROUTES
# ============================================================

@app.get("/api/flags")
async def get_flags(status_filter: Optional[str] = "open", member_id: Optional[str] = None, 
                   current_user: dict = Depends(get_current_user)):
    """Get flags"""
    query = {}
    
    if current_user["role"] == "manager":
        # Get flags for all their team members
        members_cursor = members_collection.find({"manager_id": current_user["_id"]})
        members = await members_cursor.to_list(length=1000)
        member_ids = [m["_id"] for m in members]
        query["member_id"] = {"$in": member_ids}
    else:
        # Team member can only see their own flags
        member = await members_collection.find_one({"user_id": current_user["_id"]})
        if member:
            query["member_id"] = member["_id"]
        else:
            return []
    
    if status_filter:
        query["status"] = status_filter
    if member_id:
        query["member_id"] = member_id
    
    flags_cursor = flags_collection.find(query).sort("created_at", -1)
    flags = await flags_cursor.to_list(length=1000)
    return serialize_doc(flags)


@app.patch("/api/flags/{flag_id}")
async def update_flag(flag_id: str, status_update: str, note: Optional[str] = None,
                     current_user: dict = Depends(get_current_user)):
    """Update flag status (acknowledge/resolve)"""
    # Only managers can update flags
    if current_user["role"] != "manager":
        raise HTTPException(status_code=403, detail="Only managers can update flags")
    
    flag = await flags_collection.find_one({"_id": flag_id})
    if not flag:
        raise HTTPException(status_code=404, detail="Flag not found")
    
    # Check if this manager manages the team member
    member = await members_collection.find_one({"_id": flag["member_id"]})
    if not member or member["manager_id"] != current_user["_id"]:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    update_data = {"status": status_update}
    if note:
        update_data["manager_note"] = note
    if status_update == "resolved":
        update_data["resolved_at"] = datetime.utcnow().strftime("%Y-%m-%d")
    
    await flags_collection.update_one({"_id": flag_id}, {"$set": update_data})
    updated_flag = await flags_collection.find_one({"_id": flag_id})
    return serialize_doc(updated_flag)


# ============================================================
# AI ROUTES
# ============================================================

@app.post("/api/ai/risk")
async def analyze_risk_endpoint(request: RiskAnalysisRequest, current_user: dict = Depends(get_current_user)):
    """Analyze psychological safety risks"""
    # Only managers can request risk analysis
    if current_user["role"] != "manager":
        raise HTTPException(status_code=403, detail="Only managers can request risk analysis")
    
    try:
        result = await analyze_risk(
            member_name=request.member_name,
            member_title=request.member_title,
            reflection=request.reflection.model_dump(),
            previous_sessions=request.previous_sessions,
            active_flags=request.active_flags
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Risk analysis failed: {str(e)}")


@app.post("/api/ai/starters")
async def generate_starters_endpoint(request: ConversationStartersRequest, current_user: dict = Depends(get_current_user)):
    """Generate conversation starters"""
    # Only managers can request conversation starters
    if current_user["role"] != "manager":
        raise HTTPException(status_code=403, detail="Only managers can request conversation starters")
    
    try:
        result = await generate_conversation_starters(
            member_name=request.member_name,
            member_title=request.member_title,
            reflection=request.reflection.model_dump(),
            active_flags=request.active_flags
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Starter generation failed: {str(e)}")


@app.post("/api/ai/summary")
async def generate_summary_endpoint(request: SessionSummaryRequest, current_user: dict = Depends(get_current_user)):
    """Generate session summary"""
    # Only managers can request session summaries
    if current_user["role"] != "manager":
        raise HTTPException(status_code=403, detail="Only managers can request session summaries")
    
    try:
        result = await generate_session_summary(
            manager_notes=request.manager_notes.model_dump(),
            actions=request.actions
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Summary generation failed: {str(e)}")


# ============================================================
# DASHBOARD STATS ROUTES
# ============================================================

@app.get("/api/stats/dashboard")
async def get_dashboard_stats(current_user: dict = Depends(get_current_user)):
    """Get dashboard statistics for manager"""
    if current_user["role"] != "manager":
        raise HTTPException(status_code=403, detail="Only managers can view dashboard stats")
    
    # Get all team members
    members_cursor = members_collection.find({"manager_id": current_user["_id"]})
    members = await members_cursor.to_list(length=1000)
    member_ids = [m["_id"] for m in members]
    
    # Count upcoming sessions (next 7 days)
    from datetime import datetime
    current_date = datetime(2026, 3, 21)  # Using our seed data date
    upcoming_count = len([m for m in members if m.get("next_session") and 
                         (datetime.strptime(m["next_session"], "%Y-%m-%d") - current_date).days <= 7])
    
    # Count completed this month
    completed_cursor = sessions_collection.find({
        "manager_id": current_user["_id"],
        "status": "completed",
        "date": {"$gte": "2026-03-01"}
    })
    completed_count = await sessions_collection.count_documents({
        "manager_id": current_user["_id"],
        "status": "completed",
        "date": {"$gte": "2026-03-01"}
    })
    
    # Count active flags
    active_flags_count = await flags_collection.count_documents({
        "member_id": {"$in": member_ids},
        "status": "open"
    })
    
    # Calculate team health score (simplified)
    # Get latest session for each member and average their scores
    total_score = 0
    members_with_sessions = 0
    
    for member in members:
        latest_session = await sessions_collection.find_one(
            {"member_id": member["_id"], "status": "completed"},
            sort=[("date", -1)]
        )
        if latest_session and latest_session.get("pre_meeting"):
            pm = latest_session["pre_meeting"]
            scores = []
            for field in ["feeling_about_work", "safe_to_raise_concerns", "feel_supported", "workload_manageable", "target_confidence"]:
                if pm.get(field):
                    scores.append(pm[field])
            if scores:
                avg = sum(scores) / len(scores)
                member_score = (avg / 5) * 100
                
                # Deduct for flags
                member_flags = await flags_collection.count_documents({
                    "member_id": member["_id"],
                    "status": "open"
                })
                member_score -= (member_flags * 5)
                member_score = max(0, min(100, member_score))
                
                total_score += member_score
                members_with_sessions += 1
    
    team_health_score = round(total_score / members_with_sessions) if members_with_sessions > 0 else 0
    
    return {
        "upcoming_sessions": upcoming_count,
        "completed_this_month": completed_count,
        "team_health_score": team_health_score,
        "active_flags": active_flags_count
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import List, Optional
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
import os
from dotenv import load_dotenv
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests

from database import init_db, users_collection, members_collection, submissions_collection, flags_collection
from models import (
    User, UserLogin, Token, TeamMember,
    Submission, SubmissionCreate, WeeklyReflection, ResponseItem,
    Flag
)
from auth import authenticate_user, create_access_token
from flag_detection import detect_flags_for_submission, check_missing_submissions
from seed_data import seed_database, generate_mondays, MONDAY_DATES

load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET", "performos_jwt_secret_key")
ALGORITHM = "HS256"
CURRENT_WEEK = "2026-03-23"  # The "THIS WEEK" for demo purposes

# Get allowed origins from environment or use defaults
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "https://performos.digital,http://localhost:3000,https://team-health-hub-2.preview.emergentagent.com").split(",")

app = FastAPI(title="PerformOS One-on-One Builder V2 API")

# CORS middleware - use environment variable for flexibility
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for now - deployment issue
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
    try:
        print("🚀 Starting PerformOS backend...")
        await init_db()
        print("✅ Database indexes created")
        
        # Check if database is empty and seed if needed
        user_count = await users_collection.count_documents({})
        print(f"📊 Found {user_count} users in database")
        
        if user_count == 0:
            print("🌱 Database empty - seeding with demo data...")
            await seed_database()
            print("✅ Database seeded successfully!")
        else:
            print(f"✅ Database already initialized with {user_count} users")
    except Exception as e:
        print(f"❌ STARTUP ERROR: {str(e)}")
        # Don't crash - let app start anyway
        import traceback
        traceback.print_exc()


# Root API endpoint moved - now served by React catch-all
# @app.get("/")
# async def root():
#     return {"message": "PerformOS One-on-One Builder V2 API", "status": "running", "current_week": CURRENT_WEEK}


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



@app.post("/api/auth/google/login")
async def google_login(google_token: dict):
    """
    Authenticate user with Google ID token
    Only allows existing users - no new registrations
    """
    try:
        # Get Google client ID from environment
        GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
        if not GOOGLE_CLIENT_ID:
            raise HTTPException(status_code=500, detail="Google Client ID not configured")
        
        # Verify the Google ID token
        token = google_token.get("token")
        if not token:
            raise HTTPException(status_code=400, detail="Google token required")
        
        try:
            # Verify token with Google
            idinfo = id_token.verify_oauth2_token(
                token, 
                google_requests.Request(), 
                GOOGLE_CLIENT_ID
            )
            
            # Extract user email from Google token
            email = idinfo.get("email")
            if not email:
                raise HTTPException(status_code=400, detail="Email not found in Google token")
            
        except ValueError as e:
            # Invalid token
            raise HTTPException(status_code=401, detail=f"Invalid Google token: {str(e)}")
        
        # Look up user in database by email
        user = await users_collection.find_one({"email": email})
        
        if not user:
            # User doesn't exist - reject login
            raise HTTPException(
                status_code=403, 
                detail="No account found. Please contact your administrator."
            )
        
        # User exists - create JWT token same as regular login
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user["_id"]},
            expires_delta=access_token_expires
        )
        
        # Return same format as regular login
        user_data = serialize_doc(user)
        user_data.pop("hashed_password", None)
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": user_data
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Google login failed: {str(e)}")


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
        members_cursor = members_collection.find({"manager_id": current_user["_id"]})
        members = await members_cursor.to_list(length=1000)
        return serialize_doc(members)
    else:
        member = await members_collection.find_one({"user_id": current_user["_id"]})
        return serialize_doc([member] if member else [])


# ============================================================
# WEEKLY SCHEDULE ROUTES
# ============================================================

@app.get("/api/schedule/weeks")
async def get_weekly_schedule():
    """Get all Monday dates for the schedule (March 23 - June 29, 2026)"""
    return {
        "weeks": MONDAY_DATES,
        "current_week": CURRENT_WEEK
    }


@app.get("/api/schedule/status")
async def get_schedule_status(current_user: dict = Depends(get_current_user)):
    """Get submission status for all weeks for the current team member"""
    # Get member record
    member = await members_collection.find_one({"user_id": current_user["_id"]})
    if not member:
        raise HTTPException(status_code=404, detail="Member record not found")
    
    # Get all submissions for this member
    submissions_cursor = submissions_collection.find({"member_id": member["_id"]})
    submissions = await submissions_cursor.to_list(length=1000)
    submission_dates = {sub["date"]: str(sub["_id"]) for sub in submissions}
    
    # Build status for each week
    schedule_status = []
    for date in MONDAY_DATES:
        schedule_status.append({
            "date": date,
            "submitted": date in submission_dates,
            "submission_id": submission_dates.get(date),
            "is_current_week": date == CURRENT_WEEK
        })
    
    return schedule_status


# ============================================================
# SUBMISSIONS ROUTES
# ============================================================

@app.get("/api/submissions")
async def get_submissions(date: Optional[str] = None, current_user: dict = Depends(get_current_user)):
    """Get submissions - managers see all their team's, members see their own"""
    query = {}
    
    if current_user["role"] == "manager":
        # Get all team members
        members_cursor = members_collection.find({"manager_id": current_user["_id"]})
        members = await members_cursor.to_list(length=1000)
        member_ids = [m["_id"] for m in members]
        query["member_id"] = {"$in": member_ids}
    else:
        # Team member sees only their own
        member = await members_collection.find_one({"user_id": current_user["_id"]})
        if member:
            query["member_id"] = member["_id"]
        else:
            return []
    
    if date:
        query["date"] = date
    
    submissions_cursor = submissions_collection.find(query).sort("date", -1)
    submissions = await submissions_cursor.to_list(length=1000)
    return serialize_doc(submissions)


@app.get("/api/submissions/{submission_id}")
async def get_submission(submission_id: str, current_user: dict = Depends(get_current_user)):
    """Get specific submission"""
    submission = await submissions_collection.find_one({"_id": submission_id})
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")
    
    # Check permissions
    if current_user["role"] == "manager":
        member = await members_collection.find_one({"_id": submission["member_id"]})
        if not member or member["manager_id"] != current_user["_id"]:
            raise HTTPException(status_code=403, detail="Not authorized")
    else:
        member = await members_collection.find_one({"user_id": current_user["_id"]})
        if not member or submission["member_id"] != member["_id"]:
            raise HTTPException(status_code=403, detail="Not authorized")
    
    return serialize_doc(submission)


@app.post("/api/submissions")
async def create_submission(submission_data: SubmissionCreate, current_user: dict = Depends(get_current_user)):
    """Submit weekly reflection"""
    # Only team members can submit
    if current_user["role"] != "team_member":
        raise HTTPException(status_code=403, detail="Only team members can submit reflections")
    
    # Get member record
    member = await members_collection.find_one({"user_id": current_user["_id"]})
    if not member:
        raise HTTPException(status_code=404, detail="Member record not found")
    
    # Check if submission already exists for this date (prevent duplicates)
    existing = await submissions_collection.find_one({
        "member_id": member["_id"],
        "date": submission_data.date
    })
    if existing:
        # If already locked, cannot resubmit
        if existing.get("locked"):
            raise HTTPException(status_code=400, detail="This week's reflection has already been submitted and locked")
        raise HTTPException(status_code=400, detail="Submission already exists for this week")
    
    # Create submission with locked timestamp
    submission_dict = submission_data.model_dump()
    submission_dict["member_id"] = member["_id"]
    submission_dict["submitted_at"] = datetime.utcnow().isoformat()
    submission_dict["locked"] = datetime.utcnow().isoformat()  # Lock immediately upon submission
    
    result = await submissions_collection.insert_one(submission_dict)
    submission_id = str(result.inserted_id)
    
    # Detect flags
    flags = await detect_flags_for_submission(
        submission_id=submission_id,
        member_id=member["_id"],
        member_name=member["name"],
        date=submission_data.date,
        responses=submission_data.responses.model_dump()
    )
    
    # Insert flags
    flag_ids = []
    for flag_data in flags:
        flag_result = await flags_collection.insert_one(flag_data)
        flag_ids.append(str(flag_result.inserted_id))
    
    # Update submission with flag IDs
    await submissions_collection.update_one(
        {"_id": submission_id},
        {"$set": {"flags_detected": flag_ids}}
    )
    
    submission_dict["_id"] = submission_id
    submission_dict["flags_detected"] = flag_ids
    
    return serialize_doc(submission_dict)


# ============================================================
# THIS WEEK SUBMISSIONS (Manager View)
# ============================================================

@app.get("/api/this-week/submissions")
async def get_this_week_submissions(current_user: dict = Depends(get_current_user)):
    """Get all submissions for THIS WEEK for manager's team"""
    if current_user["role"] != "manager":
        raise HTTPException(status_code=403, detail="Only managers can view this")
    
    # Get all team members
    members_cursor = members_collection.find({"manager_id": current_user["_id"]})
    members = await members_cursor.to_list(length=1000)
    member_map = {m["_id"]: m for m in members}
    member_ids = list(member_map.keys())
    
    # Get submissions for current week
    submissions_cursor = submissions_collection.find({
        "member_id": {"$in": member_ids},
        "date": CURRENT_WEEK
    })
    submissions = await submissions_cursor.to_list(length=1000)
    
    # Build result with member info
    result = []
    for member_id, member in member_map.items():
        submission = next((s for s in submissions if s["member_id"] == member_id), None)
        result.append({
            "member": serialize_doc(member),
            "submission": serialize_doc(submission) if submission else None,
            "has_submitted": submission is not None
        })
    
    # Check for missing submissions and create manager gap flags
    await check_missing_submissions(current_user["_id"], CURRENT_WEEK)
    
    return result


# ============================================================
# FLAGS ROUTES
# ============================================================

@app.get("/api/flags")
async def get_flags(status_filter: Optional[str] = None, current_user: dict = Depends(get_current_user)):
    """Get flags - defaults to showing open + in_progress (not resolved)"""
    query = {}
    
    if current_user["role"] == "manager":
        members_cursor = members_collection.find({"manager_id": current_user["_id"]})
        members = await members_cursor.to_list(length=1000)
        member_ids = [m["_id"] for m in members]
        query["member_id"] = {"$in": member_ids}
    else:
        member = await members_collection.find_one({"user_id": current_user["_id"]})
        if member:
            query["member_id"] = member["_id"]
        else:
            return []
    
    if status_filter:
        query["status"] = status_filter
    else:
        # Default: show open and in_progress, not resolved
        query["status"] = {"$ne": "resolved"}
    
    flags_cursor = flags_collection.find(query).sort("date", -1)
    flags = await flags_cursor.to_list(length=1000)
    return serialize_doc(flags)


@app.patch("/api/flags/{flag_id}")
async def update_flag(flag_id: str, update_data: dict, current_user: dict = Depends(get_current_user)):
    """Update flag status"""
    if current_user["role"] != "manager":
        raise HTTPException(status_code=403, detail="Only managers can update flags")
    
    flag = await flags_collection.find_one({"_id": flag_id})
    if not flag:
        raise HTTPException(status_code=404, detail="Flag not found")
    
    member = await members_collection.find_one({"_id": flag["member_id"]})
    if not member or member["manager_id"] != current_user["_id"]:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    update_fields = {}
    if "status" in update_data:
        update_fields["status"] = update_data["status"]
    if "manager_note" in update_data:
        update_fields["manager_note"] = update_data["manager_note"]
    if update_data.get("status") == "resolved":
        update_fields["resolved_at"] = datetime.utcnow().strftime("%Y-%m-%d")
    
    await flags_collection.update_one({"_id": flag_id}, {"$set": update_fields})
    updated_flag = await flags_collection.find_one({"_id": flag_id})
    return serialize_doc(updated_flag)



@app.post("/api/flags/{flag_id}/actions")
async def add_flag_action(flag_id: str, action_data: dict, current_user: dict = Depends(get_current_user)):
    """Add an action to a flag (manager only) - timestamp is SERVER-GENERATED"""
    if current_user["role"] != "manager":
        raise HTTPException(status_code=403, detail="Only managers can add flag actions")
    
    flag = await flags_collection.find_one({"_id": flag_id})
    if not flag:
        raise HTTPException(status_code=404, detail="Flag not found")
    
    member = await members_collection.find_one({"_id": flag["member_id"]})
    if not member or member["manager_id"] != current_user["_id"]:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Create new action with SERVER-GENERATED timestamp
    import uuid
    action = {
        "id": str(uuid.uuid4()),
        "note": action_data.get("note"),
        "savedAt": datetime.now(timezone.utc).isoformat(),  # SERVER-GENERATED, tamper-proof
        "confirmed": action_data.get("confirmed", False)
    }
    
    # Add action to flag's actions array
    await flags_collection.update_one(
        {"_id": flag_id},
        {"$push": {"actions": action}}
    )
    
    # Auto-update status to "in_progress" if this is the first action
    if not flag.get("actions") or len(flag.get("actions", [])) == 0:
        await flags_collection.update_one(
            {"_id": flag_id},
            {"$set": {"status": "in_progress"}}
        )
    
    updated_flag = await flags_collection.find_one({"_id": flag_id})
    return serialize_doc(updated_flag)

@app.patch("/api/flags/{flag_id}/resolve")
async def resolve_flag(flag_id: str, resolution_data: dict, current_user: dict = Depends(get_current_user)):
    """Resolve a flag with final note"""
    if current_user["role"] != "manager":
        raise HTTPException(status_code=403, detail="Only managers can resolve flags")
    
    flag = await flags_collection.find_one({"_id": flag_id})
    if not flag:
        raise HTTPException(status_code=404, detail="Flag not found")
    
    # Check if flag has at least one action
    if not flag.get("actions") or len(flag.get("actions", [])) == 0:
        raise HTTPException(status_code=400, detail="Cannot resolve flag without logging at least one action")
    
    member = await members_collection.find_one({"_id": flag["member_id"]})
    if not member or member["manager_id"] != current_user["_id"]:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Update flag as resolved
    await flags_collection.update_one(
        {"_id": flag_id},
        {"$set": {
            "status": "resolved",
            "resolvedAt": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
            "resolvedNote": resolution_data.get("note", "")
        }}
    )
    
    updated_flag = await flags_collection.find_one({"_id": flag_id})
    return serialize_doc(updated_flag)


# ============================================================
# DASHBOARD STATS
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
    
    # Count submissions for this week
    this_week_count = await submissions_collection.count_documents({
        "member_id": {"$in": member_ids},
        "date": CURRENT_WEEK
    })
    
    # Count total submissions
    total_submissions = await submissions_collection.count_documents({
        "member_id": {"$in": member_ids}
    })
    
    # Count active flags
    active_flags_count = await flags_collection.count_documents({
        "member_id": {"$in": member_ids},
        "status": "open"
    })
    
    # Calculate team health score
    submissions_cursor = submissions_collection.find({
        "member_id": {"$in": member_ids},
        "date": CURRENT_WEEK
    })
    this_week_submissions = await submissions_cursor.to_list(length=1000)
    
    total_health = 0
    member_count = 0
    
    for sub in this_week_submissions:
        responses = sub.get("responses", {})
        wellbeing_fields = ["feeling_about_work", "safe_to_raise_concerns", "feel_supported", "workload_manageable", "target_confidence"]
        scores = []
        for field in wellbeing_fields:
            if responses.get(field) and isinstance(responses[field], dict):
                rating = responses[field].get("rating")
                if rating:
                    scores.append(rating)
        
        if scores:
            member_health = (sum(scores) / len(scores) / 5) * 100
            # Deduct for flags
            member_flags = await flags_collection.count_documents({
                "member_id": sub["member_id"],
                "status": "open"
            })
            member_health -= (member_flags * 8)
            member_health = max(0, min(100, member_health))
            total_health += member_health
            member_count += 1
    
    team_health_score = round(total_health / member_count) if member_count > 0 else 0
    
    return {
        "this_week_submissions": this_week_count,
        "total_team_members": len(members),
        "total_submissions": total_submissions,
        "team_health_score": team_health_score,
        "active_flags": active_flags_count,
        "current_week": CURRENT_WEEK
    }


@app.post("/api/generate-coaching")
async def generate_coaching(payload: dict):
    """Generate AI coaching for manager using OpenAI API"""
    import httpx
    
    # Get OpenAI API key from environment
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise HTTPException(status_code=500, detail="OpenAI API key not configured")
    
    # Call OpenAI API
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {openai_api_key}"
                },
                json={
                    "model": "gpt-4-turbo-preview",
                    "messages": [{"role": "user", "content": payload.get("prompt")}],
                    "max_tokens": 3000,
                    "temperature": 0.7
                },
                timeout=90.0
            )
            
            if response.status_code != 200:
                error_text = response.text
                raise HTTPException(status_code=500, detail=f"OpenAI API request failed: {error_text}")
            
            return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate coaching: {str(e)}")


@app.post("/api/generate-exec-summary")
async def generate_exec_summary(payload: dict):
    """Generate AI executive summary using OpenAI API"""
    import httpx
    
    # Get OpenAI API key from environment
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise HTTPException(status_code=500, detail="OpenAI API key not configured")
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {openai_api_key}"
                },
                json={
                    "model": "gpt-4-turbo-preview",
                    "messages": [{"role": "user", "content": payload.get("prompt")}],
                    "max_tokens": 4000,
                    "temperature": 0.7
                },
                timeout=90.0
            )
            
            if response.status_code != 200:
                error_text = response.text
                raise HTTPException(status_code=500, detail=f"OpenAI API request failed: {error_text}")
            
            return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate executive summary: {str(e)}")


# ============================================================
# DATABASE SEED ENDPOINT (REMOVE AFTER FIRST USE)
# ============================================================
@app.get("/api/admin/seed")
@app.post("/api/admin/seed")
async def seed_database_endpoint():
    """One-time endpoint to seed the database with demo data"""
    try:
        from seed_data import seed_database
        await seed_database()
        return {"message": "✅ Database seeded successfully with demo users", "users": ["rachel@performos.io", "alex@performos.io", "ashley@performos.io"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Seed failed: {str(e)}")

# Static files now served by separate frontend process on port 3000


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8001))
    uvicorn.run(app, host="0.0.0.0", port=port)

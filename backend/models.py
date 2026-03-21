from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, EmailStr
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


# User Models
class UserBase(BaseModel):
    email: EmailStr
    name: str
    role: str  # "manager" or "team_member"
    title: Optional[str] = None

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: str = Field(alias="_id")
    created_at: Optional[datetime] = None

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    user: User


# Team Member Models
class TeamMemberBase(BaseModel):
    name: str
    email: EmailStr
    title: str
    manager_id: str
    cadence: str  # "weekly", "fortnightly", "monthly"
    next_session: Optional[str] = None
    last_session: Optional[str] = None
    avatar: Optional[str] = None

class TeamMemberCreate(TeamMemberBase):
    pass

class TeamMember(TeamMemberBase):
    id: str = Field(alias="_id")
    user_id: str

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


# Session Models
class PreMeetingReflection(BaseModel):
    proud_of: Optional[str] = ""
    stuck_on: Optional[str] = ""
    need_from_manager: Optional[str] = ""
    target_confidence: Optional[int] = None
    feeling_about_work: Optional[int] = None
    safe_to_raise_concerns: Optional[int] = None
    anything_affecting: Optional[str] = ""
    feel_supported: Optional[int] = None
    workload_manageable: Optional[int] = None

class ManagerNotes(BaseModel):
    check_in: Optional[str] = ""
    results_review: Optional[str] = ""
    goal_alignment: Optional[str] = ""
    support_development: Optional[str] = ""
    wellbeing: Optional[str] = ""
    private_note: Optional[str] = ""

class Action(BaseModel):
    action: str
    owner: str  # "manager" or "team_member"
    status: str = "pending"  # "pending" or "completed"

class SessionBase(BaseModel):
    manager_id: str
    member_id: str
    date: str
    status: str = "scheduled"  # "scheduled", "in_progress", "completed"
    pre_meeting: Optional[PreMeetingReflection] = None
    manager_notes: Optional[ManagerNotes] = None
    actions: Optional[List[Action]] = []
    follow_ups: Optional[List[str]] = []
    flags_detected: Optional[List[str]] = []  # List of flag IDs
    ai_summary: Optional[str] = None

class SessionCreate(SessionBase):
    pass

class Session(SessionBase):
    id: str = Field(alias="_id")
    created_at: Optional[datetime] = None

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


# Flag Models
class FlagBase(BaseModel):
    member_id: str
    session_id: Optional[str] = None
    category: str  # "wellbeing", "psychological_safety", "workload", "engagement", "performance_confidence", "team_dynamics", "manager_gap"
    severity: str  # "watch", "concern", "action_required"
    signal: str
    status: str = "open"  # "open", "acknowledged", "resolved"
    manager_note: Optional[str] = None
    resolved_at: Optional[str] = None

class FlagCreate(FlagBase):
    pass

class Flag(FlagBase):
    id: str = Field(alias="_id")
    created_at: str

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


# AI Request/Response Models
class RiskAnalysisRequest(BaseModel):
    member_id: str
    member_name: str
    member_title: str
    reflection: PreMeetingReflection
    previous_sessions: Optional[List[Dict[str, Any]]] = []
    active_flags: Optional[List[Dict[str, Any]]] = []

class RiskFlag(BaseModel):
    category: str
    severity: str
    signal: str
    quote_trigger: Optional[str] = ""

class RiskAnalysisResponse(BaseModel):
    flags: List[RiskFlag]
    overall_sentiment: str
    summary: str

class ConversationStartersRequest(BaseModel):
    member_name: str
    member_title: str
    reflection: PreMeetingReflection
    active_flags: Optional[List[Dict[str, Any]]] = []

class ConversationStartersResponse(BaseModel):
    starters: List[str]

class SessionSummaryRequest(BaseModel):
    manager_notes: ManagerNotes
    actions: List[Action]

class KeyAction(BaseModel):
    action: str
    owner: str
    due: str

class SessionSummaryResponse(BaseModel):
    summary: str
    key_actions: List[KeyAction]
    follow_ups: List[str]
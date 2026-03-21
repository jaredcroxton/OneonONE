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

class TeamMemberCreate(TeamMemberBase):
    pass

class TeamMember(TeamMemberBase):
    id: str = Field(alias="_id")
    user_id: str

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


# NEW: Weekly Submission Models with dual rating+comment
class ResponseItem(BaseModel):
    rating: int  # 1-5
    comment: str

class WeeklyReflection(BaseModel):
    # Performance questions
    proud_of: Optional[ResponseItem] = None
    stuck_on: Optional[ResponseItem] = None
    need_from_manager: Optional[ResponseItem] = None
    target_confidence: Optional[ResponseItem] = None
    # Wellbeing questions
    feeling_about_work: Optional[ResponseItem] = None
    safe_to_raise_concerns: Optional[ResponseItem] = None
    feel_supported: Optional[ResponseItem] = None
    workload_manageable: Optional[ResponseItem] = None
    anything_affecting: Optional[ResponseItem] = None

class SubmissionBase(BaseModel):
    member_id: str
    date: str  # Monday date (YYYY-MM-DD)
    responses: WeeklyReflection
    submitted_at: Optional[str] = None
    locked: Optional[str] = None  # Timestamp when submission was locked

class SubmissionCreate(SubmissionBase):
    pass

class Submission(SubmissionBase):
    id: str = Field(alias="_id")
    flags_detected: Optional[List[str]] = []  # List of flag IDs

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


# Flag Models with comment snippets
class FlagBase(BaseModel):
    member_id: str
    submission_id: Optional[str] = None
    date: str  # Monday date
    category: str  # "wellbeing", "psychological_safety", "workload", "engagement", "performance_confidence", "team_dynamics", "manager_gap"
    severity: str  # "watch", "concern", "action_required"
    signal: str  # Description of the flag
    comment_snippet: Optional[str] = None  # The comment that triggered this flag
    status: str = "open"  # "open", "acknowledged", "resolved"
    manager_note: Optional[str] = None
    resolved_at: Optional[str] = None

class FlagCreate(FlagBase):
    pass

class Flag(FlagBase):
    id: str = Field(alias="_id")

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


# AI Request/Response Models (unchanged but included for completeness)
class AIRiskAnalysisRequest(BaseModel):
    member_name: str
    member_title: str
    responses: Dict[str, ResponseItem]
    previous_submissions: Optional[List[Dict]] = []

class RiskFlag(BaseModel):
    category: str
    severity: str
    signal: str
    comment_snippet: Optional[str] = ""

class AIRiskAnalysisResponse(BaseModel):
    flags: List[RiskFlag]
    overall_sentiment: str
    summary: str
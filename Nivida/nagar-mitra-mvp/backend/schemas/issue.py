from pydantic import BaseModel, validator
from typing import Optional, List
from datetime import datetime
from models.issue import IssueStatus, IssuePriority

class IssueBase(BaseModel):
    title: str
    description: str
    category: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    address: Optional[str] = None

class IssueCreate(IssueBase):
    @validator('title')
    def validate_title(cls, v):
        if len(v.strip()) < 5:
            raise ValueError('Title must be at least 5 characters long')
        return v.strip()
    
    @validator('description')
    def validate_description(cls, v):
        if len(v.strip()) < 10:
            raise ValueError('Description must be at least 10 characters long')
        return v.strip()

class IssueUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[IssueStatus] = None
    priority: Optional[IssuePriority] = None
    worker_id: Optional[int] = None
    department_id: Optional[int] = None

class IssueMediaResponse(BaseModel):
    id: int
    file_path: str
    file_type: str
    original_filename: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class IssueResponse(IssueBase):
    id: int
    status: IssueStatus
    priority: IssuePriority
    user_id: int
    department_id: Optional[int] = None
    worker_id: Optional[int] = None
    ai_confidence: float
    needs_manual_review: bool
    upvotes: int
    downvotes: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    resolved_at: Optional[datetime] = None
    media: List[IssueMediaResponse] = []
    
    class Config:
        from_attributes = True

class IssueListResponse(BaseModel):
    issues: List[IssueResponse]
    total: int
    page: int
    per_page: int
    
class IssueVoteRequest(BaseModel):
    vote_type: str  # "up" or "down"
    
    @validator('vote_type')
    def validate_vote_type(cls, v):
        if v not in ['up', 'down']:
            raise ValueError('vote_type must be "up" or "down"')
        return v
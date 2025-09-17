import os
import uuid
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List, Optional
import shutil

from database import get_db
from models.user import User
from models.issue import Issue, IssueMedia, IssueStatus
from schemas.issue import IssueCreate, IssueResponse, IssueUpdate, IssueVoteRequest, IssueListResponse
from utils.auth import get_current_active_user, get_current_admin_user
from services.classification import get_classifier

router = APIRouter()

# Allowed file types and max size
ALLOWED_FILE_TYPES = {'image/jpeg', 'image/png', 'image/gif', 'video/mp4', 'audio/mpeg', 'audio/wav'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

def save_uploaded_file(file: UploadFile, issue_id: int) -> str:
    """Save uploaded file and return file path"""
    # Create uploads directory if it doesn't exist
    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)
    
    # Generate unique filename
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{issue_id}_{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(upload_dir, unique_filename)
    
    # Save file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    return file_path

@router.post("/", response_model=IssueResponse)
async def create_issue(
    title: str = Form(...),
    description: str = Form(...),
    latitude: Optional[float] = Form(None),
    longitude: Optional[float] = Form(None),
    address: Optional[str] = Form(None),
    files: List[UploadFile] = File(None),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create a new issue with optional media files"""
    
    # Validate files if provided
    if files:
        for file in files:
            if file.content_type not in ALLOWED_FILE_TYPES:
                raise HTTPException(
                    status_code=400,
                    detail=f"File type {file.content_type} not allowed"
                )
            
            # Note: file.size might not be available in all cases
            # In production, you'd want to check file size during upload
    
    # Create issue data
    issue_data = {
        "title": title.strip(),
        "description": description.strip(),
        "latitude": latitude,
        "longitude": longitude,
        "address": address,
        "user_id": current_user.id
    }
    
    # Use AI classifier to categorize the issue
    classifier = get_classifier(db)
    dept_id, confidence, needs_review = classifier.classify_issue(title, description)
    
    issue_data.update({
        "department_id": dept_id,
        "ai_confidence": confidence,
        "needs_manual_review": needs_review,
        "category": "general" if not dept_id else None  # Will be set by department
    })
    
    # Create issue
    db_issue = Issue(**issue_data)
    db.add(db_issue)
    db.commit()
    db.refresh(db_issue)
    
    # Handle file uploads if any
    if files and files[0].filename:  # Check if files were actually uploaded
        for file in files:
            if file.filename:  # Skip empty files
                file_path = save_uploaded_file(file, db_issue.id)
                
                # Determine file type
                file_type = "image" if file.content_type.startswith("image") else \
                           "video" if file.content_type.startswith("video") else "audio"
                
                # Create media record
                media = IssueMedia(
                    issue_id=db_issue.id,
                    file_path=file_path,
                    file_type=file_type,
                    file_size=0,  # Would calculate in production
                    original_filename=file.filename
                )
                db.add(media)
        
        db.commit()
        db.refresh(db_issue)
    
    return db_issue

@router.get("/", response_model=IssueListResponse)
async def get_issues(
    skip: int = 0,
    limit: int = 20,
    status: Optional[IssueStatus] = None,
    department_id: Optional[int] = None,
    user_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Get issues with optional filtering"""
    query = db.query(Issue)
    
    # Apply filters
    if status:
        query = query.filter(Issue.status == status)
    if department_id:
        query = query.filter(Issue.department_id == department_id)
    if user_id:
        query = query.filter(Issue.user_id == user_id)
    
    # Get total count
    total = query.count()
    
    # Get paginated results
    issues = query.offset(skip).limit(limit).all()
    
    return {
        "issues": issues,
        "total": total,
        "page": skip // limit + 1,
        "per_page": limit
    }

@router.get("/my", response_model=List[IssueResponse])
async def get_my_issues(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get current user's issues"""
    issues = db.query(Issue).filter(Issue.user_id == current_user.id).all()
    return issues

@router.get("/{issue_id}", response_model=IssueResponse)
async def get_issue(issue_id: int, db: Session = Depends(get_db)):
    """Get issue by ID"""
    issue = db.query(Issue).filter(Issue.id == issue_id).first()
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")
    return issue

@router.put("/{issue_id}", response_model=IssueResponse)
async def update_issue(
    issue_id: int,
    issue_update: IssueUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update issue (admin or issue owner only)"""
    issue = db.query(Issue).filter(Issue.id == issue_id).first()
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")
    
    # Check permissions
    if not current_user.is_admin and issue.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not enough permissions"
        )
    
    # Update fields
    update_data = issue_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(issue, field, value)
    
    # If status is being changed to resolved, set resolved_at
    if issue_update.status == IssueStatus.RESOLVED and issue.resolved_at is None:
        issue.resolved_at = datetime.utcnow()
    
    db.commit()
    db.refresh(issue)
    return issue

@router.post("/{issue_id}/vote")
async def vote_on_issue(
    issue_id: int,
    vote_request: IssueVoteRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Vote on an issue (upvote or downvote)"""
    issue = db.query(Issue).filter(Issue.id == issue_id).first()
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")
    
    # In a full implementation, you'd track user votes to prevent duplicate voting
    # For MVP, we'll just increment the counters
    if vote_request.vote_type == "up":
        issue.upvotes += 1
    else:
        issue.downvotes += 1
    
    db.commit()
    
    return {"message": "Vote recorded", "upvotes": issue.upvotes, "downvotes": issue.downvotes}

@router.get("/{issue_id}/media/{media_id}")
async def get_media_file(issue_id: int, media_id: int, db: Session = Depends(get_db)):
    """Serve media file"""
    media = db.query(IssueMedia).filter(
        IssueMedia.id == media_id,
        IssueMedia.issue_id == issue_id
    ).first()
    
    if not media:
        raise HTTPException(status_code=404, detail="Media not found")
    
    if not os.path.exists(media.file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(media.file_path, filename=media.original_filename)

@router.delete("/{issue_id}")
async def delete_issue(
    issue_id: int,
    admin_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Delete issue (admin only)"""
    issue = db.query(Issue).filter(Issue.id == issue_id).first()
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")
    
    # Delete associated media files
    for media in issue.media:
        if os.path.exists(media.file_path):
            os.remove(media.file_path)
    
    db.delete(issue)
    db.commit()
    
    return {"message": "Issue deleted successfully"}
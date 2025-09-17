from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Dict, Any

from database import get_db
from models.user import User
from models.issue import Issue, IssueStatus
from models.department import Department
from models.worker import Worker
from utils.auth import get_current_admin_user

router = APIRouter()

@router.get("/dashboard")
async def get_dashboard_stats(
    admin_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Get dashboard statistics for admin"""
    
    # Issue statistics
    total_issues = db.query(Issue).count()
    pending_issues = db.query(Issue).filter(Issue.status == IssueStatus.PENDING).count()
    in_progress_issues = db.query(Issue).filter(Issue.status == IssueStatus.IN_PROGRESS).count()
    resolved_issues = db.query(Issue).filter(Issue.status == IssueStatus.RESOLVED).count()
    
    # Issues by department
    dept_stats = db.query(
        Department.name,
        func.count(Issue.id).label('count')
    ).join(Issue, Department.id == Issue.department_id, isouter=True)\
     .group_by(Department.id, Department.name).all()
    
    # Recent issues
    recent_issues = db.query(Issue).order_by(Issue.created_at.desc()).limit(5).all()
    
    # User statistics
    total_users = db.query(User).filter(User.is_admin == False).count()
    total_workers = db.query(Worker).count()
    
    return {
        "issue_stats": {
            "total": total_issues,
            "pending": pending_issues,
            "in_progress": in_progress_issues,
            "resolved": resolved_issues
        },
        "department_stats": [
            {"department": name, "count": count} 
            for name, count in dept_stats
        ],
        "recent_issues": [
            {
                "id": issue.id,
                "title": issue.title,
                "status": issue.status,
                "created_at": issue.created_at,
                "user_id": issue.user_id
            }
            for issue in recent_issues
        ],
        "user_stats": {
            "total_citizens": total_users,
            "total_workers": total_workers
        }
    }

@router.get("/issues/pending")
async def get_pending_issues(
    admin_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Get all pending issues that need manual review"""
    issues = db.query(Issue).filter(
        Issue.needs_manual_review == True,
        Issue.status == IssueStatus.PENDING
    ).order_by(Issue.created_at.desc()).all()
    
    return issues

@router.post("/issues/{issue_id}/assign/{worker_id}")
async def assign_issue_to_worker(
    issue_id: int,
    worker_id: int,
    admin_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Assign an issue to a worker"""
    # Get issue
    issue = db.query(Issue).filter(Issue.id == issue_id).first()
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")
    
    # Get worker
    worker = db.query(Worker).filter(Worker.id == worker_id).first()
    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found")
    
    # Assign worker and update status
    issue.worker_id = worker_id
    issue.department_id = worker.department_id
    issue.status = IssueStatus.ASSIGNED
    issue.needs_manual_review = False
    
    db.commit()
    db.refresh(issue)
    
    return {"message": "Issue assigned successfully", "issue": issue}

@router.get("/departments")
async def get_departments(
    admin_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Get all departments"""
    departments = db.query(Department).all()
    return departments

@router.get("/workers")
async def get_workers(
    department_id: int = None,
    admin_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Get all workers, optionally filtered by department"""
    query = db.query(Worker)
    
    if department_id:
        query = query.filter(Worker.department_id == department_id)
    
    workers = query.all()
    return workers

@router.get("/analytics/trends")
async def get_issue_trends(
    admin_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Get issue trends for analytics"""
    
    # Issues by status over time (simplified for MVP)
    status_distribution = db.query(
        Issue.status,
        func.count(Issue.id).label('count')
    ).group_by(Issue.status).all()
    
    # Issues by department
    dept_distribution = db.query(
        Department.name,
        func.count(Issue.id).label('count')
    ).join(Issue, Department.id == Issue.department_id, isouter=True)\
     .group_by(Department.name).all()
    
    # Average resolution time (for resolved issues)
    avg_resolution_time = db.query(
        func.avg(
            func.julianday(Issue.resolved_at) - func.julianday(Issue.created_at)
        ).label('avg_days')
    ).filter(Issue.status == IssueStatus.RESOLVED).scalar()
    
    return {
        "status_distribution": [
            {"status": status, "count": count}
            for status, count in status_distribution
        ],
        "department_distribution": [
            {"department": name, "count": count}
            for name, count in dept_distribution
        ],
        "average_resolution_days": float(avg_resolution_time) if avg_resolution_time else 0
    }
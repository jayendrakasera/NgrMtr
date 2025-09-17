from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, Float, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base
import enum

class IssueStatus(str, enum.Enum):
    PENDING = "pending"
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    REJECTED = "rejected"

class IssuePriority(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class Issue(Base):
    __tablename__ = "issues"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    category = Column(String(50), nullable=False)  # water, electricity, roads, etc.
    status = Column(Enum(IssueStatus), default=IssueStatus.PENDING)
    priority = Column(Enum(IssuePriority), default=IssuePriority.MEDIUM)
    
    # Location information
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    address = Column(Text, nullable=True)
    
    # User and assignment
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=True)
    worker_id = Column(Integer, ForeignKey("workers.id"), nullable=True)
    
    # AI classification
    ai_confidence = Column(Float, default=0.0)  # AI classification confidence score
    needs_manual_review = Column(Boolean, default=False)
    
    # Voting system
    upvotes = Column(Integer, default=0)
    downvotes = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    resolved_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="issues")
    department = relationship("Department", back_populates="issues")
    worker = relationship("Worker", back_populates="issues")
    media = relationship("IssueMedia", back_populates="issue", cascade="all, delete-orphan")

class IssueMedia(Base):
    __tablename__ = "issue_media"

    id = Column(Integer, primary_key=True, index=True)
    issue_id = Column(Integer, ForeignKey("issues.id"), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_type = Column(String(50), nullable=False)  # image, video, audio
    file_size = Column(Integer, nullable=False)  # in bytes
    original_filename = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    issue = relationship("Issue", back_populates="media")
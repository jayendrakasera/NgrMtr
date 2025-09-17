from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class Worker(Base):
    __tablename__ = "workers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    employee_id = Column(String(50), unique=True, nullable=False)
    mobile_number = Column(String(15), nullable=False)
    email = Column(String(255), nullable=True)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False)
    specialization = Column(String(100), nullable=True)  # e.g., "Plumbing", "Electrical"
    is_available = Column(Boolean, default=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    department = relationship("Department", back_populates="workers")
    issues = relationship("Issue", back_populates="worker")
"""
Database initialization script
Run this to create all database tables and populate with initial data
"""
from database import engine, SessionLocal
from models import User, Issue, Department, Worker
from passlib.context import CryptContext
from sqlalchemy.orm import Session

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_tables():
    """Create all database tables"""
    from models.user import Base as UserBase
    from models.issue import Base as IssueBase  
    from models.department import Base as DepartmentBase
    from models.worker import Base as WorkerBase
    
    # Create all tables
    UserBase.metadata.create_all(bind=engine)
    IssueBase.metadata.create_all(bind=engine)
    DepartmentBase.metadata.create_all(bind=engine)
    WorkerBase.metadata.create_all(bind=engine)
    
    print("✅ Database tables created successfully!")

def create_sample_data():
    """Create sample data for testing"""
    db = SessionLocal()
    try:
        # Check if data already exists
        if db.query(Department).count() > 0:
            print("Sample data already exists, skipping...")
            return

        # Create departments
        departments_data = [
            {
                "name": "Water Department",
                "description": "Handles water supply, drainage, and related issues",
                "keywords": "water,pipe,leak,drainage,sewage,tap,supply,pressure,contamination",
                "contact_email": "water@nagarmitra.gov",
                "contact_phone": "+911234567890"
            },
            {
                "name": "Electricity Department", 
                "description": "Manages electrical infrastructure and power issues",
                "keywords": "electricity,power,outage,transformer,pole,wire,streetlight,meter",
                "contact_email": "electricity@nagarmitra.gov",
                "contact_phone": "+911234567891"
            },
            {
                "name": "Roads & Transportation",
                "description": "Road maintenance, traffic management, and transportation",
                "keywords": "road,pothole,traffic,signal,maintenance,construction,parking,footpath",
                "contact_email": "roads@nagarmitra.gov", 
                "contact_phone": "+911234567892"
            },
            {
                "name": "Waste Management",
                "description": "Garbage collection, waste disposal, and cleanliness",
                "keywords": "garbage,waste,trash,cleaning,dustbin,disposal,sanitation,sweeping",
                "contact_email": "waste@nagarmitra.gov",
                "contact_phone": "+911234567893"
            },
            {
                "name": "Public Safety",
                "description": "Law and order, security, and emergency services",
                "keywords": "safety,security,crime,emergency,police,fire,ambulance,accident",
                "contact_email": "safety@nagarmitra.gov",
                "contact_phone": "+911234567894"
            }
        ]
        
        departments = []
        for dept_data in departments_data:
            department = Department(**dept_data)
            departments.append(department)
            db.add(department)
        
        db.commit()
        db.refresh(departments[0])  # Refresh to get IDs
        
        # Create sample workers
        workers_data = [
            {"name": "Raj Kumar", "employee_id": "WTR001", "mobile_number": "+919876543210", "department_id": departments[0].id, "specialization": "Plumbing"},
            {"name": "Amit Singh", "employee_id": "ELC001", "mobile_number": "+919876543211", "department_id": departments[1].id, "specialization": "Electrical"},
            {"name": "Priya Sharma", "employee_id": "RDS001", "mobile_number": "+919876543212", "department_id": departments[2].id, "specialization": "Road Maintenance"},
            {"name": "Suresh Gupta", "employee_id": "WST001", "mobile_number": "+919876543213", "department_id": departments[3].id, "specialization": "Waste Collection"},
            {"name": "Vikram Yadav", "employee_id": "SFT001", "mobile_number": "+919876543214", "department_id": departments[4].id, "specialization": "Security"}
        ]
        
        for worker_data in workers_data:
            worker = Worker(**worker_data)
            db.add(worker)
        
        # Create admin user
        admin_user = User(
            mobile_number="+919999999999",
            name="Admin User",
            email="admin@nagarmitra.gov",
            address="Municipal Corporation Office",
            is_admin=True,
            hashed_password=pwd_context.hash("admin123")
        )
        db.add(admin_user)
        
        # Create sample citizen user
        citizen_user = User(
            mobile_number="+919888888888", 
            name="John Doe",
            email="john@example.com",
            address="123 Main Street, City",
            is_admin=False,
            hashed_password=pwd_context.hash("citizen123")
        )
        db.add(citizen_user)
        
        db.commit()
        print("✅ Sample data created successfully!")
        print("👤 Admin Login: +919999999999 / admin123")
        print("👤 Citizen Login: +919888888888 / citizen123")
        
    except Exception as e:
        print(f"❌ Error creating sample data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("🚀 Initializing Nagar Mitra Database...")
    create_tables()
    create_sample_data()
    print("🎉 Database initialization complete!")
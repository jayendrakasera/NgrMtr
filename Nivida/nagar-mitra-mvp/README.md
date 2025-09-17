# Nagar Mitra - Civic Issue Reporting Platform MVP

## Overview
Nagar Mitra is a comprehensive civic issue reporting and resolution platform that enables citizens to report municipal issues and allows administrators to efficiently manage and resolve them.

## Features
- **Citizen Portal**: User registration, issue reporting with media uploads, status tracking
- **Admin Dashboard**: Issue management, worker assignment, status updates, analytics
- **AI Classification**: Automated issue categorization and department routing
- **Map Visualization**: Geographic issue mapping and heatmap analysis
- **Notification System**: Real-time status updates and notifications

## Tech Stack
- **Backend**: FastAPI + PostgreSQL/SQLite
- **Frontend**: React.js with Vite
- **Authentication**: JWT-based authentication
- **Media Storage**: Local file storage (MVP)
- **Database**: SQLite (MVP) / PostgreSQL (Production)
- **Styling**: Tailwind CSS
- **Maps**: React Leaflet

## Project Structure
```
nagar-mitra-mvp/
├── backend/                    # FastAPI backend application
│   ├── models/                # SQLAlchemy database models
│   ├── routers/               # API route handlers
│   ├── schemas/               # Pydantic data validation schemas
│   ├── services/              # Business logic services
│   ├── utils/                 # Utility functions
│   ├── database.py            # Database configuration
│   ├── main.py                # FastAPI application entry point
│   ├── init_db.py             # Database initialization script
│   └── requirements.txt       # Python dependencies
├── frontend/                   # React.js frontend application
│   ├── src/                   # Source code
│   ├── public/                # Static assets
│   ├── package.json           # Node.js dependencies
│   └── vite.config.js         # Vite configuration
└── README.md                   # This file
```

## Quick Start

### Prerequisites
- Python 3.8 or higher
- Node.js 16 or higher
- npm or yarn

### Backend Setup

1. **Navigate to backend directory:**
```bash
cd backend
```

2. **Create virtual environment:**
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables:**
```bash
cp .env.example .env
# Edit .env file with your configuration
```

5. **Initialize database:**
```bash
python init_db.py
```

6. **Run the backend server:**
```bash
python main.py
```

The API will be available at `http://localhost:8000`
API documentation: `http://localhost:8000/api/docs`

### Frontend Setup

1. **Navigate to frontend directory:**
```bash
cd frontend
```

2. **Install dependencies:**
```bash
npm install
```

3. **Start development server:**
```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`

## API Documentation

### Authentication
- **POST** `/api/auth/register` - Register new user
- **POST** `/api/auth/login` - Login user
- **POST** `/api/auth/login/mobile` - Login with mobile number

### Users
- **GET** `/api/users/me` - Get current user profile
- **PUT** `/api/users/me` - Update user profile
- **GET** `/api/users/` - Get all users (admin only)

### Issues
- **POST** `/api/issues/` - Create new issue (with file upload)
- **GET** `/api/issues/` - Get all issues (with filtering)
- **GET** `/api/issues/my` - Get current user's issues
- **GET** `/api/issues/{id}` - Get issue by ID
- **PUT** `/api/issues/{id}` - Update issue
- **POST** `/api/issues/{id}/vote` - Vote on issue
- **DELETE** `/api/issues/{id}` - Delete issue (admin only)

### Admin
- **GET** `/api/admin/dashboard` - Get dashboard statistics
- **GET** `/api/admin/issues/pending` - Get pending issues
- **POST** `/api/admin/issues/{id}/assign/{worker_id}` - Assign issue to worker
- **GET** `/api/admin/departments` - Get all departments
- **GET** `/api/admin/workers` - Get all workers
- **GET** `/api/admin/analytics/trends` - Get issue analytics

## Sample Data

The system comes with pre-loaded sample data:

### Test Accounts
- **Admin**: `+919999999999` / `admin123`
- **Citizen**: `+919888888888` / `citizen123`

### Departments
- Water Department
- Electricity Department
- Roads & Transportation
- Waste Management
- Public Safety

### Sample Workers
- Raj Kumar (Water) - `+919876543210`
- Amit Singh (Electricity) - `+919876543211`
- Priya Sharma (Roads) - `+919876543212`
- Suresh Gupta (Waste) - `+919876543213`
- Vikram Yadav (Safety) - `+919876543214`

## Key Features

### 🤖 AI-Powered Classification
The system automatically categorizes issues using keyword-based classification:
- **Water issues**: pipe, leak, drainage, sewage, tap, supply
- **Electricity**: power, outage, transformer, streetlight
- **Roads**: pothole, traffic, signal, maintenance
- **Waste**: garbage, trash, cleaning, dustbin
- **Safety**: crime, emergency, police, fire

### 📱 SMS Notifications (MVP Mock)
The notification system logs messages to console (production ready for SMS integration):
- Issue creation confirmations
- Assignment notifications
- Status update alerts
- Worker task assignments

### 🗺️ Geographic Features
- Location-based issue reporting
- Map visualization capabilities
- Address geocoding support

### 📊 Admin Analytics
- Issue status distribution
- Department workload analysis
- Resolution time tracking
- Worker performance metrics

## Production Deployment

### Environment Variables
Create `.env` file in backend directory:
```env
# Database (for production use PostgreSQL)
DATABASE_URL=postgresql://user:password@localhost/nagar_mitra_db

# JWT Configuration
SECRET_KEY=your_super_secure_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# File Upload
MAX_FILE_SIZE_MB=10
ALLOWED_FILE_TYPES=image/jpeg,image/png,image/gif,video/mp4,audio/mpeg

# SMS Service (for production)
TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_token
TWILIO_PHONE_NUMBER=your_twilio_number
```

### Docker Deployment
```bash
# Backend
docker build -t nagar-mitra-backend ./backend
docker run -p 8000:8000 nagar-mitra-backend

# Frontend
docker build -t nagar-mitra-frontend ./frontend
docker run -p 3000:3000 nagar-mitra-frontend
```

### Database Migration
For production with PostgreSQL:
1. Install PostgreSQL
2. Create database: `nagar_mitra_db`
3. Update `DATABASE_URL` in `.env`
4. Run: `python init_db.py`

## Contributing

### Development Workflow
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

### Code Style
- Backend: Follow PEP 8 for Python
- Frontend: Use ESLint and Prettier
- Commit messages: Follow conventional commits

## License

MIT License - see LICENSE file for details

## Support

For issues and questions:
1. Check the API documentation at `/api/docs`
2. Review the sample data and test accounts
3. Examine the console logs for notification examples

---

**Status**: ✅ **MVP Complete**

The MVP includes a fully functional backend API with authentication, issue management, AI classification, admin dashboard, and notification system. The frontend structure is ready for development with modern React/Vite setup.

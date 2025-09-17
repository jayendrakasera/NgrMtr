# Nagar Mitra API Testing Guide

This guide provides step-by-step instructions for testing the Nagar Mitra API using curl commands.

## Prerequisites

1. Backend server running at `http://localhost:8000`
2. Database initialized with sample data (`python init_db.py`)
3. curl or similar HTTP client

## Testing Workflow

### 1. Health Check
```bash
curl -X GET "http://localhost:8000/api/health"
```

Expected response:
```json
{
  "status": "healthy",
  "service": "Nagar Mitra API"
}
```

### 2. User Registration
```bash
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "mobile_number": "+919123456789",
    "name": "Test User",
    "email": "test@example.com",
    "address": "123 Test Street",
    "password": "testpass123"
  }'
```

### 3. User Login
```bash
curl -X POST "http://localhost:8000/api/auth/login/mobile" \
  -H "Content-Type: application/json" \
  -d '{
    "mobile_number": "+919123456789",
    "password": "testpass123"
  }'
```

Save the `access_token` from the response for authenticated requests.

### 4. Admin Login (Using Sample Data)
```bash
curl -X POST "http://localhost:8000/api/auth/login/mobile" \
  -H "Content-Type: application/json" \
  -d '{
    "mobile_number": "+919999999999",
    "password": "admin123"
  }'
```

### 5. Get User Profile
```bash
curl -X GET "http://localhost:8000/api/users/me" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN_HERE"
```

### 6. Create Issue (Text Only)
```bash
curl -X POST "http://localhost:8000/api/issues/" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN_HERE" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "title=Broken Street Light&description=The street light on Main Road has been broken for 3 days causing safety issues&latitude=28.6139&longitude=77.2090&address=Main Road, New Delhi"
```

### 7. Create Issue with File Upload
```bash
curl -X POST "http://localhost:8000/api/issues/" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN_HERE" \
  -F "title=Water Leakage Problem" \
  -F "description=Major water leakage in the pipe near the park causing flooding" \
  -F "latitude=28.6129" \
  -F "longitude=77.2295" \
  -F "address=Park Street, Delhi" \
  -F "files=@/path/to/your/image.jpg"
```

### 8. Get All Issues
```bash
curl -X GET "http://localhost:8000/api/issues/" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN_HERE"
```

### 9. Get My Issues
```bash
curl -X GET "http://localhost:8000/api/issues/my" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN_HERE"
```

### 10. Get Specific Issue
```bash
curl -X GET "http://localhost:8000/api/issues/1" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN_HERE"
```

### 11. Vote on Issue
```bash
curl -X POST "http://localhost:8000/api/issues/1/vote" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "vote_type": "up"
  }'
```

### 12. Admin Dashboard (Admin Token Required)
```bash
curl -X GET "http://localhost:8000/api/admin/dashboard" \
  -H "Authorization: Bearer ADMIN_ACCESS_TOKEN_HERE"
```

### 13. Get Pending Issues (Admin)
```bash
curl -X GET "http://localhost:8000/api/admin/issues/pending" \
  -H "Authorization: Bearer ADMIN_ACCESS_TOKEN_HERE"
```

### 14. Get All Departments (Admin)
```bash
curl -X GET "http://localhost:8000/api/admin/departments" \
  -H "Authorization: Bearer ADMIN_ACCESS_TOKEN_HERE"
```

### 15. Get Workers (Admin)
```bash
curl -X GET "http://localhost:8000/api/admin/workers" \
  -H "Authorization: Bearer ADMIN_ACCESS_TOKEN_HERE"
```

### 16. Assign Issue to Worker (Admin)
```bash
curl -X POST "http://localhost:8000/api/admin/issues/1/assign/1" \
  -H "Authorization: Bearer ADMIN_ACCESS_TOKEN_HERE"
```

### 17. Update Issue Status
```bash
curl -X PUT "http://localhost:8000/api/issues/1" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "in_progress"
  }'
```

### 18. Get Analytics (Admin)
```bash
curl -X GET "http://localhost:8000/api/admin/analytics/trends" \
  -H "Authorization: Bearer ADMIN_ACCESS_TOKEN_HERE"
```

## API Response Examples

### Successful Issue Creation
```json
{
  "id": 1,
  "title": "Broken Street Light",
  "description": "The street light on Main Road has been broken for 3 days",
  "category": null,
  "latitude": 28.6139,
  "longitude": 77.2090,
  "address": "Main Road, New Delhi",
  "status": "pending",
  "priority": "medium",
  "user_id": 2,
  "department_id": 1,
  "worker_id": null,
  "ai_confidence": 0.6,
  "needs_manual_review": false,
  "upvotes": 0,
  "downvotes": 0,
  "created_at": "2024-01-15T10:30:00Z",
  "media": []
}
```

### Dashboard Statistics
```json
{
  "issue_stats": {
    "total": 5,
    "pending": 3,
    "in_progress": 1,
    "resolved": 1
  },
  "department_stats": [
    {"department": "Water Department", "count": 2},
    {"department": "Electricity Department", "count": 2},
    {"department": "Roads & Transportation", "count": 1}
  ],
  "user_stats": {
    "total_citizens": 10,
    "total_workers": 5
  }
}
```

## Error Handling

### Authentication Error (401)
```json
{
  "detail": "Could not validate credentials"
}
```

### Validation Error (422)
```json
{
  "detail": [
    {
      "loc": ["body", "mobile_number"],
      "msg": "Mobile number must start with +91 and be 13 characters long",
      "type": "value_error"
    }
  ]
}
```

### Not Found Error (404)
```json
{
  "detail": "Issue not found"
}
```

## File Upload Testing

### Supported File Types
- Images: `image/jpeg`, `image/png`, `image/gif`
- Videos: `video/mp4`
- Audio: `audio/mpeg`, `audio/wav`

### Test File Upload
```bash
# Create a test image file
echo "Test image content" > test_image.jpg

# Upload with issue
curl -X POST "http://localhost:8000/api/issues/" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "title=Test Issue with Image" \
  -F "description=Testing file upload functionality" \
  -F "files=@test_image.jpg"
```

## Notification Testing

When you create or update issues, check the backend console for notification logs:

```
📱 SMS NOTIFICATION
   To: +919123456789
   Message: Your issue 'Broken Street Light...' has been submitted successfully. Issue ID: #1.
   Time: 2024-01-15 10:30:00.123456
--------------------------------------------------
```

## AI Classification Testing

Test AI classification with these example titles/descriptions:

### Water Issues
```bash
curl -X POST "http://localhost:8000/api/issues/" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "title=Water Pipe Burst&description=Major water pipe leak causing flooding in the street"
```

### Electricity Issues
```bash
curl -X POST "http://localhost:8000/api/issues/" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "title=Power Outage&description=Electricity transformer is down affecting entire neighborhood"
```

### Road Issues
```bash
curl -X POST "http://localhost:8000/api/issues/" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "title=Large Pothole&description=Dangerous pothole on highway causing vehicle damage"
```

## Interactive Testing

1. **Use API Documentation**: Visit `http://localhost:8000/api/docs` for interactive testing
2. **Postman Collection**: Import the endpoints into Postman for easier testing
3. **Frontend Integration**: Test through the React frontend once developed

## Common Issues & Solutions

### 1. CORS Errors
- Ensure frontend is running on `http://localhost:3000`
- Check CORS configuration in `main.py`

### 2. File Upload Issues
- Verify file size limits (10MB max)
- Check file type is in allowed list
- Ensure proper `multipart/form-data` encoding

### 3. Authentication Problems
- Verify token is not expired (30 min default)
- Include "Bearer " prefix in Authorization header
- Check token format and validity

### 4. Database Issues
- Run `python init_db.py` if tables are missing
- Check SQLite file permissions
- Verify sample data is loaded correctly
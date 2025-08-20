# API Specification - Autonomous Research & Report Generation System

## 📋 Overview
This document provides the complete API specification for the Autonomous Research & Report Generation System, including all endpoints, request/response schemas, authentication, and integration patterns.

## 🔐 Authentication

### JWT Token Authentication
All API endpoints require JWT token authentication except for public endpoints (login, register).

```http
Authorization: Bearer <access_token>
```

### Token Types
- **Access Token**: Short-lived (15 minutes) for API requests
- **Refresh Token**: Long-lived (7 days) for token renewal

### Token Refresh
```http
POST /api/v1/auth/refresh
Content-Type: application/json

{
  "refresh_token": "string"
}
```

## 📊 Base URLs

### Development
- **Backend API**: `http://localhost:8000/api/v1`
- **Frontend**: `http://localhost:3000`
- **WebSocket**: `ws://localhost:8000/ws`

### Production
- **Backend API**: `https://api.research-system.com/api/v1`
- **Frontend**: `https://research-system.com`
- **WebSocket**: `wss://api.research-system.com/ws`

## 🔄 API Endpoints

### Authentication Endpoints

#### 1. User Registration
```http
POST /api/v1/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "secure_password123",
  "first_name": "John",
  "last_name": "Doe",
  "organization": "Acme Corp",
  "role": "researcher"
}
```

**Response:**
```json
{
  "user": {
    "id": "uuid",
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "organization": "Acme Corp",
    "role": "researcher",
    "is_active": true,
    "created_at": "2024-01-01T00:00:00Z"
  },
  "access_token": "jwt_token",
  "refresh_token": "refresh_token"
}
```

#### 2. User Login
```http
POST /api/v1/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "secure_password123"
}
```

**Response:**
```json
{
  "user": {
    "id": "uuid",
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "role": "researcher",
    "is_active": true
  },
  "access_token": "jwt_token",
  "refresh_token": "refresh_token"
}
```

#### 3. Token Refresh
```http
POST /api/v1/auth/refresh
Content-Type: application/json

{
  "refresh_token": "refresh_token"
}
```

**Response:**
```json
{
  "access_token": "new_jwt_token",
  "refresh_token": "new_refresh_token"
}
```

#### 4. User Logout
```http
POST /api/v1/auth/logout
Authorization: Bearer <access_token>
```

### Research Jobs Endpoints

#### 1. Create Research Job
```http
POST /api/v1/research-jobs
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "query": "What are the latest developments in quantum computing?",
  "description": "Research on recent quantum computing breakthroughs",
  "scope": {
    "depth": "comprehensive",
    "sources": ["academic", "industry", "news"],
    "timeframe": "last_2_years"
  },
  "output_config": {
    "format": "pdf",
    "length": "medium",
    "include_visualizations": true,
    "citation_style": "apa"
  },
  "constraints": {
    "max_sources": 20,
    "max_pages": 15,
    "required_sections": ["executive_summary", "methodology", "findings"]
  }
}
```

**Response:**
```json
{
  "job": {
    "id": "uuid",
    "query": "What are the latest developments in quantum computing?",
    "description": "Research on recent quantum computing breakthroughs",
    "status": "created",
    "progress": 0,
    "created_at": "2024-01-01T00:00:00Z",
    "estimated_completion": "2024-01-01T02:00:00Z",
    "user_id": "user_uuid"
  },
  "message": "Research job created successfully"
}
```

#### 2. List Research Jobs
```http
GET /api/v1/research-jobs?page=1&limit=10&status=active&search=quantum
Authorization: Bearer <access_token>
```

**Query Parameters:**
- `page`: Page number (default: 1)
- `limit`: Items per page (default: 10, max: 100)
- `status`: Filter by status (created, active, completed, failed)
- `search`: Search in query and description
- `sort_by`: Sort field (created_at, updated_at, status)
- `sort_order`: Sort order (asc, desc)

**Response:**
```json
{
  "jobs": [
    {
      "id": "uuid",
      "query": "What are the latest developments in quantum computing?",
      "description": "Research on recent quantum computing breakthroughs",
      "status": "active",
      "progress": 45,
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-01T01:00:00Z",
      "estimated_completion": "2024-01-01T02:00:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 10,
    "total": 25,
    "pages": 3
  }
}
```

#### 3. Get Research Job Details
```http
GET /api/v1/research-jobs/{job_id}
Authorization: Bearer <access_token>
```

**Response:**
```json
{
  "job": {
    "id": "uuid",
    "query": "What are the latest developments in quantum computing?",
    "description": "Research on recent quantum computing breakthroughs",
    "status": "active",
    "progress": 45,
    "current_step": "evidence_synthesis",
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T01:00:00Z",
    "estimated_completion": "2024-01-01T02:00:00Z",
    "scope": {
      "depth": "comprehensive",
      "sources": ["academic", "industry", "news"],
      "timeframe": "last_2_years"
    },
    "output_config": {
      "format": "pdf",
      "length": "medium",
      "include_visualizations": true,
      "citation_style": "apa"
    },
    "metrics": {
      "sources_found": 12,
      "claims_generated": 8,
      "citations_created": 15,
      "tokens_used": 45000
    },
    "errors": []
  }
}
```

#### 4. Update Research Job
```http
PUT /api/v1/research-jobs/{job_id}
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "description": "Updated description",
  "scope": {
    "depth": "comprehensive",
    "sources": ["academic", "industry"],
    "timeframe": "last_year"
  }
}
```

#### 5. Start Research Job
```http
POST /api/v1/research-jobs/{job_id}/start
Authorization: Bearer <access_token>
```

**Response:**
```json
{
  "message": "Research job started successfully",
  "job": {
    "id": "uuid",
    "status": "active",
    "progress": 0,
    "current_step": "query_understanding"
  }
}
```

#### 6. Cancel Research Job
```http
POST /api/v1/research-jobs/{job_id}/cancel
Authorization: Bearer <access_token>
```

#### 7. Retry Failed Research Job
```http
POST /api/v1/research-jobs/{job_id}/retry
Authorization: Bearer <access_token>
```

#### 8. Get Research Job Progress
```http
GET /api/v1/research-jobs/{job_id}/progress
Authorization: Bearer <access_token>
```

**Response:**
```json
{
  "progress": {
    "overall": 45,
    "current_step": "evidence_synthesis",
    "step_progress": 75,
    "steps": [
      {
        "name": "query_understanding",
        "status": "completed",
        "progress": 100,
        "started_at": "2024-01-01T00:05:00Z",
        "completed_at": "2024-01-01T00:10:00Z"
      },
      {
        "name": "retrieval_hub",
        "status": "completed",
        "progress": 100,
        "started_at": "2024-01-01T00:10:00Z",
        "completed_at": "2024-01-01T00:30:00Z"
      },
      {
        "name": "evidence_synthesis",
        "status": "active",
        "progress": 75,
        "started_at": "2024-01-01T00:30:00Z"
      }
    ]
  }
}
```

#### 9. Stream Real-time Updates (SSE)
```http
GET /api/v1/research-jobs/{job_id}/stream
Authorization: Bearer <access_token>
Accept: text/event-stream
```

**Event Types:**
- `progress`: Progress updates
- `status`: Status changes
- `step`: Step completion
- `error`: Error notifications
- `complete`: Job completion

**Example Events:**
```
event: progress
data: {"progress": 45, "current_step": "evidence_synthesis"}

event: step
data: {"step": "retrieval_hub", "status": "completed", "sources_found": 12}

event: complete
data: {"job_id": "uuid", "report_id": "report_uuid"}
```

#### 10. Get Research Sources
```http
GET /api/v1/research-jobs/{job_id}/sources
Authorization: Bearer <access_token>
```

**Response:**
```json
{
  "sources": [
    {
      "id": "uuid",
      "title": "Quantum Computing Breakthroughs 2024",
      "url": "https://example.com/quantum-2024",
      "type": "academic",
      "relevance_score": 0.95,
      "extracted_at": "2024-01-01T00:15:00Z",
      "metadata": {
        "author": "Dr. Jane Smith",
        "publication": "Nature",
        "date": "2024-01-01"
      }
    }
  ]
}
```

#### 11. Get Research Claims
```http
GET /api/v1/research-jobs/{job_id}/claims
Authorization: Bearer <access_token>
```

**Response:**
```json
{
  "claims": [
    {
      "id": "uuid",
      "content": "IBM achieved 1000+ qubit quantum processor",
      "confidence": 0.92,
      "source_ids": ["source_uuid_1", "source_uuid_2"],
      "verification_status": "verified",
      "created_at": "2024-01-01T00:45:00Z"
    }
  ]
}
```

#### 12. Get Research Job Statistics
```http
GET /api/v1/research-jobs/stats/summary
Authorization: Bearer <access_token>
```

**Response:**
```json
{
  "stats": {
    "total_jobs": 150,
    "active_jobs": 5,
    "completed_jobs": 120,
    "failed_jobs": 3,
    "average_completion_time": "2.5 hours",
    "success_rate": 0.96,
    "total_reports_generated": 120,
    "total_sources_processed": 2400,
    "total_claims_generated": 1800
  }
}
```

### Reports Endpoints

#### 1. List Reports
```http
GET /api/v1/reports?page=1&limit=10&job_id={job_id}
Authorization: Bearer <access_token>
```

**Response:**
```json
{
  "reports": [
    {
      "id": "uuid",
      "title": "Latest Developments in Quantum Computing",
      "job_id": "job_uuid",
      "format": "pdf",
      "file_size": 2048576,
      "status": "completed",
      "created_at": "2024-01-01T02:00:00Z",
      "download_count": 5
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 10,
    "total": 25,
    "pages": 3
  }
}
```

#### 2. Get Report Details
```http
GET /api/v1/reports/{report_id}
Authorization: Bearer <access_token>
```

**Response:**
```json
{
  "report": {
    "id": "uuid",
    "title": "Latest Developments in Quantum Computing",
    "job_id": "job_uuid",
    "format": "pdf",
    "file_size": 2048576,
    "status": "completed",
    "created_at": "2024-01-01T02:00:00Z",
    "download_count": 5,
    "metadata": {
      "pages": 15,
      "word_count": 8500,
      "sources_cited": 20,
      "claims_verified": 25
    },
    "download_url": "/api/v1/reports/{report_id}/download"
  }
}
```

#### 3. Download Report
```http
GET /api/v1/reports/{report_id}/download
Authorization: Bearer <access_token>
```

**Response:** File download with appropriate headers

#### 4. Export Report in Different Format
```http
POST /api/v1/reports/{report_id}/export
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "format": "docx",
  "include_appendices": true
}
```

### User Management Endpoints

#### 1. Get User Profile
```http
GET /api/v1/users/profile
Authorization: Bearer <access_token>
```

**Response:**
```json
{
  "user": {
    "id": "uuid",
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "organization": "Acme Corp",
    "role": "researcher",
    "is_active": true,
    "created_at": "2024-01-01T00:00:00Z",
    "last_login": "2024-01-01T10:00:00Z",
    "preferences": {
      "default_format": "pdf",
      "notification_email": true,
      "auto_save": true
    }
  }
}
```

#### 2. Update User Profile
```http
PUT /api/v1/users/profile
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "first_name": "John",
  "last_name": "Doe",
  "organization": "Acme Corp",
  "preferences": {
    "default_format": "docx",
    "notification_email": true
  }
}
```

#### 3. Get User Activity
```http
GET /api/v1/users/activity?page=1&limit=10
Authorization: Bearer <access_token>
```

**Response:**
```json
{
  "activities": [
    {
      "id": "uuid",
      "type": "job_created",
      "description": "Created research job: Quantum Computing",
      "created_at": "2024-01-01T00:00:00Z",
      "metadata": {
        "job_id": "job_uuid",
        "query": "What are the latest developments in quantum computing?"
      }
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 10,
    "total": 50,
    "pages": 5
  }
}
```

### System Endpoints

#### 1. Health Check
```http
GET /api/v1/health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T00:00:00Z",
  "services": {
    "database": "healthy",
    "redis": "healthy",
    "ai_services": "healthy"
  }
}
```

#### 2. System Metrics
```http
GET /api/v1/metrics
Authorization: Bearer <access_token>
```

**Response:**
```json
{
  "metrics": {
    "requests_per_minute": 150,
    "average_response_time": 250,
    "error_rate": 0.02,
    "active_users": 45,
    "jobs_in_progress": 12
  }
}
```

## 📝 Request/Response Schemas

### Common Schemas

#### Pagination
```json
{
  "page": 1,
  "limit": 10,
  "total": 100,
  "pages": 10
}
```

#### Error Response
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": {
      "field": "email",
      "issue": "Invalid email format"
    }
  }
}
```

#### Success Response
```json
{
  "success": true,
  "message": "Operation completed successfully",
  "data": {}
}
```

### Research Job Schemas

#### Job Creation Request
```json
{
  "query": "string (required)",
  "description": "string (optional)",
  "scope": {
    "depth": "basic|comprehensive|expert",
    "sources": ["academic", "industry", "news"],
    "timeframe": "last_month|last_quarter|last_year|last_2_years"
  },
  "output_config": {
    "format": "pdf|docx|pptx",
    "length": "short|medium|long",
    "include_visualizations": "boolean",
    "citation_style": "apa|mla|chicago"
  },
  "constraints": {
    "max_sources": "integer",
    "max_pages": "integer",
    "required_sections": ["string"]
  }
}
```

#### Job Status Enum
```json
{
  "status": "created|active|completed|failed|cancelled|paused"
}
```

### Report Schemas

#### Report Metadata
```json
{
  "id": "uuid",
  "title": "string",
  "job_id": "uuid",
  "format": "pdf|docx|pptx",
  "file_size": "integer (bytes)",
  "status": "processing|completed|failed",
  "created_at": "datetime",
  "download_count": "integer",
  "metadata": {
    "pages": "integer",
    "word_count": "integer",
    "sources_cited": "integer",
    "claims_verified": "integer"
  }
}
```

## 🔄 WebSocket Events

### Connection
```javascript
const ws = new WebSocket('ws://localhost:8000/ws');
ws.onopen = () => {
  ws.send(JSON.stringify({
    type: 'authenticate',
    token: 'jwt_token'
  }));
};
```

### Event Types

#### Progress Update
```json
{
  "type": "progress_update",
  "job_id": "uuid",
  "data": {
    "progress": 45,
    "current_step": "evidence_synthesis",
    "step_progress": 75
  }
}
```

#### Status Change
```json
{
  "type": "status_change",
  "job_id": "uuid",
  "data": {
    "status": "completed",
    "report_id": "report_uuid"
  }
}
```

#### Error Notification
```json
{
  "type": "error",
  "job_id": "uuid",
  "data": {
    "error": "Retrieval failed",
    "details": "Network timeout"
  }
}
```

## 🚀 Rate Limiting

### Limits
- **Authentication**: 5 requests per minute
- **API Requests**: 100 requests per minute per user
- **File Uploads**: 10 requests per minute per user
- **WebSocket Connections**: 5 connections per user

### Headers
```http
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1640995200
```

## 🔒 Security Headers

### Required Headers
```http
Content-Security-Policy: default-src 'self'
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Strict-Transport-Security: max-age=31536000; includeSubDomains
```

## 📊 Response Codes

### Success Codes
- `200 OK`: Request successful
- `201 Created`: Resource created successfully
- `204 No Content`: Request successful, no content to return

### Client Error Codes
- `400 Bad Request`: Invalid request data
- `401 Unauthorized`: Authentication required
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Resource not found
- `409 Conflict`: Resource conflict
- `422 Unprocessable Entity`: Validation error
- `429 Too Many Requests`: Rate limit exceeded

### Server Error Codes
- `500 Internal Server Error`: Server error
- `502 Bad Gateway`: Upstream service error
- `503 Service Unavailable`: Service temporarily unavailable

## 🔧 SDK Examples

### JavaScript/TypeScript
```javascript
import { ResearchAPI } from '@research-system/sdk';

const api = new ResearchAPI({
  baseURL: 'https://api.research-system.com/api/v1',
  token: 'your_jwt_token'
});

// Create research job
const job = await api.researchJobs.create({
  query: "What are the latest developments in quantum computing?",
  scope: { depth: "comprehensive" }
});

// Stream progress
api.researchJobs.streamProgress(job.id, (update) => {
  console.log('Progress:', update.progress);
});
```

### Python
```python
from research_system_sdk import ResearchAPI

api = ResearchAPI(
    base_url="https://api.research-system.com/api/v1",
    token="your_jwt_token"
)

# Create research job
job = api.research_jobs.create(
    query="What are the latest developments in quantum computing?",
    scope={"depth": "comprehensive"}
)

# Get progress
progress = api.research_jobs.get_progress(job.id)
print(f"Progress: {progress.overall}%")
```

This API specification provides comprehensive documentation for integrating with the Autonomous Research & Report Generation System, including all endpoints, schemas, authentication, and usage examples.

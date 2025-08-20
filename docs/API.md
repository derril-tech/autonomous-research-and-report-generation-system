# API Documentation

## Overview

The Autonomous Research & Report Generation System provides a comprehensive REST API for managing research jobs, user accounts, and generated reports. This document describes all available endpoints, request/response formats, and usage examples.

## Base URL

- **Development**: `http://localhost:8000`
- **Production**: `https://api.yourdomain.com`

## Authentication

The API uses JWT (JSON Web Tokens) for authentication. Include the token in the Authorization header:

```
Authorization: Bearer <your-jwt-token>
```

### Getting a Token

```bash
# Login to get access token
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "your-password"
  }'
```

## API Endpoints

### Authentication

#### POST /api/v1/auth/register

Register a new user account.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "secure-password",
  "first_name": "John",
  "last_name": "Doe",
  "company": "Acme Corp"
}
```

**Response:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "company": "Acme Corp",
  "is_active": true,
  "created_at": "2024-01-15T10:30:00Z"
}
```

#### POST /api/v1/auth/login

Authenticate user and get access token.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "secure-password"
}
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer",
  "expires_in": 1800,
  "user": {
    "id": 1,
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe"
  }
}
```

#### POST /api/v1/auth/refresh

Refresh access token using refresh token.

**Request Body:**
```json
{
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

#### POST /api/v1/auth/logout

Logout user and invalidate tokens.

**Response:**
```json
{
  "message": "Successfully logged out"
}
```

### Research Jobs

#### GET /api/v1/research-jobs

List research jobs with pagination, filtering, and sorting.

**Query Parameters:**
- `page` (int, default: 1): Page number
- `size` (int, default: 20, max: 100): Page size
- `status` (string, optional): Filter by status (pending, running, completed, failed)
- `priority` (string, optional): Filter by priority (low, normal, high, urgent)
- `search` (string, optional): Search in title and description
- `sort_by` (string, default: created_at): Sort field
- `sort_order` (string, default: desc): Sort order (asc/desc)

**Response:**
```json
{
  "items": [
    {
      "id": 1,
      "uuid": "550e8400-e29b-41d4-a716-446655440000",
      "title": "AI in Healthcare Research",
      "description": "Comprehensive analysis of AI applications in healthcare",
      "query": "What are the latest developments in AI for healthcare?",
      "status": "completed",
      "progress": 1.0,
      "current_step": "completed",
      "total_steps": 8,
      "completed_steps": 8,
      "priority": "normal",
      "output_format": "pdf",
      "include_citations": true,
      "include_sources": true,
      "include_analysis": true,
      "max_sources": 20,
      "research_depth": "standard",
      "fact_checking_enabled": true,
      "result_summary": "Research completed successfully with 15 sources analyzed",
      "error_message": null,
      "retry_count": 0,
      "tokens_used": 45000,
      "api_calls_made": 25,
      "processing_time_seconds": 180.5,
      "cost_estimate": 0.45,
      "workflow_id": "workflow_123",
      "created_at": "2024-01-15T10:30:00Z",
      "started_at": "2024-01-15T10:31:00Z",
      "completed_at": "2024-01-15T10:34:00Z",
      "duration_seconds": 210.0
    }
  ],
  "total": 25,
  "page": 1,
  "size": 20,
  "pages": 2
}
```

#### POST /api/v1/research-jobs

Create a new research job.

**Request Body:**
```json
{
  "title": "AI in Healthcare Research",
  "description": "Comprehensive analysis of AI applications in healthcare",
  "query": "What are the latest developments in AI for healthcare?",
  "config": {
    "research_depth": "comprehensive",
    "max_sources": 25,
    "time_period": "last 2 years",
    "include_technical_details": true
  },
  "priority": "high",
  "output_format": "pdf"
}
```

**Response:**
```json
{
  "id": 1,
  "uuid": "550e8400-e29b-41d4-a716-446655440000",
  "title": "AI in Healthcare Research",
  "description": "Comprehensive analysis of AI applications in healthcare",
  "query": "What are the latest developments in AI for healthcare?",
  "status": "pending",
  "progress": 0.0,
  "current_step": null,
  "total_steps": 0,
  "completed_steps": 0,
  "priority": "high",
  "output_format": "pdf",
  "include_citations": true,
  "include_sources": true,
  "include_analysis": true,
  "max_sources": 25,
  "research_depth": "comprehensive",
  "fact_checking_enabled": true,
  "created_at": "2024-01-15T10:30:00Z"
}
```

#### GET /api/v1/research-jobs/{job_id}

Get detailed information about a specific research job.

**Response:**
```json
{
  "id": 1,
  "uuid": "550e8400-e29b-41d4-a716-446655440000",
  "title": "AI in Healthcare Research",
  "description": "Comprehensive analysis of AI applications in healthcare",
  "query": "What are the latest developments in AI for healthcare?",
  "status": "completed",
  "progress": 1.0,
  "current_step": "completed",
  "total_steps": 8,
  "completed_steps": 8,
  "priority": "high",
  "output_format": "pdf",
  "include_citations": true,
  "include_sources": true,
  "include_analysis": true,
  "max_sources": 25,
  "research_depth": "comprehensive",
  "fact_checking_enabled": true,
  "result_summary": "Research completed successfully with 15 sources analyzed",
  "error_message": null,
  "retry_count": 0,
  "tokens_used": 45000,
  "api_calls_made": 25,
  "processing_time_seconds": 180.5,
  "cost_estimate": 0.45,
  "workflow_id": "workflow_123",
  "step_history": [
    {
      "step": "research_planning",
      "completed_at": "2024-01-15T10:31:30Z",
      "metadata": {
        "sources_found": 15,
        "search_queries": ["AI healthcare", "medical AI", "healthcare automation"]
      }
    }
  ],
  "sources": [
    {
      "id": 1,
      "title": "AI in Healthcare: A Comprehensive Review",
      "url": "https://example.com/ai-healthcare-review",
      "domain": "example.com",
      "source_type": "academic",
      "summary": "Comprehensive review of AI applications in healthcare...",
      "author": "Dr. Jane Smith",
      "publication_date": "2024-01-01T00:00:00Z",
      "credibility_score": 0.9,
      "relevance_score": 0.95,
      "overall_score": 0.92
    }
  ],
  "claims": [
    {
      "id": 1,
      "claim_text": "AI can improve diagnostic accuracy by 20%",
      "claim_type": "fact",
      "context": "In diagnostic imaging",
      "is_verified": true,
      "verification_status": "verified",
      "verification_score": 0.85,
      "supporting_sources": [1, 2, 3]
    }
  ],
  "reports": [
    {
      "id": 1,
      "title": "AI in Healthcare Research Report",
      "format_type": "pdf",
      "file_size_bytes": 2048576,
      "download_count": 5,
      "created_at": "2024-01-15T10:34:00Z"
    }
  ],
  "created_at": "2024-01-15T10:30:00Z",
  "started_at": "2024-01-15T10:31:00Z",
  "completed_at": "2024-01-15T10:34:00Z"
}
```

#### PUT /api/v1/research-jobs/{job_id}

Update a research job (only allowed for pending jobs).

**Request Body:**
```json
{
  "title": "Updated AI in Healthcare Research",
  "description": "Updated description",
  "priority": "urgent"
}
```

#### DELETE /api/v1/research-jobs/{job_id}

Delete a research job (soft delete).

**Response:**
```
204 No Content
```

#### POST /api/v1/research-jobs/{job_id}/start

Start a pending research job.

**Response:**
```json
{
  "id": 1,
  "status": "running",
  "started_at": "2024-01-15T10:31:00Z",
  "progress": 0.0
}
```

#### POST /api/v1/research-jobs/{job_id}/cancel

Cancel a running research job.

**Response:**
```json
{
  "id": 1,
  "status": "cancelled",
  "progress": 0.25
}
```

#### POST /api/v1/research-jobs/{job_id}/retry

Retry a failed research job.

**Response:**
```json
{
  "id": 1,
  "status": "pending",
  "retry_count": 1,
  "progress": 0.0
}
```

#### GET /api/v1/research-jobs/{job_id}/progress

Get real-time progress of a research job.

**Response:**
```json
{
  "job_id": 1,
  "status": "running",
  "progress": 0.5,
  "current_step": "source_analysis",
  "total_steps": 8,
  "completed_steps": 4,
  "estimated_completion": "2024-01-15T10:35:00Z",
  "step_history": [
    {
      "step": "research_planning",
      "completed_at": "2024-01-15T10:31:30Z"
    }
  ],
  "error_message": null
}
```

#### GET /api/v1/research-jobs/{job_id}/stream

Stream real-time updates for a research job (Server-Sent Events).

**Response:**
```
data: {"type": "progress", "data": {"progress": 0.25, "current_step": "source_analysis"}}

data: {"type": "status", "data": {"status": "completed"}}
```

#### GET /api/v1/research-jobs/{job_id}/sources

Get sources for a research job.

**Response:**
```json
[
  {
    "id": 1,
    "title": "AI in Healthcare: A Comprehensive Review",
    "url": "https://example.com/ai-healthcare-review",
    "domain": "example.com",
    "source_type": "academic",
    "summary": "Comprehensive review of AI applications in healthcare...",
    "author": "Dr. Jane Smith",
    "publication_date": "2024-01-01T00:00:00Z",
    "credibility_score": 0.9,
    "relevance_score": 0.95,
    "overall_score": 0.92,
    "is_processed": true,
    "processing_status": "completed"
  }
]
```

#### GET /api/v1/research-jobs/{job_id}/claims

Get claims for a research job.

**Response:**
```json
[
  {
    "id": 1,
    "claim_text": "AI can improve diagnostic accuracy by 20%",
    "claim_type": "fact",
    "context": "In diagnostic imaging",
    "is_verified": true,
    "verification_status": "verified",
    "verification_score": 0.85,
    "supporting_sources": [1, 2, 3],
    "contradicting_sources": [],
    "evidence_summary": "Multiple studies confirm this improvement in diagnostic accuracy"
  }
]
```

#### GET /api/v1/research-jobs/stats/summary

Get research job statistics.

**Query Parameters:**
- `time_range` (string, optional): Time range for stats (7d, 30d, 90d)

**Response:**
```json
{
  "total_jobs": 25,
  "completed_jobs": 20,
  "failed_jobs": 2,
  "running_jobs": 3,
  "completion_rate": 80.0,
  "avg_processing_time_seconds": 180.5,
  "total_tokens_used": 450000,
  "total_cost_estimate": 4.50
}
```

### Reports

#### GET /api/v1/reports

List generated reports.

**Query Parameters:**
- `page` (int, default: 1): Page number
- `size` (int, default: 20): Page size
- `format` (string, optional): Filter by format (pdf, docx, pptx, html)
- `research_job_id` (int, optional): Filter by research job ID

**Response:**
```json
{
  "items": [
    {
      "id": 1,
      "uuid": "550e8400-e29b-41d4-a716-446655440000",
      "title": "AI in Healthcare Research Report",
      "subtitle": "Comprehensive Analysis",
      "executive_summary": "This report provides a comprehensive analysis...",
      "abstract": "Artificial Intelligence is transforming healthcare...",
      "word_count": 5000,
      "page_count": 15,
      "format_type": "pdf",
      "template_used": "academic",
      "quality_score": 0.92,
      "review_status": "approved",
      "citations_count": 25,
      "sources_count": 15,
      "file_size_bytes": 2048576,
      "file_size_mb": 2.0,
      "storage_location": "s3",
      "is_public": false,
      "access_token": "abc123",
      "download_count": 5,
      "version": "1.0",
      "is_latest": true,
      "tags": ["AI", "Healthcare", "Research"],
      "categories": ["Technology", "Healthcare"],
      "keywords": ["artificial intelligence", "healthcare", "diagnosis"],
      "language": "en",
      "generation_time_seconds": 180.5,
      "tokens_used": 45000,
      "cost_estimate": 0.45,
      "created_at": "2024-01-15T10:34:00Z",
      "generated_at": "2024-01-15T10:37:00Z",
      "published_at": null,
      "reviewed_at": "2024-01-15T10:40:00Z"
    }
  ],
  "total": 15,
  "page": 1,
  "size": 20,
  "pages": 1
}
```

#### GET /api/v1/reports/{report_id}

Get detailed information about a specific report.

**Response:**
```json
{
  "id": 1,
  "uuid": "550e8400-e29b-41d4-a716-446655440000",
  "title": "AI in Healthcare Research Report",
  "subtitle": "Comprehensive Analysis",
  "executive_summary": "This report provides a comprehensive analysis...",
  "abstract": "Artificial Intelligence is transforming healthcare...",
  "content": "Full report content...",
  "content_structured": {
    "sections": [
      {
        "title": "Introduction",
        "content": "Introduction content...",
        "level": 1
      }
    ]
  },
  "word_count": 5000,
  "page_count": 15,
  "format_type": "pdf",
  "template_used": "academic",
  "styling_config": {
    "font_family": "Times New Roman",
    "font_size": 12,
    "line_spacing": 1.5
  },
  "quality_score": 0.92,
  "review_status": "approved",
  "review_notes": "Report meets quality standards",
  "reviewed_by": 2,
  "citations_count": 25,
  "sources_count": 15,
  "bibliography": [
    {
      "id": 1,
      "citation_text": "Smith, J. (2024). AI in Healthcare...",
      "source_title": "AI in Healthcare: A Comprehensive Review",
      "source_url": "https://example.com/paper",
      "source_author": "Dr. Jane Smith"
    }
  ],
  "footnotes": [
    {
      "id": 1,
      "text": "Additional information about methodology",
      "page_number": 5
    }
  ],
  "file_path": "/reports/ai-healthcare-report.pdf",
  "file_size_bytes": 2048576,
  "file_size_mb": 2.0,
  "file_hash": "abc123def456...",
  "storage_location": "s3",
  "is_public": false,
  "access_token": "abc123",
  "download_count": 5,
  "last_downloaded_at": "2024-01-15T11:00:00Z",
  "version": "1.0",
  "is_latest": true,
  "parent_report_id": null,
  "tags": ["AI", "Healthcare", "Research"],
  "categories": ["Technology", "Healthcare"],
  "keywords": ["artificial intelligence", "healthcare", "diagnosis"],
  "language": "en",
  "generation_time_seconds": 180.5,
  "tokens_used": 45000,
  "cost_estimate": 0.45,
  "created_at": "2024-01-15T10:34:00Z",
  "generated_at": "2024-01-15T10:37:00Z",
  "published_at": null,
  "reviewed_at": "2024-01-15T10:40:00Z"
}
```

#### GET /api/v1/reports/{report_id}/download

Download a report file.

**Response:**
```
File download with appropriate Content-Type header
```

#### POST /api/v1/reports/{report_id}/publish

Publish a report (make it public).

**Response:**
```json
{
  "id": 1,
  "is_public": true,
  "published_at": "2024-01-15T11:00:00Z"
}
```

#### POST /api/v1/reports/{report_id}/review

Review a report.

**Request Body:**
```json
{
  "status": "approved",
  "notes": "Report meets quality standards",
  "quality_score": 0.92
}
```

**Response:**
```json
{
  "id": 1,
  "review_status": "approved",
  "review_notes": "Report meets quality standards",
  "quality_score": 0.92,
  "reviewed_at": "2024-01-15T11:00:00Z"
}
```

### Users

#### GET /api/v1/users/me

Get current user profile.

**Response:**
```json
{
  "id": 1,
  "uuid": "550e8400-e29b-41d4-a716-446655440000",
  "email": "user@example.com",
  "is_active": true,
  "is_verified": true,
  "first_name": "John",
  "last_name": "Doe",
  "display_name": "John Doe",
  "full_name": "John Doe",
  "avatar_url": "https://example.com/avatar.jpg",
  "bio": "Research enthusiast",
  "company": "Acme Corp",
  "job_title": "Research Analyst",
  "website": "https://johndoe.com",
  "preferences": {
    "theme": "light",
    "notifications": true
  },
  "timezone": "UTC",
  "language": "en",
  "roles": ["user"],
  "permissions": ["create_job", "view_reports"],
  "subscription_plan": "pro",
  "subscription_status": "active",
  "subscription_expires_at": "2024-12-31T23:59:59Z",
  "monthly_requests_used": 15,
  "monthly_requests_limit": 50,
  "remaining_requests": 35,
  "total_requests_made": 150,
  "created_at": "2024-01-01T00:00:00Z",
  "last_login_at": "2024-01-15T10:00:00Z"
}
```

#### PUT /api/v1/users/me

Update current user profile.

**Request Body:**
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "bio": "Updated bio",
  "preferences": {
    "theme": "dark",
    "notifications": false
  }
}
```

#### GET /api/v1/users/activity

Get user activity feed.

**Query Parameters:**
- `limit` (int, default: 20): Number of activities to return
- `activity_type` (string, optional): Filter by activity type

**Response:**
```json
{
  "items": [
    {
      "id": 1,
      "uuid": "550e8400-e29b-41d4-a716-446655440000",
      "activity_type": "research_request",
      "description": "Created research job: AI in Healthcare",
      "metadata": {
        "job_id": 1,
        "job_title": "AI in Healthcare Research"
      },
      "ip_address": "192.168.1.1",
      "created_at": "2024-01-15T10:30:00Z"
    }
  ],
  "total": 50
}
```

### System

#### GET /health

Basic health check.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00Z",
  "version": "1.0.0"
}
```

#### GET /health/detailed

Detailed system status.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00Z",
  "version": "1.0.0",
  "services": {
    "database": {
      "status": "healthy",
      "response_time_ms": 5.2
    },
    "redis": {
      "status": "healthy",
      "response_time_ms": 1.1
    },
    "ai_services": {
      "status": "healthy",
      "openai": "available",
      "anthropic": "available"
    }
  },
  "metrics": {
    "active_jobs": 3,
    "total_users": 150,
    "system_load": 0.25
  }
}
```

#### GET /metrics

Prometheus metrics endpoint.

**Response:**
```
# HELP http_requests_total Total number of HTTP requests
# TYPE http_requests_total counter
http_requests_total{method="GET",endpoint="/api/v1/research-jobs"} 1250

# HELP research_jobs_total Total number of research jobs
# TYPE research_jobs_total counter
research_jobs_total{status="completed"} 850
research_jobs_total{status="failed"} 25
```

## Error Responses

### Standard Error Format

```json
{
  "detail": "Error message",
  "error_code": "VALIDATION_ERROR",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### Common HTTP Status Codes

- `200 OK` - Request successful
- `201 Created` - Resource created successfully
- `204 No Content` - Request successful, no content to return
- `400 Bad Request` - Invalid request data
- `401 Unauthorized` - Authentication required
- `403 Forbidden` - Insufficient permissions
- `404 Not Found` - Resource not found
- `422 Unprocessable Entity` - Validation error
- `429 Too Many Requests` - Rate limit exceeded
- `500 Internal Server Error` - Server error

### Error Codes

- `VALIDATION_ERROR` - Request data validation failed
- `AUTHENTICATION_ERROR` - Invalid credentials
- `AUTHORIZATION_ERROR` - Insufficient permissions
- `RESOURCE_NOT_FOUND` - Requested resource not found
- `RATE_LIMIT_EXCEEDED` - Rate limit exceeded
- `QUOTA_EXCEEDED` - User quota exceeded
- `WORKFLOW_ERROR` - AI workflow error
- `EXTERNAL_SERVICE_ERROR` - External service unavailable

## Rate Limiting

The API implements rate limiting to ensure fair usage:

- **Authenticated users**: 100 requests per minute
- **Anonymous users**: 10 requests per minute
- **Research job creation**: 5 requests per minute per user

Rate limit headers are included in responses:

```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1642234560
```

## Pagination

List endpoints support pagination with the following parameters:

- `page` - Page number (1-based)
- `size` - Page size (default: 20, max: 100)

Response includes pagination metadata:

```json
{
  "items": [...],
  "total": 150,
  "page": 1,
  "size": 20,
  "pages": 8
}
```

## Filtering and Sorting

Many endpoints support filtering and sorting:

### Filtering
- Use query parameters to filter results
- Multiple filters can be combined
- Some endpoints support search functionality

### Sorting
- `sort_by` - Field to sort by
- `sort_order` - Sort direction (asc/desc)
- Available sort fields vary by endpoint

## Webhooks

The API supports webhooks for real-time notifications:

### Webhook Events

- `research_job.created` - New research job created
- `research_job.started` - Research job started
- `research_job.completed` - Research job completed
- `research_job.failed` - Research job failed
- `report.generated` - New report generated
- `report.published` - Report published

### Webhook Configuration

```json
{
  "url": "https://your-domain.com/webhooks",
  "events": ["research_job.completed", "report.generated"],
  "secret": "webhook-secret-key"
}
```

### Webhook Payload

```json
{
  "event": "research_job.completed",
  "timestamp": "2024-01-15T10:30:00Z",
  "data": {
    "job_id": 1,
    "title": "AI in Healthcare Research",
    "status": "completed",
    "result_summary": "Research completed successfully"
  }
}
```

## SDKs and Libraries

### Python SDK

```python
from research_system import ResearchSystem

client = ResearchSystem(api_key="your-api-key")

# Create a research job
job = client.create_research_job(
    title="AI in Healthcare",
    query="What are the latest developments in AI for healthcare?",
    priority="high"
)

# Get job status
status = client.get_job_status(job.id)

# Download report
report = client.download_report(job.report_id)
```

### JavaScript SDK

```javascript
import { ResearchSystem } from '@research-system/sdk';

const client = new ResearchSystem({ apiKey: 'your-api-key' });

// Create a research job
const job = await client.createResearchJob({
  title: 'AI in Healthcare',
  query: 'What are the latest developments in AI for healthcare?',
  priority: 'high'
});

// Get job status
const status = await client.getJobStatus(job.id);

// Download report
const report = await client.downloadReport(job.reportId);
```

## Examples

### Complete Research Workflow

```bash
# 1. Authenticate
TOKEN=$(curl -s -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password"}' \
  | jq -r '.access_token')

# 2. Create research job
JOB_ID=$(curl -s -X POST "http://localhost:8000/api/v1/research-jobs" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "AI in Healthcare",
    "query": "What are the latest developments in AI for healthcare?",
    "priority": "high"
  }' | jq -r '.id')

# 3. Start the job
curl -X POST "http://localhost:8000/api/v1/research-jobs/$JOB_ID/start" \
  -H "Authorization: Bearer $TOKEN"

# 4. Monitor progress
while true; do
  PROGRESS=$(curl -s "http://localhost:8000/api/v1/research-jobs/$JOB_ID/progress" \
    -H "Authorization: Bearer $TOKEN" | jq -r '.progress')
  echo "Progress: $PROGRESS"
  if [ "$PROGRESS" = "1.0" ]; then
    break
  fi
  sleep 10
done

# 5. Get results
curl -s "http://localhost:8000/api/v1/research-jobs/$JOB_ID" \
  -H "Authorization: Bearer $TOKEN" | jq '.'
```

### Real-time Updates with SSE

```javascript
const eventSource = new EventSource(
  `http://localhost:8000/api/v1/research-jobs/${jobId}/stream`,
  {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  }
);

eventSource.onmessage = function(event) {
  const data = JSON.parse(event.data);
  
  switch(data.type) {
    case 'progress':
      updateProgressBar(data.data.progress);
      break;
    case 'status':
      updateStatus(data.data.status);
      break;
    case 'complete':
      showResults(data.data);
      eventSource.close();
      break;
  }
};
```

## Support

For API support and questions:

- **Documentation**: [https://docs.yourdomain.com](https://docs.yourdomain.com)
- **GitHub Issues**: [https://github.com/your-repo/issues](https://github.com/your-repo/issues)
- **Email Support**: api-support@yourdomain.com
- **Discord**: [https://discord.gg/your-server](https://discord.gg/your-server)

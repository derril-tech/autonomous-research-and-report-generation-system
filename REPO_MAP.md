# Repository Map - Autonomous Research & Report Generation System

## 🗺️ Overview
This repository contains a production-ready AI-powered platform that transforms natural language queries into fully cited, verifiable reports using LangGraph orchestration and multi-agent workflows.

## 📁 Directory Structure & Component Analysis

### 🎯 **Frontend Layer** (`/frontend/`)
**Technology Stack**: Next.js 14 (App Router), React 18, TypeScript, Tailwind CSS

#### Core Components:
- **`/app/`** - Next.js App Router pages and layouts
  - `layout.tsx` - Root layout with providers (React Query, Auth, etc.)
  - `page.tsx` - Main dashboard page with job overview
  - `globals.css` - Global styles with Tailwind CSS
  - `providers.tsx` - Context providers for state management

- **`/components/`** - Reusable React components
  - `Header.tsx` - Navigation bar with user menu and notifications
  - `Dashboard.tsx` - Main dashboard with statistics and job overview
  - `DashboardStats.tsx` - Statistics cards showing key metrics
  - `JobList.tsx` - Research jobs list with filtering and pagination
  - `JobCreationForm.tsx` - Form for creating new research jobs
  - `ProgressChart.tsx` - Real-time progress visualization
  - `ActivityFeed.tsx` - Recent activity timeline
  - `ReportViewer.tsx` - Report display and download component

#### Configuration Files:
- `package.json` - Dependencies and scripts
- `next.config.js` - Next.js configuration
- `tailwind.config.js` - Tailwind CSS configuration
- `tsconfig.json` - TypeScript configuration

### 🔧 **Backend Layer** (`/backend/`)
**Technology Stack**: FastAPI, Python 3.11+, SQLAlchemy 2.0, Pydantic

#### Core Application (`/app/`):
- **`/core/`** - Core application infrastructure
  - `config.py` - Configuration management with environment variables
  - `database.py` - Database connection and session management
  - `security.py` - Authentication, authorization, and security utilities
  - `dependencies.py` - FastAPI dependencies and injection

- **`/models/`** - SQLAlchemy database models
  - `user.py` - User model with authentication and profile data
  - `research_job.py` - Research job tracking and status management
  - `report.py` - Report storage and metadata
  - `source.py` - Research sources and citations
  - `claim.py` - Factual claims and verification

- **`/schemas/`** - Pydantic request/response schemas
  - `user.py` - User API schemas
  - `research_job.py` - Research job API schemas
  - `report.py` - Report API schemas

- **`/api/`** - API routes and endpoints
  - `/v1/` - API version 1
    - `api.py` - Main API router configuration
    - `/endpoints/` - Individual endpoint modules
      - `auth.py` - Authentication endpoints
      - `research_jobs.py` - Research job management
      - `reports.py` - Report management
      - `users.py` - User management

- **`/services/`** - Business logic services
  - `auth_service.py` - Authentication and user management
  - `research_service.py` - Research job orchestration
  - `report_service.py` - Report generation and management
  - `notification_service.py` - Real-time notifications

- **`/utils/`** - Utility functions
  - `logger.py` - Structured logging configuration
  - `helpers.py` - Common helper functions

#### Entry Points:
- `main.py` - FastAPI application entry point
- `requirements.txt` - Python dependencies

### 🤖 **AI Workflow Layer** (`/langgraph/`)
**Technology Stack**: LangGraph, LangChain, OpenAI GPT-4, Anthropic Claude

#### Core Components:
- **`workflow.py`** - Main LangGraph workflow orchestrator
  - `ResearchState` - State management for workflow execution
  - `ResearchWorkflow` - Main workflow class with node definitions

- **`/agents/`** - Individual AI agents
  - `coordinator.py` - Workflow coordination agent
  - `researcher.py` - Information retrieval agent
  - `analyst.py` - Data analysis and synthesis agent
  - `writer.py` - Report writing agent
  - `reviewer.py` - Quality review agent
  - `fact_checker.py` - Fact verification agent
  - `citation_manager.py` - Citation management agent
  - `formatter.py` - Document formatting agent
  - `publisher.py` - Final publication agent

- **`/tools/`** - Agent tools and utilities
  - `search_tools.py` - Web search and retrieval tools
  - `analysis_tools.py` - Data analysis tools
  - `citation_tools.py` - Citation and verification tools
  - `export_tools.py` - Document export tools

- **`/prompts/`** - Agent prompt templates
  - `coordinator_prompts.py` - Coordination prompts
  - `researcher_prompts.py` - Research prompts
  - `writer_prompts.py` - Writing prompts

### ⚙️ **Background Processing** (`/workers/`)
**Technology Stack**: Celery, Redis, Arq

#### Components:
- **`celery_app.py`** - Celery application configuration
- **`/tasks/`** - Background task definitions
  - `research_tasks.py` - Research workflow tasks
  - `report_tasks.py` - Report generation tasks
  - `maintenance_tasks.py` - System maintenance tasks

- **`/workers/`** - Worker process definitions
  - `research_worker.py` - Research task worker
  - `report_worker.py` - Report generation worker

### 🗄️ **Database Layer** (`/database/`)
**Technology Stack**: PostgreSQL, pgvector

#### Components:
- **`init.sql`** - Database initialization script
- **`/migrations/`** - Database migration files
  - `/alembic/` - Alembic migration versions
- **`/seeds/`** - Database seed data
  - `initial_data.sql` - Initial data population

### 📚 **Documentation** (`/docs/`)
- **`API.md`** - Comprehensive API documentation
- **`DEVELOPMENT.md`** - Development setup and guidelines
- **`DEPLOYMENT.md`** - Deployment instructions
- **`ARCHITECTURE.md`** - Detailed architecture guide

### 🧪 **Testing** (`/tests/`)
- **`/backend/`** - Backend test suites
  - `/unit/` - Unit tests
  - `/integration/` - Integration tests
  - `/e2e/` - End-to-end tests
- **`/frontend/`** - Frontend test suites
  - `/unit/` - Unit tests
  - `/integration/` - Integration tests
  - `/e2e/` - End-to-end tests
- **`/langgraph/`** - AI workflow tests

## 🔄 **Data Flow Architecture**

### 1. **User Request Flow**
```
Frontend (JobCreationForm) 
  → Backend API (research_jobs endpoint)
  → Research Service
  → LangGraph Workflow
  → Background Workers (Celery)
  → Database Storage
  → Real-time Updates (SSE)
  → Frontend Dashboard
```

### 2. **AI Workflow Flow**
```
Query Input
  → Query Understanding Agent
  → Retrieval Hub (Multiple Sources)
  → Evidence Synthesis
  → Report Drafting
  → Fact Checking
  → Visualization
  → Quality Review Gate
  → Human Approval (if needed)
  → Final Formatting
  → Report Export
```

### 3. **Real-time Updates Flow**
```
Background Workers
  → Database Updates
  → Redis Pub/Sub
  → Server-Sent Events (SSE)
  → Frontend Components
  → UI Updates
```

## 🛡️ **Security Architecture**

### Authentication & Authorization
- **JWT Tokens**: Access and refresh token system
- **Role-Based Access Control (RBAC)**: User roles and permissions
- **API Key Management**: Secure API key generation and validation
- **Rate Limiting**: Request throttling and abuse prevention

### Data Security
- **Password Hashing**: bcrypt with salt
- **Input Validation**: Pydantic schemas and sanitization
- **SQL Injection Prevention**: SQLAlchemy ORM with parameterized queries
- **XSS Prevention**: Input sanitization and output encoding

## 📊 **Monitoring & Observability**

### Logging
- **Structured Logging**: JSON format with correlation IDs
- **Log Levels**: DEBUG, INFO, WARNING, ERROR, CRITICAL
- **Log Aggregation**: Centralized logging with search capabilities

### Metrics
- **Application Metrics**: Request rates, response times, error rates
- **Business Metrics**: Job completion rates, user activity
- **AI Metrics**: Token usage, model performance, workflow success rates

### Tracing
- **Distributed Tracing**: OpenTelemetry integration
- **Workflow Tracing**: LangSmith for AI workflow debugging
- **Performance Monitoring**: Response time tracking and optimization

## 🚀 **Deployment Architecture**

### Containerization
- **Docker**: Application containerization
- **Docker Compose**: Local development environment
- **Multi-stage Builds**: Optimized production images

### Cloud Deployment
- **Frontend**: Vercel (Next.js optimization)
- **Backend**: Render (Python/FastAPI hosting)
- **Database**: Managed PostgreSQL with pgvector
- **Storage**: AWS S3 or Google Cloud Storage
- **Cache**: Redis Cloud or managed Redis

## 🔧 **Development Workflow**

### Local Development
1. **Environment Setup**: Docker Compose for services
2. **Database**: PostgreSQL with pgvector extension
3. **Cache**: Redis for session and task queue
4. **AI Services**: OpenAI and Anthropic API keys
5. **Storage**: Local file system or S3/GCS

### Testing Strategy
- **Unit Tests**: Individual component testing
- **Integration Tests**: API endpoint testing
- **E2E Tests**: Full workflow testing
- **AI Tests**: Workflow and agent testing

### Code Quality
- **Type Checking**: TypeScript and Python type hints
- **Linting**: ESLint, Prettier, Black, isort
- **Formatting**: Consistent code style across languages
- **Documentation**: Comprehensive API and code documentation

## 📈 **Scalability Considerations**

### Horizontal Scaling
- **Stateless Backend**: FastAPI with multiple instances
- **Database**: Connection pooling and read replicas
- **Cache**: Redis cluster for high availability
- **Workers**: Multiple Celery worker processes

### Performance Optimization
- **Database**: Indexing, query optimization, connection pooling
- **Caching**: Redis for frequently accessed data
- **CDN**: Static asset delivery optimization
- **Async Processing**: Background task processing

## 🔍 **Key Integration Points**

### External APIs
- **OpenAI API**: GPT-4 for text generation
- **Anthropic API**: Claude for analysis and writing
- **Search APIs**: Web search and academic databases
- **Storage APIs**: S3/GCS for file storage

### Internal Services
- **Database**: PostgreSQL with pgvector for embeddings
- **Cache**: Redis for sessions and task queue
- **Message Queue**: Celery for background processing
- **File Storage**: Local and cloud storage options

## 🎯 **Business Logic Domains**

### Research Management
- **Job Creation**: User input to research job
- **Status Tracking**: Real-time progress monitoring
- **Quality Control**: Automated and human review gates
- **Result Delivery**: Multiple export formats

### User Management
- **Authentication**: Secure login and session management
- **Authorization**: Role-based access control
- **Profile Management**: User preferences and settings
- **Usage Tracking**: Request limits and analytics

### Report Generation
- **Content Creation**: AI-powered report writing
- **Citation Management**: Automatic citation generation
- **Formatting**: Multiple output formats (PDF, DOCX, PPTX)
- **Quality Assurance**: Fact checking and verification

This repository map provides a comprehensive overview of the autonomous research system's architecture, helping developers and AI assistants understand the codebase structure, data flow, and integration points.

# Project Structure Guide for Claude Code

## 🏗️ Architecture Overview

This is an **Autonomous Research & Report Generation System** that uses AI agents to transform natural language queries into fully cited, verifiable reports. The system is built with a microservices architecture using modern technologies.

## 📁 Directory Structure

```
autonomous-research-system/
├── 📁 frontend/                    # Next.js 14 + React 18 + TypeScript
│   ├── 📁 app/                     # Next.js App Router
│   │   ├── 📄 layout.tsx          # Root layout with providers
│   │   ├── 📄 page.tsx            # Main dashboard page
│   │   ├── 📄 globals.css         # Global styles with Tailwind
│   │   └── 📄 providers.tsx       # React Query and other providers
│   ├── 📁 components/              # Reusable React components
│   │   ├── 📄 Header.tsx          # Navigation and user menu
│   │   ├── 📄 DashboardStats.tsx  # Statistics dashboard cards
│   │   ├── 📄 JobCreationForm.tsx # Research job creation form
│   │   └── 📄 JobList.tsx         # Research jobs list and management
│   ├── 📄 package.json            # Frontend dependencies
│   ├── 📄 next.config.js          # Next.js configuration
│   ├── 📄 tailwind.config.js      # Tailwind CSS configuration
│   └── 📄 tsconfig.json           # TypeScript configuration
│
├── 📁 backend/                     # FastAPI + Python 3.11+ + SQLAlchemy
│   ├── 📁 app/                     # Main application package
│   │   ├── 📁 api/                 # API routes and endpoints
│   │   │   └── 📁 v1/              # API version 1
│   │   │       ├── 📄 api.py       # API router configuration
│   │   │       └── 📁 endpoints/   # Individual endpoint modules
│   │   ├── 📁 core/                # Core application logic
│   │   │   ├── 📄 config.py        # Configuration management
│   │   │   ├── 📄 database.py      # Database connection setup
│   │   │   ├── 📄 security.py      # Authentication and authorization
│   │   │   └── 📄 dependencies.py  # FastAPI dependencies
│   │   ├── 📁 models/              # SQLAlchemy models
│   │   │   ├── 📄 user.py          # User model
│   │   │   ├── 📄 research_job.py  # Research job model
│   │   │   └── 📄 report.py        # Report model
│   │   ├── 📁 schemas/             # Pydantic schemas
│   │   │   ├── 📄 user.py          # User request/response schemas
│   │   │   ├── 📄 research_job.py  # Research job schemas
│   │   │   └── 📄 report.py        # Report schemas
│   │   ├── 📁 services/            # Business logic services
│   │   │   ├── 📄 auth_service.py  # Authentication service
│   │   │   ├── 📄 research_service.py # Research orchestration
│   │   │   └── 📄 report_service.py # Report generation
│   │   └── 📁 utils/               # Utility functions
│   │       ├── 📄 logger.py        # Logging configuration
│   │       └── 📄 helpers.py       # Helper functions
│   ├── 📄 main.py                  # FastAPI application entry point
│   ├── 📄 requirements.txt         # Python dependencies
│   └── 📄 alembic.ini             # Database migration configuration
│
├── 📁 langgraph/                   # Multi-agent orchestration
│   ├── 📄 workflow.py              # Main LangGraph workflow definition
│   ├── 📁 agents/                  # Individual AI agents
│   │   ├── 📄 coordinator.py       # Workflow coordinator agent
│   │   ├── 📄 researcher.py        # Research agent
│   │   ├── 📄 analyst.py           # Data analysis agent
│   │   ├── 📄 writer.py            # Report writing agent
│   │   ├── 📄 reviewer.py          # Quality review agent
│   │   ├── 📄 fact_checker.py      # Fact verification agent
│   │   ├── 📄 citation_manager.py  # Citation management agent
│   │   ├── 📄 formatter.py         # Document formatting agent
│   │   └── 📄 publisher.py         # Final publication agent
│   ├── 📁 tools/                   # Agent tools and utilities
│   │   ├── 📄 search_tools.py      # Web search tools
│   │   ├── 📄 analysis_tools.py    # Data analysis tools
│   │   ├── 📄 citation_tools.py    # Citation tools
│   │   └── 📄 export_tools.py      # Document export tools
│   └── 📁 prompts/                 # Agent prompt templates
│       ├── 📄 coordinator_prompts.py
│       ├── 📄 researcher_prompts.py
│       └── 📄 writer_prompts.py
│
├── 📁 workers/                     # Celery/Arq worker processes
│   ├── 📄 celery_app.py            # Celery application configuration
│   ├── 📁 tasks/                   # Background task definitions
│   │   ├── 📄 research_tasks.py    # Research workflow tasks
│   │   ├── 📄 report_tasks.py      # Report generation tasks
│   │   └── 📄 maintenance_tasks.py # System maintenance tasks
│   └── 📁 workers/                 # Worker process definitions
│       ├── 📄 research_worker.py   # Research task worker
│       └── 📄 report_worker.py     # Report generation worker
│
├── 📁 database/                    # PostgreSQL + pgvector schemas
│   ├── 📄 init.sql                 # Database initialization script
│   ├── 📁 migrations/              # Database migration files
│   │   └── 📄 alembic/             # Alembic migration versions
│   └── 📁 seeds/                   # Database seed data
│       └── 📄 initial_data.sql     # Initial data population
│
├── 📁 docs/                        # Documentation
│   ├── 📄 API.md                   # API documentation
│   ├── 📄 DEPLOYMENT.md            # Deployment guide
│   ├── 📄 DEVELOPMENT.md           # Development setup guide
│   └── 📄 ARCHITECTURE.md          # Detailed architecture guide
│
├── 📁 tests/                       # Test suites
│   ├── 📁 backend/                 # Backend tests
│   │   ├── 📁 unit/                # Unit tests
│   │   ├── 📁 integration/         # Integration tests
│   │   └── 📁 e2e/                 # End-to-end tests
│   ├── 📁 frontend/                # Frontend tests
│   │   ├── 📁 unit/                # Unit tests
│   │   ├── 📁 integration/         # Integration tests
│   │   └── 📁 e2e/                 # End-to-end tests
│   └── 📁 langgraph/               # LangGraph workflow tests
│
├── 📄 docker-compose.yml           # Docker Compose configuration
├── 📄 .env.example                 # Environment variables template
├── 📄 .gitignore                   # Git ignore patterns
├── 📄 README.md                    # Main project documentation
└── 📄 PROJECT_STRUCTURE.md         # This file

```

## 🔧 Key Technologies & Patterns

### Frontend (Next.js 14)
- **Framework**: Next.js 14 with App Router
- **Language**: TypeScript for type safety
- **Styling**: Tailwind CSS for utility-first styling
- **State Management**: React Query for server state
- **Forms**: React Hook Form with Zod validation
- **UI Components**: Headless UI + Heroicons + Lucide React
- **Charts**: Recharts for data visualization
- **File Handling**: React Dropzone for file uploads
- **Testing**: Jest + React Testing Library + Playwright

### Backend (FastAPI)
- **Framework**: FastAPI for high-performance API
- **Language**: Python 3.11+ with type hints
- **Database**: SQLAlchemy 2.0 with async support
- **Authentication**: JWT with Python-Jose
- **Validation**: Pydantic for data validation
- **Documentation**: Auto-generated OpenAPI/Swagger docs
- **Testing**: Pytest with async support

### AI/ML (LangGraph)
- **Orchestration**: LangGraph for multi-agent workflows
- **LLMs**: OpenAI GPT-4 + Anthropic Claude
- **Vector Database**: pgvector for embeddings
- **Observability**: LangSmith for tracing
- **Tools**: Custom tools for research, analysis, and formatting

### Infrastructure
- **Database**: PostgreSQL with pgvector extension
- **Cache**: Redis for session and task queue
- **Task Queue**: Celery for background processing
- **Storage**: S3/GCS for file storage
- **Monitoring**: OpenTelemetry + Grafana
- **Deployment**: Docker + Docker Compose

## 🚀 Development Workflow

### 1. Local Development Setup
```bash
# Clone and setup
git clone <repository>
cd autonomous-research-system

# Environment setup
cp .env.example .env
# Configure environment variables

# Database setup
docker-compose up -d postgres redis

# Backend setup
cd backend
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
alembic upgrade head
uvicorn main:app --reload

# Frontend setup
cd frontend
npm install
npm run dev

# Worker setup
cd workers
celery -A celery_app worker --loglevel=info
```

### 2. Code Organization Principles
- **Separation of Concerns**: Each component has a single responsibility
- **Type Safety**: TypeScript on frontend, type hints on backend
- **API-First Design**: Backend APIs designed before frontend implementation
- **Test-Driven Development**: Tests written before implementation
- **Documentation**: Comprehensive docs for all components

### 3. Key Design Patterns
- **Repository Pattern**: Data access abstraction
- **Service Layer**: Business logic encapsulation
- **Dependency Injection**: Loose coupling between components
- **Event-Driven Architecture**: Asynchronous processing
- **CQRS**: Command Query Responsibility Segregation

## 🎯 For Claude Code

When working with this codebase:

1. **Understand the Architecture**: This is a microservices-style application with clear separation between frontend, backend, AI orchestration, and background processing.

2. **Follow Existing Patterns**: 
   - Use TypeScript interfaces for frontend data structures
   - Use Pydantic models for backend data validation
   - Follow the established API patterns in the backend
   - Use the existing component structure in the frontend

3. **Key Integration Points**:
   - Frontend communicates with backend via REST APIs
   - Backend triggers LangGraph workflows via Celery tasks
   - LangGraph agents use various tools for research and analysis
   - Results are stored in PostgreSQL and cached in Redis

4. **Testing Strategy**:
   - Unit tests for individual components
   - Integration tests for API endpoints
   - E2E tests for complete workflows
   - LangGraph workflow tests for AI agent interactions

5. **Error Handling**:
   - Frontend: React Query error boundaries and toast notifications
   - Backend: FastAPI exception handlers and logging
   - LangGraph: Checkpointing and retry mechanisms

6. **Performance Considerations**:
   - Database connection pooling
   - Redis caching for frequently accessed data
   - Background processing for long-running tasks
   - Vector similarity search for content retrieval

This structure provides a solid foundation for building and extending the autonomous research system. Each component is designed to be modular, testable, and maintainable.

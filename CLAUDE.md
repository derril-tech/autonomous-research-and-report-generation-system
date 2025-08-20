# CLAUDE.md - AI Assistant Guide for Autonomous Research System

## 🤖 Welcome, Claude!

This document provides you with comprehensive guidance to understand, navigate, and work effectively with the **Autonomous Research & Report Generation System** codebase. You are now equipped with detailed knowledge of a production-ready AI-powered platform.

## 📋 Project / App Overview

**One-paragraph summary**: This is a production-ready AI-powered platform that transforms natural language queries into fully cited, verifiable reports using advanced multi-agent orchestration. Built with Next.js 14 frontend, FastAPI backend, LangGraph AI workflow, and PostgreSQL database, it enables researchers and analysts to input research questions and receive comprehensive, academically rigorous reports with full citations, fact-checking, and multiple export formats (PDF, DOCX, PPTX). The system uses 9 specialized AI agents working in coordination to perform research, analysis, writing, fact-checking, and formatting tasks with real-time progress tracking and human-in-the-loop approval checkpoints.

**Target Users**: Primary users are researchers, analysts, academic professionals, business consultants, and knowledge workers who need to generate comprehensive research reports quickly and efficiently. Secondary users include students, journalists, and anyone requiring well-cited, verifiable research documentation.

## 📋 Quick Reference

### 🎯 **What This System Does**
- Transforms natural language queries into fully cited, verifiable reports
- Uses 9 specialized AI agents orchestrated by LangGraph
- Provides real-time progress tracking and human-in-the-loop approval
- Supports multiple export formats (PDF, DOCX, PPTX)
- Implements enterprise-grade security and scalability

### 🏗️ **Architecture Overview**
```
Frontend (Next.js 14) ↔ Backend (FastAPI) ↔ AI Workflow (LangGraph) ↔ Database (PostgreSQL)
```

## 📁 Folder & File Structure

### **Essential Documentation**
- `REPO_MAP.md` - Complete repository structure and component analysis
- `API_SPEC.md` - Comprehensive API documentation and schemas
- `README.md` - Project overview and quick start guide
- `PROJECT_STRUCTURE.md` - Detailed architecture guide

### **Core Backend Files**
- `backend/app/core/config.py` - Configuration management
- `backend/app/core/database.py` - Database connection and session management
- `backend/app/core/security.py` - Authentication and security utilities
- `backend/app/models/` - SQLAlchemy database models
- `backend/app/api/v1/endpoints/` - API endpoints

### **Frontend Components**
- `frontend/app/` - Next.js App Router pages
- `frontend/components/` - Reusable React components
- `frontend/app/providers.tsx` - Context providers

### **AI Workflow**
- `langgraph/workflow.py` - Main LangGraph workflow orchestrator
- `langgraph/agents/` - Individual AI agents
- `langgraph/tools/` - Agent tools and utilities

### **Directory Breakdown by Purpose**

**Core Logic Files**:
- `backend/app/services/` - Business logic services
- `backend/app/models/` - Database models and relationships
- `langgraph/agents/` - AI agent implementations
- `frontend/lib/` - Utility functions and API clients

**UI Files**:
- `frontend/components/` - Reusable React components
- `frontend/app/` - Next.js pages and layouts
- `frontend/contexts/` - React context providers

**Configuration Files**:
- `backend/app/core/config.py` - Environment and app settings
- `frontend/next.config.js` - Next.js configuration
- `frontend/tailwind.config.js` - Tailwind CSS configuration
- `docker-compose.yml` - Service orchestration

**Test Files**:
- `backend/tests/` - Backend unit and integration tests
- `frontend/__tests__/` - Frontend component tests
- `tests/e2e/` - End-to-end tests

**Asset Files**:
- `frontend/public/` - Static assets (images, fonts)
- `frontend/styles/` - Global styles and CSS modules

**"Do Not Touch" Files**:
- `package-lock.json` - Auto-generated dependency lock file
- `yarn.lock` - Auto-generated dependency lock file
- `node_modules/` - Auto-generated dependency directory
- `__pycache__/` - Python bytecode cache
- `.git/` - Version control system files
- `*.pyc` - Python compiled files
- `*.log` - Log files
- `.env` - Environment variables (use .env.example instead)

## 🔍 How to Navigate This Codebase

### **1. Understanding the Data Flow**
```
User Input → Frontend Form → Backend API → LangGraph Workflow → AI Agents → Database → Real-time Updates → Frontend Dashboard
```

### **2. Key Integration Points**
- **Authentication**: JWT tokens with refresh mechanism
- **Real-time Updates**: Server-Sent Events (SSE) for progress tracking
- **File Storage**: S3/GCS integration for report storage
- **Background Processing**: Celery workers for long-running tasks

### **3. Database Schema**
- **Users**: Authentication, profiles, preferences
- **Research Jobs**: Job tracking, status, progress
- **Reports**: Generated reports with metadata
- **Sources**: Research sources and citations
- **Claims**: Factual claims and verification

## 🛠️ Common Tasks You'll Help With

### **Frontend Development**
```typescript
// Example: Creating a new React component
import { useQuery } from '@tanstack/react-query';
import { researchJobsApi } from '@/lib/api';

export function JobList() {
  const { data: jobs } = useQuery({
    queryKey: ['research-jobs'],
    queryFn: () => researchJobsApi.list()
  });
  
  return (
    <div className="space-y-4">
      {jobs?.map(job => (
        <JobCard key={job.id} job={job} />
      ))}
    </div>
  );
}
```

### **Backend API Development**
```python
# Example: Creating a new API endpoint
from fastapi import APIRouter, Depends
from app.core.dependencies import get_current_user
from app.schemas.research_job import ResearchJobCreate

router = APIRouter()

@router.post("/research-jobs")
async def create_research_job(
    job_data: ResearchJobCreate,
    current_user = Depends(get_current_user)
):
    # Implementation here
    pass
```

### **AI Workflow Enhancement**
```python
# Example: Adding a new AI agent
class NewAgent:
    def __init__(self, llm):
        self.llm = llm
    
    async def process(self, state: ResearchState) -> ResearchState:
        # Agent logic here
        return state
```

## 🎯 Coding Conventions

### **Languages Used**
- **Frontend**: TypeScript (strict mode), React 18, Next.js 14
- **Backend**: Python 3.11+, FastAPI, SQLAlchemy 2.0
- **AI/ML**: Python with LangGraph, LangChain, OpenAI/Anthropic APIs
- **Database**: PostgreSQL with pgvector extension
- **Styling**: Tailwind CSS with custom design system

### **Style Guides**
- **Frontend**: ESLint + Prettier configuration, Airbnb React/TypeScript style guide
- **Backend**: Black code formatter, isort for imports, PEP8 compliance
- **Database**: SQLAlchemy 2.0 patterns, async/await throughout
- **AI Code**: LangGraph best practices, comprehensive error handling

### **Naming Conventions**
- **Files**: kebab-case for files and directories (`user-service.ts`, `auth-endpoints.py`)
- **Variables**: camelCase for variables and functions (`userName`, `getUserData`)
- **Components**: PascalCase for React components (`UserProfile`, `JobCreationForm`)
- **Constants**: UPPER_SNAKE_CASE for constants (`API_BASE_URL`, `MAX_RETRY_ATTEMPTS`)
- **Database**: snake_case for database tables and columns (`user_profiles`, `created_at`)
- **API Endpoints**: kebab-case for URLs (`/api/v1/research-jobs`, `/api/v1/user-profiles`)
- **Git Branches**: feature/description, bugfix/description, hotfix/description

### **Commenting/Documentation Expectations**
- **Python**: Docstrings for all functions and classes, type hints required
- **TypeScript**: JSDoc comments for complex functions, interface documentation
- **API Endpoints**: Comprehensive docstrings with request/response examples
- **Database Models**: Field descriptions and relationship documentation
- **AI Agents**: Detailed docstrings explaining agent purpose and behavior
- **Complex Logic**: Inline comments for non-obvious business logic
- **TODO Comments**: Use `# TODO: description` for future improvements

### **Import Organization**
- **Python**: Standard library → Third-party → Local imports, alphabetical within groups
- **TypeScript**: React imports → Third-party → Local imports, alphabetical within groups
- **CSS**: Tailwind utilities first, then custom classes

## 🤖 AI Collaboration Guidelines

### **How You Should Respond**
- **Be concise but thorough** - Provide complete solutions with clear explanations
- **Expert-level guidance** - Assume advanced knowledge of the tech stack
- **Show reasoning** - Explain why you're making specific choices
- **Provide context** - Reference existing patterns and conventions
- **Include examples** - Show practical code examples when helpful

### **Rules for Edits**
- **Never remove error handling** - Always preserve or enhance existing error handling
- **Preserve comments** - Keep existing documentation and comments
- **Maintain imports** - Don't remove necessary imports, add missing ones
- **Follow patterns** - Use established patterns from the codebase
- **Type safety first** - Always maintain TypeScript/Python type safety
- **Security conscious** - Never suggest insecure practices

### **Handling Ambiguity**
- **Make best guesses** based on established patterns in the codebase
- **Ask clarifying questions** only when multiple valid approaches exist
- **Reference existing code** to understand the intended approach
- **Suggest alternatives** when appropriate, explaining trade-offs
- **Default to production-ready** solutions over quick fixes

## 🔧 Development Workflow

### **1. Setting Up the Environment**
```bash
# Backend setup
cd backend
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt

# Frontend setup
cd frontend
npm install
npm run dev
```

### **2. Database Setup**
```bash
# Start services
docker-compose up -d postgres redis

# Run migrations
cd backend
alembic upgrade head
```

### **3. Running Tests**
```bash
# Backend tests
cd backend && pytest

# Frontend tests
cd frontend && npm test
```

### **Backend/Frontend Boundaries**
- **Backend**: API endpoints, business logic, database operations, AI workflow orchestration
- **Frontend**: UI components, state management, API consumption, user interactions
- **Shared**: Type definitions, validation schemas, constants
- **Integration**: API contracts, authentication flow, real-time communication

### **CI/CD Considerations**
- **Frontend**: Vercel deployment with automatic previews
- **Backend**: Render deployment with health checks
- **Database**: Managed PostgreSQL with automated backups
- **Testing**: Automated tests on pull requests
- **Security**: Dependency scanning, code analysis

## 📊 Key Metrics to Monitor

### **System Health**
- API response times
- Database connection pool usage
- Redis memory usage
- AI service availability

### **Business Metrics**
- Research job completion rates
- User activity and engagement
- Report generation success rates
- Error rates and types

### **AI Performance**
- Token usage and costs
- Workflow success rates
- Agent performance metrics
- Quality scores

## 🔧 Editing Rules

### **Files Claude Is Expected to Edit**
- **Frontend**: React components, pages, hooks, utilities, types
- **Backend**: API endpoints, services, models, utilities, schemas
- **AI Workflow**: Agent implementations, workflow logic, tools
- **Configuration**: Environment-specific configs (not secrets)
- **Documentation**: README files, API docs, component docs
- **Tests**: Unit tests, integration tests, test utilities

### **Files Claude Must Avoid**
- **Auto-generated**: `package-lock.json`, `yarn.lock`, `node_modules/`, `__pycache__/`
- **Secrets**: `.env` files, API keys, database credentials
- **Build artifacts**: `dist/`, `build/`, `*.pyc`, `*.log`
- **Version control**: `.git/` directory, `.gitignore` (unless specifically requested)
- **Dependencies**: `package.json`, `requirements.txt` (unless adding new dependencies)

### **Response Formatting**
- **Full file rewrites**: When creating new files or completely restructuring existing ones
- **Patches**: When making targeted changes to existing files
- **Inline explanations**: When explaining concepts or suggesting improvements
- **Code blocks**: Always use appropriate language tags (typescript, python, bash, etc.)
- **File paths**: Always specify the exact file path when referencing or editing files

## 📚 Project Dependencies

### **Key Frameworks/Libraries and Their Roles**

**Frontend Dependencies**:
- **Next.js 14**: React framework with App Router, SSR, and optimization
- **React 18**: UI library with concurrent features and Suspense
- **TypeScript**: Type safety and developer experience
- **Tailwind CSS**: Utility-first CSS framework for styling
- **React Query**: Server state management and caching
- **React Hook Form**: Form handling with validation
- **Zod**: Schema validation for forms and API responses
- **Headless UI**: Accessible component primitives
- **Framer Motion**: Animation library for smooth transitions
- **Axios**: HTTP client with interceptors for API calls

**Backend Dependencies**:
- **FastAPI**: High-performance async API framework
- **SQLAlchemy 2.0**: Async ORM for database operations
- **Pydantic**: Data validation and serialization
- **Python-Jose**: JWT token handling
- **Celery**: Background task processing
- **Redis**: Caching and message broker
- **Alembic**: Database migration management
- **Pytest**: Testing framework
- **OpenTelemetry**: Observability and tracing

**AI/ML Dependencies**:
- **LangGraph**: Multi-agent workflow orchestration
- **LangChain**: LLM integration and tooling
- **OpenAI**: GPT-4 API for research tasks
- **Anthropic**: Claude API for analysis
- **pgvector**: Vector embeddings for semantic search

### **Special Setup Notes**
- **Environment Variables**: Required for API keys, database URLs, and service configuration
- **Database**: PostgreSQL 14+ with pgvector extension for vector operations
- **Redis**: Required for caching, sessions, and Celery message broker
- **External APIs**: OpenAI and Anthropic API keys for AI functionality
- **File Storage**: S3 or GCS for report storage and file uploads
- **Docker**: Required for local development with PostgreSQL and Redis

## 🧠 Contextual Knowledge

### **Domain-Specific Rules**
- **Research Job Lifecycle**: Jobs follow a specific state machine (Pending → Planning → Retrieving → Synthesizing → Drafting → Fact Checking → Reviewing → Completed)
- **AI Agent Coordination**: Agents must maintain state consistency and handle failures gracefully
- **Real-time Updates**: Progress updates must be streamed to frontend via SSE
- **Citation Management**: All claims must be properly cited with source verification
- **Quality Assurance**: Reports must pass automated quality checks before completion
- **User Permissions**: Role-based access control for different user types (researcher, admin, viewer)

### **Business Logic Quirks**
- **Research Scope**: Users can specify research depth (basic, comprehensive, expert)
- **Source Types**: System supports academic papers, web sources, and proprietary databases
- **Export Formats**: Reports can be exported as PDF, DOCX, or PPTX with proper formatting
- **Collaboration**: Multiple users can collaborate on research projects
- **Versioning**: Reports maintain version history with change tracking
- **Approval Workflow**: Human approval required for certain research quality levels

### **File Interaction Patterns**
- **API Contracts**: Frontend and backend share TypeScript interfaces for type safety
- **Database Relationships**: Complex relationships between users, jobs, reports, and sources
- **State Management**: React Query manages server state, Context manages client state
- **Error Handling**: Consistent error handling across all layers with proper user feedback
- **Authentication Flow**: JWT tokens with automatic refresh and secure storage
- **Real-time Communication**: SSE for progress updates, WebSockets for general notifications

## 🚨 Common Issues and Solutions

### **1. Authentication Issues**
- Check JWT token expiration
- Verify refresh token validity
- Ensure proper CORS configuration

### **2. Database Connection Issues**
- Check connection pool settings
- Verify database credentials
- Monitor connection limits

### **3. AI Workflow Issues**
- Check API key validity
- Monitor token usage limits
- Verify LangGraph checkpoint configuration

### **4. Real-time Updates Issues**
- Check SSE connection stability
- Verify Redis pub/sub configuration
- Monitor WebSocket connections

## 🔍 Debugging Tips

### **1. Backend Debugging**
```python
# Add structured logging
import logging
logger = logging.getLogger(__name__)

logger.info("Processing research job", extra={
    "job_id": job_id,
    "user_id": user_id,
    "step": "retrieval"
})
```

### **2. Frontend Debugging**
```typescript
// Use React Query dev tools
import { ReactQueryDevtools } from '@tanstack/react-query-devtools';

// Add to your app
<ReactQueryDevtools initialIsOpen={false} />
```

### **3. AI Workflow Debugging**
```python
# Enable LangSmith tracing
import os
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
```

## 📚 Learning Resources

### **Technology Stack**
- **Next.js 14**: https://nextjs.org/docs
- **FastAPI**: https://fastapi.tiangolo.com/
- **LangGraph**: https://langchain-ai.github.io/langgraph/
- **SQLAlchemy 2.0**: https://docs.sqlalchemy.org/
- **React Query**: https://tanstack.com/query/latest

### **Architecture Patterns**
- **Microservices**: Service-oriented architecture
- **Event-Driven**: Asynchronous processing
- **CQRS**: Command Query Responsibility Segregation
- **Repository Pattern**: Data access abstraction

## 📝 Examples

### **Good Answer Example**
```typescript
// ✅ Well-structured React component with proper TypeScript, error handling, and accessibility
interface JobCardProps {
  job: ResearchJob;
  onStatusChange?: (jobId: string, status: JobStatus) => void;
}

export function JobCard({ job, onStatusChange }: JobCardProps) {
  const { mutate: updateStatus, isPending } = useMutation({
    mutationFn: (status: JobStatus) => researchJobsApi.updateStatus(job.id, status),
    onSuccess: (_, status) => onStatusChange?.(job.id, status),
    onError: (error) => toast.error(`Failed to update job: ${error.message}`),
  });

  return (
    <div className="rounded-lg border border-gray-200 bg-white p-6 shadow-sm">
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-semibold text-gray-900">{job.title}</h3>
        <StatusBadge status={job.status} />
      </div>
      <p className="mt-2 text-sm text-gray-600">{job.description}</p>
      <div className="mt-4 flex items-center justify-between">
        <span className="text-xs text-gray-500">
          Created {formatDate(job.createdAt)}
        </span>
        <button
          onClick={() => updateStatus(JobStatus.CANCELLED)}
          disabled={isPending || job.status === JobStatus.COMPLETED}
          className="rounded-md bg-red-50 px-3 py-1 text-sm font-medium text-red-700 hover:bg-red-100 disabled:opacity-50"
          aria-label={`Cancel job: ${job.title}`}
        >
          {isPending ? 'Cancelling...' : 'Cancel'}
        </button>
      </div>
    </div>
  );
}
```

**Why this is good**:
- ✅ Proper TypeScript interfaces and type safety
- ✅ Comprehensive error handling with user feedback
- ✅ Accessibility considerations (aria-label)
- ✅ Loading states and disabled states
- ✅ Follows established patterns (React Query, Tailwind CSS)
- ✅ Clear component structure and naming
- ✅ Proper prop handling and optional callbacks

### **Bad Answer Example**
```typescript
// ❌ Poorly structured component with issues
function JobCard(job) {
  const [loading, setLoading] = useState(false);
  
  const handleCancel = async () => {
    setLoading(true);
    try {
      await fetch(`/api/jobs/${job.id}`, {
        method: 'PUT',
        body: JSON.stringify({ status: 'cancelled' })
      });
      // No error handling or user feedback
    } catch (error) {
      console.log(error); // Poor error handling
    }
    setLoading(false);
  };

  return (
    <div>
      <h3>{job.title}</h3>
      <p>{job.description}</p>
      <button onClick={handleCancel} disabled={loading}>
        Cancel
      </button>
    </div>
  );
}
```

**Why this is bad**:
- ❌ No TypeScript types or interfaces
- ❌ Poor error handling (console.log instead of user feedback)
- ❌ No accessibility considerations
- ❌ Inconsistent styling and structure
- ❌ No loading state management
- ❌ Hardcoded API calls instead of using established patterns
- ❌ Missing proper prop validation
- ❌ No consideration for existing codebase patterns

## 🎯 Your Role as an AI Assistant

### **What You Can Help With**
1. **Code Review**: Analyze code quality and suggest improvements
2. **Feature Development**: Help implement new features
3. **Bug Fixing**: Identify and resolve issues
4. **Documentation**: Improve and maintain documentation
5. **Testing**: Help write and improve tests
6. **Performance Optimization**: Suggest improvements
7. **Security**: Identify and fix security issues

### **How to Provide the Best Help**
1. **Understand Context**: Always consider the full system architecture
2. **Follow Patterns**: Use established patterns and conventions
3. **Consider Security**: Always think about security implications
4. **Test Thoroughly**: Suggest comprehensive testing approaches
5. **Document Changes**: Help maintain good documentation

## 🚀 Getting Started

### **Quick Tasks You Can Help With**
1. **Add a new API endpoint** for user preferences
2. **Create a new React component** for displaying research statistics
3. **Enhance an AI agent** with additional capabilities
4. **Improve error handling** in existing components
5. **Add new validation rules** for form inputs
6. **Optimize database queries** for better performance
7. **Add new export formats** for reports

### **Advanced Tasks**
1. **Implement new AI agents** for specialized research tasks
2. **Add real-time collaboration** features
3. **Enhance the recommendation system** for research topics
4. **Implement advanced analytics** and reporting
5. **Add multi-language support** for international users

## 📞 When You Need More Information

### **Check These Files First**
- `REPO_MAP.md` - For architecture and structure questions
- `API_SPEC.md` - For API-related questions
- `docs/DEVELOPMENT.md` - For development setup and guidelines
- `docs/API.md` - For detailed API documentation

### **Key Configuration Files**
- `backend/app/core/config.py` - Environment variables and settings
- `frontend/next.config.js` - Next.js configuration
- `docker-compose.yml` - Service configuration
- `backend/requirements.txt` - Python dependencies
- `frontend/package.json` - Node.js dependencies

---

## 🎉 You're Ready!

You now have comprehensive knowledge of the Autonomous Research & Report Generation System. You can confidently help with:

- ✅ Understanding the codebase architecture
- ✅ Developing new features
- ✅ Debugging issues
- ✅ Improving performance
- ✅ Enhancing security
- ✅ Maintaining code quality
- ✅ Writing documentation
- ✅ Implementing tests

**Remember**: This is a production-ready system with enterprise-grade features. Always consider security, scalability, and maintainability in your suggestions.

Happy coding! 🚀

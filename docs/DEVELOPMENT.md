# Development Guide

## 🚀 Getting Started

This guide will help you set up the Autonomous Research & Report Generation System for development.

### Prerequisites

- **Python 3.11+** - [Download here](https://www.python.org/downloads/)
- **Node.js 18+** - [Download here](https://nodejs.org/)
- **PostgreSQL 14+** - [Download here](https://www.postgresql.org/download/)
- **Redis 6+** - [Download here](https://redis.io/download)
- **Docker & Docker Compose** - [Download here](https://docs.docker.com/get-docker/)

### Quick Start

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd autonomous-research-system
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Start infrastructure services**
   ```bash
   docker-compose up -d postgres redis
   ```

4. **Set up the backend**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   alembic upgrade head
   uvicorn main:app --reload
   ```

5. **Set up the frontend**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

6. **Start the worker processes**
   ```bash
   cd workers
   celery -A celery_app worker --loglevel=info
   ```

## 🏗️ Architecture Overview

### System Components

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │    │   Workers       │
│   (Next.js)     │◄──►│   (FastAPI)     │◄──►│   (Celery)      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   PostgreSQL    │    │     Redis       │    │   LangGraph     │
│   (Database)    │    │   (Cache/Queue) │    │  (AI Workflow)  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Technology Stack

#### Frontend
- **Framework**: Next.js 14 with App Router
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **State Management**: React Query
- **UI Components**: Headless UI + Heroicons
- **Forms**: React Hook Form + Zod
- **Charts**: Recharts
- **Testing**: Jest + React Testing Library

#### Backend
- **Framework**: FastAPI
- **Language**: Python 3.11+
- **Database**: SQLAlchemy 2.0 (async)
- **Authentication**: JWT with Python-Jose
- **Validation**: Pydantic
- **Task Queue**: Celery + Redis
- **Testing**: Pytest

#### AI/ML
- **Orchestration**: LangGraph
- **LLMs**: OpenAI GPT-4 + Anthropic Claude
- **Vector Database**: pgvector
- **Observability**: LangSmith
- **Tools**: Custom research and analysis tools

#### Infrastructure
- **Database**: PostgreSQL with pgvector
- **Cache**: Redis
- **Storage**: S3/GCS (configurable)
- **Monitoring**: OpenTelemetry + Grafana
- **Deployment**: Docker + Docker Compose

## 📁 Project Structure

```
autonomous-research-system/
├── frontend/                 # Next.js frontend application
│   ├── app/                 # Next.js App Router pages
│   ├── components/          # Reusable React components
│   ├── hooks/              # Custom React hooks
│   ├── lib/                # Utility libraries
│   ├── types/              # TypeScript type definitions
│   └── public/             # Static assets
├── backend/                 # FastAPI backend application
│   ├── app/                # Main application package
│   │   ├── api/            # API routes and endpoints
│   │   ├── core/           # Core application logic
│   │   ├── models/         # SQLAlchemy models
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── services/       # Business logic services
│   │   └── utils/          # Utility functions
│   ├── tests/              # Backend tests
│   └── alembic/            # Database migrations
├── langgraph/              # AI workflow orchestration
│   ├── agents/             # Individual AI agents
│   ├── tools/              # Agent tools and utilities
│   └── prompts/            # Agent prompt templates
├── workers/                # Background task processing
│   ├── tasks/              # Celery task definitions
│   └── workers/            # Worker process definitions
├── database/               # Database schemas and migrations
├── docs/                   # Documentation
└── docker/                 # Docker configuration
```

## 🔧 Development Setup

### Environment Configuration

Create a `.env` file in the root directory with the following variables:

```bash
# Application
APP_NAME="Autonomous Research System"
DEBUG=true
ENVIRONMENT=development

# Database
DATABASE_URL=postgresql+asyncpg://research_user:password@localhost:5432/research_db

# Redis
REDIS_URL=redis://localhost:6379

# Security
SECRET_KEY=your-development-secret-key
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# AI Services
OPENAI_API_KEY=your-openai-api-key
ANTHROPIC_API_KEY=your-anthropic-api-key
LANGCHAIN_API_KEY=your-langsmith-api-key

# Search APIs
TAVILY_API_KEY=your-tavily-api-key
SERPAPI_API_KEY=your-serpapi-key

# Storage
STORAGE_TYPE=local
UPLOAD_DIR=./uploads

# Task Queue
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

### Database Setup

1. **Install PostgreSQL extensions**
   ```sql
   CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
   CREATE EXTENSION IF NOT EXISTS "pgvector";
   ```

2. **Run migrations**
   ```bash
   cd backend
   alembic upgrade head
   ```

3. **Seed initial data (optional)**
   ```bash
   python scripts/seed_data.py
   ```

### Development Workflow

#### Backend Development

1. **Start the development server**
   ```bash
   cd backend
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Run tests**
   ```bash
   pytest
   pytest --cov=app tests/
   pytest -v tests/test_api/
   ```

3. **Code formatting and linting**
   ```bash
   black app/
   isort app/
   flake8 app/
   mypy app/
   ```

#### Frontend Development

1. **Start the development server**
   ```bash
   cd frontend
   npm run dev
   ```

2. **Run tests**
   ```bash
   npm test
   npm run test:coverage
   npm run test:e2e
   ```

3. **Code formatting and linting**
   ```bash
   npm run lint
   npm run type-check
   ```

#### AI Workflow Development

1. **Test LangGraph workflows**
   ```bash
   cd langgraph
   python -m pytest tests/
   ```

2. **Run workflow examples**
   ```bash
   python examples/basic_research.py
   ```

## 🧪 Testing

### Backend Testing

The backend uses pytest for testing with the following structure:

```
backend/tests/
├── unit/                   # Unit tests
│   ├── test_models.py     # Model tests
│   ├── test_services.py   # Service tests
│   └── test_utils.py      # Utility tests
├── integration/           # Integration tests
│   ├── test_api.py        # API endpoint tests
│   └── test_database.py   # Database integration tests
└── e2e/                   # End-to-end tests
    └── test_workflows.py  # Complete workflow tests
```

**Running tests:**
```bash
# All tests
pytest

# Specific test file
pytest tests/test_api.py

# With coverage
pytest --cov=app --cov-report=html

# Parallel execution
pytest -n auto
```

### Frontend Testing

The frontend uses Jest and React Testing Library:

```
frontend/tests/
├── unit/                   # Unit tests
│   ├── components/        # Component tests
│   └── hooks/             # Hook tests
├── integration/           # Integration tests
└── e2e/                   # End-to-end tests (Playwright)
```

**Running tests:**
```bash
# Unit tests
npm test

# Watch mode
npm run test:watch

# Coverage
npm run test:coverage

# E2E tests
npm run test:e2e
```

## 🔍 Debugging

### Backend Debugging

1. **Enable debug logging**
   ```bash
   export LOG_LEVEL=DEBUG
   uvicorn main:app --reload --log-level debug
   ```

2. **Use Python debugger**
   ```python
   import pdb; pdb.set_trace()
   ```

3. **Database debugging**
   ```bash
   # Enable SQL logging
   export SQLALCHEMY_ECHO=true
   ```

### Frontend Debugging

1. **React Developer Tools**
   - Install browser extension
   - Use React DevTools for component inspection

2. **Network debugging**
   ```bash
   # Enable API request logging
   export REACT_APP_DEBUG_API=true
   ```

3. **Error boundaries**
   - Check browser console for errors
   - Use React Error Boundary components

## 📊 Monitoring and Observability

### Logging

The application uses structured logging with different levels:

```python
import logging

logger = logging.getLogger(__name__)
logger.info("User action", extra={"user_id": user_id, "action": "create_job"})
logger.error("Database error", exc_info=True)
```

### Metrics

Key metrics to monitor:

- **API Response Times**: Average and 95th percentile
- **Database Query Performance**: Slow query detection
- **Task Queue Performance**: Queue length and processing time
- **AI Workflow Performance**: Token usage and completion rates
- **User Activity**: Active users and job creation rates

### Health Checks

Health check endpoints:

- `GET /health` - Basic health check
- `GET /health/detailed` - Detailed system status
- `GET /metrics` - Prometheus metrics

## 🔒 Security

### Authentication

- JWT tokens with configurable expiration
- Refresh token rotation
- Role-based access control (RBAC)

### Data Protection

- Input validation with Pydantic
- SQL injection prevention with SQLAlchemy
- XSS protection with proper content encoding
- CSRF protection with tokens

### API Security

- Rate limiting per user/IP
- Request size limits
- CORS configuration
- API key authentication for external services

## 🚀 Deployment

### Development Deployment

```bash
# Using Docker Compose
docker-compose up -d

# Manual deployment
./scripts/deploy-dev.sh
```

### Production Deployment

```bash
# Using Docker
docker build -t research-system .
docker run -p 8000:8000 research-system

# Using Kubernetes
kubectl apply -f k8s/
```

## 🤝 Contributing

### Code Style

#### Python (Backend)
- Follow PEP 8 style guide
- Use type hints
- Maximum line length: 88 characters (Black)
- Import sorting with isort

#### TypeScript (Frontend)
- Use ESLint and Prettier
- Follow React best practices
- Use TypeScript strict mode
- Component naming: PascalCase

### Git Workflow

1. **Create feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make changes and commit**
   ```bash
   git add .
   git commit -m "feat: add new research feature"
   ```

3. **Push and create PR**
   ```bash
   git push origin feature/your-feature-name
   ```

### Commit Message Format

Use conventional commits:

```
type(scope): description

feat(api): add research job creation endpoint
fix(frontend): resolve job list pagination issue
docs(readme): update installation instructions
test(backend): add unit tests for user service
```

## 📚 Additional Resources

### Documentation
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Next.js Documentation](https://nextjs.org/docs)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)

### Tools
- [Postman](https://www.postman.com/) - API testing
- [pgAdmin](https://www.pgadmin.org/) - Database management
- [Redis Commander](https://github.com/joeferner/redis-commander) - Redis management
- [LangSmith](https://smith.langchain.com/) - AI workflow debugging

### Community
- [Discord Server](https://discord.gg/your-server)
- [GitHub Issues](https://github.com/your-repo/issues)
- [Discussion Forum](https://github.com/your-repo/discussions)

## 🆘 Troubleshooting

### Common Issues

1. **Database connection errors**
   - Check PostgreSQL is running
   - Verify DATABASE_URL format
   - Ensure database exists

2. **Redis connection errors**
   - Check Redis is running
   - Verify REDIS_URL format
   - Check Redis authentication

3. **API key errors**
   - Verify API keys are set correctly
   - Check API key permissions
   - Ensure sufficient credits

4. **Frontend build errors**
   - Clear node_modules and reinstall
   - Check Node.js version compatibility
   - Verify environment variables

### Getting Help

1. Check the [FAQ](docs/FAQ.md)
2. Search [GitHub Issues](https://github.com/your-repo/issues)
3. Ask in [Discord](https://discord.gg/your-server)
4. Create a new issue with detailed information

### Performance Optimization

1. **Database optimization**
   - Add appropriate indexes
   - Use connection pooling
   - Monitor slow queries

2. **Frontend optimization**
   - Code splitting
   - Image optimization
   - Bundle analysis

3. **AI workflow optimization**
   - Parallel processing
   - Caching strategies
   - Token usage optimization

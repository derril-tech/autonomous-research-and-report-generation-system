# Autonomous Research & Report Generation System

A production-ready AI-powered platform that transforms natural language queries into fully cited, verifiable reports using LangGraph orchestration and multi-agent workflows.

### 🚀 Features

- **Natural Language Interface**: Simple query input that triggers autonomous research
- **Multi-Agent Orchestration**: 9 specialized AI agents working in harmony
- **Human-in-the-Loop**: Interactive approval checkpoints throughout the process
- **Durability**: Checkpointed long runs with resume capability
- **Observability**: Full traces, timings, and token usage monitoring
- **Multiple Export Formats**: PDF, Docx, PPTX with proper formatting
- **Continuous Monitoring**: Scheduled refreshes with change detection
- **Enterprise Security**: JWT auth, rate limiting, PII handling

### 🏗️ Architecture

```
├── frontend/                 # Next.js 14 + React 18 + TypeScript
├── backend/                  # FastAPI + Python 3.11+ + SQLAlchemy
├── workers/                  # Celery/Arq worker processes
├── langgraph/               # Multi-agent orchestration
├── database/                # PostgreSQL + pgvector schemas
├── docker/                  # Containerization setup
└── docs/                    # Documentation
```

### 🛠️ Tech Stack

- **Frontend**: Next.js 14, React 18, TypeScript, Tailwind CSS
- **Backend**: FastAPI, Python 3.11+, SQLAlchemy, JWT
- **Database**: PostgreSQL, pgvector, Redis
- **AI/ML**: LangGraph, LangChain, OpenAI, Anthropic Claude
- **Storage**: S3/GCS for artifacts
- **Observability**: LangSmith, OpenTelemetry
- **Deployment**: Vercel (Frontend), Render (Backend)

### 📋 Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL 14+
- Redis 6+
- Docker & Docker Compose

### 🚀 Quick Start

1. **Clone and Setup**
   ```bash
   git clone <repository>
   cd autonomous-research-system
   ```

2. **Environment Setup**
   ```bash
   cp .env.example .env
   # Configure your environment variables
   ```

3. **Database Setup**
   ```bash
   docker-compose up -d postgres redis
   cd backend && alembic upgrade head
   ```

4. **Backend Setup**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # or `venv\Scripts\activate` on Windows
   pip install -r requirements.txt
   uvicorn main:app --reload
   ```

5. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

6. **Worker Setup**
   ```bash
   cd workers
   celery -A worker.celery worker --loglevel=info
   ```

### 🔧 Configuration

Key environment variables:
- `DATABASE_URL`: PostgreSQL connection string
- `REDIS_URL`: Redis connection string
- `OPENAI_API_KEY`: OpenAI API key
- `ANTHROPIC_API_KEY`: Anthropic Claude API key
- `JWT_SECRET_KEY`: JWT signing secret
- `AWS_ACCESS_KEY_ID`: S3 access key
- `AWS_SECRET_ACCESS_KEY`: S3 secret key

### 📊 API Documentation

Once running, visit:
- **Backend API**: http://localhost:8000/docs
- **Frontend**: http://localhost:3000

### 🧪 Testing

```bash
# Backend tests
cd backend && pytest

# Frontend tests
cd frontend && npm test

# E2E tests
npm run test:e2e
```

### 🚀 Deployment

The system is configured for deployment on:
- **Frontend**: Vercel
- **Backend**: Render
- **Database**: Managed PostgreSQL
- **Storage**: AWS S3 or Google Cloud Storage

### 📈 Monitoring

- **LangSmith**: AI workflow traces and debugging
- **OpenTelemetry**: Application metrics and traces
- **Grafana**: Dashboard and alerting

### 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

### 📄 License

MIT License - see LICENSE file for details

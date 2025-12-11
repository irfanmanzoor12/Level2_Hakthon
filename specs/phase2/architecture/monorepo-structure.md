# Phase II - Monorepo Structure

## Overview

Phase II uses a **monorepo** approach with frontend and backend in a single repository.

## Benefits of Monorepo

✅ **Single source of truth** - All code in one place
✅ **Shared specs** - Specs accessible to both frontend and backend
✅ **Atomic commits** - Change frontend + backend together
✅ **Simplified CI/CD** - One repository to deploy
✅ **Claude Code friendly** - Single context for AI

## Directory Structure

```
hackathon-todo-phase2/
├── .spec-kit/
│   └── config.yaml              # Spec-Kit configuration for Phase II
│
├── specs/                       # All specifications
│   ├── phase1/                  # Phase I specs (reference)
│   │   ├── constitution.md
│   │   └── features/
│   └── phase2/                  # Phase II specs ⭐
│       ├── constitution.md      # Phase II vision
│       ├── architecture/        # System architecture
│       │   ├── overview.md
│       │   ├── monorepo-structure.md
│       │   └── database-schema.md
│       ├── api/                 # API specifications
│       │   ├── endpoints.md
│       │   └── authentication.md
│       ├── frontend/            # Frontend specifications
│       │   ├── architecture.md
│       │   ├── components.md
│       │   └── pages.md
│       ├── backend/             # Backend specifications
│       │   ├── architecture.md
│       │   └── services.md
│       └── features/            # Feature specifications
│           ├── user-auth.md
│           └── task-management.md
│
├── frontend/                    # Next.js application ⭐
│   ├── app/                     # Next.js App Router
│   │   ├── layout.tsx           # Root layout
│   │   ├── page.tsx             # Home page
│   │   ├── (auth)/              # Auth routes group
│   │   │   ├── login/
│   │   │   │   └── page.tsx
│   │   │   └── register/
│   │   │       └── page.tsx
│   │   └── (dashboard)/         # Protected routes group
│   │       ├── layout.tsx
│   │       └── tasks/
│   │           └── page.tsx
│   ├── components/              # React components
│   │   ├── ui/                  # Base UI components
│   │   │   ├── button.tsx
│   │   │   ├── input.tsx
│   │   │   └── card.tsx
│   │   ├── task-list.tsx
│   │   ├── task-item.tsx
│   │   ├── task-form.tsx
│   │   └── navbar.tsx
│   ├── lib/                     # Utilities
│   │   ├── api.ts               # API client
│   │   ├── auth.ts              # Auth utilities
│   │   └── utils.ts             # General utilities
│   ├── hooks/                   # Custom React hooks
│   │   ├── use-tasks.ts
│   │   └── use-auth.ts
│   ├── types/                   # TypeScript types
│   │   ├── task.ts
│   │   └── user.ts
│   ├── public/                  # Static assets
│   ├── .env.local               # Environment variables
│   ├── next.config.js           # Next.js config
│   ├── tailwind.config.js       # Tailwind config
│   ├── tsconfig.json            # TypeScript config
│   ├── package.json             # Dependencies
│   └── CLAUDE.md                # Frontend-specific instructions
│
├── backend/                     # FastAPI application ⭐
│   ├── app/
│   │   ├── main.py              # FastAPI entry point
│   │   ├── config.py            # Configuration
│   │   ├── models/              # SQLModel database models
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   └── task.py
│   │   ├── routes/              # API endpoints
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   └── tasks.py
│   │   ├── services/            # Business logic
│   │   │   ├── __init__.py
│   │   │   ├── auth_service.py
│   │   │   └── task_service.py
│   │   ├── middleware/          # Middleware
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   └── cors.py
│   │   ├── database.py          # Database connection
│   │   └── dependencies.py      # FastAPI dependencies
│   ├── tests/                   # Backend tests
│   │   ├── test_auth.py
│   │   └── test_tasks.py
│   ├── .env                     # Environment variables
│   ├── pyproject.toml           # UV dependencies
│   └── CLAUDE.md                # Backend-specific instructions
│
├── docker-compose.yml           # Local development setup
├── .gitignore                   # Git ignore rules
├── CLAUDE.md                    # Root Claude Code instructions
├── README.md                    # Project documentation
├── GETTING_STARTED.md           # Quick start guide
└── DEPLOYMENT.md                # Deployment instructions
```

## File Descriptions

### Root Level

**CLAUDE.md**
- How to navigate the monorepo
- Reference to frontend/backend CLAUDE.md
- Spec-driven workflow instructions

**README.md**
- Project overview
- Features list
- Setup instructions
- Links to frontend/backend

**docker-compose.yml**
- Local development environment
- PostgreSQL container
- Backend service
- Frontend service (optional)

### Frontend (Next.js)

**Key Files:**
- `app/layout.tsx` - Root layout with auth provider
- `app/(auth)/login/page.tsx` - Login page
- `app/(dashboard)/tasks/page.tsx` - Main tasks page
- `components/task-list.tsx` - Task list component
- `lib/api.ts` - API client with JWT handling
- `types/task.ts` - Task TypeScript types

### Backend (FastAPI)

**Key Files:**
- `app/main.py` - FastAPI app with routes
- `app/models/task.py` - Task SQLModel
- `app/routes/tasks.py` - Task API endpoints
- `app/services/task_service.py` - Task business logic
- `app/middleware/auth.py` - JWT validation
- `app/database.py` - Neon connection

## Environment Variables

### Frontend `.env.local`
```bash
# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000

# Better Auth
BETTER_AUTH_SECRET=your-secret-key-here
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

### Backend `.env`
```bash
# Database
DATABASE_URL=postgresql://user:pass@localhost/todo_db

# Auth
BETTER_AUTH_SECRET=your-secret-key-here
JWT_SECRET=your-jwt-secret-here
JWT_ALGORITHM=HS256
JWT_EXPIRATION_DAYS=7

# CORS
CORS_ORIGINS=http://localhost:3000,https://your-app.vercel.app

# Environment
ENVIRONMENT=development
```

## Development Workflow

### Starting the Application

**Option 1: Docker Compose (Recommended)**
```bash
# Start all services
docker-compose up

# Frontend: http://localhost:3000
# Backend: http://localhost:8000
# Database: PostgreSQL on port 5432
```

**Option 2: Manual Start**
```bash
# Terminal 1: Backend
cd backend
uv run uvicorn app.main:app --reload --port 8000

# Terminal 2: Frontend
cd frontend
npm run dev

# Frontend: http://localhost:3000
# Backend: http://localhost:8000
```

### Working with Specs

**Create new spec:**
```bash
# Create in appropriate directory
touch specs/phase2/features/new-feature.md
```

**Reference spec in Claude Code:**
```
@specs/phase2/features/new-feature.md implement this feature
```

### Making Changes

**Backend change:**
1. Update spec in `specs/phase2/backend/`
2. Ask Claude Code to implement
3. Code generated in `backend/`
4. Test with Swagger UI at http://localhost:8000/docs

**Frontend change:**
1. Update spec in `specs/phase2/frontend/`
2. Ask Claude Code to implement
3. Code generated in `frontend/`
4. Test in browser at http://localhost:3000

**Full-stack feature:**
1. Update specs in both backend and frontend
2. Implement backend first (API)
3. Test API endpoints
4. Implement frontend (UI)
5. Test integration

## Git Workflow

### Branch Strategy
```bash
main          # Production code
├── develop   # Development branch
    ├── feature/auth        # Feature branches
    ├── feature/tasks
    └── feature/ui
```

### Commit Convention
```bash
# Format
<type>(<scope>): <description>

# Examples
feat(backend): add task API endpoints
feat(frontend): add task list component
fix(auth): fix JWT token validation
docs(specs): update database schema spec
```

### Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting
- `refactor`: Code restructuring
- `test`: Tests
- `chore`: Maintenance

## Package Management

### Frontend (pnpm)
```bash
cd frontend
pnpm install              # Install dependencies
pnpm add <package>        # Add package
pnpm dev                  # Run dev server
pnpm build                # Build for production
```

### Backend (UV)
```bash
cd backend
uv sync                   # Install dependencies
uv add <package>          # Add package
uv run uvicorn app.main:app --reload  # Run dev server
```

## Testing Strategy

### Backend Tests
```bash
cd backend
uv run pytest
```

### Frontend Tests (Future)
```bash
cd frontend
pnpm test
```

### Integration Tests
```bash
# Test full flow: register → login → create task
```

## Deployment

### Frontend (Vercel)
```bash
cd frontend
vercel --prod
```

### Backend (Railway)
```bash
cd backend
railway up
```

## Monorepo Benefits in Practice

### 1. Shared Types
```typescript
// Frontend can reference backend types
// (Copy from backend or use shared package)
```

### 2. Atomic Changes
```bash
git commit -m "feat: add task priority field to backend and frontend"
# Single commit updates both
```

### 3. Unified Specs
```
@specs/phase2/features/task-priority.md
- Defines frontend UI
- Defines backend API
- Defines database schema
- All in one spec!
```

### 4. Claude Code Context
```
You: "Implement task priority feature"
Claude: [Reads spec, updates backend + frontend]
```

## Common Commands Reference

```bash
# Start everything
docker-compose up

# Backend only
cd backend && uv run uvicorn app.main:app --reload

# Frontend only
cd frontend && pnpm dev

# Install dependencies
cd frontend && pnpm install
cd backend && uv sync

# Run tests
cd backend && uv run pytest
cd frontend && pnpm test

# Deploy
cd frontend && vercel --prod
cd backend && railway up

# View API docs
# Open http://localhost:8000/docs
```

---

**This monorepo structure keeps everything organized while allowing Claude Code to work efficiently across the full stack.**

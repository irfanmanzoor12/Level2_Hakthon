# Phase II - Implementation Plan

## Overview

This document provides a step-by-step plan for implementing Phase II: Full-Stack Web Application.

**Timeline**: December 9-14, 2025 (6 days)
**Points**: 150
**Deadline**: Sunday, December 14, 2025

---

## Implementation Strategy

### ✅ Spec-Driven Development Approach

1. All specs are written ✅ (Done!)
2. Use Claude Code to generate implementation
3. Test as you build
4. Deploy early, deploy often
5. Iterate based on feedback

### 🎯 Build Order: Backend → Frontend → Integration

**Why Backend First?**
- API is the foundation
- Can test with Swagger UI
- Frontend depends on working API
- Easier to debug

---

## Day-by-Day Plan

### **Day 1 (Dec 9): Project Setup & Backend Foundation**

#### Morning: Project Structure
- [ ] Create Phase II monorepo folder
- [ ] Initialize frontend/ and backend/ directories
- [ ] Copy Phase I specs to specs/phase1/
- [ ] Set up git repository
- [ ] Create .gitignore

#### Afternoon: Backend Setup
- [ ] Initialize FastAPI project (backend/)
- [ ] Set up SQLModel models (User, Task)
- [ ] Connect to Neon database
- [ ] Create database tables
- [ ] Test database connection

**Deliverables:**
- ✅ Monorepo structure
- ✅ Backend skeleton
- ✅ Database connected

---

### **Day 2 (Dec 10): Backend API - Authentication**

#### Morning: Auth Implementation
- [ ] Implement user registration endpoint
- [ ] Implement password hashing (bcrypt)
- [ ] Implement login endpoint
- [ ] Implement JWT token generation

#### Afternoon: Auth Middleware
- [ ] Create JWT validation middleware
- [ ] Test auth endpoints with Swagger UI
- [ ] Handle auth errors properly

**Deliverables:**
- ✅ POST /api/auth/register
- ✅ POST /api/auth/login
- ✅ JWT middleware working

**Testing:**
```bash
# Register user
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"Test123","name":"Test"}'

# Login
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"Test123"}'
```

---

### **Day 3 (Dec 11): Backend API - Tasks**

#### Morning: Task CRUD
- [ ] Implement GET /api/{user_id}/tasks
- [ ] Implement POST /api/{user_id}/tasks
- [ ] Implement GET /api/{user_id}/tasks/{id}

#### Afternoon: More Task Operations
- [ ] Implement PUT /api/{user_id}/tasks/{id}
- [ ] Implement DELETE /api/{user_id}/tasks/{id}
- [ ] Implement PATCH /api/{user_id}/tasks/{id}/complete
- [ ] Add user isolation (verify user_id matches JWT)

**Deliverables:**
- ✅ All 6 task endpoints working
- ✅ User isolation enforced
- ✅ API fully tested

**Testing:**
```bash
# Get token from login, then:
curl -X GET http://localhost:8000/api/{user_id}/tasks \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

### **Day 4 (Dec 12): Frontend Setup & Authentication UI**

#### Morning: Frontend Setup
- [ ] Initialize Next.js project (frontend/)
- [ ] Install dependencies (Tailwind, shadcn/ui)
- [ ] Set up Better Auth configuration
- [ ] Create API client (lib/api.ts)
- [ ] Configure environment variables

#### Afternoon: Auth Pages
- [ ] Create login page
- [ ] Create registration page
- [ ] Implement auth context/provider
- [ ] Test login/register flow

**Deliverables:**
- ✅ Next.js app running
- ✅ Login page working
- ✅ Registration page working
- ✅ JWT stored in cookies/localStorage

---

### **Day 5 (Dec 13): Frontend - Tasks UI**

#### Morning: Task List
- [ ] Create tasks page layout
- [ ] Implement task list component
- [ ] Fetch tasks from API
- [ ] Display tasks with status indicators

#### Afternoon: Task Operations
- [ ] Create "Add Task" form/modal
- [ ] Implement task creation
- [ ] Implement task completion toggle
- [ ] Implement task deletion
- [ ] Implement task editing

**Deliverables:**
- ✅ Full tasks UI working
- ✅ All CRUD operations functional
- ✅ Responsive design

---

### **Day 6 (Dec 14): Polish, Deploy & Submit**

#### Morning: Final Polish
- [ ] Add loading states
- [ ] Add error handling
- [ ] Improve UI/UX
- [ ] Test all features end-to-end
- [ ] Fix any bugs

#### Afternoon: Deployment
- [ ] Deploy backend to Railway/Render
- [ ] Deploy frontend to Vercel
- [ ] Configure environment variables
- [ ] Test production deployment
- [ ] Verify all features work

#### Evening: Submission
- [ ] Record demo video (< 90 seconds)
- [ ] Update README with live URLs
- [ ] Push final code to GitHub
- [ ] Submit hackathon form
- [ ] Join Zoom presentation

**Deliverables:**
- ✅ Production deployment live
- ✅ Demo video recorded
- ✅ Form submitted
- ✅ Phase II complete!

---

## Detailed Implementation Steps

### Step 1: Backend Setup

```bash
# Create backend directory
mkdir -p backend/app/{models,routes,services,middleware}
cd backend

# Initialize UV project
uv init

# Add dependencies
uv add fastapi uvicorn sqlmodel psycopg2-binary python-jose passlib bcrypt python-multipart

# Create main.py
touch app/main.py
```

**Files to Create:**
```
backend/
├── app/
│   ├── main.py              # FastAPI app
│   ├── config.py            # Configuration
│   ├── database.py          # Database connection
│   ├── models/
│   │   ├── user.py          # User model
│   │   └── task.py          # Task model
│   ├── routes/
│   │   ├── auth.py          # Auth endpoints
│   │   └── tasks.py         # Task endpoints
│   ├── services/
│   │   ├── auth_service.py  # Auth logic
│   │   └── task_service.py  # Task logic
│   └── middleware/
│       └── auth.py          # JWT middleware
├── .env                     # Environment variables
└── pyproject.toml          # UV config
```

### Step 2: Database Setup

**Create Neon Database:**
1. Go to neon.tech
2. Create new project "hackathon-todo"
3. Copy connection string
4. Add to .env

**Initialize Database:**
```python
# app/database.py
from sqlmodel import create_engine, SQLModel
import os

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

def create_tables():
    SQLModel.metadata.create_all(engine)
```

### Step 3: Frontend Setup

```bash
# Create frontend
npx create-next-app@latest frontend --typescript --tailwind --app
cd frontend

# Install dependencies
pnpm add better-auth jose

# Install shadcn/ui
pnpm dlx shadcn@latest init
pnpm dlx shadcn@latest add button input card form
```

**Files to Create:**
```
frontend/
├── app/
│   ├── layout.tsx
│   ├── page.tsx             # Home/redirect
│   ├── (auth)/
│   │   ├── login/page.tsx
│   │   └── register/page.tsx
│   └── (dashboard)/
│       └── tasks/page.tsx
├── components/
│   ├── task-list.tsx
│   ├── task-item.tsx
│   └── task-form.tsx
├── lib/
│   ├── api.ts               # API client
│   └── auth.ts              # Auth utilities
└── .env.local               # Environment variables
```

---

## Using Claude Code for Implementation

### Backend Implementation

**Example Prompt:**
```
@specs/phase2/architecture/database-schema.md
@specs/phase2/api/endpoints.md

Implement the User and Task SQLModel models according to these specs.
Create them in backend/app/models/
```

**Another Example:**
```
@specs/phase2/api/endpoints.md

Implement POST /api/auth/register endpoint in backend/app/routes/auth.py
Include:
- Email validation
- Password hashing
- User creation
- JWT token generation
```

### Frontend Implementation

**Example Prompt:**
```
@specs/phase2/frontend/pages.md

Create the tasks page in frontend/app/(dashboard)/tasks/page.tsx
Include:
- Fetch tasks from API
- Display in a list
- Add task form
- Toggle complete
- Delete task
```

---

## Testing Strategy

### Backend Testing

**Manual Testing with Swagger:**
1. Start backend: `uv run uvicorn app.main:app --reload`
2. Open http://localhost:8000/docs
3. Test each endpoint

**cURL Testing:**
```bash
# Register
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"Test123","name":"Test"}'

# Save token from response, then:
export TOKEN="YOUR_JWT_TOKEN"

# Create task
curl -X POST http://localhost:8000/api/{user_id}/tasks \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"Test task","description":"Test"}'

# List tasks
curl -X GET http://localhost:8000/api/{user_id}/tasks \
  -H "Authorization: Bearer $TOKEN"
```

### Frontend Testing

**Manual Testing:**
1. Start frontend: `pnpm dev`
2. Open http://localhost:3000
3. Register new user
4. Login
5. Create tasks
6. Test all CRUD operations
7. Test on mobile viewport

### Integration Testing

**End-to-End Flow:**
1. Register → Login → Create task → View task → Complete task → Delete task
2. Test error cases (invalid input, unauthorized access)
3. Test multi-user isolation (two users, separate data)

---

## Deployment Guide

### Backend Deployment (Railway)

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Initialize project
railway init

# Add environment variables in Railway dashboard:
# - DATABASE_URL
# - BETTER_AUTH_SECRET
# - JWT_SECRET
# - CORS_ORIGINS

# Deploy
railway up
```

### Frontend Deployment (Vercel)

```bash
# Install Vercel CLI
npm install -g vercel

# Login
vercel login

# Deploy
cd frontend
vercel --prod

# Add environment variables in Vercel dashboard:
# - NEXT_PUBLIC_API_URL (Railway URL)
# - BETTER_AUTH_SECRET
```

---

## Troubleshooting Guide

### Common Issues

**Issue: Database connection fails**
- Check DATABASE_URL in .env
- Verify Neon database is active
- Check SSL mode in connection string

**Issue: JWT token not working**
- Verify JWT_SECRET is same in .env
- Check token expiration
- Verify Authorization header format

**Issue: CORS errors**
- Add frontend URL to CORS_ORIGINS
- Check middleware configuration
- Verify preflight requests

**Issue: Frontend can't reach backend**
- Check NEXT_PUBLIC_API_URL
- Verify backend is running
- Check network tab for errors

---

## Success Criteria Checklist

### Functional Requirements
- [ ] User can register
- [ ] User can login
- [ ] User can add tasks
- [ ] User can view tasks
- [ ] User can update tasks
- [ ] User can delete tasks
- [ ] User can mark tasks complete
- [ ] Users only see their own tasks
- [ ] Data persists across sessions

### Technical Requirements
- [ ] Backend API deployed and accessible
- [ ] Frontend deployed and accessible
- [ ] Database connected and working
- [ ] Authentication working
- [ ] All specs implemented
- [ ] Code in GitHub
- [ ] Demo video recorded
- [ ] Form submitted

### Quality Requirements
- [ ] UI is responsive (mobile + desktop)
- [ ] Error handling works
- [ ] Loading states shown
- [ ] Code is clean and documented
- [ ] README has setup instructions

---

## Demo Video Script (90 seconds)

**0:00-0:10** - Introduction
- "Phase II: Full-stack Todo web app"
- Show homepage

**0:10-0:25** - Authentication
- Register new user
- Login

**0:25-0:50** - Task Management
- Create 2-3 tasks
- Mark one complete
- Update one task
- Delete one task

**0:50-0:70** - Technical Highlights
- Show responsive design (resize browser)
- Mention tech stack (Next.js, FastAPI, PostgreSQL)
- Show it's deployed online

**0:70-0:90** - Spec-Driven Approach
- Briefly show specs folder
- Explain all code generated from specs
- Thank judges, show GitHub link

---

## Post-Submission Checklist

- [ ] GitHub repository is public
- [ ] README has live URLs
- [ ] Both deployments are working
- [ ] Demo video is under 90 seconds
- [ ] Form submitted with all info
- [ ] Joined Zoom for presentation (if invited)

---

## Next: Preparing for Phase III

After Phase II submission, start planning:
- MCP server architecture
- OpenAI Agents SDK integration
- Natural language processing
- Chatbot UI design

---

**Follow this plan, use Claude Code for implementation, and you'll complete Phase II successfully!** 🚀

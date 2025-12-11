# Todo App - Phase I & II

> **Hackathon II**: The Evolution of Todo - Mastering Spec-Driven Development & Cloud Native AI

A full-stack todo application built using **Spec-Driven Development** with Claude Code and Spec-Kit Plus.

## 🎯 Project Overview

This project demonstrates spec-driven development across two phases:
- **Phase I**: Python console application
- **Phase II**: Full-stack web application (Next.js + FastAPI + PostgreSQL)

## 📋 Features

### Phase I - Console App ✅
- Add Task - Create new todo items
- View Tasks - Display all tasks with status indicators
- Update Task - Modify existing task details
- Delete Task - Remove tasks from the list
- Mark Complete - Toggle task completion status

### Phase II - Web App ✅
- **User Authentication** - Register and login with JWT
- **Task Management** - Full CRUD operations via web interface
- **User Isolation** - Each user sees only their tasks
- **Persistent Storage** - PostgreSQL database via Neon
- **RESTful API** - FastAPI backend with Swagger docs
- **Modern Frontend** - Next.js 15 with TypeScript and Tailwind CSS

## 🏗️ Project Structure

```
hackathon-todo/
├── .spec-kit/
│   └── config.yaml              # Spec-Kit configuration
│
├── specs/                       # All specifications
│   ├── phase1/                  # Phase I specs
│   │   ├── constitution.md
│   │   └── features/
│   └── phase2/                  # Phase II specs ⭐
│       ├── constitution.md
│       ├── architecture/
│       ├── api/
│       ├── frontend/
│       └── IMPLEMENTATION_PLAN.md
│
├── src/                         # Phase I console app
│   ├── main.py
│   ├── models.py
│   ├── storage.py
│   └── ui.py
│
├── backend/                     # Phase II backend ⭐
│   ├── app/
│   │   ├── main.py
│   │   ├── models/
│   │   ├── routes/
│   │   ├── services/
│   │   └── middleware/
│   └── pyproject.toml
│
├── frontend/                    # Phase II frontend ⭐
│   ├── app/
│   │   ├── auth/               # Login/Register
│   │   └── dashboard/          # Tasks page
│   ├── components/
│   ├── lib/api.ts
│   └── package.json
│
└── README.md                    # This file
```

## 🚀 Quick Start

### Phase I - Console App

```bash
# Run the console app
python src/main.py
```

### Phase II - Full Stack App

#### Backend (FastAPI)

```bash
cd backend

# Install dependencies
uv sync

# Create .env file
cp .env.example .env
# Add your Neon DATABASE_URL and JWT_SECRET

# Run server
uv run uvicorn app.main:app --reload --port 8000

# API: http://localhost:8000
# Docs: http://localhost:8000/docs
```

#### Frontend (Next.js)

```bash
cd frontend

# Install dependencies
npm install

# Create .env.local file
cp .env.local.example .env.local

# Run development server
npm run dev

# App: http://localhost:3000
```

## 🔧 Tech Stack

### Phase I
- **Language**: Python 3.13+
- **Package Manager**: UV
- **Storage**: In-memory
- **Interface**: Command-line

### Phase II
**Backend:**
- **Framework**: FastAPI
- **Database**: PostgreSQL (Neon)
- **ORM**: SQLModel
- **Authentication**: JWT (python-jose + bcrypt)

**Frontend:**
- **Framework**: Next.js 15 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **State**: React Hooks + localStorage

## 📖 API Documentation

### Authentication Endpoints
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user

### Task Endpoints (Protected)
- `GET /api/{user_id}/tasks` - List all tasks
- `POST /api/{user_id}/tasks` - Create task
- `GET /api/{user_id}/tasks/{id}` - Get specific task
- `PUT /api/{user_id}/tasks/{id}` - Update task (full)
- `PATCH /api/{user_id}/tasks/{id}` - Update task (partial)
- `PATCH /api/{user_id}/tasks/{id}/complete` - Toggle completion
- `DELETE /api/{user_id}/tasks/{id}` - Delete task

**Interactive API Docs**: http://localhost:8000/docs

## 🧪 Testing

### Phase I Testing
```bash
python test_app.py
```

### Phase II Testing

**Backend:**
- Use Swagger UI at http://localhost:8000/docs
- Test with cURL or Postman

**Frontend:**
1. Register a new user
2. Login
3. Create tasks
4. Test all CRUD operations
5. Test on mobile viewport

**End-to-End Flow:**
1. Register → Login → Create task → View task → Complete task → Delete task
2. Test error cases (invalid input, unauthorized access)
3. Test multi-user isolation (two users, separate data)

## 🌐 Deployment

### Backend - Railway/Render

```bash
cd backend

# Set environment variables:
# - DATABASE_URL (Neon PostgreSQL)
# - JWT_SECRET
# - CORS_ORIGINS

# Deploy
railway up
# or
render deploy
```

### Frontend - Vercel

```bash
cd frontend

# Set environment variables:
# - NEXT_PUBLIC_API_URL (Backend URL)

# Deploy
vercel --prod
```

## 🎓 Development Approach

This project follows **Spec-Driven Development**:

1. **Write Specifications First**: All features defined in `/specs`
2. **Generate with AI**: Claude Code generates implementation from specs
3. **Test & Refine**: Iterate on specs and regenerate code
4. **No Manual Coding**: Following hackathon rules strictly

### Working with Specs

```bash
# Reference specs in Claude Code
@specs/phase2/api/endpoints.md implement this

# Create new specs
touch specs/phase2/features/new-feature.md
```

## 🎯 Hackathon Details

**Phases**: I & II of V
**Points**: 100 (Phase I) + 150 (Phase II) = 250 total
**Focus**: Spec-Driven Development

### Completed Objectives
- ✅ Master spec-driven development workflow
- ✅ Build Python console application
- ✅ Create full-stack web application
- ✅ Implement user authentication
- ✅ Set up PostgreSQL database
- ✅ Deploy production-ready app

### Future Phases
- **Phase III**: AI chatbot with OpenAI ChatKit + MCP
- **Phase IV**: Kubernetes deployment with Minikube
- **Phase V**: Cloud deployment with Kafka + Dapr

## 📊 Database Schema

### Users Table
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255),
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
);
```

### Tasks Table
```sql
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
);
```

## 🛡️ Security

- **Password Hashing**: bcrypt with passlib
- **JWT Tokens**: 7-day expiration
- **User Isolation**: Backend verifies user_id matches JWT
- **CORS**: Configured origins only
- **SQL Injection**: Protected by SQLModel ORM

## 🤝 Contributing

This is a hackathon project following spec-driven development:

1. Update or create specifications in `/specs`
2. Use Claude Code to generate implementation
3. Test and refine specifications as needed
4. Submit via hackathon form with demo video

## 👥 Credits

**Developed by**: Irfan Manzoor
**Hackathon**: Hackathon II - Panaversity, PIAIC, GIAIC
**Approach**: Spec-Driven Development
**AI Assistant**: Claude Code (Anthropic)

## 🔗 Resources

- **Spec-Kit Plus**: [github.com/panaversity/spec-kit-plus](https://github.com/panaversity/spec-kit-plus)
- **Claude Code**: [claude.com/product/claude-code](https://claude.com/product/claude-code)
- **FastAPI**: [fastapi.tiangolo.com](https://fastapi.tiangolo.com)
- **Next.js**: [nextjs.org](https://nextjs.org)
- **Neon**: [neon.tech](https://neon.tech)

## 📄 License

This project is part of Hackathon II for educational purposes.

---

*Built with specifications, powered by AI* ✨
**Phase I**: Console App ✅
**Phase II**: Full-Stack Web App ✅

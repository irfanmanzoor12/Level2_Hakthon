# Todo App Phase II - Constitution

## Vision Evolution

Transform the Phase I console application into a **modern, full-stack web application** that provides:
- Beautiful, intuitive user interface
- Multi-user support with authentication
- Persistent data storage
- RESTful API architecture
- Foundation for Phase III AI integration

## Core Principles

### 1. User Experience First
- **Intuitive UI**: Users should accomplish tasks without thinking
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Fast Performance**: Instant feedback, optimistic updates
- **Accessibility**: WCAG compliant, keyboard navigation

### 2. Security by Design
- **Authentication**: Secure user registration and login
- **Authorization**: Users only see their own data
- **Data Protection**: JWT tokens, secure password hashing
- **API Security**: CORS, rate limiting, input validation

### 3. Scalable Architecture
- **API-First**: Backend independent of frontend
- **Stateless API**: Ready for horizontal scaling
- **Database**: Serverless PostgreSQL (Neon)
- **Deployment**: Vercel (frontend), separate backend

### 4. Maintainable Code
- **Monorepo**: Frontend + Backend in single repository
- **Type Safety**: TypeScript (frontend), type hints (backend)
- **Code Quality**: Linting, formatting, testing
- **Documentation**: Clear README, API docs, architecture docs

### 5. Spec-Driven Development
- **Specifications First**: All features spec'd before implementation
- **AI-Generated Code**: Use Claude Code to generate from specs
- **Iterative Refinement**: Refine specs, regenerate code
- **No Manual Coding**: Stay true to spec-driven approach

## Technical Decisions

### Frontend Stack
```
Framework: Next.js 15+ (App Router)
Language: TypeScript
Styling: Tailwind CSS
UI Components: shadcn/ui
State Management: React hooks + Context (simple state)
Authentication: Better Auth (client-side)
API Client: Fetch API with custom wrapper
Deployment: Vercel
```

### Backend Stack
```
Framework: FastAPI
Language: Python 3.13+
ORM: SQLModel
Database: Neon Serverless PostgreSQL
Authentication: Better Auth + JWT
Validation: Pydantic
API Docs: FastAPI automatic OpenAPI
Deployment: Railway / Render / DigitalOcean
```

### Development Tools
```
Package Managers: UV (Python), pnpm (Node.js)
Code Quality: Ruff (Python), ESLint (TypeScript)
Spec Management: Spec-Kit Plus
AI Assistant: Claude Code
```

## Architecture Principles

### 1. Monorepo Structure
```
hackathon-todo-phase2/
├── frontend/          # Next.js application
├── backend/           # FastAPI application
├── specs/             # All specifications
├── docker-compose.yml # Local development
└── README.md          # Project documentation
```

### 2. API-First Design
- Backend exposes RESTful API
- Frontend consumes API
- API can be used by multiple clients (web, mobile, AI chatbot in Phase III)
- Clear API contracts defined in specs

### 3. Database Design
- Relational data model (PostgreSQL)
- User table (managed by Better Auth)
- Tasks table (owned by users)
- Proper foreign keys and indexes
- Migration system for schema changes

### 4. Authentication Flow
- Better Auth handles user management
- JWT tokens for API authentication
- Token stored in HTTP-only cookies (secure)
- Backend validates JWT on every request
- User isolation at API level

## Success Criteria

### Functional Requirements
- ✅ User can register and login
- ✅ User can add, view, update, delete, complete tasks
- ✅ Each user sees only their own tasks
- ✅ Data persists across sessions
- ✅ Responsive UI works on all devices

### Non-Functional Requirements
- ✅ Page load time < 2 seconds
- ✅ API response time < 200ms
- ✅ Handles 100+ tasks per user without slowdown
- ✅ Mobile-friendly responsive design
- ✅ Accessible (keyboard navigation, screen readers)

### Technical Requirements
- ✅ Full TypeScript coverage (frontend)
- ✅ Full type hints (backend)
- ✅ API documentation (OpenAPI/Swagger)
- ✅ Error handling on all endpoints
- ✅ Input validation on all forms

## User Stories

### Authentication
- As a new user, I can register with email and password
- As a returning user, I can log in to access my tasks
- As a logged-in user, I can log out securely
- As a user, my session persists across page refreshes

### Task Management (Same as Phase I, but in web UI)
- As a user, I can add a new task with title and description
- As a user, I can view all my tasks in a list
- As a user, I can update a task's title or description
- As a user, I can delete a task I no longer need
- As a user, I can mark a task as complete or incomplete

### User Experience
- As a user, I see immediate feedback when I perform actions
- As a user, I can use the app on my phone
- As a user, I can navigate using keyboard shortcuts
- As a user, errors are explained clearly

## Evolution Path

### From Phase I
- ✅ Console app → Web app
- ✅ In-memory storage → PostgreSQL
- ✅ Single user → Multi-user
- ✅ Local only → Deployed online

### To Phase III
- Web app → AI chatbot interface
- REST API → MCP tools
- Manual interactions → Natural language
- Human-driven → AI-assisted

### To Phase IV-V
- Single server → Kubernetes cluster
- Synchronous → Event-driven (Kafka)
- Monolith → Microservices (Dapr)
- Simple features → Advanced (recurring, reminders)

## Development Philosophy

### Spec-Driven Workflow
```
1. Write detailed specifications
   ↓
2. Review and refine specs
   ↓
3. Use Claude Code to generate implementation
   ↓
4. Test generated code
   ↓
5. Refine specs if needed
   ↓
6. Regenerate code
   ↓
7. Deploy and verify
```

### Quality Standards
- **Code**: Clean, readable, well-structured
- **Tests**: Core functionality tested
- **Docs**: Clear setup and usage instructions
- **Specs**: Detailed, unambiguous, implementable
- **UI**: Polished, professional appearance

## Constraints and Assumptions

### Constraints
- Must complete by December 14, 2025
- Must deploy frontend to Vercel (free tier)
- Must use Neon PostgreSQL (free tier)
- Must demonstrate in 90-second video
- Must be single-person project

### Assumptions
- Users have modern web browsers
- Users have internet connection
- Basic familiarity with todo apps
- English language interface (bonus for Urdu)
- Desktop and mobile usage expected

## Risk Management

### Technical Risks
- **Database limits**: Neon free tier has limits → Monitor usage
- **Deployment issues**: Free tier downtime → Have backup plan
- **Integration complexity**: Auth + API → Test thoroughly

### Mitigation Strategies
- Start with backend API first (foundation)
- Test authentication early
- Deploy early, deploy often
- Keep features simple initially
- Add polish iteratively

## Deliverables

### Required for Submission
1. ✅ Public GitHub repository
2. ✅ Deployed frontend (Vercel URL)
3. ✅ Deployed backend API (public endpoint)
4. ✅ All specs in /specs directory
5. ✅ README with setup instructions
6. ✅ CLAUDE.md with Claude Code instructions
7. ✅ Demo video (< 90 seconds)
8. ✅ Form submission with all URLs

### Nice to Have
- [ ] API documentation (Swagger UI)
- [ ] Loading states and animations
- [ ] Dark mode
- [ ] Keyboard shortcuts
- [ ] Task categories/tags

## Measuring Success

### Phase II Success = 150 Points When:
- All 5 basic features work in web UI
- Users can register and login
- Data persists in database
- Deployed and accessible online
- Spec-driven approach documented
- Demo video shows all features

### Bonus Points Available:
- Start planning Reusable Intelligence (+planning ahead)
- Clean, professional UI (+good impression)
- Excellent documentation (+helps others)
- Early submission (+shows confidence)

---

**This constitution guides all Phase II development. All specifications must align with these principles.**

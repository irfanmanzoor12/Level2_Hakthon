# Phase II - Architecture Overview

## System Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         CLIENT TIER                          │
│  ┌────────────────────────────────────────────────────────┐  │
│  │                Web Browser (Desktop/Mobile)            │  │
│  │  ┌──────────────────────────────────────────────────┐  │  │
│  │  │        Next.js Frontend Application              │  │  │
│  │  │  • React Components                              │  │  │
│  │  │  • Better Auth Client                            │  │  │
│  │  │  • API Client Layer                              │  │  │
│  │  │  • State Management                              │  │  │
│  │  └──────────────────────────────────────────────────┘  │  │
│  └────────────────────────────────────────────────────────┘  │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            │ HTTPS / REST API
                            │ JWT Authentication
                            │
┌───────────────────────────▼─────────────────────────────────┐
│                      APPLICATION TIER                        │
│  ┌────────────────────────────────────────────────────────┐  │
│  │             FastAPI Backend Application                │  │
│  │  ┌──────────────────────────────────────────────────┐  │  │
│  │  │  API Routes                                      │  │  │
│  │  │  • /api/tasks/*     - Task operations           │  │  │
│  │  │  • /api/auth/*      - Authentication            │  │  │
│  │  │  • /docs            - API documentation         │  │  │
│  │  └──────────────────────────────────────────────────┘  │  │
│  │  ┌──────────────────────────────────────────────────┐  │  │
│  │  │  Middleware                                      │  │  │
│  │  │  • JWT Validation                                │  │  │
│  │  │  • CORS                                          │  │  │
│  │  │  • Error Handling                                │  │  │
│  │  └──────────────────────────────────────────────────┘  │  │
│  │  ┌──────────────────────────────────────────────────┐  │  │
│  │  │  Business Logic                                  │  │  │
│  │  │  • Task Service                                  │  │  │
│  │  │  • User Service                                  │  │  │
│  │  │  • Validation                                    │  │  │
│  │  └──────────────────────────────────────────────────┘  │  │
│  │  ┌──────────────────────────────────────────────────┐  │  │
│  │  │  Data Access Layer                               │  │  │
│  │  │  • SQLModel ORM                                  │  │  │
│  │  │  • Database Models                               │  │  │
│  │  │  • Queries                                       │  │  │
│  │  └──────────────────────────────────────────────────┘  │  │
│  └────────────────────────────────────────────────────────┘  │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            │ PostgreSQL Protocol
                            │ SSL/TLS
                            │
┌───────────────────────────▼─────────────────────────────────┐
│                        DATA TIER                             │
│  ┌────────────────────────────────────────────────────────┐  │
│  │          Neon Serverless PostgreSQL Database           │  │
│  │                                                        │  │
│  │  Tables:                                               │  │
│  │  • users         - User accounts (Better Auth)        │  │
│  │  • sessions      - User sessions (Better Auth)        │  │
│  │  • tasks         - Todo tasks                         │  │
│  │                                                        │  │
│  └────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## Component Details

### Frontend (Next.js)

**Deployment**: Vercel
**URL**: https://your-app.vercel.app

**Key Components**:
- `/app` - Next.js App Router pages
- `/components` - Reusable UI components
- `/lib` - Utilities and API client
- `/styles` - Tailwind CSS

**Key Features**:
- Server-side rendering (SSR)
- Client-side routing
- Optimistic updates
- JWT token management
- Responsive design

### Backend (FastAPI)

**Deployment**: Railway / Render / DigitalOcean
**URL**: https://your-api.example.com

**Key Components**:
- `main.py` - FastAPI app entry point
- `routes/` - API endpoint handlers
- `models/` - SQLModel database models
- `services/` - Business logic
- `middleware/` - Auth, CORS, etc.

**Key Features**:
- RESTful API
- JWT authentication
- OpenAPI documentation
- Input validation
- Error handling

### Database (Neon PostgreSQL)

**Type**: Serverless PostgreSQL
**Provider**: Neon.tech
**Access**: SSL/TLS encrypted

**Key Tables**:
- `users` - User accounts
- `sessions` - Auth sessions
- `tasks` - Todo items

## Data Flow

### User Registration
```
1. User fills registration form (frontend)
   ↓
2. Frontend → POST /api/auth/register (backend)
   ↓
3. Backend validates input
   ↓
4. Backend creates user in database
   ↓
5. Backend returns success + JWT token
   ↓
6. Frontend stores JWT token
   ↓
7. Frontend redirects to tasks page
```

### User Login
```
1. User enters credentials (frontend)
   ↓
2. Frontend → POST /api/auth/login (backend)
   ↓
3. Backend validates credentials
   ↓
4. Backend generates JWT token
   ↓
5. Backend returns JWT token
   ↓
6. Frontend stores JWT token
   ↓
7. Frontend redirects to tasks page
```

### Create Task
```
1. User fills task form (frontend)
   ↓
2. Frontend → POST /api/{user_id}/tasks (with JWT)
   ↓
3. Backend validates JWT token
   ↓
4. Backend extracts user_id from token
   ↓
5. Backend validates input
   ↓
6. Backend creates task in database
   ↓
7. Backend returns created task
   ↓
8. Frontend updates UI (optimistic)
```

### View Tasks
```
1. User visits tasks page (frontend)
   ↓
2. Frontend → GET /api/{user_id}/tasks (with JWT)
   ↓
3. Backend validates JWT token
   ↓
4. Backend queries tasks WHERE user_id = token.user_id
   ↓
5. Backend returns filtered tasks
   ↓
6. Frontend renders task list
```

## Authentication Flow

### JWT Token Structure
```json
{
  "user_id": "uuid",
  "email": "user@example.com",
  "exp": 1234567890,
  "iat": 1234567890
}
```

### Token Storage
- **Frontend**: HTTP-only cookie (secure)
- **Transmission**: Authorization header
- **Validation**: Every API request

### Security Measures
- Passwords hashed with bcrypt
- JWT signed with secret key
- Token expiration (7 days)
- HTTPS only in production
- CORS configured properly

## API Design

### RESTful Principles
- **Resource-based URLs**: `/api/tasks`, not `/api/getTask`
- **HTTP methods**: GET (read), POST (create), PUT (update), DELETE (delete)
- **Status codes**: 200 (success), 201 (created), 400 (bad request), 401 (unauthorized), 404 (not found)
- **JSON format**: All requests and responses use JSON

### URL Structure
```
/api/auth/register          - User registration
/api/auth/login             - User login
/api/{user_id}/tasks        - List/create tasks
/api/{user_id}/tasks/{id}   - Get/update/delete specific task
```

### Authentication Header
```
Authorization: Bearer <jwt_token>
```

## Database Schema

### Users Table (Better Auth)
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255),
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
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
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_completed ON tasks(completed);
```

## Error Handling

### Frontend
- Display user-friendly error messages
- Validate input before submission
- Handle network errors gracefully
- Provide retry mechanisms

### Backend
- Validate all inputs
- Return appropriate HTTP status codes
- Include error messages in response
- Log errors for debugging

### Example Error Response
```json
{
  "error": "Task not found",
  "detail": "Task with ID 123 does not exist",
  "status_code": 404
}
```

## Performance Considerations

### Frontend
- Code splitting (Next.js automatic)
- Image optimization (Next.js Image component)
- Lazy loading components
- Caching API responses

### Backend
- Database connection pooling
- Efficient queries (indexes)
- Response pagination (if many tasks)
- Gzip compression

### Database
- Indexes on frequently queried columns
- Neon automatic connection pooling
- Query optimization

## Deployment Architecture

### Frontend (Vercel)
```
Git Push → Vercel Build → Deploy → CDN Edge Nodes
```

### Backend (Railway/Render)
```
Git Push → Container Build → Deploy → Public URL
```

### Database (Neon)
```
Always available (serverless)
Automatic backups
Connection pooling
```

## Environment Variables

### Frontend (.env.local)
```bash
NEXT_PUBLIC_API_URL=https://your-api.example.com
NEXT_PUBLIC_BETTER_AUTH_URL=https://your-app.vercel.app
BETTER_AUTH_SECRET=your-secret-key
```

### Backend (.env)
```bash
DATABASE_URL=postgresql://user:pass@host/db
BETTER_AUTH_SECRET=your-secret-key
CORS_ORIGINS=https://your-app.vercel.app
JWT_SECRET=your-jwt-secret
```

## Monitoring and Debugging

### Frontend
- Vercel deployment logs
- Browser console errors
- Network tab for API calls

### Backend
- Application logs
- API endpoint metrics
- Error tracking

### Database
- Neon dashboard
- Query performance
- Connection metrics

## Scalability Considerations

### Current (Phase II)
- Single backend server
- Serverless database (auto-scales)
- CDN for frontend (Vercel)

### Future (Phase IV-V)
- Multiple backend instances (Kubernetes)
- Load balancer
- Event-driven architecture (Kafka)
- Microservices (Dapr)

## Security Checklist

- [x] HTTPS everywhere
- [x] JWT authentication
- [x] Password hashing
- [x] Input validation
- [x] SQL injection prevention (ORM)
- [x] XSS prevention (React escaping)
- [x] CORS configuration
- [x] Rate limiting (future)
- [x] User data isolation

## Development Workflow

1. **Write Specs** - Define feature in specs/
2. **Backend First** - Implement API endpoint
3. **Test API** - Use Swagger UI or Postman
4. **Frontend** - Build UI component
5. **Integration** - Connect frontend to API
6. **Test E2E** - Test full user flow
7. **Deploy** - Push to Vercel + Railway
8. **Verify** - Test production deployment

---

**This architecture ensures a scalable, maintainable, and secure Phase II application.**

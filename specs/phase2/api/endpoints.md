# Phase II - API Endpoints Specification

## API Overview

**Base URL**: `https://your-api.example.com`
**Version**: v1
**Format**: JSON
**Authentication**: JWT Bearer Token
**Documentation**: `/docs` (FastAPI Swagger UI)

## API Structure

```
/api/
├── auth/
│   ├── POST   /register      - User registration
│   ├── POST   /login         - User login
│   └── POST   /logout        - User logout
│
├── {user_id}/tasks/
│   ├── GET    /              - List all tasks
│   ├── POST   /              - Create new task
│   ├── GET    /{id}          - Get specific task
│   ├── PUT    /{id}          - Update task
│   ├── DELETE /{id}          - Delete task
│   └── PATCH  /{id}/complete - Toggle completion
│
└── health/
    └── GET    /              - Health check
```

## Authentication Endpoints

### POST /api/auth/register

Register a new user account.

**Request:**
```http
POST /api/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePass123",
  "name": "John Doe"
}
```

**Response (201 Created):**
```json
{
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "name": "John Doe",
    "created_at": "2025-12-09T10:30:00Z"
  },
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Errors:**
- `400 Bad Request` - Invalid input
- `409 Conflict` - Email already exists

---

### POST /api/auth/login

Authenticate user and receive JWT token.

**Request:**
```http
POST /api/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePass123"
}
```

**Response (200 OK):**
```json
{
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "name": "John Doe"
  },
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Errors:**
- `400 Bad Request` - Invalid input
- `401 Unauthorized` - Invalid credentials

---

## Task Endpoints

All task endpoints require JWT authentication via `Authorization` header.

### GET /api/{user_id}/tasks

List all tasks for the authenticated user.

**Request:**
```http
GET /api/550e8400-e29b-41d4-a716-446655440000/tasks
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Query Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| status | string | No | Filter by status: `all`, `pending`, `completed` (default: `all`) |
| sort | string | No | Sort by: `created`, `updated`, `title` (default: `created`) |
| order | string | No | Order: `asc`, `desc` (default: `desc`) |
| limit | integer | No | Limit results (default: 100, max: 1000) |
| offset | integer | No | Skip results (default: 0) |

**Response (200 OK):**
```json
{
  "tasks": [
    {
      "id": 1,
      "user_id": "550e8400-e29b-41d4-a716-446655440000",
      "title": "Buy groceries",
      "description": "Milk, eggs, bread",
      "completed": false,
      "created_at": "2025-12-09T10:30:00Z",
      "updated_at": "2025-12-09T10:30:00Z"
    },
    {
      "id": 2,
      "user_id": "550e8400-e29b-41d4-a716-446655440000",
      "title": "Call mom",
      "description": "",
      "completed": true,
      "created_at": "2025-12-09T09:15:00Z",
      "updated_at": "2025-12-09T11:45:00Z"
    }
  ],
  "total": 2,
  "limit": 100,
  "offset": 0
}
```

**Errors:**
- `401 Unauthorized` - Missing/invalid token
- `403 Forbidden` - user_id doesn't match token

---

### POST /api/{user_id}/tasks

Create a new task.

**Request:**
```http
POST /api/550e8400-e29b-41d4-a716-446655440000/tasks
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json

{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread"
}
```

**Validation Rules:**
- `title`: Required, 1-200 characters
- `description`: Optional, max 1000 characters (auto-truncate)

**Response (201 Created):**
```json
{
  "id": 1,
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": false,
  "created_at": "2025-12-09T10:30:00Z",
  "updated_at": "2025-12-09T10:30:00Z"
}
```

**Errors:**
- `400 Bad Request` - Invalid input (empty title, too long, etc.)
- `401 Unauthorized` - Missing/invalid token
- `403 Forbidden` - user_id doesn't match token

---

### GET /api/{user_id}/tasks/{id}

Get a specific task by ID.

**Request:**
```http
GET /api/550e8400-e29b-41d4-a716-446655440000/tasks/1
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Response (200 OK):**
```json
{
  "id": 1,
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": false,
  "created_at": "2025-12-09T10:30:00Z",
  "updated_at": "2025-12-09T10:30:00Z"
}
```

**Errors:**
- `401 Unauthorized` - Missing/invalid token
- `403 Forbidden` - Task doesn't belong to user
- `404 Not Found` - Task not found

---

### PUT /api/{user_id}/tasks/{id}

Update an existing task (replace all fields).

**Request:**
```http
PUT /api/550e8400-e29b-41d4-a716-446655440000/tasks/1
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json

{
  "title": "Buy groceries and fruits",
  "description": "Milk, eggs, bread, apples",
  "completed": false
}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Buy groceries and fruits",
  "description": "Milk, eggs, bread, apples",
  "completed": false,
  "created_at": "2025-12-09T10:30:00Z",
  "updated_at": "2025-12-09T11:45:00Z"
}
```

**Errors:**
- `400 Bad Request` - Invalid input
- `401 Unauthorized` - Missing/invalid token
- `403 Forbidden` - Task doesn't belong to user
- `404 Not Found` - Task not found

---

### PATCH /api/{user_id}/tasks/{id}

Partially update a task (update only provided fields).

**Request:**
```http
PATCH /api/550e8400-e29b-41d4-a716-446655440000/tasks/1
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json

{
  "title": "Buy groceries and snacks"
}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Buy groceries and snacks",
  "description": "Milk, eggs, bread",
  "completed": false,
  "created_at": "2025-12-09T10:30:00Z",
  "updated_at": "2025-12-09T12:00:00Z"
}
```

---

### PATCH /api/{user_id}/tasks/{id}/complete

Toggle task completion status.

**Request:**
```http
PATCH /api/550e8400-e29b-41d4-a716-446655440000/tasks/1/complete
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Response (200 OK):**
```json
{
  "id": 1,
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": true,
  "created_at": "2025-12-09T10:30:00Z",
  "updated_at": "2025-12-09T13:15:00Z"
}
```

---

### DELETE /api/{user_id}/tasks/{id}

Delete a task.

**Request:**
```http
DELETE /api/550e8400-e29b-41d4-a716-446655440000/tasks/1
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Response (204 No Content):**
```
(empty body)
```

**Errors:**
- `401 Unauthorized` - Missing/invalid token
- `403 Forbidden` - Task doesn't belong to user
- `404 Not Found` - Task not found

---

## Health Check

### GET /api/health

Check API health status (no authentication required).

**Request:**
```http
GET /api/health
```

**Response (200 OK):**
```json
{
  "status": "healthy",
  "timestamp": "2025-12-09T10:30:00Z",
  "version": "1.0.0",
  "database": "connected"
}
```

---

## Authentication & Authorization

### JWT Token Format

```
Authorization: Bearer <token>
```

### Token Payload

```json
{
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "user@example.com",
  "exp": 1234567890,
  "iat": 1234567890
}
```

### Token Expiration

- Default: 7 days
- Refresh: Not implemented in Phase II (future)

### Security Rules

1. **User Isolation**: Backend must verify `user_id` in URL matches `user_id` in JWT token
2. **Token Validation**: Every protected endpoint validates JWT
3. **Task Ownership**: Users can only access their own tasks

---

## Error Response Format

All errors follow this structure:

```json
{
  "error": "Error type",
  "detail": "Detailed error message",
  "status_code": 400
}
```

### Common Status Codes

| Code | Meaning | When Used |
|------|---------|-----------|
| 200 | OK | Successful GET/PUT/PATCH |
| 201 | Created | Successful POST |
| 204 | No Content | Successful DELETE |
| 400 | Bad Request | Invalid input/validation error |
| 401 | Unauthorized | Missing/invalid JWT token |
| 403 | Forbidden | Valid token but unauthorized action |
| 404 | Not Found | Resource doesn't exist |
| 409 | Conflict | Resource already exists (email) |
| 500 | Server Error | Internal server error |

---

## Rate Limiting (Future)

Not implemented in Phase II, but plan for Phase IV:

```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1638360000
```

---

## CORS Configuration

### Allowed Origins

```python
CORS_ORIGINS = [
    "http://localhost:3000",  # Development
    "https://your-app.vercel.app",  # Production
]
```

### Allowed Methods

```
GET, POST, PUT, PATCH, DELETE, OPTIONS
```

### Allowed Headers

```
Authorization, Content-Type
```

---

## API Testing

### Using Swagger UI

Navigate to `http://localhost:8000/docs`

1. Click "Authorize" button
2. Enter JWT token
3. Try endpoints interactively

### Using cURL

**Register:**
```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Test123","name":"Test User"}'
```

**Create Task:**
```bash
curl -X POST http://localhost:8000/api/{user_id}/tasks \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"Test task","description":"Test description"}'
```

---

## Implementation Checklist

Backend implementation order:

- [ ] Setup FastAPI app
- [ ] Create database models (SQLModel)
- [ ] Implement auth endpoints
  - [ ] POST /register
  - [ ] POST /login
- [ ] Implement JWT middleware
- [ ] Implement task endpoints
  - [ ] GET /tasks
  - [ ] POST /tasks
  - [ ] GET /tasks/{id}
  - [ ] PUT /tasks/{id}
  - [ ] PATCH /tasks/{id}
  - [ ] PATCH /tasks/{id}/complete
  - [ ] DELETE /tasks/{id}
- [ ] Add error handling
- [ ] Add CORS middleware
- [ ] Test all endpoints
- [ ] Deploy backend

---

**This API specification defines the complete contract between frontend and backend for Phase II.**

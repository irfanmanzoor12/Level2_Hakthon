# Phase II - Database Schema

## Database Overview

**Provider**: Neon Serverless PostgreSQL
**Version**: PostgreSQL 15+
**ORM**: SQLModel (Python)
**Migrations**: Alembic (future)

## Schema Diagram

```
┌─────────────────────────────────┐
│           users                  │
├─────────────────────────────────┤
│ id (UUID) PK                    │
│ email (VARCHAR) UNIQUE          │
│ name (VARCHAR)                  │
│ password_hash (VARCHAR)         │
│ created_at (TIMESTAMP)          │
│ updated_at (TIMESTAMP)          │
└─────────────────────────────────┘
                │
                │ 1:N
                │
                ▼
┌─────────────────────────────────┐
│           tasks                  │
├─────────────────────────────────┤
│ id (SERIAL) PK                  │
│ user_id (UUID) FK               │───┐
│ title (VARCHAR)                 │   │
│ description (TEXT)              │   │ References
│ completed (BOOLEAN)             │   │ users(id)
│ created_at (TIMESTAMP)          │   │ ON DELETE CASCADE
│ updated_at (TIMESTAMP)          │◀──┘
└─────────────────────────────────┘

Indexes:
- idx_tasks_user_id ON tasks(user_id)
- idx_tasks_completed ON tasks(completed)
```

## Table Definitions

### Users Table

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255),
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes
CREATE UNIQUE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_created_at ON users(created_at DESC);
```

**Column Details:**

| Column | Type | Nullable | Default | Description |
|--------|------|----------|---------|-------------|
| id | UUID | NO | gen_random_uuid() | Primary key, auto-generated |
| email | VARCHAR(255) | NO | - | User's email (unique) |
| name | VARCHAR(255) | YES | NULL | User's display name |
| password_hash | VARCHAR(255) | NO | - | Bcrypt hashed password |
| created_at | TIMESTAMP | NO | NOW() | Account creation time |
| updated_at | TIMESTAMP | NO | NOW() | Last update time |

**Constraints:**
- PRIMARY KEY on `id`
- UNIQUE on `email`
- NOT NULL on `email`, `password_hash`

### Tasks Table

```sql
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_completed ON tasks(completed);
CREATE INDEX idx_tasks_user_completed ON tasks(user_id, completed);
CREATE INDEX idx_tasks_created_at ON tasks(created_at DESC);
```

**Column Details:**

| Column | Type | Nullable | Default | Description |
|--------|------|----------|---------|-------------|
| id | SERIAL | NO | AUTO | Primary key, auto-increment |
| user_id | UUID | NO | - | Foreign key to users.id |
| title | VARCHAR(200) | NO | - | Task title |
| description | TEXT | YES | NULL | Task description |
| completed | BOOLEAN | NO | FALSE | Completion status |
| created_at | TIMESTAMP | NO | NOW() | Task creation time |
| updated_at | TIMESTAMP | NO | NOW() |Last update time |

**Constraints:**
- PRIMARY KEY on `id`
- FOREIGN KEY `user_id` REFERENCES `users(id)` ON DELETE CASCADE
- NOT NULL on `user_id`, `title`, `completed`
- CHECK constraint: `title` length 1-200 characters

## SQLModel Definitions

### User Model

```python
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
import uuid

class User(SQLModel, table=True):
    """User model for authentication."""
    __tablename__ = "users"

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        nullable=False
    )
    email: str = Field(
        max_length=255,
        unique=True,
        nullable=False,
        index=True
    )
    name: Optional[str] = Field(
        max_length=255,
        default=None
    )
    password_hash: str = Field(
        max_length=255,
        nullable=False
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False
    )
```

### Task Model

```python
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
import uuid

class Task(SQLModel, table=True):
    """Task model for todo items."""
    __tablename__ = "tasks"

    id: Optional[int] = Field(
        default=None,
        primary_key=True
    )
    user_id: uuid.UUID = Field(
        foreign_key="users.id",
        nullable=False,
        index=True
    )
    title: str = Field(
        max_length=200,
        min_length=1,
        nullable=False
    )
    description: Optional[str] = Field(
        default=None
    )
    completed: bool = Field(
        default=False,
        nullable=False,
        index=True
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False
    )
```

## Relationships

### User → Tasks (One-to-Many)

A user can have many tasks:
```python
# In User model (if using relationships)
from sqlmodel import Relationship
from typing import List

class User(SQLModel, table=True):
    # ... other fields ...
    tasks: List["Task"] = Relationship(back_populates="user")

class Task(SQLModel, table=True):
    # ... other fields ...
    user: User = Relationship(back_populates="tasks")
```

**Cascade Behavior:**
- When a user is deleted, all their tasks are automatically deleted (CASCADE)

## Data Validation

### User Validation

```python
from pydantic import EmailStr, validator

class UserCreate(SQLModel):
    """Schema for user registration."""
    email: EmailStr  # Validates email format
    name: Optional[str] = None
    password: str  # Min 8 chars, will be validated

    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        return v

class UserResponse(SQLModel):
    """Schema for user response (no password)."""
    id: uuid.UUID
    email: str
    name: Optional[str]
    created_at: datetime
```

### Task Validation

```python
class TaskCreate(SQLModel):
    """Schema for creating a task."""
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = None

    @validator('description')
    def validate_description(cls, v):
        if v and len(v) > 1000:
            return v[:1000]  # Truncate
        return v

class TaskUpdate(SQLModel):
    """Schema for updating a task."""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    completed: Optional[bool] = None

class TaskResponse(SQLModel):
    """Schema for task response."""
    id: int
    user_id: uuid.UUID
    title: str
    description: Optional[str]
    completed: bool
    created_at: datetime
    updated_at: datetime
```

## Indexes Strategy

### Primary Indexes (Automatic)
- `users.id` (Primary key)
- `tasks.id` (Primary key)

### Unique Indexes
- `users.email` - Enforce unique emails

### Foreign Key Indexes
- `tasks.user_id` - Fast user task lookups

### Query Optimization Indexes
- `tasks.completed` - Filter by status
- `tasks(user_id, completed)` - Combined filter
- `users.created_at DESC` - Sort by registration
- `tasks.created_at DESC` - Sort by creation

## Sample Data

### Users
```sql
INSERT INTO users (email, name, password_hash) VALUES
('alice@example.com', 'Alice', '$2b$12$...'),
('bob@example.com', 'Bob', '$2b$12$...');
```

### Tasks
```sql
INSERT INTO tasks (user_id, title, description, completed) VALUES
((SELECT id FROM users WHERE email = 'alice@example.com'),
 'Buy groceries', 'Milk, eggs, bread', FALSE),
((SELECT id FROM users WHERE email = 'alice@example.com'),
 'Call mom', 'Wish happy birthday', TRUE),
((SELECT id FROM users WHERE email = 'bob@example.com'),
 'Review PR #123', 'Check code quality', FALSE);
```

## Database Connection

### Connection String Format
```
postgresql://user:password@host:port/database?sslmode=require
```

### Neon Connection Example
```python
from sqlmodel import create_engine, Session
import os

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(
    DATABASE_URL,
    echo=True,  # Log SQL queries (development)
    pool_pre_ping=True,  # Verify connections
)

def get_session():
    """Dependency for FastAPI."""
    with Session(engine) as session:
        yield session
```

## Migrations (Future)

### Using Alembic
```bash
# Initialize Alembic
alembic init alembic

# Create migration
alembic revision --autogenerate -m "Add tasks table"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

### Manual Migration Script (Phase II)
```python
from sqlmodel import SQLModel, create_engine

def create_tables():
    """Create all tables."""
    engine = create_engine(DATABASE_URL)
    SQLModel.metadata.create_all(engine)

if __name__ == "__main__":
    create_tables()
```

## Query Examples

### Get all tasks for a user
```python
from sqlmodel import select

def get_user_tasks(session: Session, user_id: uuid.UUID):
    statement = select(Task).where(Task.user_id == user_id)
    return session.exec(statement).all()
```

### Get completed tasks
```python
def get_completed_tasks(session: Session, user_id: uuid.UUID):
    statement = select(Task).where(
        Task.user_id == user_id,
        Task.completed == True
    )
    return session.exec(statement).all()
```

### Create task
```python
def create_task(session: Session, task_data: TaskCreate, user_id: uuid.UUID):
    task = Task(**task_data.dict(), user_id=user_id)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task
```

### Update task
```python
def update_task(session: Session, task_id: int, task_update: TaskUpdate):
    task = session.get(Task, task_id)
    if not task:
        return None

    update_data = task_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)

    task.updated_at = datetime.utcnow()
    session.add(task)
    session.commit()
    session.refresh(task)
    return task
```

### Delete task
```python
def delete_task(session: Session, task_id: int, user_id: uuid.UUID):
    task = session.get(Task, task_id)
    if not task or task.user_id != user_id:
        return False

    session.delete(task)
    session.commit()
    return True
```

## Security Considerations

### Password Hashing
```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
```

### User Isolation
```sql
-- Always filter by user_id in queries
SELECT * FROM tasks WHERE user_id = $1;

-- Never expose other users' data
-- Backend must verify user_id matches JWT token
```

## Performance Tips

### Query Optimization
- Use indexes for frequently queried columns
- Add `LIMIT` for large result sets
- Use `COUNT(*)` carefully (can be slow)
- Batch operations when possible

### Connection Pooling
- Neon provides automatic pooling
- Configure pool size based on traffic
- Use `pool_pre_ping` to handle stale connections

### Caching (Future)
- Cache user data (Redis)
- Cache task counts
- Invalidate on updates

---

**This schema provides a solid foundation for Phase II with room to grow in Phase III-V.**

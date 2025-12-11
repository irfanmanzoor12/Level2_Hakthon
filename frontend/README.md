# Hackathon Todo - Frontend

Phase II - Next.js Frontend Application

## Tech Stack

- **Framework**: Next.js 15+ (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Authentication**: JWT (stored in localStorage)
- **API Client**: Custom fetch wrapper

## Setup

### 1. Install Dependencies

```bash
cd frontend
npm install
# or
pnpm install
```

### 2. Configure Environment

Create `.env.local` file:

```bash
cp .env.local.example .env.local
```

Update `.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

### 3. Run Development Server

```bash
npm run dev
# or
pnpm dev
```

Open http://localhost:3000

## Features

### Authentication
- User registration
- User login
- JWT token management
- Automatic redirect based on auth state

### Task Management
- Create tasks
- View all tasks
- Update tasks (title, description)
- Toggle task completion
- Delete tasks
- Real-time UI updates

## Project Structure

```
frontend/
├── app/
│   ├── layout.tsx           # Root layout
│   ├── page.tsx             # Home (redirect)
│   ├── globals.css          # Global styles
│   ├── auth/                # Auth pages
│   │   ├── login/page.tsx
│   │   └── register/page.tsx
│   └── dashboard/           # Protected pages
│       ├── layout.tsx       # Dashboard layout
│       └── tasks/page.tsx   # Tasks page
├── components/              # React components
├── lib/
│   └── api.ts              # API client
├── types/                  # TypeScript types
│   ├── user.ts
│   └── task.ts
└── public/                 # Static files
```

## API Integration

The frontend communicates with the FastAPI backend through the API client (`lib/api.ts`):

```typescript
import { api } from '@/lib/api'

// Login
await api.login({ email, password })

// Get tasks
const response = await api.getTasks(userId)

// Create task
await api.createTask(userId, { title, description })
```

## Pages

### `/` - Home
Redirects to `/dashboard/tasks` if authenticated, otherwise `/auth/login`

### `/auth/login` - Login
Email and password login form

### `/auth/register` - Register
User registration form

### `/dashboard/tasks` - Tasks (Protected)
Main task management interface with:
- Task list
- Create task form
- Edit/Delete/Complete actions

## Deployment

See main README for deployment instructions to Vercel.

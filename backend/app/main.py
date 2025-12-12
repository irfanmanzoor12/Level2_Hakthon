from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .database import create_tables
from .routes import auth_router, tasks_router

# Create FastAPI app
app = FastAPI(
    title="Hackathon Todo API",
    description="Phase II - Full-Stack Web Application Backend",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)
app.include_router(tasks_router)


@app.on_event("startup")
def on_startup():
    """Create database tables on startup."""
    try:
        create_tables()
        print("✅ Database tables created successfully")
    except Exception as e:
        print(f"⚠️  Warning: Could not create database tables: {e}")
        print("The app will still start, but database operations may fail")


@app.get("/api/health")
def health_check():
    """Health check endpoint."""
    from datetime import datetime

    # Test database connection
    db_status = "disconnected"
    try:
        from .database import engine
        with engine.connect() as conn:
            conn.execute("SELECT 1")
        db_status = "connected"
    except Exception as e:
        print(f"Database health check failed: {e}")
        db_status = f"error: {str(e)[:50]}"

    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "version": "1.0.0",
        "database": db_status
    }


@app.get("/")
def root():
    """Root endpoint."""
    return {
        "message": "Hackathon Todo API - Phase II",
        "docs": "/docs",
        "health": "/api/health"
    }

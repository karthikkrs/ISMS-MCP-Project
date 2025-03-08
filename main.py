"""
Main entry point for the ISMS (Information Security Management System) application.

This module initializes the FastAPI application, sets up database connections,
includes routers, and configures middleware for authentication and CORS.
"""

import os
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import routers
from routers import user, asset, risk, policy, incident

# Create FastAPI app
app = FastAPI(
    title="ISMS API",
    description="Information Security Management System API",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost/isms")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency to get DB session
def get_db():
    """
    Dependency function to get a database session.
    
    Yields:
        SQLAlchemy session: A database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Include routers
app.include_router(user.router, prefix="/api/users", tags=["users"])
app.include_router(asset.router, prefix="/api/assets", tags=["assets"])
app.include_router(risk.router, prefix="/api/risks", tags=["risks"])
app.include_router(policy.router, prefix="/api/policies", tags=["policies"])
app.include_router(incident.router, prefix="/api/incidents", tags=["incidents"])

@app.get("/")
async def root():
    """
    Root endpoint to verify API is running.
    
    Returns:
        dict: A simple message indicating the API is running
    """
    return {"message": "ISMS API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
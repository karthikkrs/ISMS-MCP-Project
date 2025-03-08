"""
Main application entry point for the ISMS API.

This module initializes the FastAPI application, includes routers,
and configures middleware, authentication, and documentation.
"""

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List, Optional
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="Information Security Management System API",
    description="API for managing information security assets, risks, policies, and incidents",
    version="1.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint returning API information."""
    return {
        "message": "ISMS API is running",
        "documentation": "/docs",
        "version": "1.0.0"
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }

# Import and include routers
# Note: These will be implemented in separate files
# from routers import users, assets, risks, policies, incidents
# 
# app.include_router(users.router, prefix="/api/users", tags=["Users"])
# app.include_router(assets.router, prefix="/api/assets", tags=["Assets"])
# app.include_router(risks.router, prefix="/api/risks", tags=["Risks"])
# app.include_router(policies.router, prefix="/api/policies", tags=["Policies"])
# app.include_router(incidents.router, prefix="/api/incidents", tags=["Incidents"])

# Run the application
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    uvicorn.run("main:app", host=host, port=port, reload=True)
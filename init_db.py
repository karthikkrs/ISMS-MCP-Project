"""
Database initialization script.

This script initializes the database with tables and mock data for testing.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Role, RoleEnum, User, Asset, Risk, Policy, Incident
from models import AssetTypeEnum, RiskStatusEnum, PolicyStatusEnum, IncidentSeverityEnum, IncidentStatusEnum
from passlib.context import CryptContext
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

# Load environment variables
load_dotenv()

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_tables():
    """Create all tables in the database."""
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully")

def create_roles(db):
    """Create roles if they don't exist."""
    # Check if roles already exist
    existing_roles = db.query(Role).all()
    if existing_roles:
        print("Roles already exist")
        return

    # Add roles
    admin_role = Role(role_id=1, role_name=RoleEnum.ADMIN.value)
    analyst_role = Role(role_id=2, role_name=RoleEnum.ANALYST.value)
    auditor_role = Role(role_id=3, role_name=RoleEnum.AUDITOR.value)
    user_role = Role(role_id=4, role_name=RoleEnum.USER.value)
    
    db.add_all([admin_role, analyst_role, auditor_role, user_role])
    db.commit()
    print("Roles created successfully")

def create_users(db):
    """Create users if they don't exist."""
    # Check if admin user exists
    admin_user = db.query(User).filter(User.username == "admin").first()
    if admin_user:
        print("Admin user already exists")
    else:
        # Create admin user
        hashed_password = pwd_context.hash("admin123")
        admin_user = User(
            username="admin",
            email="admin@example.com",
            password_hash=hashed_password,
            role_id=1  # Admin role
        )
        db.add(admin_user)
        db.commit()
        print("Admin user created successfully")
    
    # Create other users with different roles
    analyst_user = db.query(User).filter(User.username == "analyst").first()
    if not analyst_user:
        hashed_password = pwd_context.hash("analyst123")
        analyst_user = User(
            username="analyst",
            email="analyst@example.com",
            password_hash=hashed_password,
            role_id=2  # Analyst role
        )
        db.add(analyst_user)
        db.commit()
        print("Analyst user created successfully")
    
    auditor_user = db.query(User).filter(User.username == "auditor").first()
    if not auditor_user:
        hashed_password = pwd_context.hash("auditor123")
        auditor_user = User(
            username="auditor",
            email="auditor@example.com",
            password_hash=hashed_password,
            role_id=3  # Auditor role
        )
        db.add(auditor_user)
        db.commit()
        print("Auditor user created successfully")

def main():
    """Initialize the database."""
    try:
        # Create session
        db = SessionLocal()
        
        # Create tables
        create_tables()
        
        # Create roles
        create_roles(db)
        
        # Create users
        create_users(db)
        
        print("Database initialization completed successfully")
    except Exception as e:
        print(f"Error initializing database: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    main()
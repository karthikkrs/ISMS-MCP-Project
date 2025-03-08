"""
Database models for the ISMS application.

This module defines SQLAlchemy ORM models for all entities in the database schema,
including Users, Roles, Assets, Risks, Policies, Incidents, and their relationships.
"""

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, Enum, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
import enum

Base = declarative_base()

# Association table for many-to-many relationship between Risks and Policies
risk_policy_link = Table(
    'risk_policy_links',
    Base.metadata,
    Column('risk_id', Integer, ForeignKey('risks.risk_id'), primary_key=True),
    Column('policy_id', Integer, ForeignKey('policies.policy_id'), primary_key=True)
)

class RoleEnum(str, enum.Enum):
    """
    Enumeration of possible user roles in the system.
    """
    ADMIN = "Administrator"
    ANALYST = "Analyst"
    AUDITOR = "Auditor"
    USER = "User"

class Role(Base):
    """
    Role model for role-based access control.
    
    Attributes:
        role_id: Primary key
        role_name: Name of the role
        users: Relationship to User model
    """
    __tablename__ = 'roles'
    
    role_id = Column(Integer, primary_key=True, index=True)
    role_name = Column(String(50), unique=True, nullable=False)
    
    # Relationships
    users = relationship("User", back_populates="role")

class User(Base):
    """
    User model for authentication and authorization.
    
    Attributes:
        user_id: Primary key
        username: Unique username
        password_hash: Hashed password
        email: User's email address
        role_id: Foreign key to Role
        role: Relationship to Role model
        owned_assets: Relationship to Asset model
        audit_logs: Relationship to AuditLog model
    """
    __tablename__ = 'users'
    
    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    role_id = Column(Integer, ForeignKey('roles.role_id'), nullable=False)
    
    # Relationships
    role = relationship("Role", back_populates="users")
    owned_assets = relationship("Asset", back_populates="owner")
    audit_logs = relationship("AuditLog", back_populates="user")

class AssetTypeEnum(str, enum.Enum):
    """
    Enumeration of possible asset types.
    """
    HARDWARE = "Hardware"
    SOFTWARE = "Software"
    DATA = "Data"
    NETWORK = "Network"
    PERSONNEL = "Personnel"

class Asset(Base):
    """
    Asset model representing organizational assets.
    
    Attributes:
        asset_id: Primary key
        asset_name: Name of the asset
        asset_type: Type of asset (from AssetTypeEnum)
        description: Detailed description of the asset
        owner_id: Foreign key to User (owner)
        owner: Relationship to User model
        risks: Relationship to Risk model
        incidents: Relationship to Incident model
    """
    __tablename__ = 'assets'
    
    asset_id = Column(Integer, primary_key=True, index=True)
    asset_name = Column(String(100), nullable=False)
    asset_type = Column(Enum(AssetTypeEnum), nullable=False)
    description = Column(Text)
    owner_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    
    # Relationships
    owner = relationship("User", back_populates="owned_assets")
    risks = relationship("Risk", back_populates="asset")
    incidents = relationship("Incident", back_populates="asset")

class RiskStatusEnum(str, enum.Enum):
    """
    Enumeration of possible risk statuses.
    """
    IDENTIFIED = "Identified"
    ASSESSED = "Assessed"
    MITIGATED = "Mitigated"
    ACCEPTED = "Accepted"
    TRANSFERRED = "Transferred"

class Risk(Base):
    """
    Risk model representing potential security risks.
    
    Attributes:
        risk_id: Primary key
        risk_description: Description of the risk
        severity: Risk severity (1-5)
        likelihood: Risk likelihood (1-5)
        asset_id: Foreign key to Asset
        status: Current status of the risk
        asset: Relationship to Asset model
        policies: Relationship to Policy model (many-to-many)
    """
    __tablename__ = 'risks'
    
    risk_id = Column(Integer, primary_key=True, index=True)
    risk_description = Column(Text, nullable=False)
    severity = Column(Integer, nullable=False)  # 1-5 scale
    likelihood = Column(Integer, nullable=False)  # 1-5 scale
    asset_id = Column(Integer, ForeignKey('assets.asset_id'), nullable=False)
    status = Column(Enum(RiskStatusEnum), nullable=False, default=RiskStatusEnum.IDENTIFIED)
    
    # Relationships
    asset = relationship("Asset", back_populates="risks")
    policies = relationship("Policy", secondary=risk_policy_link, back_populates="risks")

class PolicyStatusEnum(str, enum.Enum):
    """
    Enumeration of possible policy statuses.
    """
    DRAFT = "Draft"
    REVIEW = "Review"
    APPROVED = "Approved"
    DEPRECATED = "Deprecated"

class Policy(Base):
    """
    Policy model representing security policies.
    
    Attributes:
        policy_id: Primary key
        policy_title: Title of the policy
        policy_content: Full content of the policy
        version: Version number of the policy
        status: Current status of the policy
        risks: Relationship to Risk model (many-to-many)
    """
    __tablename__ = 'policies'
    
    policy_id = Column(Integer, primary_key=True, index=True)
    policy_title = Column(String(200), nullable=False)
    policy_content = Column(Text, nullable=False)
    version = Column(String(20), nullable=False)
    status = Column(Enum(PolicyStatusEnum), nullable=False, default=PolicyStatusEnum.DRAFT)
    
    # Relationships
    risks = relationship("Risk", secondary=risk_policy_link, back_populates="policies")

class IncidentSeverityEnum(str, enum.Enum):
    """
    Enumeration of possible incident severity levels.
    """
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"

class IncidentStatusEnum(str, enum.Enum):
    """
    Enumeration of possible incident statuses.
    """
    OPEN = "Open"
    INVESTIGATING = "Investigating"
    RESOLVED = "Resolved"
    CLOSED = "Closed"

class Incident(Base):
    """
    Incident model representing security incidents.
    
    Attributes:
        incident_id: Primary key
        incident_description: Description of the incident
        date_reported: Date and time the incident was reported
        severity: Severity level of the incident
        asset_id: Foreign key to Asset
        status: Current status of the incident
        asset: Relationship to Asset model
    """
    __tablename__ = 'incidents'
    
    incident_id = Column(Integer, primary_key=True, index=True)
    incident_description = Column(Text, nullable=False)
    date_reported = Column(DateTime, nullable=False, default=func.now())
    severity = Column(Enum(IncidentSeverityEnum), nullable=False)
    asset_id = Column(Integer, ForeignKey('assets.asset_id'), nullable=False)
    status = Column(Enum(IncidentStatusEnum), nullable=False, default=IncidentStatusEnum.OPEN)
    
    # Relationships
    asset = relationship("Asset", back_populates="incidents")

class AuditLog(Base):
    """
    AuditLog model for tracking user actions.
    
    Attributes:
        log_id: Primary key
        user_id: Foreign key to User
        action: Description of the action performed
        timestamp: Date and time of the action
        user: Relationship to User model
    """
    __tablename__ = 'audit_logs'
    
    log_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    action = Column(Text, nullable=False)
    timestamp = Column(DateTime, nullable=False, default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="audit_logs")
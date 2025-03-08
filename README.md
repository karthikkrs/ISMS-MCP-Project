# Information Security Management System (ISMS)

A comprehensive security management platform with AI integration using Model Context Protocol (MCP).

## Features

- **User Management**: Role-based access control with multiple user types (Admin, Analyst, Auditor, User)
- **Asset Management**: Track and manage IT assets with risk assessment
- **Policy Management**: Create, update, and track security policies
- **Risk Management**: Identify, assess, and mitigate security risks
- **Incident Management**: Track and respond to security incidents
- **AI Integration**: Leveraging MCP for intelligent security analysis
- **Audit Logging**: Comprehensive audit trail of system activities

## Tech Stack

- **Backend**: FastAPI
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Vector Store**: Qdrant
- **AI Integration**: Model Context Protocol (MCP)
- **Authentication**: JWT with role-based access control
- **Testing**: pytest

## Getting Started

### Prerequisites

- Python 3.8+
- PostgreSQL
- Qdrant

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/karthikkrs/ISMS-MCP-Project.git
   cd ISMS-MCP-Project
   ```

2. Create and activate virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. Initialize the database:
   ```bash
   python init_db.py
   ```

6. Run the application:
   ```bash
   uvicorn main:app --reload
   ```

## Project Structure

```
ISMS-MCP-Project/
├── main.py           # FastAPI application entry point
├── models.py         # SQLAlchemy models
├── init_db.py        # Database initialization script
├── requirements.txt  # Project dependencies
├── routers/         # API route handlers
├── services/        # Business logic
└── tests/           # Test suite
```

## API Documentation

Once the application is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Testing

Run the test suite:
```bash
pytest
```

## License

MIT License
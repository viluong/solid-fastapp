# SOLID FastAPI application
- Apply SOLID princible to application for readability, flexibility, reusability and scalability.
- Some basic features: Register, Authentication with JWT, ...
- Status: To be continue...
## Install
1. Clone repository
2. Run ```docker-compose up -d --build```
## Structure:
```
alembic/                   # alemic migration
app/
├── entities/              #### For Data Transfer Object
    ├── user.py            # User entity
├── core/                  #### For configurations, security, logging
│   ├── config.py          # Configuration settings
│   ├── security.py        # JWT and password utilities
│   ├── logger.py          # Logging configuration
│   └── exceptions.py      # Custom exception handlers
├── models/                #### For SQLAlchemy models
│   ├── base.py            # Base database model
│   └── user.py            # User model
├── schemas/               #### For Pydantic models
│   ├── token.py           # Token schemas
│   └── user.py            # User schemas
├── repositories/          #### For database operations, interfaces
│   ├── base.py            # Base repository interface
│   └── user.py            # User repository implementation
├── services/              #### For business logic, depends on repositories
│   ├── auth.py            # Authentication service
│   └── user.py            # User service
├── api/                   #### For FastAPI routes, depends on services
│   ├── v1/
│   │   ├── endpoints/
│   │   │   ├── auth.py    # Auth endpoints
│   │   │   └── users.py   # User endpoints
│   │   └── router.py      # API router configuration
├── dependencies.py        # Dependency injection setup
├── database.py            # Config database connection
└── main.py                # FastAPI app initialization
```
## Explain how to apply SOLID princibles to this app
- Single Responsibility Principle suggests each class/module should have one responsibility. So, separating routes, models, services, dependencies, and schemas makes sense. For example, register logic should be in its own module, not mixed with database setup.
- Open/Closed Principle: classes should be open for extension but closed for modification. Using abstract base classes or interfaces for dependencies like databases or caches could help.
- Liskov Substitution: Subclasses should be substitutable for their base classes. Maybe not directly applicable here unless we have inheritance hierarchies. Let me see. For services, perhaps creating a base service class that others can extend without changing behavior.

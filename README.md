# SOLID FastAPI application

- Apply SOLID principles to application for readability, flexibility, reusability and scalability.
- Some basic features: User Registration, Authentication with JWT, ...
- Status: **To be continue...**

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

- **Single Responsibility Principle** suggests each class/module should have one responsibility. So, separating routes,
  models, services, dependencies, and schemas makes sense. For example, User Registration logic should be in its own
  module, not mixed with database setup.
    ```
    # app/services/user.py
    
    class IUserService(ABC):
    
        @abstractmethod
        async def create_user(self, user_create: UserCreate) -> UserEntity:
            pass
    
    
    class UserService(IUserService):
        def __init__(self, repository: IUserRepository):
            self.repository = repository
    
        async def create_user(self, user_create: UserCreate) -> UserEntity:
            user: UserEntity = await self.repository.get_by_email(user_create.email)
            if user:
                raise DuplicateEmailException
    
            new_user: UserEntity = UserEntity(
                email=user_create.email,
                name=user_create.name,
                birth_date=user_create.birth_date,
                hashed_password=get_password_hash(user_create.password),
            )
    
            new_user: UserEntity = await self.repository.create(new_user)
            return new_user
    ```
  The logic for calculating a user's age will be handled in the ```UserEntity``` class instead of the ```User``` model:
    ```
    # app/models/user.py
    class User(Base):
        __tablename__ = "users"
    
        id: int = Column(Integer, primary_key=True, index=True)
        email: str = Column(String, unique=True, index=True)
        name: str = Column(String(100), nullable=False)
        birth_date: date = Column(Date, nullable=True)
        hashed_password: str = Column(String)
        is_active: bool = Column(Boolean, default=True)
    
        created_at: datetime = Column(
            TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
        )
    
        updated_at: datetime = Column(
            TIMESTAMP(timezone=True),
            nullable=False,
            server_default=func.now(),
            onupdate=func.now(),
        )
    
        def to_entity(self) -> UserEntity:
            return UserEntity(
                id=self.id,
                email=self.email,
                name=self.name,
                hashed_password=self.hashed_password,
                is_active=self.is_active,
                birth_date=self.birth_date,
                created_at=self.created_at,
                updated_at=self.updated_at,
            )
    
        @staticmethod
        def from_entity(user: UserEntity) -> "User":
            return User(
                id=user.id,
                email=user.email,
                name=user.name,
                hashed_password=user.hashed_password,
                is_active=user.is_active,
                birth_date=user.birth_date,
                created_at=user.created_at,
                updated_at=user.updated_at,
            )
    ```

    ```
    # app/entities/user.py
    
    @dataclass
    class UserEntity:
        id: Optional[int] = None
        email: Optional[str] = None
        name: Optional[str] = None
        hashed_password: Optional[str] = None
        is_active: Optional[bool] = None
        birth_date: Optional[date] = None
        created_at: Optional[datetime] = None
        updated_at: Optional[datetime] = None
    
        @property
        def age(self) -> int:
            today = date.today()
            return (
                today.year
                - self.birth_date.year
                - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
            )
    ```
- **Open/Closed Principle**: classes should be open for extension but closed for modification. Using abstract base
  classes or interfaces for dependencies.<br>
  "Closed for modification" means that a class/module is complete and tested, and its internal code does not need to be
  changed when adding new features. Instead of modifying the code directly, you extend function throught inheritance,
  using interfaces, or dependency injection.<br>
  For example: Create a ```BaseRepository``` class. When I need to get or create other data such as User or Product, I
  will create ```UserRepository``` class or ```ProductRepository``` class that inherits from ```BaseRepository``` and
  implements the get and create functions.
  ```
      # app/repositories/base.py
      class BaseRepository(ABC):
        @abstractmethod
        async def get(self, id: int):
            pass
    
        @abstractmethod
        async def create(self, entity):
            pass
  ```
  ```
  # app/repositories/user.py
  class IUserRepository(BaseRepository):
    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[UserEntity]:
        pass


  class UserRepository(IUserRepository, ABC):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user_entity: UserEntity) -> UserEntity:
        user = User.from_entity(user_entity)

        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user.to_entity()

    async def get(self, id: int) -> Optional[UserEntity]:
        result = await self.session.execute(select(User).where(User.id == id))
        user: User = result.scalars().first()
        return user.to_entity() if user else None

    async def get_by_email(self, email: str) -> Optional[UserEntity]:
        result = await self.session.execute(select(User).where(User.email == email))
        user: User = result.scalars().first()
        return user.to_entity() if user else None
  ```

- **Liskov Substitution:** Subclasses should be substitutable for their base classes. Maybe not directly applicable here
  unless we have inheritance hierarchies. For services, perhaps creating a base service class (```IUserService```) that
  other services (```UserService```) can extend without changing behavior.
  ```
    # app/services/user.py
    class IUserService(ABC):
    
        async def create_user(self, user_create: UserCreate) -> UserEntity:
            pass
    
    
    class UserService(IUserService):
        def __init__(self, repository: IUserRepository):
            self.repository = repository
    
        async def create_user(self, user_create: UserCreate) -> UserEntity:
            user: UserEntity = await self.repository.get_by_email(user_create.email)
            if user:
                raise DuplicateEmailException
    
            new_user: UserEntity = UserEntity(
                email=user_create.email,
                name=user_create.name,
                birth_date=user_create.birth_date,
                hashed_password=get_password_hash(user_create.password),
            )
    
            new_user: UserEntity = await self.repository.create(new_user)
            return new_user
  ```
- **Interface Segregation:** Clients shouldn't depend on interfaces they don't use. So, creating smaller interfaces for
  different operations. For example, a UserRepository interface that has methods for user operations, separate from
  other entities. The number of separations from other entities depends on scope of the project, which is large or
  small.
- **Dependency Inversion:** Depend on abstractions, not concretions. Using dependency injection in FastAPI with
  Depends() is good here. The routes depend on abstract services, which are implemented by concrete classes that depend
  on abstract repositories.
    ```
    # app/api/v1/endpoints/users.py

    @router.post("/register", response_model=UserResponse)
    async def register_user(
        user_create: UserCreate, service: UserService = Depends(get_user_service)
    ):
        return await service.create_user(user_create)
    ```
    ```
    # app/dependencies.py
    def get_user_repository(db: AsyncSession = Depends(get_db)) -> IUserRepository:
        return UserRepository(db)
    
    
    def get_user_service(
        user_repo: IUserRepository = Depends(get_user_repository),
    ) -> IUserService:
        return UserService(user_repo)
    ```

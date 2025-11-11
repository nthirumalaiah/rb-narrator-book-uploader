# RB Narrator Book Uploader API

A well-architected FastAPI application following SOLID principles and clean architecture patterns.

## 🏗️ Architecture Overview

This application follows **Clean Architecture** and **SOLID principles** to ensure maintainability, testability, and scalability.

### 📁 Project Structure

```
├── api/                          # API Layer (Controllers)
│   └── routes/
│       ├── chapter_routes.py     # Chapter endpoints
│       └── health_routes.py      # Health check endpoints
├── core/                         # Core Infrastructure
│   ├── config.py                 # Configuration management
│   ├── db.py                     # Database configuration
│   ├── dependencies.py           # Original dependencies (legacy)
│   ├── dependencies_container.py # Dependency injection container
│   └── exception_handlers.py     # Global exception handling
├── exceptions/                   # Custom Exceptions
│   ├── base_exceptions.py        # Base exception classes
│   └── chapter_exceptions.py     # Chapter-specific exceptions
├── models/                       # Database Models (Entities)
│   └── chapter.py               # Chapter SQLAlchemy model
├── repositories/                 # Data Access Layer
│   ├── interfaces/
│   │   └── chapter_repository.py # Repository interface
│   └── chapter_repository.py     # Repository implementation
├── schemas/                      # API Schemas (DTOs)
│   └── chapter.py               # Pydantic models
├── services/                     # Business Logic Layer
│   ├── interfaces/
│   │   └── chapter_service.py    # Service interface
│   └── chapter_service.py        # Service implementation
├── main.py                      # Application entry point
└── requirements.txt             # Python dependencies
```
### Repository Pattern
```python
# Abstract interface
class ChapterRepositoryInterface(ABC):
    @abstractmethod
    def create(self, chapter: Chapter) -> Chapter: ...

# Concrete implementation
class SQLAlchemyChapterRepository(ChapterRepositoryInterface):
    def create(self, chapter: Chapter) -> Chapter:
        # Implementation details...
```

### Service Layer Pattern
```python
# Business logic isolated from HTTP concerns
class ChapterService:
    def __init__(self, repository: ChapterRepositoryInterface):
        self._repository = repository
    
    async def create_chapter(self, data: ChapterCreate) -> ChapterResponse:
        # Business validation and logic...
        return self._repository.create(chapter)
```

### Dependency Injection
```python
# Dependencies injected via constructor
def get_chapter_service(db: Session = Depends(get_db)) -> ChapterServiceInterface:
    container = get_container()
    return container.get_chapter_service(db)
```

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- MySQL 8.0+
- Virtual Environment

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd rb-narrator-book-uploader
```

2. **Create virtual environment**
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
# or
source .venv/bin/activate  # Linux/Mac
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your settings
```

5. **Run the application**
```bash
python main.py
# or
uvicorn main:app --reload
```

## 📝 Environment Configuration

Create a `.env` file with the following settings:

```env
# Database
DB_HOST=localhost
DB_PORT=3306
DB_USERNAME=root
DB_PASSWORD=your_password
DB_NAME=narrator_portal

# Application
APP_TITLE="RB Narrator Book Uploader API"
APP_VERSION=1.0.0
APP_DEBUG=true
APP_HOST=0.0.0.0
APP_PORT=8000

# AWS (Optional)
AWS_REGION=us-west-2
AWS_ACCESS_KEY_ID=your_key_id
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_S3_BUCKET=your_bucket_name

# Logging
LOG_LEVEL=INFO
LOG_FORMAT="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
```

## 📚 API Documentation

Once running, access the interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## 🧪 Testing

The architecture supports easy testing through dependency injection:

```python
# Example unit test
def test_create_chapter():
    # Mock repository
    mock_repo = Mock(spec=ChapterRepositoryInterface)
    
    # Inject mock into service
    service = ChapterService(mock_repo)
    
    # Test business logic in isolation
    result = await service.create_chapter(test_data)
    
    assert result is not None
    mock_repo.create.assert_called_once()
```

## 🔒 Error Handling

The application uses a comprehensive error handling system:

- **Custom Exceptions**: Domain-specific error types
- **Global Handlers**: Consistent error responses
- **Logging**: Detailed error tracking
- **HTTP Status Codes**: Proper REST API responses

## 📈 Benefits of This Architecture

1. **Maintainability**: Clear separation of concerns
2. **Testability**: Easy to mock and unit test
3. **Scalability**: Easy to add new features
4. **Flexibility**: Easy to change implementations
5. **Robustness**: Comprehensive error handling
6. **Documentation**: Self-documenting code structure

## 🔄 Adding New Features

To add a new entity (e.g., "Book"):

1. Create model in `models/book.py`
2. Create schemas in `schemas/book.py`
3. Create repository interface in `repositories/interfaces/book_repository.py`
4. Create repository implementation in `repositories/book_repository.py`
5. Create service interface in `services/interfaces/book_service.py`
6. Create service implementation in `services/book_service.py`
7. Create routes in `api/routes/book_routes.py`
8. Register routes in `main.py`

## 🤝 Contributing

1. Follow the existing architecture patterns
2. Write tests for new features
3. Update documentation
4. Follow SOLID principles
5. Use type hints
6. Add proper error handling

## 📄 License

This project is licensed under the RB Media License.
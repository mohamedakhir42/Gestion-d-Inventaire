# Installation Guide

## Prerequisites

- Python 3.12+
- Docker and Docker Compose
- Git
- PostgreSQL client (optional)

## Local Development Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd Syst-me-de-Gestion-d-Inventaire
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Configuration

Copy the example environment file:

```bash
cp .env.example .env
```

Edit `.env` with your configuration:

```bash
SECRET_KEY=your-secret-key-here
DEBUG=True
DATABASE_URL=postgres://postgres:postgres@localhost:5432/inventory_db
REDIS_URL=redis://localhost:6379/0
# ... other variables
```

### 5. Database Setup with Docker

```bash
docker-compose up -d db redis
```

### 6. Run Migrations

```bash
python manage.py migrate
```

### 7. Create Superuser

```bash
python manage.py createsuperuser
```

### 8. Run Development Server

```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000`

### 9. Access API Documentation

- Swagger UI: `http://localhost:8000/api/docs/`
- ReDoc: `http://localhost:8000/api/redoc/`
- Schema: `http://localhost:8000/api/schema/`

## Docker Setup

### Using Docker Compose (Full Stack)

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f web

# Stop all services
docker-compose down
```

### Production Docker Compose

```bash
# Start production services
docker-compose -f docker-compose.prod.yml up -d
```

## Code Quality Tools

### Install Pre-commit Hooks

```bash
pip install pre-commit
pre-commit install
```

### Run Code Quality Checks

```bash
# Format code
black .

# Lint code
ruff check .

# Sort imports
isort .

# Type check
mypy config/ apps/ --ignore-missing-imports
```

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest apps/accounts/tests.py

# Run specific test
pytest apps/accounts/tests.py::TestUserModel::test_create_user
```

## Troubleshooting

### Database Connection Issues

```bash
# Check if PostgreSQL is running
docker-compose ps db

# View database logs
docker-compose logs db

# Restart database
docker-compose restart db
```

### Redis Connection Issues

```bash
# Check if Redis is running
docker-compose ps redis

# View Redis logs
docker-compose logs redis

# Restart Redis
docker-compose restart redis
```

### Migration Issues

```bash
# Reset migrations (development only)
python manage.py migrate --fake-initial
python manage.py migrate --run-syncdb

# Create new migration
python manage.py makemigrations

# Apply migration
python manage.py migrate
```

### Permission Issues

```bash
# Fix file permissions
chmod +x manage.py
```

## Production Deployment

### Environment Variables

Ensure all required environment variables are set in production:

- `SECRET_KEY`: Strong random key
- `DEBUG=False`
- `ALLOWED_HOSTS`: Your domain(s)
- `DATABASE_URL`: Production PostgreSQL URL
- `REDIS_URL`: Production Redis URL
- `RESEND_API_KEY`: Resend API key
- Cloudflare R2 credentials
- CORS settings

### Build Docker Image

```bash
docker build -t inventory-management .
```

### Run with Docker Compose

```bash
docker-compose -f docker-compose.prod.yml up -d
```

### SSL/TLS Configuration

Configure SSL/TLS in production:
- Set `SECURE_SSL_REDIRECT=True`
- Set `SESSION_COOKIE_SECURE=True`
- Set `CSRF_COOKIE_SECURE=True`
- Configure `SECURE_HSTS_*` settings

### Static Files

Collect static files:

```bash
python manage.py collectstatic --noinput
```

### Database Migrations

```bash
python manage.py migrate --noinput
```

### Create Superuser

```bash
python manage.py createsuperuser --noinput
```

## Health Check

The system includes a health check endpoint:

```bash
curl http://localhost:8000/health/
```

Response:
```json
{
  "status": "healthy",
  "service": "inventory-management-system"
}
```

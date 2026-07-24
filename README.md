# Industrial Inventory Management System

A production-ready backend for industrial inventory management, built with Django 5 and Django REST Framework. Designed for companies like OCP Phosboucraa requiring robust, scalable inventory tracking.

## Features

- **Authentication & Authorization**: JWT-based auth with RBAC, invitation-based user registration
- **Inventory Management**: Products, categories, brands, units, and suppliers
- **Warehouse Management**: Multi-warehouse support with zones, rows, shelves, and bins
- **Stock Management**: Real-time stock tracking, reservations, and low-stock alerts
- **Stock Movements**: Entry, exit, transfer, adjustment, and workflow-based requests
- **Audit Logging**: Comprehensive tracking of all system changes
- **Notifications**: Email notifications via Resend
- **Dashboard**: Analytics and reporting with export capabilities
- **API Documentation**: OpenAPI/Swagger documentation
- **Testing**: Comprehensive test suite with pytest
- **Code Quality**: Black, Ruff, isort, mypy, pre-commit
- **CI/CD**: GitHub Actions for automated testing and deployment
- **Docker**: Containerized deployment with Docker Compose

## Technology Stack

- **Backend**: Django 5.0.7, Django REST Framework 3.15.2
- **Database**: PostgreSQL 16 (Neon)
- **Cache**: Redis
- **Authentication**: JWT (SimpleJWT)
- **Storage**: Cloudflare R2
- **Email**: Resend SMTP
- **Testing**: pytest, pytest-django, factory-boy
- **Code Quality**: Black, Ruff, isort, mypy, pre-commit
- **CI/CD**: GitHub Actions
- **Containerization**: Docker, Docker Compose

## Architecture

The system follows Clean Architecture principles with modular structure:

```
apps/
├── accounts/          # Authentication & user management
├── inventory/         # Product & inventory management
├── categories/        # Product categorization
├── suppliers/         # Supplier management
├── warehouses/        # Warehouse & location management
├── locations/         # Product storage locations
├── stock/             # Stock management
├── movements/        # Stock movements & transfers
├── notifications/     # Email notifications
├── dashboard/         # Analytics & reporting
├── audit/             # Audit logging
├── core/              # Base models & middleware
└── common/            # Shared utilities & services
```

## Quick Start

### Prerequisites

- Python 3.12+
- Docker and Docker Compose
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Syst-me-de-Gestion-d-Inventaire
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Start services with Docker**
   ```bash
   docker-compose up -d db redis
   ```

6. **Run migrations**
   ```bash
   python manage.py migrate
   ```

7. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

8. **Run development server**
   ```bash
   python manage.py runserver
   ```

The API will be available at `http://localhost:8000`

### API Documentation

- Swagger UI: `http://localhost:8000/api/docs/`
- ReDoc: `http://localhost:8000/api/redoc/`
- Schema: `http://localhost:8000/api/schema/`

## User Registration Flow

The platform is **not public**. User registration follows an invitation-based flow:

1. Admin creates employee account with details
2. System generates invitation token
3. Employee receives invitation email via Resend
4. Employee activates account by choosing password
5. Account becomes active

## User Roles

- **SUPER_ADMIN**: Full system access
- **ADMINISTRATOR**: User and system management
- **WAREHOUSE_MANAGER**: Warehouse operations
- **MAINTENANCE_MANAGER**: Stock request approval
- **WAREHOUSE_OPERATOR**: Stock operations and validation
- **TECHNICIAN**: Create stock requests
- **VIEWER**: Read-only access

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest apps/accounts/tests.py
```

## Code Quality

```bash
# Format code
black .

# Lint code
ruff check .

# Sort imports
isort .

# Type check
mypy config/ apps/ --ignore-missing-imports

# Run pre-commit hooks
pre-commit run --all-files
```

## Docker

### Development

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f web

# Stop all services
docker-compose down
```

### Production

```bash
# Start production services
docker-compose -f docker-compose.prod.yml up -d
```

## Documentation

Comprehensive documentation is available in the `docs/` directory:

- [Architecture.md](docs/Architecture.md) - System architecture and design
- [Installation.md](docs/Installation.md) - Installation guide
- [Environment.md](docs/Environment.md) - Environment configuration
- [API.md](docs/API.md) - Complete API reference
- [Database.md](docs/Database.md) - Database schema
- [Deployment.md](docs/Deployment.md) - Production deployment
- [Authentication.md](docs/Authentication.md) - Authentication guide
- [Troubleshooting.md](docs/Troubleshooting.md) - Common issues

## Security

- JWT-based authentication with access/refresh tokens
- Role-Based Access Control (RBAC)
- Password complexity requirements
- Rate limiting
- CORS configuration
- Secure headers
- Environment-based configuration
- Audit logging

## Contributing

1. Create a feature branch
2. Make your changes
3. Run tests and code quality checks
4. Submit a pull request

## License

Proprietary - All rights reserved

## Support

For issues and questions, refer to the documentation or contact the development team.

# Architecture Documentation

## System Overview

The Industrial Inventory Management System is a production-ready backend built with Django 5 and Django REST Framework, designed for industrial-scale inventory management suitable for companies like OCP Phosboucraa.

## Architecture Principles

### Clean Architecture

The system follows Clean Architecture principles with clear separation of concerns:

- **Models**: Data layer with business logic
- **Serializers**: Data validation and serialization
- **Views**: Request handling and response formatting
- **Services**: Business logic layer
- **Selectors**: Data retrieval layer
- **Permissions**: Access control layer

### SOLID Principles

- **Single Responsibility**: Each class has one reason to change
- **Open/Closed**: Open for extension, closed for modification
- **Liskov Substitution**: Subtypes must be substitutable for base types
- **Interface Segregation**: Clients depend only on interfaces they use
- **Dependency Inversion**: Depend on abstractions, not concretions

## Modular Structure

```
apps/
├── accounts/          # Authentication and user management
├── inventory/         # Product and inventory management
├── categories/        # Product categorization
├── suppliers/         # Supplier management
├── warehouses/        # Warehouse and location management
├── locations/         # Product storage locations
├── stock/             # Stock management and calculations
├── movements/        # Stock movements and transfers
├── notifications/     # Email and notification system
├── dashboard/         # Analytics and reporting
├── audit/             # Audit logging system
├── core/              # Base models and middleware
└── common/            # Shared utilities and services
```

## Data Flow

### Request Flow

1. **Request Reception**: Middleware intercepts request
2. **Authentication**: JWT token validation
3. **Authorization**: Permission checks
4. **View Processing**: Request handling
5. **Service Layer**: Business logic execution
6. **Data Layer**: Database operations
7. **Response**: JSON response formatting
8. **Audit Logging**: Action logged

### Stock Movement Flow

1. **Request Creation**: Technician creates stock request
2. **Approval**: Maintenance manager approves
3. **Validation**: Warehouse operator validates
4. **Movement Generation**: Automatic movement creation
5. **Stock Update**: Stock quantities adjusted
6. **Audit Logging**: All actions logged

## Technology Stack

### Backend
- Django 5.0.7
- Django REST Framework 3.15.2
- PostgreSQL (Neon)
- Redis (caching and Celery)

### Authentication
- JWT (SimpleJWT)
- Access/Refresh tokens
- Token blacklisting

### Storage
- Cloudflare R2 (production)
- Local storage (development)

### Email
- Resend SMTP provider
- HTML email templates

### Code Quality
- Black (formatting)
- Ruff (linting)
- isort (import sorting)
- mypy (type checking)
- pre-commit (hooks)

### Testing
- pytest
- pytest-django
- pytest-cov
- factory-boy
- faker

### CI/CD
- GitHub Actions
- Docker
- Docker Compose

## Database Design

### Primary Keys
- All tables use UUID primary keys
- Ensures uniqueness across distributed systems
- Prevents ID enumeration attacks

### Indexing Strategy
- Foreign keys indexed
- Frequently queried fields indexed
- Composite indexes for common query patterns

### Soft Delete
- Implemented via `SoftDeleteModel`
- `is_deleted` flag
- `deleted_at` timestamp
- `deleted_by` reference

### Audit Trail
- Comprehensive audit logging
- Tracks all CRUD operations
- Stores old/new data
- IP address and user agent tracking

## Security

### Authentication
- JWT-based authentication
- Access token: 60 minutes
- Refresh token: 7 days
- Token rotation on refresh
- Blacklist after rotation

### Authorization
- Role-Based Access Control (RBAC)
- Granular permissions
- Custom permission classes
- Permission inheritance

### Data Validation
- Pydantic models for validation
- DRF serializers
- Custom validators
- Password complexity requirements

### Rate Limiting
- Per-endpoint rate limiting
- User-based throttling
- Anonymous user throttling
- Configurable limits

## Scalability Considerations

### Horizontal Scaling
- Stateless API design
- Redis for session management
- Database connection pooling
- Celery for async tasks

### Caching Strategy
- Redis for frequently accessed data
- Query result caching
- View caching for analytics
- Cache invalidation on updates

### Database Optimization
- Query optimization
- Select related/prefetch related
- Database indexing
- Connection pooling

## Monitoring and Logging

### Logging
- Structured logging
- Log levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- File and console handlers
- Request/response logging

### Error Tracking
- Sentry integration (optional)
- Comprehensive error handling
- Custom exception classes
- Error response formatting

## Deployment Architecture

### Development
- Docker Compose
- Local PostgreSQL
- Local Redis
- Console email backend

### Production
- Docker containers
- Neon PostgreSQL
- Redis (managed)
- Resend email
- Cloudflare R2 storage
- Gunicorn WSGI server
- Nginx reverse proxy

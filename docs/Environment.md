# Environment Configuration Guide

## Overview

This guide explains all environment variables used in the Industrial Inventory Management System.

## Environment Variables

### Django Core Settings

#### SECRET_KEY
- **Purpose**: Cryptographic signing key for Django
- **How to obtain**: Generate using `python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'`
- **Where to create**: `.env` file
- **Example**: `django-insecure-#k8z^$1q@w*2p&3r%4s(5t)6u=7v+8w-9x*0y`
- **Security**: Must be kept secret, never commit to version control

#### DEBUG
- **Purpose**: Enable/disable debug mode
- **Values**: `True` (development), `False` (production)
- **Development**: `True`
- **Production**: `False`
- **Security**: Always `False` in production

#### ALLOWED_HOSTS
- **Purpose**: Allowed hostnames for the application
- **Format**: Comma-separated list
- **Development**: `localhost,127.0.0.1`
- **Production**: `yourdomain.com,www.yourdomain.com`
- **Security**: Must match your domain(s) in production

### Database Settings

#### DATABASE_URL
- **Purpose**: PostgreSQL connection string
- **Format**: `postgres://user:password@host:port/dbname`
- **Development**: `postgres://postgres:postgres@localhost:5432/inventory_db`
- **Production**: Get from Neon dashboard
- **How to obtain**: Create Neon database and copy connection string

#### POSTGRES_DB
- **Purpose**: Database name (alternative to DATABASE_URL)
- **Development**: `inventory_db`
- **Production**: Your Neon database name

#### POSTGRES_USER
- **Purpose**: Database username (alternative to DATABASE_URL)
- **Development**: `postgres`
- **Production**: Your Neon username

#### POSTGRES_PASSWORD
- **Purpose**: Database password (alternative to DATABASE_URL)
- **Development**: `postgres`
- **Production**: Your Neon password
- **Security**: Must be kept secret

#### POSTGRES_HOST
- **Purpose**: Database host (alternative to DATABASE_URL)
- **Development**: `localhost`
- **Production**: Your Neon host

#### POSTGRES_PORT
- **Purpose**: Database port (alternative to DATABASE_URL)
- **Development**: `5432`
- **Production**: `5432` (Neon default)

### JWT Authentication Settings

#### JWT_SECRET
- **Purpose**: Secret key for JWT token signing
- **How to obtain**: Generate random string or use SECRET_KEY
- **Example**: `your-jwt-secret-key-here`
- **Security**: Must be kept secret

#### JWT_ACCESS_TOKEN_LIFETIME_MINUTES
- **Purpose**: Access token validity duration
- **Default**: `60` (minutes)
- **Production**: Adjust based on security requirements

#### JWT_REFRESH_TOKEN_LIFETIME_DAYS
- **Purpose**: Refresh token validity duration
- **Default**: `7` (days)
- **Production**: Adjust based on security requirements

### Email Settings (Resend)

#### RESEND_API_KEY
- **Purpose**: API key for Resend email service
- **How to obtain**: 
  1. Go to https://resend.com/api-keys
  2. Sign up or log in
  3. Create API key
  4. Copy the key
- **Example**: `re_xxxxxxxxxxxxxxxxxxxxxxxx`
- **Security**: Must be kept secret

#### DEFAULT_FROM_EMAIL
- **Purpose**: Default sender email address
- **Format**: Valid email address
- **How to obtain**: Verify domain in Resend dashboard
- **Example**: `noreply@yourdomain.com`
- **Note**: Domain must be verified in Resend

#### EMAIL_BACKEND
- **Purpose**: Email backend to use
- **Development**: `django.core.mail.backends.console.EmailBackend`
- **Production**: `django.core.mail.backends.smtp.EmailBackend`

#### EMAIL_HOST
- **Purpose**: SMTP server host
- **Resend**: `smtp.resend.com`
- **Development**: Can use console backend

#### EMAIL_PORT
- **Purpose**: SMTP server port
- **Resend**: `587`
- **Development**: N/A for console backend

#### EMAIL_USE_TLS
- **Purpose**: Use TLS for SMTP
- **Resend**: `True`
- **Development**: N/A for console backend

#### EMAIL_HOST_USER
- **Purpose**: SMTP username
- **Resend**: `resend`
- **Development**: N/A for console backend

#### EMAIL_HOST_PASSWORD
- **Purpose**: SMTP password
- **Resend**: Your RESEND_API_KEY
- **Development**: N/A for console backend
- **Security**: Must be kept secret

### Cloudflare R2 Storage Settings

#### CLOUDFLARE_ACCOUNT_ID
- **Purpose**: Cloudflare account identifier
- **How to obtain**:
  1. Go to https://dash.cloudflare.com/
  2. Select your account
  3. Copy Account ID from right sidebar
- **Example**: `xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
- **Security**: Not secret but should be kept private

#### CLOUDFLARE_R2_BUCKET
- **Purpose**: R2 bucket name
- **How to obtain**:
  1. Go to Cloudflare R2 dashboard
  2. Create bucket
  3. Use bucket name
- **Example**: `inventory-management`
- **Note**: Must be unique across R2

#### CLOUDFLARE_R2_ACCESS_KEY
- **Purpose**: R2 access key ID
- **How to obtain**:
  1. Go to R2 dashboard
  2. Manage R2 API Tokens
  3. Create token with appropriate permissions
  4. Copy Access Key ID
- **Example**: `xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
- **Security**: Must be kept secret

#### CLOUDFLARE_R2_SECRET_KEY
- **Purpose**: R2 secret access key
- **How to obtain**: Generated when creating R2 API token
- **Example**: `xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
- **Security**: Must be kept secret

#### CLOUDFLARE_ENDPOINT
- **Purpose**: R2 endpoint URL
- **Format**: `https://<account-id>.r2.cloudflarestorage.com`
- **Example**: `https://xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx.r2.cloudflarestorage.com`
- **Note**: Use your account ID

#### MEDIA_URL
- **Purpose**: URL prefix for media files
- **Development**: `/media/`
- **Production**: Your CDN domain or R2 public URL
- **Example**: `https://your-cdn-domain.com/media/`

#### STATIC_URL
- **Purpose**: URL prefix for static files
- **Development**: `/static/`
- **Production**: Your CDN domain or R2 public URL
- **Example**: `https://your-cdn-domain.com/static/`

### CORS Settings

#### CORS_ALLOWED_ORIGINS
- **Purpose**: Allowed origins for CORS
- **Format**: Comma-separated list
- **Development**: `http://localhost:3000,http://127.0.0.1:3000`
- **Production**: Your frontend domain(s)
- **Example**: `https://your-frontend-domain.com`

#### CORS_ALLOW_CREDENTIALS
- **Purpose**: Allow credentials in CORS requests
- **Values**: `True`, `False`
- **Default**: `True`

### Redis Settings

#### REDIS_URL
- **Purpose**: Redis connection string
- **Format**: `redis://host:port/db`
- **Development**: `redis://localhost:6379/0`
- **Production**: Your Redis instance URL
- **How to obtain**: Set up Redis instance (managed or self-hosted)

### Celery Settings

#### CELERY_BROKER_URL
- **Purpose**: Celery broker URL
- **Format**: Same as REDIS_URL
- **Development**: `redis://localhost:6379/0`
- **Production**: Your Redis instance URL

#### CELERY_RESULT_BACKEND
- **Purpose**: Celery result backend URL
- **Format**: Same as REDIS_URL
- **Development**: `redis://localhost:6379/0`
- **Production**: Your Redis instance URL

### Security Settings

#### SECURE_SSL_REDIRECT
- **Purpose**: Redirect HTTP to HTTPS
- **Development**: `False`
- **Production**: `True`

#### SESSION_COOKIE_SECURE
- **Purpose**: Use secure cookies for sessions
- **Development**: `False`
- **Production**: `True`

#### CSRF_COOKIE_SECURE
- **Purpose**: Use secure cookies for CSRF
- **Development**: `False`
- **Production**: `True`

#### SECURE_HSTS_SECONDS
- **Purpose**: HSTS max-age in seconds
- **Development**: `0` (disabled)
- **Production**: `31536000` (1 year)

#### SECURE_HSTS_INCLUDE_SUBDOMAINS
- **Purpose**: Include subdomains in HSTS
- **Development**: `False`
- **Production**: `True`

#### SECURE_HSTS_PRELOAD
- **Purpose**: Allow HSTS preloading
- **Development**: `False`
- **Production**: `True`

### Rate Limiting

#### RATE_LIMIT_PER_MINUTE
- **Purpose**: Maximum requests per minute per user
- **Default**: `60`
- **Production**: Adjust based on traffic

### Sentry (Optional)

#### SENTRY_DSN
- **Purpose**: Sentry Data Source Name for error tracking
- **How to obtain**:
  1. Go to https://sentry.io/
  2. Create project
  3. Copy DSN
- **Example**: `https://xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx@o123456.ingest.sentry.io/123456`
- **Security**: Must be kept secret
- **Optional**: Only needed if using Sentry

### Timezone and Language

#### TIME_ZONE
- **Purpose**: System timezone
- **Default**: `UTC`
- **Production**: Set to your timezone

#### LANGUAGE_CODE
- **Purpose**: System language code
- **Default**: `en-us`
- **Production**: Set to your language

### Logging

#### LOG_LEVEL
- **Purpose**: Logging level
- **Values**: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`
- **Development**: `DEBUG`
- **Production**: `INFO` or `WARNING`

## Environment Files

### Development (.env)

```bash
SECRET_KEY=django-insecure-development-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DATABASE_URL=postgres://postgres:postgres@localhost:5432/inventory_db
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend

CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

SECURE_SSL_REDIRECT=False
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False
SECURE_HSTS_SECONDS=0

LOG_LEVEL=DEBUG
```

### Production (.env.prod)

```bash
SECRET_KEY=<strong-random-key>
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

DATABASE_URL=postgres://user:password@ep-xxx.neon.tech/neondb?sslmode=require
REDIS_URL=redis://your-redis-host:6379/0
CELERY_BROKER_URL=redis://your-redis-host:6379/0
CELERY_RESULT_BACKEND=redis://your-redis-host:6379/0

RESEND_API_KEY=re_xxxxxxxxx
DEFAULT_FROM_EMAIL=noreply@yourdomain.com
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.resend.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=resend
EMAIL_HOST_PASSWORD=re_xxxxxxxxx

CLOUDFLARE_ACCOUNT_ID=xxxxxxxx
CLOUDFLARE_R2_BUCKET=inventory-management
CLOUDFLARE_R2_ACCESS_KEY=xxxxxxxx
CLOUDFLARE_R2_SECRET_KEY=xxxxxxxx
CLOUDFLARE_ENDPOINT=https://xxxxxxxx.r2.cloudflarestorage.com
MEDIA_URL=https://your-cdn-domain.com/media/
STATIC_URL=https://your-cdn-domain.com/static/

CORS_ALLOWED_ORIGINS=https://your-frontend-domain.com

SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_HSTS_PRELOAD=True

LOG_LEVEL=INFO
```

## Security Best Practices

1. **Never commit `.env` files** to version control
2. **Use strong, random values** for all secrets
3. **Rotate secrets regularly** in production
4. **Use different values** for development and production
5. **Limit access** to production environment variables
6. **Use secret management tools** (AWS Secrets Manager, HashiCorp Vault)
7. **Audit access** to sensitive environment variables
8. **Document ownership** for each environment variable

## Testing Environment Variables

To test your environment configuration:

```bash
python manage.py check --deploy
```

This will check for common deployment configuration issues.

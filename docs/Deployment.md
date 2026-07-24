# Deployment Guide

## Production Deployment

### Prerequisites

- Docker and Docker Compose
- Cloudflare R2 account
- Neon PostgreSQL account
- Resend API account
- Domain name with SSL certificate

### Environment Configuration

1. **Create Production Environment File**

```bash
cp .env.example .env.prod
```

2. **Configure Production Variables**

Edit `.env.prod` with production values:

```bash
# Security
SECRET_KEY=<strong-random-key>
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database
DATABASE_URL=postgres://user:password@ep-xxx.neon.tech/neondb?sslmode=require

# Redis
REDIS_URL=redis://your-redis-host:6379/0
CELERY_BROKER_URL=redis://your-redis-host:6379/0
CELERY_RESULT_BACKEND=redis://your-redis-host:6379/0

### Email
RESEND_API_KEY=re_xxxxxxxxx
DEFAULT_FROM_EMAIL=noreply@yourdomain.com

### Cloudflare R2
CLOUDFLARE_ACCOUNT_ID=xxxxxxxx
CLOUDFLARE_R2_BUCKET=inventory-management
CLOUDFLARE_R2_ACCESS_KEY=xxxxxxxx
CLOUDFLARE_R2_SECRET_KEY=xxxxxxxx
CLOUDFLARE_ENDPOINT=https://xxxxxxxx.r2.cloudflarestorage.com
MEDIA_URL=https://your-cdn-domain.com/media/
STATIC_URL=https://your-cdn-domain.com/static/

### CORS
CORS_ALLOWED_ORIGINS=https://your-frontend-domain.com

### Security
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_HSTS_PRELOAD=True
```

### Docker Deployment

1. **Build Docker Image**

```bash
docker build -t inventory-management:latest .
```

2. **Tag for Registry**

```bash
docker tag inventory-management:latest your-registry/inventory-management:latest
```

3. **Push to Registry**

```bash
docker push your-registry/inventory-management:latest
```

4. **Deploy with Docker Compose**

```bash
docker-compose -f docker-compose.prod.yml up -d
```

### Nginx Configuration

Create Nginx configuration file:

```nginx
upstream inventory_backend {
    server localhost:8000;
}

server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;

    ssl_certificate /etc/ssl/certs/yourdomain.com.crt;
    ssl_certificate_key /etc/ssl/private/yourdomain.com.key;

    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    client_max_body_size 10M;

    location / {
        proxy_pass http://inventory_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /var/www/static/;
        expires 30d;
    }

    location /media/ {
        alias /var/www/media/;
        expires 30d;
    }
}
```

### Systemd Service

Create systemd service file:

```ini
[Unit]
Description=Inventory Management System
After=network.target

[Service]
Type=notify
User=www-data
Group=www-data
WorkingDirectory=/var/www/inventory-management
Environment="PATH=/var/www/inventory-management/venv/bin"
ExecStart=/var/www/inventory-management/venv/bin/gunicorn config.wsgi:application --bind unix:/var/www/inventory-management/inventory.sock --workers 4 --threads 2 --timeout 120
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start service:

```bash
sudo systemctl enable inventory
sudo systemctl start inventory
```

### Monitoring

#### Health Checks

Configure health check endpoint monitoring:

```bash
curl https://yourdomain.com/health/
```

#### Log Monitoring

```bash
# View application logs
docker-compose -f docker-compose.prod.yml logs -f web

# View Celery logs
docker-compose -f docker-compose.prod.yml logs -f celery_worker
```

#### Performance Monitoring

Consider integrating:
- Sentry for error tracking
- Prometheus for metrics
- Grafana for visualization

### Backup Strategy

#### Database Backups

Automate PostgreSQL backups:

```bash
# Daily backup
0 2 * * * pg_dump -h <neon-host> -U <user> -d <database> > /backups/daily_$(date +\%Y\%m\%d).sql

# Weekly backup
0 3 * * 0 pg_dump -h <neon-host> -U <user> -d <database> > /backups/weekly_$(date +\%Y\%m\%d).sql
```

#### Media Backups

Sync R2 bucket to backup location:

```bash
aws s3 sync s3://inventory-bucket /backups/media/
```

### SSL/TLS Configuration

Use Let's Encrypt for free SSL:

```bash
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

Auto-renewal is configured automatically.

### Security Hardening

1. **Firewall Configuration**

```bash
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

2. **Fail2Ban**

Install and configure Fail2Ban:

```bash
sudo apt install fail2ban
```

3. **Security Headers**

Add security headers in Nginx:

```nginx
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Referrer-Policy "no-referrer-when-downgrade" always;
```

### Scaling

#### Horizontal Scaling

1. **Load Balancer**

Use Nginx or cloud load balancer:

```nginx
upstream inventory_backend {
    server server1:8000;
    server server2:8000;
    server server3:8000;
}
```

2. **Session Storage**

Use Redis for session storage:

```python
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'
```

3. **Database Connection Pooling**

Configure connection pool in settings:

```python
DATABASES['default']['OPTIONS'] = {
    'MAX_CONNS': 20,
}
```

#### Vertical Scaling

Increase worker count based on CPU cores:

```bash
# 2 workers per CPU core
gunicorn config.wsgi:application --workers 8 --threads 2
```

### CI/CD Pipeline

The GitHub Actions workflow automatically:

1. Runs code quality checks
2. Executes tests
3. Builds Docker image
4. Pushes to registry
5. Deploys to production (on main branch)

### Rollback Procedure

1. **Database Rollback**

```bash
python manage.py migrate <app> <previous_migration>
```

2. **Code Rollback**

```bash
git checkout <previous_tag>
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml up -d --build
```

3. **Docker Rollback**

```bash
docker pull your-registry/inventory-management:<previous_tag>
docker-compose -f docker-compose.prod.yml up -d
```

### Troubleshooting

#### Application Won't Start

```bash
# Check logs
docker-compose -f docker-compose.prod.yml logs web

# Check environment variables
docker-compose -f docker-compose.prod.yml config

# Check database connection
docker-compose -f docker-compose.prod.yml exec web python manage.py dbshell
```

#### Database Connection Issues

```bash
# Check database status
docker-compose -f docker-compose.prod.yml exec web python manage.py check --database default

# Test connection
psql $DATABASE_URL
```

#### Celery Tasks Not Running

```bash
# Check Celery logs
docker-compose -f docker-compose.prod.yml logs celery_worker

# Check Celery beat
docker-compose -f docker-compose.prod.yml logs celery_beat

# Check Flower
curl http://localhost:5555
```

#### High Memory Usage

```bash
# Check container stats
docker stats

# Restart services
docker-compose -f docker-compose.prod.yml restart
```

### Performance Tuning

#### Database Optimization

```sql
-- Update statistics
ANALYZE;

-- Reindex
REINDEX DATABASE inventory_db;

-- Vacuum
VACUUM ANALYZE;
```

#### Cache Configuration

```python
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': env('REDIS_URL'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'CONNECTION_POOL_KWARGS': {'max_connections': 50}
        },
        'KEY_PREFIX': 'inventory',
        'TIMEOUT': 300
    }
}
```

#### Gunicorn Tuning

```bash
gunicorn config.wsgi:application \
    --workers 4 \
    --threads 2 \
    --worker-class gthread \
    --timeout 120 \
    --keepalive 5 \
    --max-requests 1000 \
    --max-requests-jitter 50
```

## Monitoring and Alerting

### Application Monitoring

- **Sentry**: Error tracking
- **Prometheus**: Metrics collection
- **Grafana**: Visualization

### Log Aggregation

- **ELK Stack**: Elasticsearch, Logstash, Kibana
- **CloudWatch**: AWS logging
- **Papertrail**: Cloud logging service

### Uptime Monitoring

- **UptimeRobot**: Free uptime monitoring
- **Pingdom**: Advanced monitoring
- **Statuspage**: Public status page

## Disaster Recovery

### Backup Strategy

1. **Daily database backups**
2. **Weekly full backups**
3. **Off-site backup storage**
4. **Backup verification**

### Recovery Procedure

1. **Assess damage**
2. **Restore from latest backup**
3. **Verify data integrity**
4. **Test application functionality**
5. **Monitor for issues**

### Business Continuity

- **Failover server**: Standby server ready
- **DNS failover**: Automatic DNS switching
- **Load balancing**: Distribute traffic
- **Data replication**: Multi-region replication

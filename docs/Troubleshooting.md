# Troubleshooting Guide

## Common Issues and Solutions

### Database Issues

#### Connection Refused

**Symptom**: `could not connect to server: Connection refused`

**Solutions**:
1. Check PostgreSQL is running:
   ```bash
   docker-compose ps db
   ```

2. Check DATABASE_URL in `.env`:
   ```bash
   DATABASE_URL=postgres://postgres:postgres@localhost:5432/inventory_db
   ```

3. Restart database:
   ```bash
   docker-compose restart db
   ```

#### Migration Errors

**Symptom**: Migration fails with error

**Solutions**:
1. Check for pending migrations:
   ```bash
   python manage.py showmigrations
   ```

2. Reset migrations (development only):
   ```bash
   python manage.py migrate --fake-initial
   ```

3. Create new migration:
   ```bash
   python manage.py makemigrations
   ```

#### Lock Timeout

**Symptom**: Database lock timeout

**Solutions**:
1. Check for long-running queries
2. Kill stuck connections:
   ```sql
   SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE state = 'idle in transaction';
   ```
3. Restart database

### Authentication Issues

#### Invalid Token

**Symptom**: `Given token not valid for any token type`

**Solutions**:
1. Check JWT_SECRET matches between requests
2. Verify token hasn't expired
3. Check if token is blacklisted
4. Generate new token

#### Login Fails

**Symptom**: Login returns 401

**Solutions**:
1. Verify user exists and is active
2. Check password is correct
3. Verify account status is ACTIVE
4. Check invitation was accepted

#### Permission Denied

**Symptom**: 403 Forbidden

**Solutions**:
1. Verify user role
2. Check permission assignment
3. Review permission logic
4. Ensure user is authenticated

### Docker Issues

#### Container Won't Start

**Symptom**: Container exits immediately

**Solutions**:
1. Check container logs:
   ```bash
   docker-compose logs web
   ```

2. Check environment variables:
   ```bash
   docker-compose config
   ```

3. Rebuild container:
   ```bash
   docker-compose up -d --build
   ```

#### Port Already in Use

**Symptom**: Port 8000 already in use

**Solutions**:
1. Find process using port:
   ```bash
   lsof -i :8000
   ```

2. Kill process or change port in docker-compose.yml

#### Volume Mount Issues

**Symptom**: Files not persisting

**Solutions**:
1. Check volume permissions
2. Verify volume exists:
   ```bash
   docker volume ls
   ```
3. Recreate volumes

### Redis Issues

#### Connection Refused

**Symptom**: Redis connection refused

**Solutions**:
1. Check Redis is running:
   ```bash
   docker-compose ps redis
   ```

2. Check REDIS_URL in `.env`
3. Restart Redis:
   ```bash
   docker-compose restart redis
   ```

#### Memory Issues

**Symptom**: Redis out of memory

**Solutions**:
1. Check Redis memory usage:
   ```bash
   docker exec redis redis-cli INFO memory
   ```
2. Increase memory limit in docker-compose.yml
3. Clear cache:
   ```bash
   python manage.py shell
   >>> from django.core.cache import cache
   >>> cache.clear()
   ```

### Email Issues

#### Emails Not Sending

**Symptom**: Emails not being sent

**Solutions**:
1. Check RESEND_API_KEY is valid
2. Verify DEFAULT_FROM_EMAIL is verified
3. Check email backend configuration
4. Test with console backend in development

#### Email Template Errors

**Symptom**: Template rendering fails

**Solutions**:
1. Check template exists in `templates/emails/`
2. Verify template syntax
3. Check context variables
4. Test template rendering:
   ```python
   from django.template.loader import render_to_string
   render_to_string('emails/invitation.html', context)
   ```

### Storage Issues

#### File Upload Fails

**Symptom**: File upload returns error

**Solutions**:
1. Check Cloudflare R2 credentials
2. Verify bucket exists
3. Check bucket permissions
4. Verify CLOUDFLARE_ENDPOINT is correct

#### File Not Accessible

**Symptom**: Uploaded file returns 404

**Solutions**:
1. Check MEDIA_URL configuration
2. Verify file was uploaded
3. Check bucket public access settings
4. Verify CDN configuration

### Performance Issues

#### Slow API Response

**Symptom**: API endpoints slow

**Solutions**:
1. Check database query performance
2. Add missing indexes
3. Use select_related/prefetch_related
4. Enable query caching
5. Check server resources

#### High Memory Usage

**Symptom**: Application using too much memory

**Solutions**:
1. Check for memory leaks
2. Reduce worker count
3. Enable connection pooling
4. Monitor with tools like `memory_profiler`

#### Database Slow Queries

**Symptom**: Database queries slow

**Solutions**:
1. Enable query logging:
   ```python
   LOGGING = {
       'loggers': {
           'django.db.backends': {
               'level': 'DEBUG',
           },
       },
   }
   ```
2. Analyze slow queries
3. Add appropriate indexes
4. Optimize queries

### Celery Issues

#### Tasks Not Executing

**Symptom**: Celery tasks not running

**Solutions**:
1. Check Celery worker is running:
   ```bash
   docker-compose ps celery_worker
   ```

2. Check worker logs:
   ```bash
   docker-compose logs celery_worker
   ```

3. Verify broker connection:
   ```python
   from celery import current_app
   current_app.send_task('task_name')
   ```

#### Beat Not Scheduling

**Symptom**: Scheduled tasks not running

**Solutions**:
1. Check Celery beat is running:
   ```bash
   docker-compose ps celery_beat
   ```

2. Check beat schedule configuration
3. Verify beat logs
4. Restart beat service

### Testing Issues

#### Tests Fail

**Symptom**: pytest tests fail

**Solutions**:
1. Check test database configuration
2. Verify fixtures are loading
3. Check for missing dependencies
4. Run with verbose output:
   ```bash
   pytest -v
   ```

#### Coverage Low

**Symptom**: Test coverage below threshold

**Solutions**:
1. Identify untested code
2. Add missing tests
3. Check coverage report:
   ```bash
   pytest --cov-report=html
   open htmlcov/index.html
   ```

### Code Quality Issues

#### Black Formatting Errors

**Symptom**: Black formatting fails

**Solutions**:
1. Run black with diff:
   ```bash
   black --diff .
   ```
2. Fix formatting issues
3. Re-run black

#### Ruff Linting Errors

**Symptom**: Ruff finds issues

**Solutions**:
1. Review ruff output
2. Fix reported issues
3. Ignore specific rules if needed:
   ```bash
   ruff check --ignore=E501 .
   ```

#### isort Errors

**Symptom**: Import sorting fails

**Solutions**:
1. Run isort with diff:
   ```bash
   isort --diff-only .
   ```
2. Fix import order
3. Re-run isort

### Deployment Issues

#### Build Fails

**Symptom**: Docker build fails

**Solutions**:
1. Check Dockerfile syntax
2. Verify base image exists
3. Check for network issues
4. Clean build cache:
   ```bash
   docker system prune -a
   ```

#### Container Crashes

**Symptom**: Container crashes in production

**Solutions**:
1. Check container logs
2. Verify environment variables
3. Check resource limits
4. Monitor health checks

#### SSL Certificate Issues

**Symptom**: SSL certificate errors

**Solutions**:
1. Verify certificate is valid
2. Check certificate chain
3. Renew expired certificate
4. Verify SSL configuration

### Debugging Tips

#### Enable Debug Mode

```python
DEBUG=True
```

#### Enable SQL Logging

```python
LOGGING = {
    'loggers': {
        'django.db.backends': {
            'level': 'DEBUG',
        },
    },
}
```

#### Use Django Debug Toolbar

```python
INSTALLED_APPS += ['debug_toolbar']
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
```

#### Check Request/Response

```python
from django.http import HttpResponse

def debug_request(request):
    return HttpResponse({
        'method': request.method,
        'path': request.path,
        'headers': dict(request.headers),
    })
```

#### Shell Access

```bash
python manage.py shell
```

#### Database Shell

```bash
python manage.py dbshell
```

### Getting Help

If you can't resolve the issue:

1. Check the documentation
2. Review error logs
3. Search for similar issues
4. Check GitHub issues
5. Contact support team

### Log Locations

#### Development
- Application logs: `logs/django.log`
- Docker logs: `docker-compose logs`

#### Production
- Application logs: Configured in deployment
- Docker logs: `docker-compose -f docker-compose.prod.yml logs`
- System logs: `/var/log/`

### Monitoring Commands

#### Check System Resources

```bash
# CPU usage
top

# Memory usage
free -h

# Disk usage
df -h

# Network connections
netstat -tulpn
```

#### Check Docker Resources

```bash
# Container stats
docker stats

# Container processes
docker top <container_name>

# Container logs
docker logs <container_name>
```

### Recovery Procedures

#### Database Recovery

1. Stop application
2. Restore from backup
3. Verify data integrity
4. Restart application

#### Application Recovery

1. Identify issue
2. Fix configuration
3. Restart services
4. Verify functionality

#### Disaster Recovery

1. Assess damage
2. Restore from off-site backup
3. Verify all systems
4. Monitor for issues

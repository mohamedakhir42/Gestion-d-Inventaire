# Authentication and Authorization

## Overview

The Industrial Inventory Management System uses JWT (JSON Web Token) based authentication with Role-Based Access Control (RBAC).

## Authentication Flow

### User Registration

The platform is **not public**. User registration follows an invitation-based flow:

1. **Admin creates employee account**
   - Admin fills in employee details
   - System generates invitation token
   - Invitation email sent via Resend

2. **Employee receives invitation**
   - Email contains activation link
   - Link includes invitation token

3. **Employee activates account**
   - Opens activation link
   - Chooses password
   - Uploads avatar (optional)
   - Accepts terms and conditions
   - Account becomes active

### Login Flow

1. **User submits credentials**
   - Email and password
   - Request to `/api/auth/login/`

2. **Server validates credentials**
   - Checks user exists
   - Verifies password
   - Checks account status

3. **Server issues tokens**
   - Access token (short-lived)
   - Refresh token (long-lived)
   - User information included

4. **Client stores tokens**
   - Access token in memory
   - Refresh token in secure storage

5. **Client includes token in requests**
   - `Authorization: Bearer <access_token>`

### Token Refresh

1. **Access token expires**
   - Client detects 401 response
   - Uses refresh token

2. **Client requests new access token**
   - POST to `/api/auth/token/refresh/`
   - Includes refresh token

3. **Server validates refresh token**
   - Checks token validity
   - Checks if blacklisted

4. **Server issues new access token**
   - Old refresh token blacklisted
   - New refresh token issued

### Logout Flow

1. **Client requests logout**
   - POST to `/api/auth/logout/`
   - Includes refresh token

2. **Server blacklists tokens**
   - Access token blacklisted
   - Refresh token blacklisted

3. **Client clears tokens**
   - Remove from storage
   - Redirect to login

## User Roles

### Role Hierarchy

```
SUPER_ADMIN (Level 7)
    ↓
ADMINISTRATOR (Level 6)
    ↓
WAREHOUSE_MANAGER (Level 5)
MAINTENANCE_MANAGER (Level 5)
    ↓
WAREHOUSE_OPERATOR (Level 4)
    ↓
TECHNICIAN (Level 3)
    ↓
VIEWER (Level 1)
```

### Role Permissions

#### SUPER_ADMIN
- Full system access
- User management (all operations)
- All warehouse operations
- All inventory operations
- System configuration
- Audit log access

#### ADMINISTRATOR
- User management (except SUPER_ADMIN)
- Warehouse management
- Inventory management
- Stock operations
- Report generation

#### WAREHOUSE_MANAGER
- Warehouse operations
- Stock management
- Movement approval
- Location management
- Team management (warehouse staff)

#### MAINTENANCE_MANAGER
- Stock request approval
- Request management
- Team management (maintenance staff)
- View inventory

#### WAREHOUSE_OPERATOR
- Stock operations
- Movement validation
- Location updates
- Stock counting

#### TECHNICIAN
- Create stock requests
- View inventory
- View own requests
- Update profile

#### VIEWER
- Read-only access
- View inventory
- View reports
- View dashboard

## Permission System

### Granular Permissions

Permissions are defined in the `accounts_permission` table:

- **Format**: `module.action`
- **Examples**:
  - `inventory.create_product`
  - `warehouses.manage_zones`
  - `stock.update_quantity`

### Role-Permission Mapping

Permissions are assigned to roles via `accounts_rolepermission`:

```python
# Example: Assign permission to role
role_permission = RolePermission.objects.create(
    role="WAREHOUSE_MANAGER",
    permission=permission  # Permission object
)
```

### Permission Checking

```python
# Check if user has permission
from apps.accounts.services import PermissionService

service = PermissionService()
has_permission = service.user_has_permission(user, "inventory.create_product")
```

## API Authentication

### Including Tokens

```bash
curl -H "Authorization: Bearer <access_token>" \
  https://api.example.com/api/inventory/products/
```

### Token Expiration

- **Access Token**: 60 minutes (configurable)
- **Refresh Token**: 7 days (configurable)

### Error Responses

#### Invalid Token
```json
{
  "detail": "Given token not valid for any token type",
  "code": "token_not_valid"
}
```

#### Expired Token
```json
{
  "detail": "Token is blacklisted",
  "code": "token_not_valid"
}
```

#### Missing Token
```json
{
  "detail": "Authentication credentials were not provided.",
  "code": "not_authenticated"
}
```

## Security Features

### Password Requirements

- Minimum 12 characters
- At least 1 uppercase letter
- At least 1 lowercase letter
- At least 1 digit
- At least 1 special character

### Token Security

- HS256 algorithm
- Secret key from environment
- Token rotation on refresh
- Blacklist after rotation
- Short-lived access tokens

### Account Security

- Invitation-based registration
- Email verification
- Terms acceptance required
- Account status tracking
- Login history logging

### Session Security

- JWT-based (no server-side sessions)
- Secure cookie flags in production
- CSRF protection
- Rate limiting
- IP-based tracking

## User Management

### Creating Users (Admin)

```bash
POST /api/auth/users/
{
  "email": "newuser@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "employee_id": "EMP001",
  "department": "Operations",
  "position": "Manager",
  "role": "WAREHOUSE_MANAGER"
}
```

### User Actions

#### Suspend User
```bash
POST /api/auth/users/{id}/suspend/
```

#### Restore User
```bash
POST /api/auth/users/{id}/restore/
```

#### Resend Invitation
```bash
POST /api/auth/users/{id}/resend-invitation/
```

### Password Management

#### Change Password
```bash
POST /api/auth/password/change/
{
  "old_password": "oldpass123",
  "new_password": "newpass456",
  "confirm_password": "newpass456"
}
```

#### Reset Password
```bash
POST /api/auth/password/reset/
{
  "email": "user@example.com"
}
```

#### Confirm Password Reset
```bash
POST /api/auth/password/reset/confirm/
{
  "token": "reset_token",
  "new_password": "newpass456",
  "confirm_password": "newpass456"
}
```

## Best Practices

### Client-Side

1. **Store tokens securely**
   - Use httpOnly cookies or secure storage
   - Never store in localStorage
   - Clear on logout

2. **Handle token expiration**
   - Refresh before expiration
   - Handle 401 responses
   - Redirect to login on failure

3. **Include tokens in requests**
   - Use Authorization header
   - Format: `Bearer <token>`
   - Include in all authenticated requests

### Server-Side

1. **Validate tokens on every request**
   - Check signature
   - Check expiration
   - Check blacklist

2. **Use appropriate permissions**
   - Check user role
   - Check specific permissions
   - Return 403 for unauthorized

3. **Log authentication events**
   - Successful logins
   - Failed attempts
   - Token refreshes
   - Logout events

## Troubleshooting

### Common Issues

#### Token Not Valid
- Check token expiration
- Verify secret key matches
- Check if token is blacklisted

#### Permission Denied
- Verify user role
- Check permission assignment
- Review permission logic

#### Invitation Not Working
- Check email configuration
- Verify invitation token
- Check invitation expiration

### Debugging

Enable debug logging for authentication:

```python
LOGGING = {
    'loggers': {
        'django.contrib.auth': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}
```

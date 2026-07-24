# API Documentation

## Base URL

- Development: `http://localhost:8000/api`
- Production: `https://your-domain.com/api`

## Authentication

### Login

**Endpoint:** `POST /api/auth/login/`

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "user": {
    "id": "uuid",
    "email": "user@example.com",
    "full_name": "John Doe",
    "role": "WAREHOUSE_MANAGER"
  }
}
```

### Token Refresh

**Endpoint:** `POST /api/auth/token/refresh/`

**Request Body:**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Response:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### Logout

**Endpoint:** `POST /api/auth/logout/`

**Headers:** `Authorization: Bearer <access_token>`

**Response:**
```json
{
  "detail": "Successfully logged out."
}
```

## Users

### List Users

**Endpoint:** `GET /api/auth/users/`

**Headers:** `Authorization: Bearer <access_token>`

**Query Parameters:**
- `role`: Filter by role
- `status`: Filter by status
- `department`: Filter by department
- `search`: Search by name or email
- `page`: Page number
- `page_size`: Items per page

**Response:**
```json
{
  "count": 100,
  "next": "http://localhost:8000/api/auth/users/?page=2",
  "previous": null,
  "page_size": 50,
  "current_page": 1,
  "total_pages": 2,
  "results": [
    {
      "id": "uuid",
      "email": "user@example.com",
      "first_name": "John",
      "last_name": "Doe",
      "full_name": "John Doe",
      "role": "WAREHOUSE_MANAGER",
      "status": "ACTIVE",
      "created_at": "2024-01-01T00:00:00Z"
    }
  ]
}
```

### Create User (Admin Only)

**Endpoint:** `POST /api/auth/users/`

**Request Body:**
```json
{
  "email": "newuser@example.com",
  "first_name": "Jane",
  "last_name": "Smith",
  "employee_id": "EMP001",
  "department": "Operations",
  "position": "Manager",
  "role": "WAREHOUSE_MANAGER"
}
```

### Update User

**Endpoint:** `PATCH /api/auth/users/{id}/`

**Request Body:**
```json
{
  "first_name": "Jane",
  "last_name": "Doe",
  "department": "Logistics"
}
```

### User Actions

**Endpoint:** `POST /api/auth/users/{id}/{action}/`

**Actions:** `suspend`, `restore`

**Response:**
```json
{
  "detail": "User suspended successfully."
}
```

## Inventory

### Products

#### List Products

**Endpoint:** `GET /api/inventory/products/`

**Query Parameters:**
- `category`: Filter by category
- `brand`: Filter by brand
- `supplier`: Filter by supplier
- `status`: Filter by status
- `search`: Search by name or code
- `ordering`: Order by field

**Response:**
```json
{
  "count": 100,
  "results": [
    {
      "id": "uuid",
      "internal_code": "PRD001",
      "barcode": "1234567890123",
      "name": "Product Name",
      "category": "uuid",
      "category_name": "Electronics",
      "brand": "uuid",
      "brand_name": "BrandX",
      "current_stock": 100,
      "available_stock": 100,
      "minimum_stock": 10,
      "is_below_minimum": false
    }
  ]
}
```

#### Create Product

**Endpoint:** `POST /api/inventory/products/`

**Request Body:**
```json
{
  "internal_code": "PRD001",
  "barcode": "1234567890123",
  "name": "Product Name",
  "description": "Product description",
  "category": "uuid",
  "brand": "uuid",
  "unit": "uuid",
  "supplier": "uuid",
  "purchase_price": 100.00,
  "selling_price": 150.00,
  "minimum_stock": 10,
  "maximum_stock": 1000
}
```

#### Get Product by Barcode

**Endpoint:** `GET /api/inventory/products/barcode/{barcode}/`

### Categories

#### List Categories

**Endpoint:** `GET /api/inventory/categories/`

#### Category Tree

**Endpoint:** `GET /api/inventory/categories/tree/`

**Response:**
```json
{
  "id": "uuid",
  "name": "Electronics",
  "code": "ELEC",
  "children": [
    {
      "id": "uuid",
      "name": "Computers",
      "code": "COMP",
      "children": []
    }
  ]
}
```

### Brands

#### List Brands

**Endpoint:** `GET /api/inventory/brands/`

### Units

#### List Units

**Endpoint:** `GET /api/inventory/units/`

### Suppliers

#### List Suppliers

**Endpoint:** `GET /api/inventory/suppliers/`

## Warehouses

### Warehouses

#### List Warehouses

**Endpoint:** `GET /api/warehouses/`

**Response:**
```json
{
  "count": 5,
  "results": [
    {
      "id": "uuid",
      "code": "WH001",
      "name": "Main Warehouse",
      "city": "Casablanca",
      "country": "Morocco",
      "status": "ACTIVE",
      "total_capacity": 10000,
      "used_capacity": 7500
    }
  ]
}
```

### Zones

#### List Warehouse Zones

**Endpoint:** `GET /api/warehouses/{warehouse_id}/zones/`

### Rows

#### List Zone Rows

**Endpoint:** `GET /api/warehouses/zones/{zone_id}/rows/`

### Shelves

#### List Row Shelves

**Endpoint:** `GET /api/warehouses/rows/{row_id}/shelves/`

### Bins

#### List Shelf Bins

**Endpoint:** `GET /api/warehouses/shelves/{shelf_id}/bins/`

## Stock

### Stock Records

#### List Stock

**Endpoint:** `GET /api/stock/stocks/`

**Query Parameters:**
- `warehouse`: Filter by warehouse
- `product`: Filter by product

**Response:**
```json
{
  "count": 100,
  "results": [
    {
      "id": "uuid",
      "product": "uuid",
      "product_name": "Product Name",
      "warehouse": "uuid",
      "warehouse_name": "WH001",
      "quantity": 100,
      "reserved_quantity": 20,
      "available_quantity": 80,
      "minimum_level": 10,
      "is_below_minimum": false
    }
  ]
}
```

#### Stock Count

**Endpoint:** `POST /api/stock/stocks/{id}/count/`

**Request Body:**
```json
{
  "counted_quantity": 95
}
```

#### Low Stock Alert

**Endpoint:** `GET /api/stock/stocks/low_stock/`

#### Reorder Stock

**Endpoint:** `GET /api/stock/stocks/reorder_stock/`

### Stock Reservations

#### List Reservations

**Endpoint:** `GET /api/stock/reservations/`

#### Create Reservation

**Endpoint:** `POST /api/stock/reservations/`

**Request Body:**
```json
{
  "stock": "uuid",
  "quantity": 10,
  "reserved_until": "2024-12-31T23:59:59Z",
  "notes": "Reservation notes"
}
```

#### Confirm Reservation

**Endpoint:** `POST /api/stock/reservations/{id}/confirm/`

#### Cancel Reservation

**Endpoint:** `POST /api/stock/reservations/{id}/cancel/`

## Movements

### Stock Movements

#### List Movements

**Endpoint:** `GET /api/movements/movements/`

**Query Parameters:**
- `movement_type`: Filter by type
- `status`: Filter by status
- `warehouse`: Filter by warehouse
- `product`: Filter by product

**Response:**
```json
{
  "count": 100,
  "results": [
    {
      "id": "uuid",
      "reference_number": "MOV-1234567890",
      "movement_type": "ENTRY",
      "status": "COMPLETED",
      "product": "uuid",
      "product_name": "Product Name",
      "warehouse": "uuid",
      "warehouse_name": "WH001",
      "quantity": 100,
      "reason": "Initial stock",
      "movement_date": "2024-01-01T00:00:00Z"
    }
  ]
}
```

#### Create Movement

**Endpoint:** `POST /api/movements/movements/`

**Request Body:**
```json
{
  "movement_type": "ENTRY",
  "product": "uuid",
  "warehouse": "uuid",
  "quantity": 100,
  "reason": "Stock entry",
  "comment": "Additional notes"
}
```

#### Approve Movement

**Endpoint:** `POST /api/movements/movements/{id}/approve/`

#### Validate Movement

**Endpoint:** `POST /api/movements/movements/{id}/validate/`

#### Complete Movement

**Endpoint:** `POST /api/movements/movements/{id}/complete/`

### Stock Requests

#### List Requests

**Endpoint:** `GET /api/movements/requests/`

**Query Parameters:**
- `status`: Filter by status
- `priority`: Filter by priority
- `warehouse`: Filter by warehouse

**Response:**
```json
{
  "count": 50,
  "results": [
    {
      "id": "uuid",
      "reference_number": "REQ-1234567890",
      "title": "Stock Request",
      "status": "PENDING",
      "priority": "HIGH",
      "warehouse": "uuid",
      "warehouse_name": "WH001",
      "requested_by": "uuid",
      "requested_by_name": "John Doe",
      "requested_at": "2024-01-01T00:00:00Z",
      "items": [
        {
          "id": "uuid",
          "product": "uuid",
          "product_name": "Product Name",
          "quantity": 10,
          "unit": "uuid",
          "unit_symbol": "pc"
        }
      ]
    }
  ]
}
```

#### Create Request

**Endpoint:** `POST /api/movements/requests/`

**Request Body:**
```json
{
  "title": "Stock Request",
  "description": "Need materials for maintenance",
  "warehouse": "uuid",
  "priority": "HIGH",
  "required_by": "2024-12-31",
  "items": [
    {
      "product": "uuid",
      "quantity": 10,
      "unit": "uuid",
      "notes": "Item notes"
    }
  ]
}
```

#### Approve Request

**Endpoint:** `POST /api/movements/requests/{id}/approve/`

#### Reject Request

**Endpoint:** `POST /api/movements/requests/{id}/reject/`

**Request Body:**
```json
{
  "reason": "Insufficient stock"
}
```

#### Validate Request

**Endpoint:** `POST /api/movements/requests/{id}/validate/`

#### Create Movements from Request

**Endpoint:** `POST /api/movements/requests/{id}/create_movements/`

#### My Requests

**Endpoint:** `GET /api/movements/requests/my_requests/`

#### Pending Requests

**Endpoint:** `GET /api/movements/requests/pending/`

#### Urgent Requests

**Endpoint:** `GET /api/movements/requests/urgent/`

## Dashboard

### Overview

**Endpoint:** `GET /api/dashboard/`

**Response:**
```json
{
  "total_products": 1000,
  "total_warehouses": 5,
  "total_stock_value": 500000.00,
  "low_stock_items": 15,
  "pending_requests": 8,
  "today_movements": 25
}
```

### Stock by Warehouse

**Endpoint:** `GET /api/dashboard/stock_by_warehouse/`

### Movement Statistics

**Endpoint:** `GET /api/dashboard/movement_stats/`

**Query Parameters:**
- `days`: Number of days (default: 30)

### Top Products

**Endpoint:** `GET /api/dashboard/top_products/`

**Query Parameters:**
- `limit`: Number of products (default: 10)

### Warehouse Utilization

**Endpoint:** `GET /api/dashboard/warehouse_utilization/`

### Category Distribution

**Endpoint:** `GET /api/dashboard/category_distribution/`

### Recent Activity

**Endpoint:** `GET /api/dashboard/recent_activity/`

**Query Parameters:**
- `limit`: Number of items (default: 20)

## Reports

### Inventory Report

**Endpoint:** `GET /api/dashboard/reports/inventory/`

**Query Parameters:**
- `warehouse_id`: Filter by warehouse (optional)

### Movement Report

**Endpoint:** `GET /api/dashboard/reports/movement/`

**Query Parameters:**
- `start_date`: Start date (YYYY-MM-DD)
- `end_date`: End date (YYYY-MM-DD)
- `warehouse_id`: Filter by warehouse (optional)

### Request Report

**Endpoint:** `GET /api/dashboard/reports/request/`

**Query Parameters:**
- `start_date`: Start date (YYYY-MM-DD)
- `end_date`: End date (YYYY-MM-DD)

## Audit Logs

### List Audit Logs

**Endpoint:** `GET /api/audit/`

**Query Parameters:**
- `action`: Filter by action
- `entity_type`: Filter by entity type
- `user`: Filter by user
- `search`: Search in various fields

**Response:**
```json
{
  "count": 1000,
  "results": [
    {
      "id": "uuid",
      "action": "CREATE",
      "entity_type": "Product",
      "user_email": "user@example.com",
      "user_role": "WAREHOUSE_MANAGER",
      "timestamp": "2024-01-01T00:00:00Z",
      "description": "Created product PRD001"
    }
  ]
}
```

### Audit Log by User

**Endpoint:** `GET /api/audit/user/{user_id}/`

### Audit Log by Entity

**Endpoint:** `GET /api/audit/entity/{entity_type}/{entity_id}/`

### Recent Audit Logs

**Endpoint:** `GET /api/audit/recent/{days}/`

## Notifications

### List Notifications

**Endpoint:** `GET /api/notifications/`

**Query Parameters:**
- `notification_type`: Filter by type
- `status`: Filter by status
- `recipient`: Filter by recipient

### My Notifications

**Endpoint:** `GET /api/notifications/my/`

## Error Responses

All endpoints return consistent error responses:

```json
{
  "detail": "Error message",
  "code": "error_code"
}
```

### Common HTTP Status Codes

- `200 OK`: Successful request
- `201 Created`: Resource created successfully
- `400 Bad Request`: Invalid request data
- `401 Unauthorized`: Authentication required
- `403 Forbidden`: Permission denied
- `404 Not Found`: Resource not found
- `409 Conflict`: Resource conflict
- `429 Too Many Requests`: Rate limit exceeded
- `500 Internal Server Error`: Server error

## Pagination

All list endpoints support pagination:

- `page`: Page number (default: 1)
- `page_size`: Items per page (default: 50, max: 1000)

## Filtering

Most list endpoints support filtering via query parameters.

## Searching

Most list endpoints support full-text search via the `search` parameter.

## Ordering

Most list endpoints support ordering via the `ordering` parameter.
Prefix with `-` for descending order.

## Rate Limiting

- Default: 60 requests per minute per user
- Anonymous users: 60 requests per minute
- Authenticated users: 60 requests per minute

# Database Documentation

## Database System

- **Database**: PostgreSQL 16
- **Provider**: Neon (production)
- **ORM**: Django ORM
- **Migrations**: Django Migrations

## Schema Design

### Primary Keys

All tables use UUID primary keys for:
- Global uniqueness
- Security (prevents ID enumeration)
- Distributed system compatibility

### Soft Delete

Tables that support soft delete include:
- `is_deleted`: Boolean flag
- `deleted_at`: Timestamp
- `deleted_by`: Foreign key to User

### Timestamps

All tables include:
- `created_at`: Auto-generated on creation
- `updated_at`: Auto-generated on update

## Tables

### accounts_user

User accounts and authentication.

**Columns:**
- `id` (UUID, PK)
- `email` (VARCHAR, unique, indexed)
- `first_name` (VARCHAR)
- `last_name` (VARCHAR)
- `phone` (VARCHAR)
- `avatar` (VARCHAR)
- `employee_id` (VARCHAR, unique, indexed)
- `department` (VARCHAR)
- `position` (VARCHAR)
- `role` (VARCHAR, indexed)
- `status` (VARCHAR, indexed)
- `is_staff` (BOOLEAN)
- `is_active` (BOOLEAN)
- `invitation_token` (UUID)
- `invitation_sent_at` (TIMESTAMP)
- `invitation_accepted_at` (TIMESTAMP)
- `terms_accepted` (BOOLEAN)
- `terms_accepted_at` (TIMESTAMP)
- `last_login` (TIMESTAMP)
- `created_by` (FK to User)
- `updated_by` (FK to User)
- `is_deleted` (BOOLEAN)
- `deleted_at` (TIMESTAMP)
- `deleted_by` (FK to User)
- `created_at` (TIMESTAMP, indexed)
- `updated_at` (TIMESTAMP)

**Indexes:**
- `email` (unique)
- `employee_id` (unique)
- `role`
- `status`
- `created_at`

### accounts_permission

Custom permissions for RBAC.

**Columns:**
- `id` (UUID, PK)
- `name` (VARCHAR, unique)
- `codename` (VARCHAR, unique)
- `description` (TEXT)
- `module` (VARCHAR)
- `created_at` (TIMESTAMP)

### accounts_rolepermission

Role to permission mapping.

**Columns:**
- `id` (UUID, PK)
- `role` (VARCHAR)
- `permission` (FK to Permission)
- `granted_at` (TIMESTAMP)

**Unique Constraint:** `(role, permission)`

### accounts_loginhistory

User login history tracking.

**Columns:**
- `id` (UUID, PK)
- `user` (FK to User)
- `ip_address` (INET)
- `user_agent` (TEXT)
- `login_time` (TIMESTAMP, indexed)
- `logout_time` (TIMESTAMP)
- `status` (VARCHAR)

**Indexes:**
- `login_time`

### categories_category

Product categories.

**Columns:**
- `id` (UUID, PK)
- `name` (VARCHAR, unique)
- `code` (VARCHAR, unique, indexed)
- `description` (TEXT)
- `parent` (FK to Category)
- `image` (VARCHAR)
- `is_active` (BOOLEAN)
- `is_deleted` (BOOLEAN)
- `deleted_at` (TIMESTAMP)
- `deleted_by` (FK to User)
- `created_at` (TIMESTAMP)
- `updated_at` (TIMESTAMP)

**Indexes:**
- `code`
- `parent`
- `is_active`

### suppliers_supplier

Supplier information.

**Columns:**
- `id` (UUID, PK)
- `code` (VARCHAR, unique, indexed)
- `name` (VARCHAR)
- `contact_person` (VARCHAR)
- `email` (VARCHAR, indexed)
- `phone` (VARCHAR)
- `address` (TEXT)
- `city` (VARCHAR)
- `country` (VARCHAR)
- `tax_id` (VARCHAR)
- `website` (VARCHAR)
- `status` (VARCHAR, indexed)
- `payment_terms` (VARCHAR)
- `notes` (TEXT)
- `rating` (DECIMAL)
- `is_deleted` (BOOLEAN)
- `deleted_at` (TIMESTAMP)
- `deleted_by` (FK to User)
- `created_at` (TIMESTAMP)
- `updated_at` (TIMESTAMP)

**Indexes:**
- `code`
- `email`
- `status`

### inventory_brand

Product brands.

**Columns:**
- `id` (UUID, PK)
- `name` (VARCHAR, unique)
- `code` (VARCHAR, unique, indexed)
- `description` (TEXT)
- `website` (VARCHAR)
- `logo` (VARCHAR)
- `is_active` (BOOLEAN)
- `is_deleted` (BOOLEAN)
- `deleted_at` (TIMESTAMP)
- `deleted_by` (FK to User)
- `created_at` (TIMESTAMP)
- `updated_at` (TIMESTAMP)

**Indexes:**
- `code`
- `is_active`

### inventory_unit

Units of measurement.

**Columns:**
- `id` (UUID, PK)
- `name` (VARCHAR, unique)
- `code` (VARCHAR, unique, indexed)
- `symbol` (VARCHAR, unique)
- `description` (TEXT)
- `is_base_unit` (BOOLEAN)
- `conversion_factor` (DECIMAL)
- `base_unit` (FK to Unit)
- `is_active` (BOOLEAN)
- `is_deleted` (BOOLEAN)
- `deleted_at` (TIMESTAMP)
- `deleted_by` (FK to User)
- `created_at` (TIMESTAMP)
- `updated_at` (TIMESTAMP)

**Indexes:**
- `code`
- `is_active`

### inventory_product

Product catalog.

**Columns:**
- `id` (UUID, PK)
- `internal_code` (VARCHAR, unique, indexed)
- `barcode` (VARCHAR, unique, indexed)
- `qr_code` (VARCHAR, unique, indexed)
- `name` (VARCHAR)
- `description` (TEXT)
- `category` (FK to Category, indexed)
- `brand` (FK to Brand, indexed)
- `unit` (FK to Unit)
- `supplier` (FK to Supplier, indexed)
- `purchase_price` (DECIMAL)
- `average_cost` (DECIMAL)
- `selling_price` (DECIMAL)
- `minimum_stock` (DECIMAL)
- `maximum_stock` (DECIMAL)
- `current_stock` (DECIMAL)
- `reserved_stock` (DECIMAL)
- `available_stock` (DECIMAL)
- `image` (VARCHAR)
- `specifications` (JSONB)
- `status` (VARCHAR, indexed)
- `created_by` (FK to User)
- `updated_by` (FK to User)
- `is_deleted` (BOOLEAN)
- `deleted_at` (TIMESTAMP)
- `deleted_by` (FK to User)
- `created_at` (TIMESTAMP)
- `updated_at` (TIMESTAMP)

**Indexes:**
- `internal_code` (unique)
- `barcode` (unique)
- `qr_code` (unique)
- `category`
- `brand`
- `supplier`
- `status`
- `created_at`

### warehouses_warehouse

Warehouse locations.

**Columns:**
- `id` (UUID, PK)
- `code` (VARCHAR, unique, indexed)
- `name` (VARCHAR)
- `description` (TEXT)
- `address` (TEXT)
- `city` (VARCHAR)
- `country` (VARCHAR)
- `postal_code` (VARCHAR)
- `phone` (VARCHAR)
- `email` (VARCHAR)
- `manager` (FK to User, indexed)
- `status` (VARCHAR, indexed)
- `capacity` (DECIMAL)
- `area` (DECIMAL)
- `temperature_min` (DECIMAL)
- `temperature_max` (DECIMAL)
- `humidity_min` (DECIMAL)
- `humidity_max` (DECIMAL)
- `is_deleted` (BOOLEAN)
- `deleted_at` (TIMESTAMP)
- `deleted_by` (FK to User)
- `created_at` (TIMESTAMP)
- `updated_at` (TIMESTAMP)

**Indexes:**
- `code`
- `status`
- `manager`

### warehouses_zone

Warehouse zones.

**Columns:**
- `id` (UUID, PK)
- `code` (VARCHAR, indexed)
- `name` (VARCHAR)
- `warehouse` (FK to Warehouse, indexed)
- `zone_type` (VARCHAR, indexed)
- `description` (TEXT)
- `capacity` (DECIMAL)
- `used_capacity` (DECIMAL)
- `is_active` (BOOLEAN)
- `is_deleted` (BOOLEAN)
- `deleted_at` (TIMESTAMP)
- `deleted_by` (FK to User)
- `created_at` (TIMESTAMP)
- `updated_at` (TIMESTAMP)

**Indexes:**
- `(warehouse, code)` (unique)
- `zone_type`

### warehouses_row

Warehouse rows.

**Columns:**
- `id` (UUID, PK)
- `code` (VARCHAR, indexed)
- `name` (VARCHAR)
- `zone` (FK to Zone, indexed)
- `description` (TEXT)
- `capacity` (DECIMAL)
- `used_capacity` (DECIMAL)
- `is_active` (BOOLEAN)
- `is_deleted` (BOOLEAN)
- `deleted_at` (TIMESTAMP)
- `deleted_by` (FK to User)
- `created_at` (TIMESTAMP)
- `updated_at` (TIMESTAMP)

**Indexes:**
- `(zone, code)` (unique)

### warehouses_shelf

Warehouse shelves.

**Columns:**
- `id` (UUID, PK)
- `code` (VARCHAR, indexed)
- `name` (VARCHAR)
- `row` (FK to Row, indexed)
- `description` (TEXT)
- `capacity` (DECIMAL)
- `used_capacity` (DECIMAL)
- `height` (DECIMAL)
- `weight_limit` (DECIMAL)
- `is_active` (BOOLEAN)
- `is_deleted` (BOOLEAN)
- `deleted_at` (TIMESTAMP)
- `deleted_by` (FK to User)
- `created_at` (TIMESTAMP)
- `updated_at` (TIMESTAMP)

**Indexes:**
- `(row, code)` (unique)

### warehouses_bin

Warehouse bins.

**Columns:**
- `id` (UUID, PK)
- `code` (VARCHAR, indexed)
- `name` (VARCHAR)
- `shelf` (FK to Shelf, indexed)
- `description` (TEXT)
- `capacity` (DECIMAL)
- `used_capacity` (DECIMAL)
- `length` (DECIMAL)
- `width` (DECIMAL)
- `depth` (DECIMAL)
- `is_active` (BOOLEAN)
- `is_deleted` (BOOLEAN)
- `deleted_at` (TIMESTAMP)
- `deleted_by` (FK to User)
- `created_at` (TIMESTAMP)
- `updated_at` (TIMESTAMP)

**Indexes:**
- `(shelf, code)` (unique)

### locations_productlocation

Product storage locations.

**Columns:**
- `id` (UUID, PK)
- `product` (FK to Product, indexed)
- `warehouse` (FK to Warehouse, indexed)
- `zone` (FK to Zone)
- `row` (FK to Row)
- `shelf` (FK to Shelf)
- `bin` (FK to Bin, indexed)
- `quantity` (DECIMAL)
- `is_primary` (BOOLEAN, indexed)
- `is_deleted` (BOOLEAN)
- `deleted_at` (TIMESTAMP)
- `deleted_by` (FK to User)
- `created_at` (TIMESTAMP)
- `updated_at` (TIMESTAMP)

**Indexes:**
- `(product, warehouse)`
- `bin`
- `is_primary`

### stock_stock

Stock records.

**Columns:**
- `id` (UUID, PK)
- `product` (FK to Product, indexed)
- `warehouse` (FK to Warehouse, indexed)
- `quantity` (DECIMAL)
- `reserved_quantity` (DECIMAL)
- `available_quantity` (DECIMAL)
- `minimum_level` (DECIMAL)
- `maximum_level` (DECIMAL)
- `reorder_level` (DECIMAL)
- `reorder_quantity` (DECIMAL)
- `last_count_date` (DATE)
- `last_count_quantity` (DECIMAL)
- `variance` (DECIMAL)
- `is_deleted` (BOOLEAN)
- `deleted_at` (TIMESTAMP)
- `deleted_by` (FK to User)
- `created_at` (TIMESTAMP)
- `updated_at` (TIMESTAMP)

**Indexes:**
- `(product, warehouse)` (unique)
- `warehouse`

### stock_stockreservation

Stock reservations.

**Columns:**
- `id` (UUID, PK)
- `stock` (FK to Stock)
- `reference_number` (VARCHAR, unique, indexed)
- `quantity` (DECIMAL)
- `status` (VARCHAR, indexed)
- `reserved_by` (FK to User)
- `reserved_until` (TIMESTAMP, indexed)
- `notes` (TEXT)
- `is_deleted` (BOOLEAN)
- `deleted_at` (TIMESTAMP)
- `deleted_by` (FK to User)
- `created_at` (TIMESTAMP)
- `updated_at` (TIMESTAMP)

**Indexes:**
- `reference_number` (unique)
- `status`
- `reserved_until`

### movements_movement

Stock movements.

**Columns:**
- `id` (UUID, PK)
- `movement_type` (VARCHAR, indexed)
- `status` (VARCHAR, indexed)
- `reference_number` (VARCHAR, unique, indexed)
- `product` (FK to Product, indexed)
- `warehouse` (FK to Warehouse, indexed)
- `from_location` (FK to Bin)
- `to_location` (FK to Bin)
- `from_warehouse` (FK to Warehouse)
- `to_warehouse` (FK to Warehouse)
- `quantity` (DECIMAL)
- `unit_cost` (DECIMAL)
- `total_cost` (DECIMAL)
- `reason` (TEXT)
- `comment` (TEXT)
- `requested_by` (FK to User)
- `approved_by` (FK to User)
- `approved_at` (TIMESTAMP)
- `validated_by` (FK to User)
- `validated_at` (TIMESTAMP)
- `performed_by` (FK to User)
- `performed_at` (TIMESTAMP)
- `movement_date` (TIMESTAMP, indexed)
- `expected_date` (TIMESTAMP)
- `is_deleted` (BOOLEAN)
- `deleted_at` (TIMESTAMP)
- `deleted_by` (FK to User)
- `created_at` (TIMESTAMP)
- `updated_at` (TIMESTAMP)

**Indexes:**
- `reference_number` (unique)
- `movement_type`
- `status`
- `product`
- `warehouse`
- `movement_date`

### movements_stockrequest

Stock requests.

**Columns:**
- `id` (UUID, PK)
- `reference_number` (VARCHAR, unique, indexed)
- `status` (VARCHAR, indexed)
- `priority` (VARCHAR, indexed)
- `title` (VARCHAR)
- `description` (TEXT)
- `warehouse` (FK to Warehouse, indexed)
- `requested_by` (FK to User)
- `requested_at` (TIMESTAMP, indexed)
- `approved_by` (FK to User)
- `approved_at` (TIMESTAMP)
- `rejected_by` (FK to User)
- `rejected_at` (TIMESTAMP)
- `rejection_reason` (TEXT)
- `validated_by` (FK to User)
- `validated_at` (TIMESTAMP)
- `required_by` (DATE)
- `is_deleted` (BOOLEAN)
- `deleted_at` (TIMESTAMP)
- `deleted_by` (FK to User)
- `created_at` (TIMESTAMP)
- `updated_at` (TIMESTAMP)

**Indexes:**
- `reference_number` (unique)
- `status`
- `priority`
- `warehouse`
- `requested_at`

### movements_stockrequestitem

Stock request items.

**Columns:**
- `id` (UUID, PK)
- `stock_request` (FK to StockRequest)
- `product` (FK to Product)
- `quantity` (DECIMAL)
- `unit` (FK to Unit)
- `notes` (TEXT)
- `is_deleted` (BOOLEAN)
- `deleted_at` (TIMESTAMP)
- `deleted_by` (FK to User)
- `created_at` (TIMESTAMP)
- `updated_at` (TIMESTAMP)

### audit_auditlog

Audit logs.

**Columns:**
- `id` (UUID, PK)
- `user` (FK to User, indexed)
- `user_email` (VARCHAR)
- `user_role` (VARCHAR)
- `action` (VARCHAR, indexed)
- `entity_type` (VARCHAR, indexed)
- `entity_id` (UUID)
- `content_type` (FK to ContentType)
- `object_id` (UUID)
- `old_data` (JSONB)
- `new_data` (JSONB)
- `changed_fields` (JSONB)
- `ip_address` (INET)
- `user_agent` (TEXT)
- `request_method` (VARCHAR)
- `request_path` (VARCHAR)
- `description` (TEXT)
- `reason` (TEXT)
- `timestamp` (TIMESTAMP, indexed)
- `is_deleted` (BOOLEAN)
- `deleted_at` (TIMESTAMP)
- `deleted_by` (FK to User)
- `created_at` (TIMESTAMP)
- `updated_at` (TIMESTAMP)

**Indexes:**
- `user`
- `action`
- `entity_type`
- `timestamp`
- `(content_type, object_id)`

### notifications_notification

Notification records.

**Columns:**
- `id` (UUID, PK)
- `recipient` (FK to User, indexed)
- `recipient_email` (VARCHAR)
- `notification_type` (VARCHAR, indexed)
- `status` (VARCHAR, indexed)
- `subject` (VARCHAR)
- `body` (TEXT)
- `data` (JSONB)
- `sent_at` (TIMESTAMP)
- `error_message` (TEXT)
- `is_deleted` (BOOLEAN)
- `deleted_at` (TIMESTAMP)
- `deleted_by` (FK to User)
- `created_at` (TIMESTAMP, indexed)
- `updated_at` (TIMESTAMP)

**Indexes:**
- `recipient`
- `notification_type`
- `status`
- `created_at`

## Database Migrations

### Creating Migrations

```bash
python manage.py makemigrations
```

### Applying Migrations

```bash
python manage.py migrate
```

### Rolling Back Migrations

```bash
python manage.py migrate <app> <migration_name>
```

### Showing Migration Status

```bash
python manage.py showmigrations
```

## Database Backup

### Using pg_dump

```bash
pg_dump -h <host> -U <user> -d <database> > backup.sql
```

### Restoring from Backup

```bash
psql -h <host> -U <user> -d <database> < backup.sql
```

## Performance Optimization

### Query Optimization

- Use `select_related` for foreign keys
- Use `prefetch_related` for many-to-many
- Use `only()` to select specific fields
- Use `defer()` to exclude specific fields

### Indexing Strategy

- Index foreign keys
- Index frequently queried fields
- Use composite indexes for multi-column queries
- Monitor index usage

### Connection Pooling

- Configure database connection pool
- Set appropriate pool size
- Monitor connection usage

## Database Maintenance

### Vacuum

```sql
VACUUM ANALYZE;
```

### Reindex

```sql
REINDEX DATABASE <database_name>;
```

### Analyze

```sql
ANALYZE;
```

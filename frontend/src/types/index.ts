// User & Auth Types
export interface User {
  id: string
  email: string
  firstName: string
  lastName: string
  avatar?: string
  role: "admin" | "manager" | "user" | "viewer"
  department?: string
  createdAt: string
  updatedAt: string
}

export interface AuthState {
  isAuthenticated: boolean
  user: User | null
  loading: boolean
}

// Product Types
export interface Product {
  id: string
  sku: string
  name: string
  barcode: string
  category: string
  supplier: string
  unit: string
  currentStock: number
  reservedStock: number
  minStock: number
  maxStock: number
  price: number
  createdAt: string
  updatedAt: string
}

// Inventory Types
export interface InventoryItem {
  id: string
  productId: string
  warehouseId: string
  locationId: string
  quantity: number
  reservedQuantity: number
  lastChecked: string
  expiryDate?: string
}

// Warehouse Types
export interface Warehouse {
  id: string
  name: string
  code: string
  address: string
  city: string
  country: string
  capacity: number
  currentLoad: number
  manager: string
  zones: Zone[]
  createdAt: string
  updatedAt: string
}

export interface Zone {
  id: string
  name: string
  rows: Row[]
}

export interface Row {
  id: string
  name: string
  shelves: Shelf[]
}

export interface Shelf {
  id: string
  name: string
  bins: Bin[]
}

export interface Bin {
  id: string
  name: string
  quantity: number
  capacity: number
}

// Stock Request Types
export interface StockRequest {
  id: string
  productId: string
  quantity: number
  reason: "adjustment" | "transfer" | "consumption" | "return"
  fromWarehouse?: string
  toWarehouse?: string
  status: "pending" | "approved" | "rejected" | "completed"
  requester: string
  approver?: string
  createdAt: string
  updatedAt: string
}

// Stock Movement Types
export interface StockMovement {
  id: string
  productId: string
  fromLocation: string
  toLocation: string
  quantity: number
  reason: string
  user: string
  createdAt: string
}

// Category Types
export interface Category {
  id: string
  name: string
  description?: string
  parentId?: string
  createdAt: string
}

// Supplier Types
export interface Supplier {
  id: string
  name: string
  email: string
  phone: string
  address: string
  city: string
  country: string
  contactPerson: string
  createdAt: string
  updatedAt: string
}

// Employee Types
export interface Employee {
  id: string
  userId: string
  firstName: string
  lastName: string
  email: string
  phone: string
  department: string
  position: string
  avatar?: string
  createdAt: string
  updatedAt: string
}

// Audit Log Types
export interface AuditLog {
  id: string
  user: string
  action: string
  entity: string
  entityId: string
  changes: Record<string, unknown>
  createdAt: string
}

// Notification Types
export interface Notification {
  id: string
  userId: string
  title: string
  message: string
  type: "alert" | "approval" | "system" | "info"
  read: boolean
  createdAt: string
}

// Dashboard Stats
export interface DashboardStats {
  totalProducts: number
  inventoryValue: number
  criticalStockItems: number
  pendingRequests: number
  activeEmployees: number
  totalWarehouses: number
}

// Chart Data
export interface ChartDataPoint {
  name: string
  value: number
  [key: string]: string | number
}

// API Response Types
export interface ApiResponse<T> {
  success: boolean
  data: T
  message?: string
  error?: string
}

// Filter & Sort Types
export interface TableFilter {
  field: string
  value: string | number | boolean | string[]
}

export interface TableSort {
  field: string
  direction: "asc" | "desc"
}

export type Status = "pending" | "approved" | "rejected" | "completed" | "active" | "inactive"

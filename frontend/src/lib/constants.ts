export const APP_NAME = "Industrial Inventory Manager"
export const APP_DESCRIPTION = "Enterprise-grade inventory management system"

// Status Colors
export const STATUS_COLORS = {
  pending: { bg: "bg-yellow-100", text: "text-yellow-800", label: "Pending" },
  approved: { bg: "bg-green-100", text: "text-green-800", label: "Approved" },
  rejected: { bg: "bg-red-100", text: "text-red-800", label: "Rejected" },
  completed: { bg: "bg-blue-100", text: "text-blue-800", label: "Completed" },
  active: { bg: "bg-green-100", text: "text-green-800", label: "Active" },
  inactive: { bg: "bg-gray-100", text: "text-gray-800", label: "Inactive" },
}

// Role Permissions
export const ROLE_PERMISSIONS = {
  admin: [
    "view_dashboard",
    "manage_products",
    "manage_inventory",
    "manage_warehouses",
    "manage_employees",
    "manage_settings",
    "view_reports",
    "view_audit_logs",
  ],
  manager: [
    "view_dashboard",
    "manage_products",
    "manage_inventory",
    "manage_warehouses",
    "view_employees",
    "view_reports",
  ],
  user: [
    "view_dashboard",
    "view_products",
    "manage_inventory",
    "view_reports",
  ],
  viewer: ["view_dashboard", "view_products", "view_reports"],
}

// Warehouse Hierarchy
export const WAREHOUSE_STRUCTURE = {
  warehouse: "Warehouse",
  zone: "Zone",
  row: "Row",
  shelf: "Shelf",
  bin: "Bin",
}

// Stock Movement Reasons
export const STOCK_REASONS = [
  "Physical Stock Count",
  "Damage/Loss",
  "Return from Customer",
  "New Stock Receipt",
  "Transfer Between Warehouses",
  "Production Consumption",
  "Adjustment",
]

// Notification Types
export const NOTIFICATION_TYPES = {
  alert: { color: "bg-red-100 text-red-800", icon: "AlertCircle" },
  approval: { color: "bg-blue-100 text-blue-800", icon: "CheckCircle" },
  system: { color: "bg-gray-100 text-gray-800", icon: "Info" },
  info: { color: "bg-green-100 text-green-800", icon: "Bell" },
}

// Chart Colors
export const CHART_COLORS = {
  primary: "#1FA83A",
  secondary: "#6d6d6d",
  accent: "#f13c2e",
  success: "#059669",
  warning: "#d97706",
  error: "#dc2626",
  info: "#0ea5e9",
}

// Pagination
export const ITEMS_PER_PAGE_OPTIONS = [10, 25, 50, 100]
export const DEFAULT_ITEMS_PER_PAGE = 25

// Navigation Menu
export const NAVIGATION_ITEMS = [
  { id: "dashboard", label: "Dashboard", path: "/dashboard", icon: "BarChart3" },
  { id: "inventory", label: "Inventory", path: "/inventory", icon: "Package" },
  { id: "products", label: "Products", path: "/products", icon: "Boxes" },
  { id: "warehouses", label: "Warehouses", path: "/warehouses", icon: "Building2" },
  { id: "stocks", label: "Stock Levels", path: "/stocks", icon: "Layers" },
  { id: "requests", label: "Stock Requests", path: "/requests", icon: "ClipboardList" },
  { id: "movements", label: "Stock Movements", path: "/movements", icon: "ArrowRightLeft" },
  { id: "employees", label: "Employees", path: "/employees", icon: "Users" },
  { id: "notifications", label: "Notifications", path: "/notifications", icon: "Bell" },
  { id: "audit", label: "Audit Logs", path: "/audit-logs", icon: "FileText" },
  { id: "reports", label: "Reports", path: "/reports", icon: "BarChart" },
]

// Settings Sections
export const SETTINGS_SECTIONS = [
  { id: "company", label: "Company Information" },
  { id: "units", label: "Units of Measurement" },
  { id: "brands", label: "Brands" },
  { id: "notifications", label: "Notification Preferences" },
  { id: "system", label: "System Settings" },
]

// API Endpoints (for reference)
export const API_ENDPOINTS = {
  auth: "/api/auth",
  products: "/api/products",
  inventory: "/api/inventory",
  warehouses: "/api/warehouses",
  employees: "/api/employees",
  reports: "/api/reports",
  auditLogs: "/api/audit-logs",
}

// Time Formats
export const DATE_FORMAT = "MMM dd, yyyy"
export const TIME_FORMAT = "HH:mm:ss"
export const DATETIME_FORMAT = "MMM dd, yyyy HH:mm:ss"

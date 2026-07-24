import { useQuery as useRQQuery } from "@tanstack/react-query"
import { apiClient, type PaginatedResponse } from "@/lib/api-client"
import type {
  Product,
  Warehouse,
  Category,
  Supplier,
  Employee,
  StockMovement,
  AuditLog,
  Notification,
  DashboardStats,
  StockRequest,
  InventoryItem,
} from "@/types"

interface QueryState<T> {
  data: T | null | undefined
  loading: boolean
  error: Error | null
}

function toQueryState<T>(result: { data?: T; isLoading: boolean; error: unknown }): QueryState<T> {
  return {
    data: result.data ?? null,
    loading: result.isLoading,
    error: (result.error as Error) ?? null,
  }
}

// ---------------------------------------------------------------------------
// Backend response shapes (only the fields we actually consume)
// ---------------------------------------------------------------------------

interface ApiProduct {
  id: string
  internal_code: string
  name: string
  barcode: string
  category_name: string
  supplier_name: string
  unit_symbol: string
  current_stock: number
  reserved_stock: number
  minimum_stock: number
  maximum_stock: number
  selling_price: number
  created_at: string
  updated_at: string
}

interface ApiWarehouse {
  id: string
  name: string
  code: string
  address: string
  city: string
  country: string
  manager_name: string
  status: string
  capacity: number
  total_capacity: number
  used_capacity: number
  created_at: string
  updated_at: string
}

interface ApiCategory {
  id: string
  name: string
  description: string | null
  parent: string | null
  created_at: string
}

interface ApiSupplier {
  id: string
  name: string
  email: string
  phone: string
  address: string
  city: string
  country: string
  contact_person: string
  created_at: string
  updated_at: string
}

interface ApiUser {
  id: string
  email: string
  first_name: string
  last_name: string
  full_name: string
  phone: string
  avatar: string | null
  department: string
  position: string
  status: string
  created_at: string
  updated_at: string
}

interface ApiStock {
  id: string
  product: string
  product_name: string
  product_code: string
  warehouse: string
  warehouse_code: string
  quantity: number
  reserved_quantity: number
  minimum_level: number
  maximum_level: number
  is_below_minimum: boolean
  is_below_reorder: boolean
  is_above_maximum: boolean
  updated_at: string
}

interface ApiMovement {
  id: string
  product: string
  from_location_name: string | null
  to_location_name: string | null
  from_warehouse: string | null
  to_warehouse: string | null
  quantity: number
  reason: string
  type_display: string
  performed_by_name: string | null
  requested_by_name: string | null
  movement_date: string | null
  created_at: string
}

interface ApiStockRequest {
  id: string
  reference_number: string
  status: string
  warehouse_name: string
  requested_by_name: string
  approved_by_name: string | null
  requested_at: string
  approved_at: string | null
  validated_at: string | null
  items: { product: string; quantity: number }[]
}

interface ApiNotification {
  id: string
  recipient: string
  notification_type: string
  status: string
  subject: string
  body: string
  created_at: string
}

interface ApiAuditLog {
  id: string
  user_name: string | null
  user_email: string
  action: string
  entity_type: string
  entity_id: string
  changed_fields: Record<string, unknown> | null
  timestamp: string
}

interface ApiOverviewStats {
  total_products: number
  total_warehouses: number
  total_stock_value: number
  low_stock_items: number
  pending_requests: number
  today_movements: number
}

// ---------------------------------------------------------------------------
// Mappers: backend shape -> frontend UI shape
// ---------------------------------------------------------------------------

function mapProduct(p: ApiProduct): Product {
  return {
    id: p.id,
    sku: p.internal_code,
    name: p.name,
    barcode: p.barcode,
    category: p.category_name,
    supplier: p.supplier_name,
    unit: p.unit_symbol,
    currentStock: Number(p.current_stock),
    reservedStock: Number(p.reserved_stock),
    minStock: Number(p.minimum_stock),
    maxStock: Number(p.maximum_stock),
    price: Number(p.selling_price),
    createdAt: p.created_at,
    updatedAt: p.updated_at,
  }
}

function mapWarehouse(w: ApiWarehouse): Warehouse {
  const capacity = Number(w.total_capacity ?? w.capacity ?? 0)
  const used = Number(w.used_capacity ?? 0)
  return {
    id: w.id,
    name: w.name,
    code: w.code,
    address: w.address,
    city: w.city,
    country: w.country,
    location: [w.city, w.country].filter(Boolean).join(", "),
    capacity,
    currentLoad: used,
    utilization: capacity > 0 ? Math.round((used / capacity) * 100) : 0,
    manager: w.manager_name || "—",
    status: w.status === "ACTIVE" ? "active" : "inactive",
    zones: [],
    createdAt: w.created_at,
    updatedAt: w.updated_at,
  }
}

function mapCategory(c: ApiCategory): Category {
  return {
    id: c.id,
    name: c.name,
    description: c.description ?? undefined,
    parentId: c.parent ?? undefined,
    createdAt: c.created_at,
  }
}

function mapSupplier(s: ApiSupplier): Supplier {
  return {
    id: s.id,
    name: s.name,
    email: s.email,
    phone: s.phone,
    address: s.address,
    city: s.city,
    country: s.country,
    contactPerson: s.contact_person,
    createdAt: s.created_at,
    updatedAt: s.updated_at,
  }
}

function mapEmployee(u: ApiUser): Employee {
  return {
    id: u.id,
    userId: u.id,
    name: u.full_name,
    firstName: u.first_name,
    lastName: u.last_name,
    email: u.email,
    phone: u.phone,
    department: u.department,
    position: u.position,
    avatar: u.avatar ?? undefined,
    // The backend only tracks PENDING/ACTIVE/SUSPENDED/DEACTIVATED — there is
    // no "on leave" concept yet, so that state is never produced today.
    status: u.status === "ACTIVE" ? "active" : "inactive",
    createdAt: u.created_at,
    updatedAt: u.updated_at,
  }
}

function mapStockToInventoryItem(s: ApiStock): InventoryItem {
  const status: InventoryItem["status"] = s.is_below_minimum
    ? "critical"
    : s.is_below_reorder
      ? "low"
      : s.is_above_maximum
        ? "overstock"
        : "optimal"

  return {
    id: s.id,
    productId: s.product,
    productName: s.product_name,
    sku: s.product_code,
    warehouseId: s.warehouse,
    locationId: s.warehouse_code,
    quantity: Number(s.quantity),
    reservedQuantity: Number(s.reserved_quantity),
    currentStock: Number(s.quantity),
    minimumLevel: Number(s.minimum_level),
    maximumLevel: Number(s.maximum_level),
    // Stock records don't carry a unit price themselves (that lives on the
    // related Product); until we join it in, value totals default to 0.
    unitPrice: 0,
    status,
    lastChecked: s.updated_at,
  }
}

function mapMovement(m: ApiMovement): StockMovement {
  return {
    id: m.id,
    productId: m.product,
    fromLocation: m.from_location_name || m.from_warehouse || "—",
    toLocation: m.to_location_name || m.to_warehouse || "—",
    quantity: Number(m.quantity),
    reason: m.reason || m.type_display,
    user: m.performed_by_name || m.requested_by_name || "—",
    createdAt: m.movement_date || m.created_at,
  }
}

function mapStockRequest(r: ApiStockRequest): StockRequest {
  const totalQuantity = r.items?.reduce((sum, item) => sum + Number(item.quantity), 0) ?? 0
  return {
    id: r.id,
    productId: r.items?.[0]?.product ?? "",
    quantity: totalQuantity,
    // The backend models requests as a title/description + line items rather
    // than a single "reason" enum; "adjustment" is used as a safe default.
    reason: "adjustment",
    toWarehouse: r.warehouse_name,
    status: r.status.toLowerCase() as StockRequest["status"],
    requester: r.requested_by_name,
    approver: r.approved_by_name ?? undefined,
    createdAt: r.requested_at,
    updatedAt: r.validated_at || r.approved_at || r.requested_at,
  }
}

function mapNotificationType(type: string): Notification["type"] {
  if (type === "LOW_STOCK") return "alert"
  if (type === "REQUEST_APPROVED" || type === "REQUEST_REJECTED") return "approval"
  if (type === "SYSTEM" || type === "INVITATION" || type === "PASSWORD_RESET") return "system"
  return "info"
}

function mapNotification(n: ApiNotification): Notification {
  return {
    id: n.id,
    userId: n.recipient,
    title: n.subject,
    message: n.body,
    type: mapNotificationType(n.notification_type),
    // Backend status (PENDING/SENT/FAILED) tracks delivery, not read state;
    // there's no read-receipt field yet, so this is a placeholder.
    read: n.status === "SENT",
    createdAt: n.created_at,
  }
}

function mapAuditLog(a: ApiAuditLog): AuditLog {
  return {
    id: a.id,
    user: a.user_name || a.user_email,
    action: a.action,
    entity: a.entity_type,
    entityId: a.entity_id,
    changes: a.changed_fields ?? {},
    createdAt: a.timestamp,
  }
}

// ---------------------------------------------------------------------------
// Query hooks
// ---------------------------------------------------------------------------

export function useProducts() {
  const result = useRQQuery({
    queryKey: ["products"],
    queryFn: async () => {
      const res = await apiClient.get<PaginatedResponse<ApiProduct>>("/inventory/products/", { page_size: 200 })
      return res.results.map(mapProduct)
    },
  })
  return toQueryState(result)
}

export function useProduct(id: string) {
  const products = useProducts()
  return {
    ...products,
    data: products.data?.find((p) => p.id === id) || null,
  }
}

export function useWarehouses() {
  const result = useRQQuery({
    queryKey: ["warehouses"],
    queryFn: async () => {
      const res = await apiClient.get<PaginatedResponse<ApiWarehouse>>("/warehouses/", { page_size: 100 })
      return res.results.map(mapWarehouse)
    },
  })
  return toQueryState(result)
}

export function useWarehouse(id: string) {
  const warehouses = useWarehouses()
  return {
    ...warehouses,
    data: warehouses.data?.find((w) => w.id === id) || null,
  }
}

export function useCategories() {
  const result = useRQQuery({
    queryKey: ["categories"],
    queryFn: async () => {
      const res = await apiClient.get<PaginatedResponse<ApiCategory>>("/categories/", { page_size: 200 })
      return res.results.map(mapCategory)
    },
  })
  return toQueryState(result)
}

export function useSuppliers() {
  const result = useRQQuery({
    queryKey: ["suppliers"],
    queryFn: async () => {
      const res = await apiClient.get<PaginatedResponse<ApiSupplier>>("/suppliers/", { page_size: 200 })
      return res.results.map(mapSupplier)
    },
  })
  return toQueryState(result)
}

export function useEmployees() {
  const result = useRQQuery({
    queryKey: ["employees"],
    queryFn: async () => {
      const res = await apiClient.get<PaginatedResponse<ApiUser>>("/auth/users/", { page_size: 200 })
      return res.results.map(mapEmployee)
    },
  })
  return toQueryState(result)
}

export function useInventoryItems() {
  const result = useRQQuery({
    queryKey: ["stock"],
    queryFn: async () => {
      const res = await apiClient.get<PaginatedResponse<ApiStock>>("/stock/stocks/", { page_size: 200 })
      return res.results.map(mapStockToInventoryItem)
    },
  })
  return toQueryState(result)
}

export function useStockMovements() {
  const result = useRQQuery({
    queryKey: ["movements"],
    queryFn: async () => {
      const res = await apiClient.get<PaginatedResponse<ApiMovement>>("/movements/movements/", {
        page_size: 100,
        ordering: "-created_at",
      })
      return res.results.map(mapMovement)
    },
  })
  return toQueryState(result)
}

export function useStockRequests() {
  const result = useRQQuery({
    queryKey: ["stock-requests"],
    queryFn: async () => {
      const res = await apiClient.get<PaginatedResponse<ApiStockRequest>>("/movements/requests/", { page_size: 100 })
      return res.results.map(mapStockRequest)
    },
  })
  return toQueryState(result)
}

export function useNotifications() {
  const result = useRQQuery({
    queryKey: ["notifications"],
    queryFn: async () => {
      const res = await apiClient.get<PaginatedResponse<ApiNotification>>("/notifications/my/", { page_size: 50 })
      return res.results.map(mapNotification)
    },
  })
  return toQueryState(result)
}

export function useAuditLogs() {
  const result = useRQQuery({
    queryKey: ["audit-logs"],
    queryFn: async () => {
      const res = await apiClient.get<PaginatedResponse<ApiAuditLog>>("/audit/", { page_size: 100 })
      return res.results.map(mapAuditLog)
    },
  })
  return toQueryState(result)
}

export function useDashboardStats() {
  const result = useRQQuery({
    queryKey: ["dashboard-stats"],
    queryFn: async () => {
      const [overview, activeUsers] = await Promise.all([
        apiClient.get<ApiOverviewStats>("/dashboard/"),
        apiClient.get<PaginatedResponse<ApiUser>>("/auth/users/", { status: "ACTIVE", page_size: 1 }),
      ])
      const stats: DashboardStats = {
        totalProducts: overview.total_products,
        inventoryValue: Number(overview.total_stock_value),
        criticalStockItems: overview.low_stock_items,
        pendingRequests: overview.pending_requests,
        activeEmployees: activeUsers.count,
        totalWarehouses: overview.total_warehouses,
      }
      return stats
    },
  })
  return toQueryState(result)
}

// ---------------------------------------------------------------------------
// Derived / convenience hooks
// ---------------------------------------------------------------------------

export function useSearchProducts(query: string) {
  const products = useProducts()
  const filtered = products.data?.filter(
    (p) =>
      p.name.toLowerCase().includes(query.toLowerCase()) ||
      p.sku.toLowerCase().includes(query.toLowerCase()) ||
      p.barcode.toLowerCase().includes(query.toLowerCase())
  )

  return {
    ...products,
    data: filtered,
  }
}

export function useWarehouseInventory(warehouseId: string) {
  const inventory = useInventoryItems()
  const filtered = inventory.data?.filter((item) => item.warehouseId === warehouseId)

  return {
    ...inventory,
    data: filtered,
  }
}

export function useLowStockItems() {
  const products = useProducts()
  const lowStock = products.data?.filter((p) => p.currentStock <= p.minStock)

  return {
    ...products,
    data: lowStock,
  }
}

export function usePaginatedData<T extends { id: string }>(data: T[], pageSize: number = 25) {
  const totalPages = Math.ceil(data.length / pageSize)

  return {
    data,
    totalPages,
    totalItems: data.length,
    pageSize,
  }
}
